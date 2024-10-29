import argparse, sys
import numpy as np
from pwdata.fairchem.datasets.ase_datasets import AseDBDataset

Omat24_train = [
"/share/public/PWMLFF_test_data/eqv2-models/datasets/decompress/Omat24/train/rattled-1000",
"/share/public/PWMLFF_test_data/eqv2-models/datasets/decompress/Omat24/train/rattled-1000-subsampled",
"/share/public/PWMLFF_test_data/eqv2-models/datasets/decompress/Omat24/train/rattled-300",
"/share/public/PWMLFF_test_data/eqv2-models/datasets/decompress/Omat24/train/rattled-300-subsampled",
"/share/public/PWMLFF_test_data/eqv2-models/datasets/decompress/Omat24/train/rattled-500",
"/share/public/PWMLFF_test_data/eqv2-models/datasets/decompress/Omat24/train/rattled-500-subsampled",
"/share/public/PWMLFF_test_data/eqv2-models/datasets/decompress/Omat24/train/rattled-relax",
"/share/public/PWMLFF_test_data/eqv2-models/datasets/decompress/Omat24/train/aimd-from-PBE-1000-npt",
"/share/public/PWMLFF_test_data/eqv2-models/datasets/decompress/Omat24/train/aimd-from-PBE-1000-nvt",
"/share/public/PWMLFF_test_data/eqv2-models/datasets/decompress/Omat24/train/aimd-from-PBE-3000-npt",
"/share/public/PWMLFF_test_data/eqv2-models/datasets/decompress/Omat24/train/aimd-from-PBE-3000-nvt",
]

Omat24_valid = [
"/share/public/PWMLFF_test_data/eqv2-models/datasets/decompress/Omat24/valid/rattled-1000",
"/share/public/PWMLFF_test_data/eqv2-models/datasets/decompress/Omat24/valid/rattled-1000-subsampled",
"/share/public/PWMLFF_test_data/eqv2-models/datasets/decompress/Omat24/valid/rattled-300",
"/share/public/PWMLFF_test_data/eqv2-models/datasets/decompress/Omat24/valid/rattled-300-subsampled",
"/share/public/PWMLFF_test_data/eqv2-models/datasets/decompress/Omat24/valid/rattled-500",
"/share/public/PWMLFF_test_data/eqv2-models/datasets/decompress/Omat24/valid/rattled-500-subsampled",
"/share/public/PWMLFF_test_data/eqv2-models/datasets/decompress/Omat24/valid/rattled-relax",
"/share/public/PWMLFF_test_data/eqv2-models/datasets/decompress/Omat24/valid/aimd-from-PBE-1000-npt",
"/share/public/PWMLFF_test_data/eqv2-models/datasets/decompress/Omat24/valid/aimd-from-PBE-1000-nvt",
"/share/public/PWMLFF_test_data/eqv2-models/datasets/decompress/Omat24/valid/aimd-from-PBE-3000-npt",
"/share/public/PWMLFF_test_data/eqv2-models/datasets/decompress/Omat24/valid/aimd-from-PBE-3000-nvt",
]

Alexandria_train = ["/share/public/PWMLFF_test_data/eqv2-models/datasets/decompress/Alexandria/train"]
Alexandria_valid = ["/share/public/PWMLFF_test_data/eqv2-models/datasets/decompress/Alexandria/val"]

def atoms2xyzstr(atoms):
    num_atom = atoms.get_global_number_of_atoms()
    vol = atoms.get_volume()
    virial = -atoms.get_stress() * vol
    pos = atoms.positions
    forces = atoms.get_forces()
    energy = atoms.get_potential_energy()
    cell = atoms.cell
    xyzstr = "%d\n" % num_atom
    xyzstr += 'Lattice="%.3f %.3f %.3f %.3f %.3f %.3f %.3f %.3f %.3f" Properties=species:S:1:pos:R:3:force:R:3 energy=%.8f virial="%.8f %.8f %.8f %.8f %.8f %.8f %.8f %.8f %.8f"\n' \
        %(cell[0,0],cell[0,1],cell[0,2],cell[1,0],cell[1,1],cell[1,2],cell[2,0],cell[2,1],cell[2,2],energy,\
        virial[0],virial[5],virial[4],virial[5],virial[1],virial[3],virial[4],virial[3],virial[2])
    for i in range(num_atom):
        xyzstr += "%2s %14.8f %14.8f %14.8f %14.8f %14.8f %14.8f\n" %\
        (atoms[i].symbol,pos[i,0],pos[i,1],pos[i,2],forces[i,0],forces[i,1],forces[i,2])
    return xyzstr

def db2xyzstr(db):
    num_atom = db.natoms
    vol = db.volume
    virial = -np.array(db.stress) * vol
    pos = np.array(db.positions)
    forces = np.array(db.forces)
    energy = np.array(db.energy)
    cell = np.array(db.cell)
    xyzstr = "%d\n" % num_atom
    xyzstr += 'Lattice="%.3f %.3f %.3f %.3f %.3f %.3f %.3f %.3f %.3f" Properties=species:S:1:pos:R:3:force:R:3 energy=%.8f virial="%.8f %.8f %.8f %.8f %.8f %.8f %.8f %.8f %.8f"\n' \
        %(cell[0,0],cell[0,1],cell[0,2],cell[1,0],cell[1,1],cell[1,2],cell[2,0],cell[2,1],cell[2,2],energy,\
        virial[0],virial[5],virial[4],virial[5],virial[1],virial[3],virial[4],virial[3],virial[2])
    for i in range(num_atom):
        xyzstr += "%2s %14.8f %14.8f %14.8f %14.8f %14.8f %14.8f\n" %\
        (db.symbols[i],pos[i,0],pos[i,1],pos[i,2],forces[i,0],forces[i,1],forces[i,2])
    return xyzstr

def old():
    parser = argparse.ArgumentParser()
    parser.add_argument('-s', '--elements', help='specify input elements (e.g. Li,Fe,Mn,P,O or Li Fe Mn P O)', type=str, default=None)
    args = parser.parse_args(sys.argv[1:])
    input_elements = args.elements
    if "," in input_elements:
        elements = [i for i in input_elements.split(",")]
    elif " " in input_elements:
        elements = [i for i in input_elements.split()]
    else:
        elements = [input_elements]
    filename = ""
    for i in sorted(elements):
        filename += i
    from fairchem.core.datasets import AseDBDataset
    valid_file = open("%s_valid.xyz"%filename,"w")
    for dataset_path in Alexandria_valid + Omat24_valid:
        count = 0
        dataset = AseDBDataset(config=dict(src=dataset_path))
        for i in range(dataset.num_samples):
            atoms = dataset.get_atoms(i)
            if sorted(set(atoms.get_chemical_symbols())) == sorted(elements):
                valid_file.write(atoms2xyzstr(atoms))
                count += 1
        print("In %s"%dataset_path[62:])
        print("%d images are selected from whole %d images"%(count,dataset.num_samples))
        print()
    valid_file.close()

    train_file = open("%s_train.xyz"%filename,"w")
    for dataset_path in Alexandria_train + Omat24_train:
        count = 0
        dataset = AseDBDataset(config=dict(src=dataset_path))
        for i in range(dataset.num_samples):
            atoms = dataset.get_atoms(i)
            if sorted(set(atoms.get_chemical_symbols())) == sorted(elements):
                train_file.write(atoms2xyzstr(atoms))
                count += 1
        print("In %s"%dataset_path[62:])
        print("%d images are selected from whole %d images"%(count,dataset.num_samples))
        print()
    train_file.close()

def make_query(elements):
    # 这个闭包函数将捕获 elements 参数
    print("make query ", elements)
    def query(row):
        if sorted(set(row.symbols)) == sorted(elements):
            return True
        return False
    return query

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-s', '--elements', help='specify input elements (e.g. Li,Fe,Mn,P,O or Li Fe Mn P O)', type=str, default=None)
    args = parser.parse_args(sys.argv[1:])
    input_elements = args.elements
    if "," in input_elements:
        elements = [i for i in input_elements.split(",")]
    elif " " in input_elements:
        elements = [i for i in input_elements.split()]
    else:
        elements = [input_elements]

    filename = ""
    for i in sorted(elements):
        filename += i
    
    valid_file = open("%s_valid.xyz"%filename,"w")
    for dataset_path in Alexandria_valid + Omat24_valid:
        count = 0
        dataset = AseDBDataset(config=dict(src=dataset_path))
        for dbs in dataset.dbs:
            atom_list = list(dbs.select(filename,filter=make_query(elements)))
            count += len(atom_list)
            for tmp in atom_list:
                valid_file.write(db2xyzstr(tmp))
        print("In %s"%dataset_path[62:])
        print("%d images are selected from whole %d images"%(count,dataset.num_samples))
        print()
    valid_file.close()

    train_file = open("%s_train.xyz"%filename,"w")
    for dataset_path in Alexandria_train + Omat24_train:
        count = 0
        dataset = AseDBDataset(config=dict(src=dataset_path))
        for dbs in dataset.dbs:
            atom_list = list(dbs.select(filename,filter=make_query(elements)))
            count += len(atom_list)
            for tmp in atom_list:
                train_file.write(db2xyzstr(tmp))
        print("In %s"%dataset_path[62:])
        print("%d images are selected from whole %d images"%(count,dataset.num_samples))
        print()
    train_file.close()

if __name__ == "__main__":
    main()
