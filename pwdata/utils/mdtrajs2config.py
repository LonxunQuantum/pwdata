from pwdata import Config
from pwdata.utils.constant import FORMAT
import json
from pwdata.fairchem.datasets.ase_datasets import LMDBDatabase
from ase import Atoms
from ase.db.row import AtomsRow
from pwdata.utils.constant import get_atomic_number_from_name
from tqdm import tqdm
import numpy as np

def trajs2config():
    atom_types = ["Hf", "O"] # for lammps
    input_file = "/data/home/wuxingxing/codespace/pwdata/examples/lmps_data/HfO2/30.lammpstrj"
    input_format="lammps/dump"
    save_format = "pwmat/config"

    image = Config(data_path=input_file, format=input_format, atom_names=atom_types)
    tmp_image_data = image.images
    save_dir = "./tmp_test"
    for id, config in enumerate(tmp_image_data):
        savename = "{}_{}".format(id, FORMAT.get_filename_by_format(save_format))
        image.iamges = [config]
        image.to(output_path = save_dir,
            data_name = savename,
            save_format = save_format,
            sort = True)

def MPjson2lmdb():
    mp_file = "/data/home/wuxingxing/codespace/pwdata/examples/mp_data/mptest.json"
    save_file = "/data/home/wuxingxing/codespace/pwdata/examples/mp_data/sub.aselmdb"
    Mpjson = json.load(open(mp_file))
    db = LMDBDatabase(filename=save_file, readonly=False)
    for key_1, val_1 in tqdm(Mpjson.items(), total=len(Mpjson.keys())):
        for key_2, val_2 in val_1.items():
            _atomrow, data = cvt_dict_2_atomrow(val_2)
            db._write(_atomrow, key_value_pairs={}, data=data)
    db.close()
    
def cvt_dict_2_atomrow(config:dict):
    # read cell
    cell = read_from_dict('matrix', config['structure']['lattice'], require=True)
    # read position
    atom_type_list = get_atomic_number_from_name([_['label'] for _ in config['structure']['sites']])
    position = [_['xyz'] for _ in config['structure']['sites']]
    # read magmom
    magmom = read_from_dict('magmom', config, require=True)
    
    atom = Atoms(positions=position,
                numbers=atom_type_list,
                magmoms=magmom,
                cell=cell)

    atom_rows = AtomsRow(atom)
    atom_rows.pbc = np.ones(3, bool)
    # read stress -> xx, yy, zz, yz, xz, xy
    stress = read_from_dict('stress', config, require=True)
    atom_rows.stress = [stress[0][0],stress[1][1],stress[2][2],stress[1][2],stress[0][2],stress[0][1]]
    # read force and energy
    force = read_from_dict('force', config, require=True)
    energy = read_from_dict('corrected_total_energy', config, require=True)
    atom_rows.__setattr__('force',  force)
    atom_rows.__setattr__('energy', energy)
    data = {}
    data['uncorrected_total_energy'] = read_from_dict('uncorrected_total_energy', config, default=None)
    data['corrected_total_energy'] = read_from_dict('uncorrected_total_energy', config, default=None)
    data['energy_per_atom'] = read_from_dict('energy_per_atom', config, default=None)
    data['ef_per_atom'] = read_from_dict('ef_per_atom', config, default=None)
    data['e_per_atom_relaxed'] = read_from_dict('e_per_atom_relaxed', config, default=None)
    data['ef_per_atom_relaxed'] = read_from_dict('ef_per_atom_relaxed', config, default=None)
    data['bandgap'] = read_from_dict('bandgap', config, default=None)
    data['mp_id'] = read_from_dict('mp_id', config, default=None)
    # atom_rows._data = data
    return atom_rows, data

def read_from_dict(key:str, config:dict, default=None, require=False):
    if key in config:
        return config[key]
    else:
        if require:
            raise ValueError("key {} not found in config".format(key))
        else:
            return default

def test_lmdb():
    from pwdata.fairchem.datasets.ase_datasets import AseDBDataset
    # search_dict = {'src': '/data/home/wuxingxing/codespace/pwdata/examples/meta_data/alex_val/alex_go_aao_001.aselmdb'}
    # dataset = AseDBDataset(config=search_dict)
    # #2 data omat 非平衡态
    # atom_list = list(dataset.dbs[0].select("Li"))
    # std = atom_list[0]
    
    # search_dict = {'src': '/data/home/wuxingxing/codespace/pwdata/examples/MPtrj.aselmdb'}
    # dataset2 = AseDBDataset(config=search_dict)
    # #2 data omat 非平衡态
    # atom_list2 = list(dataset2.dbs[0].select("Li"))
    # dev = atom_list2[0]

    search_dict = {'src': '/data/home/wuxingxing/codespace/pwdata/examples/mp_data/sub.aselmdb'}
    dataset3 = AseDBDataset(config=search_dict)
    #2 data omat 非平衡态
    atom_list3 = list(dataset3.dbs[0].select())
    std3 = atom_list3[0]

    print()

if __name__=="__main__":
    MPjson2lmdb()
    test_lmdb()

	