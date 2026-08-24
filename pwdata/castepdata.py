"""Parse CASTEP output files (.castep / .geom / .md) into pwdata Image objects.

Supported formats:
- castep/scf  : single-point / geometry-optimisation ``<seed>.castep`` output,
                one Image per converged ionic step (1 for a single-point run)
- castep/geom : ``<seed>.geom`` geometry-optimisation trajectory, one Image
                per optimisation step
- castep/md   : ``<seed>.md`` AIMD trajectory, one Image per MD step

Conventions:
- ``.castep`` values are natively in eV / Angstrom / GPa. Both the modern
  markers (``Final energy, E = ...``, ``Cartesian components of stress
  tensor (GPa)``) and the older CASTEP <= 6.x / Materials Studio markers
  (``Final energy = ...``, ``Cartesian components (GPa)``) are recognised.
- One Image is emitted per step that carries an energy AND a complete force
  table (older versions print per-iteration energies several times during
  the cut-off convergence sweep but forces only for the final structure, so
  energy-only intermediates are not emitted); a pending energy-only step is
  emitted at end of file as a structural salvage image. Positions are taken
  from the last ``Cell Contents`` table (older versions print it once).
- ``.geom`` and ``.md`` values are in atomic units (Hartree / Bohr); both the
  classic tag layout (``<-- E``, ``<-- h``, ``<-- R``, ``<-- F``, ``<-- S``)
  and the restructured layout of newer CASTEP versions (``BEGIN header`` /
  ``END header`` block followed by blank-line separated frames carrying the
  same tags) are handled by the same parser.
- CASTEP positions in ``.geom``/``.md`` are Cartesian; ``.castep`` fractional
  coordinates are stored as fractional (``image.cartesian=False``).
- CASTEP prints stress with positive = compression; the virial is stored as
  ``virial = stress[GPa] * volume[A^3] / 160.21766208`` with no sign flip,
  consistent with the CP2K path (``pwdata.utils.constant.gpa2ev``).
- Velocities, temperatures and pressures are skipped (``Image`` has no fields
  for them).
"""
import os
import glob
import re
import numpy as np
from collections import Counter
from tqdm import tqdm
from pwdata.image import Image
from pwdata.calculators.const import ELEMENTTABLE
from pwdata.utils.format_change import to_numpy_array, to_integer, to_float
from pwdata.utils.constant import HARTREE2EV, BOHR2ANG, HARTREE2EV_PER_BOHR2ANG, HARTREE_PER_BOHR3_TO_GPA, gpa2ev

NUMBER_PATTERN = re.compile(r"[-+]?\d+(?:\.\d+)?(?:[eE][-+]?\d+)?")
TAG_PATTERN = re.compile(r"<--\s*([A-Za-z]+)")
# tags carried by .geom/.md frames; anything else (e.g. '<-- c' constraint
# rows, '<-- T/P' scalars, '<-- V' velocities) is ignored
TRAJ_TAGS = ["E", "h", "S", "R", "F"]


def species_to_element(species):
    """Map a CASTEP species label ('H', 'Fe_1', 'O2-', 'Fe:Fe_1') to its atomic number."""
    label = species.split(':')[0] if ':' in species else species
    if label in ELEMENTTABLE:
        return ELEMENTTABLE[label]
    stripped = label.rstrip('0123456789_+-')
    if stripped in ELEMENTTABLE:
        return ELEMENTTABLE[stripped]
    stripped = stripped.capitalize()
    if stripped in ELEMENTTABLE:
        return ELEMENTTABLE[stripped]
    raise ValueError("Cannot map CASTEP species label %r to an element" % species)


def resolve_castep_file(file_path, ext):
    """Return the CASTEP file path; file_path may be the file itself or a directory."""
    if os.path.isfile(file_path):
        return file_path
    if os.path.isdir(file_path):
        matches = sorted(glob.glob(os.path.join(file_path, "*" + ext)))
        if len(matches) == 0:
            raise FileNotFoundError("No *{} file found in {}".format(ext, file_path))
        if len(matches) > 1:
            raise ValueError("Multiple *{} files found in {}, please specify the file directly".format(ext, file_path))
        return matches[0]
    raise FileNotFoundError("No such file or directory: {}".format(file_path))


def looks_like_castep_traj(file_path, n_probe=50):
    """Cheap content sniff: does the file carry '<--' data tags or a CASTEP header?

    Used to keep foreign files with a CASTEP-like extension (e.g. markdown
    *.md files) out of directory searches and format inference.
    """
    try:
        with open(file_path, 'r') as f:
            for i, line in enumerate(f):
                if i > n_probe:
                    break
                if TAG_PATTERN.search(line) or "END header" in line or "BEGIN header" in line:
                    return True
    except OSError:
        return False
    return False


def _fill_atom_info(image, species_list):
    """Set atom_type/atom_type_num/atom_types_image/atomic_energy on an Image."""
    atom_types_image = [species_to_element(species) for species in species_list]
    image.atom_nums = to_integer(len(atom_types_image))
    image.atom_types_image = to_numpy_array(atom_types_image)
    counter = Counter(atom_types_image)
    image.atom_type = to_numpy_array(list(counter.keys()))
    image.atom_type_num = to_numpy_array(list(counter.values()))
    # If Atomic-Energy is not in the file, calculate it from the Ep
    if image.atomic_energy is None and image.Ep is not None and image.atom_type_num is not None:
        atomic_energy, _, _, _ = np.linalg.lstsq([image.atom_type_num], np.array([image.Ep]), rcond=1e-3)
        atomic_energy = np.repeat(atomic_energy, image.atom_type_num)
        image.atomic_energy = to_numpy_array(atomic_energy.tolist())


def _parse_atom_row(line):
    """Parse a '<-- R/F' style row 'H  1  0.0  0.0  0.0  <-- R' into (species, [x, y, z])."""
    fields = line.split()
    species = fields[0]
    try:
        int(fields[1])
        xyz = [float(_) for _ in fields[2:5]]
    except (ValueError, IndexError):
        numbers = NUMBER_PATTERN.findall(line)
        xyz = [float(_) for _ in numbers[-3:]]
    return species, xyz


def _frame_to_image(frame, iteration):
    """Convert one parsed .geom/.md frame (tag -> rows) into an Image, or None if unusable.

    Frames with missing/incomplete force blocks are dropped with a warning:
    training data always requires forces.
    """
    if not frame["R"] or not frame["h"]:
        return None
    if not frame["F"] or len(frame["F"]) != len(frame["R"]):
        print("Warning: iteration {} has a missing/incomplete force block, the frame is skipped".format(iteration))
        return None
    species_list = [row[0] for row in frame["R"]]
    positions = np.array([row[1] for row in frame["R"]]) * BOHR2ANG
    lattice = np.array(frame["h"][:3]) * BOHR2ANG
    image = Image(lattice=lattice, position=positions, pbc=np.array([1, 1, 1]), iteration=iteration)
    image.cartesian = True
    image.force = to_numpy_array(np.array([row[1] for row in frame["F"]]) * HARTREE2EV_PER_BOHR2ANG)
    if frame["E"]:
        energies = frame["E"][0]
        image.Ep = to_float(energies[0] * HARTREE2EV)
        if len(energies) >= 3:
            image.Ek = to_float(energies[2] * HARTREE2EV)
    if len(frame["S"]) >= 3:
        stress_gpa = np.array(frame["S"][:3]) * HARTREE_PER_BOHR3_TO_GPA
        volume = np.abs(np.linalg.det(lattice))
        image.virial = to_numpy_array(gpa2ev(stress_gpa, volume))
    _fill_atom_info(image, species_list)
    return image


def _parse_trajectory_frames(file_path):
    """Parse a classic or restructured .geom/.md file into a list of frame dicts.

    Frames are blank-line separated blocks (restructured layout) carrying
    '<-- tag' labelled lines; a new '<-- E' line also starts a new frame so
    files without blank-line separators still parse. Lines before the
    'END header' marker are skipped when the header block is present.
    """
    frames = []
    current = None
    with open(file_path, 'r') as f:
        # skip the optional 'BEGIN/END header' block; files without one are
        # parsed from the beginning
        header_found = False
        for i, line in enumerate(f):
            if "END header" in line:
                header_found = True
                break
            if i > 50:
                break
        if not header_found:
            f.seek(0)
        for line in tqdm(f, desc="Reading %s" % os.path.basename(file_path)):
            stripped = line.strip()
            if stripped == "":
                if current is not None and current["R"]:
                    frames.append(current)
                current = None
                continue
            match = TAG_PATTERN.search(line)
            if match is None:
                continue    # bare lines: time value (md) / step counter (geom)
            tag = match.group(1)
            if tag not in TRAJ_TAGS:
                continue    # '<-- c' constraint rows, '<-- T/P/V' rows etc.
            if tag == "E" and current is not None and current["E"]:
                if current["R"]:
                    frames.append(current)
                current = None
            if current is None:
                current = {tag_key: [] for tag_key in TRAJ_TAGS}
            if tag in ("R", "F"):
                species, xyz = _parse_atom_row(line)
                current[tag].append((species, xyz))
            else:
                numbers = NUMBER_PATTERN.findall(line)
                current[tag].append([float(_) for _ in numbers])
        if current is not None and current["R"]:
            frames.append(current)
    return frames


class _CASTEPTrajectory(object):
    """Shared implementation of the .geom and .md trajectory parsers."""

    def __init__(self, traj_file, ext):
        self.image_list: list[Image] = []
        self.traj_file = resolve_castep_file(traj_file, ext)
        frames = _parse_trajectory_frames(self.traj_file)
        for iteration, frame in enumerate(frames):
            image = _frame_to_image(frame, iteration)
            if image is not None:
                self.image_list.append(image)
        assert len(self.image_list) > 0, "No system loaded!"
        for image in self.image_list:
            image.image_nums = len(self.image_list)
        print("Load data %s successfully! \t\t\t\t Image nums: %d" % (self.traj_file, len(self.image_list)))

    def get(self):
        return self.image_list


class CASTEPGEOM(_CASTEPTrajectory):
    """Parse a <seed>.geom geometry-optimisation trajectory (one Image per step)."""

    def __init__(self, geom_file):
        super(CASTEPGEOM, self).__init__(geom_file, ".geom")


class CASTEPMD(_CASTEPTrajectory):
    """Parse a <seed>.md AIMD trajectory (one Image per MD step)."""

    def __init__(self, md_file):
        super(CASTEPMD, self).__init__(md_file, ".md")


class CASTEPSCF(object):
    """Parse a <seed>.castep output file (single-point or geometry-optimisation).

    One Image is created per converged ionic step; the lattice, species and
    fractional positions are carried forward between steps because CASTEP may
    print them only once in highly symmetric runs. Images of steps whose SCF
    did not converge are skipped.
    """

    def __init__(self, castep_file):
        self.image_list: list[Image] = []
        self.castep_file = resolve_castep_file(castep_file, ".castep")
        self.load_castep_file()
        assert len(self.image_list) > 0, "No system loaded!"
        for image in self.image_list:
            image.image_nums = len(self.image_list)
        print("Load data %s successfully! \t\t\t\t Image nums: %d" % (self.castep_file, len(self.image_list)))

    def get(self):
        return self.image_list

    def _finalize(self, lattice, species_list, frac_positions, cur_energy,
                  cur_forces, cur_stress, cur_unconverged, cur_iteration):
        """Build an Image from the current ionic step's carried state."""
        if cur_energy is None or species_list is None or cur_unconverged:
            return None
        image = Image(lattice=lattice, position=frac_positions,
                      pbc=np.array([1, 1, 1]), iteration=cur_iteration)
        image.cartesian = False
        image.Ep = to_float(cur_energy)
        if cur_forces is not None:
            image.force = to_numpy_array(cur_forces)
        if cur_stress is not None and lattice is not None:
            volume = np.abs(np.linalg.det(lattice))
            image.virial = to_numpy_array(gpa2ev(cur_stress, volume))
        _fill_atom_info(image, species_list)
        self.image_list.append(image)
        return image

    def load_castep_file(self):
        with open(self.castep_file, 'r') as rf:
            castep_contents = rf.readlines()

        lattice = None
        species_list = None
        frac_positions = None
        cur_energy = None
        cur_forces = None
        cur_stress = None
        # cur_unconverged refers to the step being accumulated; next_unconverged
        # is set by 'SCF not converged' lines which occur during the SCF loop
        # of the FOLLOWING step (after this step's forces), so it must not be
        # applied to the pending step
        cur_unconverged = False
        next_unconverged = False
        cur_iteration = 0

        def finalize_pending():
            nonlocal cur_energy, cur_forces, cur_stress, cur_unconverged
            self._finalize(lattice, species_list, frac_positions, cur_energy,
                           cur_forces, cur_stress, cur_unconverged, cur_iteration)
            cur_energy = None
            cur_forces = None
            cur_stress = None
            cur_unconverged = False

        for idx, line in tqdm(enumerate(castep_contents), total=len(castep_contents), desc="Processing data"):
            if "SCF not converged" in line:
                next_unconverged = True
            elif "starting iteration" in line:
                match = re.search(r"starting iteration\s+(\d+)", line)
                if match is not None:
                    cur_iteration = int(match.group(1))
            elif "Real Lattice(A)" in line:
                # next lines carry the real-space lattice in Angstrom
                rows = []
                j = idx + 1
                while j < len(castep_contents) and len(rows) < 3 and j <= idx + 10:
                    numbers = NUMBER_PATTERN.findall(castep_contents[j])
                    if len(numbers) >= 3:
                        rows.append([float(_) for _ in numbers[:3]])
                    j += 1
                if len(rows) == 3:
                    lattice = np.array(rows)
            elif "Cell Contents" in line:
                # bordered table: x  Element  Count  u  v  w  x ; take rows
                # between the 'xxxx' borders, skipping header/separator rows
                rows = []
                j = idx + 1
                in_table = False
                while j < len(castep_contents) and j <= idx + 300:
                    jline = castep_contents[j]
                    if "xxxx" in jline:
                        if in_table:
                            break
                        in_table = True
                    elif in_table and rows and jline.strip() == "":
                        # blank line closes the table when the closing border
                        # is absent; the table itself never contains blanks
                        break
                    elif in_table:
                        fields = jline.split()
                        if len(fields) >= 5:
                            if fields[0] == 'x':
                                species, pos_fields = fields[1], fields[3:6]
                            else:
                                species, pos_fields = fields[0], fields[2:5]
                            try:
                                pos = [float(_) for _ in pos_fields]
                                rows.append((species, pos))
                            except ValueError:
                                pass    # header / separator rows
                    j += 1
                if rows:
                    species_list = [row[0] for row in rows]
                    frac_positions = np.array([row[1] for row in rows])
            elif "Final energy" in line:
                # covers both the modern 'Final energy, E = ...' and the old
                # CASTEP <= 6.x 'Final energy = ...'; a pending step is only
                # emitted once it carries an energy AND a complete force table
                if cur_energy is not None and cur_forces is not None:
                    finalize_pending()
                cur_unconverged = next_unconverged
                next_unconverged = False
                numbers = NUMBER_PATTERN.findall(line)
                cur_energy = float(numbers[0]) if numbers else None
                cur_forces = None
                cur_stress = None
            elif "Cartesian components (eV/A)" in line and species_list is not None:
                # one row per atom: 'spec idx fx fy fz'; force rows carry an
                # integer atom index as the second field, which distinguishes
                # them from neighbouring tables (e.g. stress rows); the scan is
                # bounded so a truncated block cannot swallow later sections
                target = len(species_list)
                forces = []
                j = idx + 1
                while j < len(castep_contents) and len(forces) < target and j <= idx + target + 20:
                    jline = castep_contents[j]
                    fields = jline.replace('*', ' ').split()
                    try:
                        int(fields[1])
                    except (ValueError, IndexError):
                        j += 1
                        continue    # decoration / header / other-section rows
                    numbers = NUMBER_PATTERN.findall(jline)
                    if len(numbers) >= 3:
                        forces.append([float(_) for _ in numbers[-3:]])
                    j += 1
                if len(forces) == target:
                    cur_forces = np.array(forces)
            elif "Cartesian components" in line and "(GPa)" in line:
                # covers both the modern 'Cartesian components of stress tensor
                # (GPa)' and the old CASTEP <= 6.x 'Cartesian components (GPa)'
                # 3 rows, each carrying the 3 stress components after the axis label
                stress_rows = []
                j = idx + 1
                while j < len(castep_contents) and len(stress_rows) < 3 and j <= idx + 8:
                    numbers = NUMBER_PATTERN.findall(castep_contents[j])
                    if len(numbers) >= 3:
                        stress_rows.append([float(_) for _ in numbers[-3:]])
                    j += 1
                if len(stress_rows) == 3:
                    cur_stress = np.array(stress_rows)
                    if cur_energy is not None and cur_forces is not None:
                        finalize_pending()    # stress table closes the step
        if cur_energy is not None:
            finalize_pending()    # salvage an energy-only step at end of file
