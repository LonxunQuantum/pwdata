import os, re
import numpy as np
from tqdm import tqdm
from pwdata.calculators.const import elements, ELEMENTTABLE
from pwdata.image import Image
from ase.io import read
from math import ceil
from collections import Counter

class EXTXYZ(object):
    # index is not used in this reading
    def __init__(self, xyz_file, index=None) -> None:
        self.image_list:list[Image] = []
        self.number_pattern = re.compile(r"[-+]?\d+(?:\.\d+)?(?:[eE][-+]?\d+)?")
        self.load_xyz_file(xyz_file, index)

    def get(self):
        return self.image_list

    def load_xyz_file(self, xyz_file, index):
        image_list = read_structures(xyz_file)
        self.image_list=image_list

def save_to_extxyz(image_data_all: list, data_path: str, data_name=None, random = False, seed = None, retain_raw = False, write_patthen="a"
                    ):
    if not os.path.exists(data_path):
        os.makedirs(data_path)
    if data_name is None:
        data_name = "train.xyz"
    elif ".xyz" not in data_name:
        data_name += ".xyz"
    train_file = open(os.path.join(data_path, data_name), write_patthen)
    image_nums = image_data_all.__len__()
    if seed:
        np.random.seed(seed)
    indices = np.arange(image_nums)    # 0, 1, 2, ..., image_nums-1
    if random:
        np.random.shuffle(indices)              # shuffle the indices

    for i in indices:
        image_data = image_data_all[i]
        if not image_data.cartesian:
            image_data._set_cartesian()
        xyz_content = get_xyz_content(image_data)
        train_file.write(xyz_content)
    train_file.close()
        # print("Convert to {} and {} successfully!".format(train_data_path, valid_data_path))
    # else:
        # print("Convert to %s successfully!" % train_data_path)

def get_xyz_content(image_data:Image):
    xyz_content = ""
    if not image_data.cartesian:
        image_data._set_cartesian()
    xyz_content +="%d\n" % image_data.atom_nums
    # data_name.write("Iteration: %s\n" % image_data.iteration)
    has_bec = image_data.bec is not None and len(image_data.bec) > 0
    has_fragment = image_data.fragment is not None and len(image_data.fragment) > 0
    has_charge = image_data.charge is not None and len(image_data.charge) > 0
    properties_head = "Properties=species:S:1:pos:R:3:"
    properties_head += "bec:R:9:" if has_bec else ""
    properties_head += "force:R:3"
    properties_head += ":fragment:I:1" if has_fragment else ""
    properties_head += ":charge:R:1" if has_charge else ""
    output_head = 'Lattice="%.5f %.5f %.5f %.5f %.5f %.5f %.5f %.5f %.5f" {} pbc="T T T" energy={} '.format(properties_head, image_data.Ep)
    output_extended = (image_data.lattice[0][0], image_data.lattice[0][1], image_data.lattice[0][2], 
                        image_data.lattice[1][0], image_data.lattice[1][1], image_data.lattice[1][2], 
                        image_data.lattice[2][0], image_data.lattice[2][1], image_data.lattice[2][2])
    if image_data.virial is not None and len(image_data.virial) > 0:
        output_head += 'virial="%.4f %.4f %.4f %.4f %.4f %.4f %.4f %.4f %.4f" '
        virial = image_data.get_virial()
        output_extended += (virial[0][0], virial[0][1], virial[0][2], 
                            virial[1][0], virial[1][1], virial[1][2], 
                            virial[2][0], virial[2][1], virial[2][2])
    if image_data.fragment_charge_status is not None:
        output_head += "fragment_charge_status={} ".format(image_data.fragment_charge_status)
    output_head += '\n'
    xyz_content += output_head % output_extended

    for j in range(image_data.atom_nums):
        properties_format = "%s"
        properties = [elements[image_data.atom_types_image[j]], image_data.position[j][0], image_data.position[j][1], image_data.position[j][2]]
        properties_format += " %14.8f %14.8f %14.8f"
        if has_bec:
            properties_format += " " + " %14.8f" * 9
            properties.extend(image_data.bec[j].reshape(-1))
        properties_format += " %14.8f %14.8f %14.8f"
        properties.extend([image_data.force[j][0], image_data.force[j][1], image_data.force[j][2]])
        if has_fragment:
            properties_format += " %d"
            properties.append(image_data.fragment[j])
        if has_charge:
            properties_format += " %14.8f"
            properties.append(image_data.charge[j])
        properties_format += "\n"
        xyz_content += properties_format % tuple(properties)
    return xyz_content

def read_structures(
    file_name:str
):
    """
    Reads structures from a file based on the given configuration.

    Args:
        config (Config): The configuration object.
        file_name (str): The name of the file to read from.
        is_train (bool, optional): Whether the data is for training. Defaults to True.

    Returns:
        List[Structure]: A list of structures read from the file.
    """
    image_list = []
    index_cout = 0
    with open(file_name, "r") as file:
        
        while True:
            num_lines_per_frame = file.readline().strip()
            index_cout += 1
            if not num_lines_per_frame:
                break
            num_lines_per_frame = int(num_lines_per_frame)
            assert (
                num_lines_per_frame
            ), "Number of lines per frame should be a positive integer"

            frames = [file.readline().strip()]
            index_cout += 1
            for _ in range(num_lines_per_frame):
                line = file.readline().strip()
                if line:
                    frames.append(line)
            index_cout += num_lines_per_frame
            image = read_one_structures_from_lines(frames)
            image_list.append(image)
    assert len(image_list) > 0, "extxyz file {} parsing failed".format(file_name)
    return image_list

def read_one_structures_from_lines(lines:list[str]):
    """
    Reads and parses structure data from a list of lines.
    Returns:
        Structure: Parsed structure object.
    """
    image = Image()
    image.format = 'extxyz'
    image.atom_nums = len(lines) - 1

    # 使用正则表达式 (\w+)=("[^"]*"|\S+) 匹配键值对。其中：
    # (\w+) 匹配键，即一个或多个字母数字字符。
    # = 匹配等号。
    # ("[^"]*"|\S+) 匹配值，其中 "[^"]*" 匹配带引号的字符串，\S+ 匹配不带引号的字
    pattern = r'(\w+)=("[^"]*"|\S+)'
    matches = re.findall(pattern, lines[0])
    result_dict = {key.lower(): value.strip('"') for key, value in matches}
    image.Ep = float(result_dict["energy"])
    properties = result_dict["properties"].split(":")
    atom_types_image, postion, force, bec, fragment, charge = read_properties_data(image.atom_nums, properties, lines[1:])
    image.force = force
    image.position = postion
    image.atom_types_image = atom_types_image
    image.bec = bec
    image.fragment = fragment
    image.charge = charge
    image.fragment_charge_status = result_dict.get("fragment_charge_status")
    lattice = [float(i) for i in result_dict["lattice"].split()]
    assert len(lattice) == 9, "lattice in extxyz file should has 9 elements"
    image.lattice = np.array(lattice).reshape(-1, 3)
    image.cartesian = True

    element_counts = Counter(atom_types_image)
    image.atom_type = np.array(list(element_counts.keys()))
    image.atom_type_num = np.array(list(element_counts.values()))

    if "virial" in result_dict.keys():
        virial = [float(i) for i in result_dict["virial"].split()]
        assert len(virial) == 9, "virial in extxyz file should has 9 elements"
        image.virial = np.array(virial).reshape(3, 3)
    elif "stress" in result_dict.keys():
        stress = [float(i) for i in result_dict["stress"].split()]
        assert len(stress) == 9, "stress in extxyz file should has 9 elements"
        volume = np.abs(np.linalg.det(image.lattice))
        image.virial = -volume * np.reshape(stress, (3, 3))
    
    atomic_energy, _, _, _ = np.linalg.lstsq([image.atom_type_num], np.array([image.Ep]), rcond=1e-3)
    atomic_energy = np.repeat(atomic_energy, image.atom_type_num)
    image.atomic_energy = atomic_energy

    return image

def read_properties_data(
    num_atom:int, properties: list[str], lines: list[str]
):
    assert len(properties) % 3 == 0
    property_map = {}
    offset = 0
    for i in range(len(properties) // 3):
        name = properties[i * 3].lower()
        size = int(properties[i * 3 + 2])
        property_map[name] = (offset, size)
        offset += size

    assert "species" in property_map, "species property is required in extxyz file"
    assert "pos" in property_map, "pos property is required in extxyz file"
    force_key = "forces" if "forces" in property_map else "force"
    assert force_key in property_map, "force or forces property is required in extxyz file"
    if "bec" in property_map:
        assert property_map["bec"][1] == 9, "bec in extxyz file should has 9 elements per atom"
    if "fragment" in property_map:
        assert property_map["fragment"][1] == 1, "fragment in extxyz file should has 1 element per atom"
    if "charge" in property_map:
        assert property_map["charge"][1] == 1, "charge in extxyz file should has 1 element per atom"

    species_offset, _ = property_map["species"]
    pos_offset, pos_size = property_map["pos"]
    force_offset, force_size = property_map[force_key]
    assert pos_size == 3, "pos in extxyz file should has 3 elements per atom"
    assert force_size == 3, "force in extxyz file should has 3 elements per atom"

    bec_offset = property_map["bec"][0] if "bec" in property_map else None
    fragment_offset = property_map["fragment"][0] if "fragment" in property_map else None
    charge_offset = property_map["charge"][0] if "charge" in property_map else None
    assert num_atom == len(lines)
    type_list = []
    force = []
    position= []
    bec = [] if bec_offset is not None else None
    fragment = [] if fragment_offset is not None else None
    charge = [] if charge_offset is not None else None
    for line in lines:
        data = line.split()
        type_list.append(ELEMENTTABLE[data[species_offset]])
        force.append([float(data[force_offset]), float(data[force_offset + 1]), float(data[force_offset + 2])])
        position.append([float(data[pos_offset]), float(data[pos_offset + 1]), float(data[pos_offset + 2])])
        if bec_offset is not None:
            bec.append([float(data[bec_offset + i]) for i in range(9)])
        if fragment_offset is not None:
            fragment.append(int(data[fragment_offset]))
        if charge_offset is not None:
            charge.append(float(data[charge_offset]))
    type_list = np.array(type_list) #.reshape(-1, 1)
    position = np.array(position)
    force = np.array(force)
    bec = np.array(bec).reshape(num_atom, 9) if bec is not None else None
    fragment = np.array(fragment, dtype=int) if fragment is not None else None
    charge = np.array(charge, dtype=float) if charge is not None else None
    return type_list, position, force, bec, fragment, charge

