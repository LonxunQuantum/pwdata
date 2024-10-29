import os
import sys
import numpy as np
from pwdata.config import Config
from pwdata.build.supercells import make_supercell
from pwdata.pertub.perturbation import perturb_structure
from pwdata.pertub.scale import scale_cell
from pwdata.utils.constant import FORMAT, ELEMENTTABLE
from pwdata.utils.constant import get_atomic_name_from_number
from pwdata.image import Image
from collections import Counter
from ase.db.row import AtomsRow
from pwdata.fairchem.datasets.ase_datasets import AseDBDataset
from concurrent.futures import ProcessPoolExecutor, as_completed
import multiprocessing

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
                    scale_factor:list[float],
                    direct:bool = True): # True: save as fractional coordinates, False for cartesian coordinates
    # for pwamt/movement movement or MLMD.OUT files
    if not isinstance(scale_factor, list):
        scale_factor = [scale_factor]
    image = Config(data_path=input_file, format=input_format, atom_names=atom_types)
    for idx, factor in enumerate(scale_factor):
        scaled_structs = scale_cell(image, factor)
        scaled_structs.to(output_path = os.path.dirname(os.path.abspath(savename)),
            data_name = "{}_{}".format(factor, os.path.basename(savename)),
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
                    direct:bool = True
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
    atom_types:list[str]=None,
    query:str=None,
    cpu_nums:int=None,
    merge:bool=True
):
    data_files = search_images(input, input_format)
    image_data = load_files(data_files, input_format, atom_types=atom_types, query=query, cpu_nums=cpu_nums)
    save_images(savepath, image_data, output_format, train_valid_ratio, data_shuffle, merge)

'''
description: 
    save the image_datas to pwmlff/npy or extxyz format
    for pwmlff/npy, the images will save to subdir accordding to the atom types and atom nums of each type, such as Pb20Te30, Pb21Te30, ... 
    for extxyz, the images will save to subdir accordding to the atom types, such as PbTe, PbTeG
param {*} savepath
param {*} image_data
param {*} output_format
param {*} train_valid_ratio
param {*} data_shuffle
return {*}
author: wuxingxing
'''
def save_images(savepath, image_data, output_format, train_valid_ratio=1, data_shuffle=False, merge=True):
    if merge is True and output_format == FORMAT.extxyz:
        save_dir = savepath
        image_data.to(
                        output_path=save_dir,
                        save_format=output_format,
                        train_ratio = train_valid_ratio, 
                        random=data_shuffle,
                        seed = 2024, 
                        retain_raw = False,
                        write_patthen="a"
                        )
    else:
        save_dict = split_image_by_atomtype_nums(image_data, format=output_format)
        for key, images in save_dict.items():
            # print(len(images))
            save_dir = os.path.join(savepath, key) if output_format==FORMAT.extxyz else savepath #pwmlff/npy will do split when saving images
            image_data.images = images
            image_data.to(
                        output_path=save_dir,
                        save_format=output_format,
                        train_ratio = train_valid_ratio, 
                        random=data_shuffle,
                        seed = 2024, 
                        retain_raw = False,
                        write_patthen="a"
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
            
            elif input_format == FORMAT.meta:
                for root, dirs, files in os.walk(workDir):
                    for file in files:
                        if '.aselmdb' in file:
                            res_list.add(root)
                            break

    return list(res_list)

def load_files(input_list:list[str], input_format:str, atom_types:list[str]=None, query:str=None, cpu_nums=None):
    image_data = None
    if input_format == FORMAT.meta:
        image_data = Config(input_format, input_list, atom_names=atom_types, query=query, cpu_nums=cpu_nums)
        if not isinstance(image_data.images, list): # for the first pwmlff/npy dir only has one picture
            image_data.images = [image_data.images]
    else:
        for data_path in input_list:
            if image_data is not None:
                tmp_config = Config(input_format, data_path, atom_names=atom_types, query=query, cpu_nums=cpu_nums)
                image_data.append(tmp_config)
            else:
                image_data = Config(input_format, data_path, atom_names=atom_types, query=query, cpu_nums=cpu_nums)
                if not isinstance(image_data.images, list): # for the first pwmlff/npy dir only has one picture
                    image_data.images = [image_data.images]
    return image_data

def split_image_by_atomtype_nums(image_data, format=None):
    key_dict = {}
    for idx, image in enumerate(image_data.images):
        element_counts = Counter(image.atom_types_image)
        atom_type = list(element_counts.keys())
        counts = list(element_counts.values())
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

def make_query(elements:list[str]):
    # 这个闭包函数将捕获 elements 参数
    def query(row):
        if sorted(set(row.symbols)) == sorted(elements):
            return True
        return False
    return query
    
def do_meta_data(input,
                savepath,
                output_format,
                train_valid_ratio,
                split_rand,
                atom_types:list[str]=None,
                query_str:str=None,
                cpu_nums:int=None):
    image_data = load_meta_datas(input, atom_types, query_str, cpu_nums)
    save_images(savepath, image_data, output_format, train_valid_ratio, split_rand)

def load_meta_datas(input, atom_types: list[str] = None, query_str: str = None, cpu_nums: int=None):
    search_dict = {'src': input}
    dataset = AseDBDataset(config=search_dict)
    image_list = []
    for ids, dbs in enumerate(dataset.dbs):
        if query_str is None and atom_types is None:
            atom_list = list(dbs.select())
        elif query_str is None and atom_types is not None:
            atom_list = list(dbs.select("".join(atom_types)))
        elif query_str is not None and atom_types is not None:
            atom_list = list(dbs.select(query_str,filter=make_query))
        else:# query_str is not None and atom_types is None:
            atom_list = list(dbs.select(query_str))
        for Atoms in atom_list:
            image = to_image(Atoms)
            image_list.append(image)
    image_data = Config()
    image_data.images = image_list
    return image_data

### ProcessPoolExecutor
def load_meta_datas_cpus(input, atom_types: list[str] = None, query_str: str = None, cpu_nums: int=None):
    search_dict = {'src': input}
    dataset = AseDBDataset(config=search_dict)
    image_list = []
    # 定义一个辅助函数，用于查询和转换每个数据库中的数据
    def process_dbs(dbs):
        # 根据条件构建 atom_list
        if query_str is None and atom_types is None:
            atom_list = list(dbs.select())
        elif query_str is None and atom_types is not None:
            atom_list = list(dbs.select("".join(atom_types)))
        elif query_str is not None and atom_types is not None:
            atom_list = list(dbs.select(query_str, filter=make_query))
        else:
            atom_list = list(dbs.select(query_str))
        # 对每个原子对象进行转换并返回 image 列表
        return [to_image(Atoms) for Atoms in atom_list]

    # 使用多进程并行处理每个子数据库
    if cpu_nums is None:
        cpu_nums = multiprocessing.cpu_count()
    with ProcessPoolExecutor(max_workers=cpu_nums) as executor:
        futures = [executor.submit(process_dbs, dbs) for dbs in dataset.dbs]
        for future in as_completed(futures):
            image_list.extend(future.result())
    
    image_data = Config()
    image_data.images = image_list
    return image_data

def to_image(Atoms):
    image = Image()
    image.formula = Atoms.formula
    image.pbc = Atoms.pbc
    image.atom_nums = Atoms.natoms
    type_nums_dict = Counter(Atoms.numbers)
    image.atom_type = np.array(list(type_nums_dict.keys()))
    image.atom_type_num = np.array(list(type_nums_dict.values()))
    image.atom_types_image = np.array(Atoms.numbers)
    image.lattice = np.array(Atoms.cell)
    image.position = Atoms.positions
    image.cartesian = True
    image.force = Atoms.forces
    image.Ep = Atoms.energy

    # 计算 Atomic-Energy
    atomic_energy, _, _, _ = np.linalg.lstsq([image.atom_type_num], np.array([image.Ep]), rcond=1e-3)
    atomic_energy = np.repeat(atomic_energy, image.atom_type_num)
    image.atomic_energy = atomic_energy.tolist()

    vol = Atoms.volume
    virial = (-np.array(Atoms.stress) * vol)
    image.virial = np.array([
        [virial[0], virial[5], virial[4]],
        [virial[5], virial[1], virial[3]],
        [virial[4], virial[3], virial[2]]
    ])
    image.format = 'metadata'
    return image