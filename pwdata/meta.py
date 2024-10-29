import numpy as np
import os, glob
from tqdm import tqdm
from pwdata.image import Image
from concurrent.futures import ProcessPoolExecutor, as_completed
import multiprocessing
from collections import Counter
from functools import partial

class META(object):
    def __init__(self, files: list[str], atom_names: list[str] = None, query: str = None, cpu_nums: int=None):
        self.image_list:list[Image] = []
        self.load_files_cpus(files, atom_names, query, cpu_nums)
        # assert len(self.image_list) > 0, "No data loaded!"

    def get(self):
        return self.image_list
    
    def load_files(self, input:list[str], atom_types: list[str] = None, query: str = None, cpu_nums: int=None):
        from pwdata.fairchem.datasets.ase_datasets import AseDBDataset
        
        def query_fun(row, elements:list[str]=None):
            if elements is None:
                return True
            return sorted(set(row.symbols)) == elements

        search_dict = {'src': input}
        dataset = AseDBDataset(config=search_dict)
        if atom_types is not None:
            filter_with_elements = partial(query_fun, elements=sorted(atom_types))
        for ids, dbs in enumerate(dataset.dbs):
            if query is None and atom_types is None:
                atom_list = list(dbs.select())
            elif query is None and atom_types is not None:
                atom_list = list(dbs.select("".join(atom_types), filter=filter_with_elements))
            elif query is not None and atom_types is not None:
                atom_list = list(dbs.select(query, filter=filter_with_elements))
            else:# query is not None and atom_types is None:
                atom_list = list(dbs.select(query))
            for Atoms in atom_list:
                image = to_image(Atoms)
                self.image_list.append(image)

    def load_files_cpus(self, input: list[str], atom_types: list[str] = None, query: str = None, cpu_nums: int = None):
        from pwdata.fairchem.datasets.ase_datasets import AseDBDataset
        
        def query_fun(row, elements):
            return sorted(set(row.symbols)) == elements

        # 设置数据源和查询过滤器
        search_dict = {'src': input}
        dataset = AseDBDataset(config=search_dict)
        if atom_types is not None:
            filter_with_elements = partial(query_fun, elements=sorted(atom_types))
        if cpu_nums is None:
            cpu_nums = multiprocessing.cpu_count()
        else:
            cpu_nums = min(cpu_nums, multiprocessing.cpu_count())
        # 使用多进程并行处理数据库查询
        with ProcessPoolExecutor(max_workers=cpu_nums) as executor:
            futures = []
            for dbs in dataset.dbs:
                if query is None and atom_types is None:
                    atom_list = list(dbs.select())
                elif query is None and atom_types is not None:
                    atom_list = list(dbs.select("".join(atom_types), filter=filter_with_elements))
                elif query is not None and atom_types is not None:
                    atom_list = list(dbs.select(query, filter=filter_with_elements))
                else:  # query is not None and atom_types is None
                    atom_list = list(dbs.select(query))
                
                # 提交查询和转换任务
                futures.append(executor.submit(self.process_atoms, atom_list))

            # 收集所有结果
            for future in as_completed(futures):
                self.image_list.extend(future.result())

    @staticmethod
    def process_atoms(atom_list):
        """处理每个 atom_list 并转换为图像对象列表"""
        return [to_image(Atoms) for Atoms in atom_list]


# def make_query(elements:list[str]):
#     # 这个闭包函数将捕获 elements 参数
#     def query(row):
#         if sorted(set(row.symbols)) == sorted(elements):
#             return True
#         return False
#     return query

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