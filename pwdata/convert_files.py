import os
import sys
import numpy as np
from pwdata.config import Config, Save_Data
from pwdata.build.supercells import make_supercell
from pwdata.pertub.perturbation import perturb_structure
from pwdata.pertub.scale import scale_cell
from pwdata.utils.constant import FORMAT
from pwdata.utils.constant import get_atomic_name_from_number
def do_convert_config(input_file:str, 
                    input_format:str, 
                    atom_types:list[str],
                    savename:str, 
                    output_format:str, 
                    direct:bool = True): # True: save as fractional coordinates, False for cartesian coordinates
    image = Config(data_path=input_file, format=input_format, atom_names=atom_types)
    image.to(output_path = os.path.dirname(os.path.abspath(savename)),
          data_name = os.path.basename(savename),
          save_format = output_format,
          direct = direct,
          sort = True)
    return os.path.abspath(savename)

def do_scale_cell(input_file:str, 
                    input_format:str,
                    atom_types:list[str],
                    savename:str, 
                    output_format:str, 
                    scale_factor:float,
                    direct:bool = True): # True: save as fractional coordinates, False for cartesian coordinates
    # for pwamt/movement movement or MLMD.OUT files
    image = Config(data_path=input_file, format=input_format, atom_names=atom_types)
    scaled_structs = scale_cell(image, scale_factor)
    scaled_structs.to(output_path = os.path.dirname(os.path.abspath(savename)),
          data_name = os.path.basename(savename),
          save_format = output_format,
          direct = direct,
          sort = True)
    return os.path.abspath(savename)

def do_super_cell(input_file:str, 
                    input_format:str, 
                    atom_types:list[str],
                    savename:str, 
                    output_format:str, 
                    supercell_matrix:list[int],
                    direct:bool = True,
                    pbc:list =[1, 1, 1],
                    wrap=True, 
                    tol=1e-5
                    ): # True: save as fractional coordinates, False for cartesian coordinates
    # for pwamt/movement movement or MLMD.OUT files
    image = Config(data_path=input_file, format=input_format, atom_names=atom_types)
    scaled_structs = make_supercell(image, supercell_matrix, pbc=pbc, wrap=wrap, tol=tol)
    scaled_structs.to(output_path = os.path.dirname(os.path.abspath(savename)),
          data_name = os.path.basename(savename),
          save_format = output_format,
          direct = direct,
          sort = True)
    return os.path.abspath(savename)

def do_perturb(input_file:str, 
                    input_format:str, 
                    atom_types:list[str],
                    save_path:str, 
                    save_name_prefix:str,
                    output_format:str, 
                    cell_pert_fraction:float,
                    atom_pert_distance:float,
                    pert_num:int,
                    direct:bool = True,
                    pbc:list =[1, 1, 1],
                    wrap=True, 
                    tol=1e-5
                    ): # True: save as fractional coordinates, False for cartesian coordinates
    # for pwamt/movement movement or MLMD.OUT files
    image = Config(data_path=input_file, format=input_format, atom_names=atom_types)
    save_path = os.path.abspath(save_path)
    perturbed_structs = perturb_structure(
            image_data = image,
            pert_num = pert_num,
            cell_pert_fraction = cell_pert_fraction,
            atom_pert_distance = atom_pert_distance)

    perturb_files = []
    for tmp_perturbed_idx, tmp_pertubed_struct in enumerate(perturbed_structs):
        tmp_pertubed_struct.to(output_path = save_path,
                                data_name = "{}_{}".format(tmp_perturbed_idx, save_name_prefix),
                                save_format = output_format,
                                direct = direct,
                                sort = True)
        perturb_files.append("{}_{}".format(tmp_perturbed_idx, save_name_prefix))
    return perturb_files, perturbed_structs

def do_convert_images(
    input:list[str], 
    input_format:str, 
    savepath, #'the/path/pwmlff-datas'
    output_format, 
    train_valid_ratio, 
    data_shuffle, 
    gap,
    atom_types:list[str]=None
):
    data_files = search_images(input, input_format)
    image_data = load_files(data_files, input_format, atom_types=atom_types)
    save_dict = split_image_by_atomtype_nums(image_data, format=output_format)
    for key, images in save_dict.items():
        save_dir = os.path.join(savepath, key) if output_format == FORMAT.extxyz else savepath
        image_data.images = images
        image_data.to(
                    output_path=save_dir,
                    save_format=output_format,
                    train_ratio = train_valid_ratio, 
                    random=data_shuffle,
                    seed = 2024, 
                    retain_raw = False
                    )

def search_images(input_list:list[str], input_format:str):
    res_list = set()
    for workDir in input_list:
        workDir = os.path.abspath(workDir)
        if os.path.isfile(workDir):
            res_list.add(workDir)
        else:
            if input_format == FORMAT.pwmlff_npy:
                for root, dirs, files in os.walk(workDir):
                    if 'energies.npy' in files:
                        if "train" in os.path.basename(root):
                            res_list.add(os.path.dirname(root))

            elif input_format == FORMAT.extxyz:
                for path, dirList, fileList in os.walk(workDir, followlinks=True):
                    for _ in fileList:
                        if ".xyz" in _:
                            res_list.add(os.path.join(path, _))
            
            elif input_format == FORMAT.deepmd_npy:
                for root, dirs, files in os.walk(workDir):
                    if 'energy.npy' in files:
                        res_list.add(os.path.dirname(root))

            elif input_format == FORMAT.deepmd_raw:
                for root, dirs, files in os.walk(workDir):
                    if 'energy.raw' in files:
                        res_list.add(os.path.dirname(root))   
    
    return res_list

def load_files(input_list:list[str], input_format:str, atom_types:list[str]=None):
    image_data = None
    for data_path in input_list:
        if image_data is not None:
            tmp_config = Config(input_format, data_path, atom_names=atom_types)
            image_data.append(tmp_config)
        else:
            image_data = Config(input_format, data_path, atom_names=atom_types)
            if not isinstance(image_data.images, list): # for the first pwmlff/npy dir only has one picture
                image_data.images = [image_data.images]
    return image_data

def split_image_by_atomtype_nums(image_data, format=None):
    key_dict = {}
    for idx, image in enumerate(image_data.images):
        atom_type, counts = np.unique(image.atom_types_image, return_counts=True)
        tmp_key = ""
        for element, count in zip(atom_type, counts):
            tmp_key += "{}_{}_".format(element, count)
        if tmp_key not in key_dict:
            key_dict[tmp_key] = [image]
        else:
            key_dict[tmp_key].append(image)

    new_split = {}
    for key in key_dict.keys():
        elements = key.split('_')[:-1]
        new_array = [int(elements[i]) for i in range(0, len(elements), 2)]
        type_nums = elements[1::2]
        atom_list = get_atomic_name_from_number(new_array)
        new_key = []
        if format == FORMAT.extxyz:
            new_key = "".join(atom_list)
            if new_key not in new_split:
                new_split[new_key] = key_dict[key]
            else:
                new_split[new_key].extend(key_dict[key])
        else: # for pwmlff/npy
            for atom, num in zip(atom_list, type_nums):
                new_key.append(atom)
                new_key.append(num)
            new_key = "".join(new_key)
            new_split[new_key] = key_dict[key]
    return new_split
