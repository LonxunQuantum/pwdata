
import os, sys
import argparse
from fairchem.core.datasets import AseDBDataset
from ase.db.row import AtomsRow
def read_meta_datas(dataset_path, **config_kwargs):
    dataset = AseDBDataset(config=dict(src=dataset_path, **config_kwargs))
    # atoms objects can be retrieved by index
    def query(row:AtomsRow):
        for atom in row.symbols:
            if atom not in elements:
                return False
        return True
    
    # atoms = dataset.get_atoms(0)
    elements = ["Hf", "Ge", "H"]
    atom_list = list(dataset.dbs[0].select('Hf,Ge,H', filter=query))
    atoms = dataset.get_atoms(0)
    
def write_meta_datas():
    pass

def get_meta_data(cmd_list:list[str]):
    parser = argparse.ArgumentParser(description='handle meta data')
    parser.add_argument('-i', '--input', help='specify dataset paths of meta data', nargs='+', type=str, default=None)
    # parser.add_argument('--format', type=str, required=False, help='Format of the input file', default="outcar")
    # parser.add_argument('--save_format', type=str, required=False, help='Format of the output file', default="config")
    # parser.add_argument('--outcar_file', type=str, required=False, help='Path to the OUTCAR file')
    # parser.add_argument('--movement_file', type=str, required=False, help='Path to the MOVEMENT file')
    args = parser.parse_args(cmd_list)
    dataset_path = args.input
    read_meta_datas(dataset_path)
    