import shutil

import numpy as np
import pytest
from ase import Atoms
from ase.calculators.singlepoint import SinglePointCalculator

from pwdata.config import Config
from pwdata.fairchem.datasets.ase_datasets import LMDBDatabase


@pytest.mark.parametrize("cpu_nums", [1, 2])
@pytest.mark.parametrize("relative_path", ["mptrj.aselmdb", "MPTRJ/dataset.aselmdb"])
def test_meta_stress_is_independent_of_database_path(tmp_path, cpu_nums, relative_path):
    stress = np.array([[0.1, 0.02, 0.03], [0.02, -0.2, 0.04], [0.03, 0.04, 0.3]])
    atoms = Atoms("H", positions=[[0.0, 0.0, 0.0]], cell=[2.0, 3.0, 4.0], pbc=True)
    atoms.calc = SinglePointCalculator(
        atoms, energy=-1.25, forces=np.zeros((1, 3)), stress=stress
    )
    source = tmp_path / "standard.aselmdb"
    db = LMDBDatabase(filename=str(source), readonly=False)
    try:
        db.write(atoms)
    finally:
        db.close()
    copied = tmp_path / relative_path
    copied.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(source, copied)

    expected = -stress * atoms.get_volume()
    for path in (source, copied):
        image = Config(data_path=str(path), format="meta", cpu_nums=cpu_nums).images[0]
        np.testing.assert_allclose(image.virial, expected)
        assert image.Ep == -1.25
        np.testing.assert_array_equal(image.force, np.zeros((1, 3)))
