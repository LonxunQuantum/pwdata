from pwdata import Config
import json
import os
os.chdir("/data/home/wuxingxing/codespace/pwdata/examples")

def test_convert_config():
    configs = json.load(open("./config.json"))["convert_image"]
    save_dir = "./test_workdir"
    for config in configs:
        config_file = config["input_file"]
        config_format= config["input_format"]
        if "atom_types" in config.keys():
            atom_types = config["atom_types"]
        else:
            atom_types = None
        for idx, save_format in enumerate(["pwmat/config","vasp/poscar","lammps/lmp"]):
            save_name = "{}-{}-to-{}".format(idx, config_format.replace('/', '-'), save_format.replace('/','-'))
            config = Config(format=config_format, data_path=config_file, atom_names=atom_types)
            config.to(output_path=save_dir, data_name=save_name, save_format = save_format, direct = False, sort = True)
            print("load {} succeess, convert to {} done".format(config_file, save_name))

def test_convert_configs():
    configs = json.load(open("./config.json"))["call_convert_configs"]
    save_dir = "./test_workdir"
    for idi, config in enumerate(configs):
        config_file = config["input_file"]
        config_format= config["input_format"]
        if "atom_types" in config.keys():
            atom_types = config["atom_types"]
        else:
            atom_types = None
        # res = search_images(config_file, config_format)
        # print(res)
        for idj, save_format in enumerate(['pwmlff/npy', 'extxyz']):
            save_path =  os.path.join(save_dir, "{}_{}_{}_{}".format(idi, idj, config_format.replace('/','_'), save_format.replace('/','_')))
            config = Config(format=config_format, data_path=config_file, atom_names=atom_types)
            config.to(
                output_path=save_path,
                save_format=save_format,
                train_ratio = 0.8, 
                random=False,
                seed = 2024, 
                retain_raw = False,
                write_patthen="a"
                )
            print("load {} done!".format(config_file))
            if config_format == "lammps/dump":
                print("save {} done!\n\n".format(save_path))
                continue
            data_files = search_images([save_path], save_format)
            image_data = load_files(data_files, save_format, atom_types=atom_types)
            assert(len(image_data.images)) == len(config.images)
            print("save {} done!\n\n".format(save_path))

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


class FORMAT:
    pwmat_config="pwmat/config"
    pwmat_config_name="atom.config"
    pwmat_movement="pwmat/movement"
    pwmat_movement_name="MOVEMENT"
    vasp_poscar="vasp/poscar"
    vasp_poscar_name="POSCAR"
    vasp_outcar="vasp/outcar"
    vasp_outcar_name="OUTCAR"
    vasp_potcar="vasp/potcar"
    vasp_potcar_name="POTCAR"
    lammps_lmp="lammps/lmp"
    lammps_lmp_name="lammps.lmp"
    lammps_dump="lammps/dump"
    cp2k_md="cp2k/md"
    cp2k_scf="cp2k/scf"
    pwmlff_npy="pwmlff/npy"
    pwmlff_npy_name="PWdata"
    deepmd_npy="deepmd/npy"
    deepmd_raw="deepmd/raw"
    extxyz="extxyz"
    extxyz_name="extxyz.xyz"
    meta = "meta"
    
    support_config_format = [pwmat_config, vasp_poscar, lammps_lmp, cp2k_scf]
    support_images_format = [pwmat_movement, vasp_outcar, lammps_dump, cp2k_md, pwmlff_npy, deepmd_npy, deepmd_raw, extxyz, meta]

    @staticmethod
    def get_filename_by_format(input_format:str):
        input_format = input_format.lower()
        if input_format == FORMAT.pwmat_config:
            return FORMAT.pwmat_config_name
        elif input_format==FORMAT.pwmat_movement:
            return FORMAT.pwmat_movement_name
        elif input_format == FORMAT.vasp_poscar:
            return FORMAT.vasp_poscar_name
        elif input_format == FORMAT.vasp_outcar:
            return FORMAT.vasp_outcar_name
        elif input_format == FORMAT.vasp_potcar:
            return FORMAT.vasp_potcar_name
        elif input_format == FORMAT.lammps_lmp:
            return FORMAT.lammps_lmp_name
        elif input_format == FORMAT.pwmlff_npy:
            return FORMAT.pwmlff_npy_name
        elif input_format == FORMAT.extxyz:
            return FORMAT.extxyz_name
        else:
            raise ValueError("Unknown format: {}".format(input_format))

    @staticmethod
    def check_format(input_format:str, support_format:list[str]=None):
        input_format = input_format.lower()
        if support_format is None:
            if input_format in [FORMAT.pwmat_config, FORMAT.pwmat_movement, FORMAT.vasp_poscar, FORMAT.vasp_outcar, FORMAT.vasp_potcar, FORMAT.lammps_lmp, FORMAT.pwmlff_npy, FORMAT.extxyz]:
                return True
            else:
                raise Exception("the input format is not supported, please check the input format {}, the supported format as:\n{}".format(input_format, [FORMAT.pwmat_config, FORMAT.pwmat_movement, FORMAT.vasp_poscar, FORMAT.vasp_outcar, FORMAT.vasp_potcar, FORMAT.lammps_lmp, FORMAT.pwmlff_npy, FORMAT.extxyz]))
        else:
            if input_format in support_format:
                return True
            else:
                raise Exception("the input format is not supported, please check the input format {}, the supported format as:\n{}".format(input_format, support_format))

if __name__=="__main__":
    # test_convert_config()
    test_convert_configs()