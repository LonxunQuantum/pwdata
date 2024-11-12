'''
description: 
Convert various trajectory files ('pwmat/movement','vasp/outcar','cp2k/md', or 'lammps/dump')
    to a single structure format ('pwmat/config', 'vasp/poscar', 'lammps/lmp')
'''

from pwdata import Config
from pwdata.utils.constant import FORMAT

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

if __name__=="__main__":
    trajs2config()

	
