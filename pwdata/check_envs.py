def print_cmd():
    cmd_infos()

def cmd_infos():
    info = ""
    info += "In functional development, please refer to the link\n\t\thttp://doc.lonxun.com/PWMLFF/Appendix-2/\n"
    
    info += "scale_cell:\n"
    info += "\tScaling the structural lattice, the command example is shown below, :\n"
    info += "\tpwdata scale_cell -i input_file -f input_file_format -n output_format_name -o output_format\n\n"

    info += "super_cell:\n"
    info += "\tThe command used to scale the cell, the command example:\n"
    info += "\tpwdata super_cell -i input_file -f input_file_format -n output_format_name -o output_format\n"
    info += "\tFor detailed parameter explanations, please use the command 'pwdata super_cell -h'\n\n"
    
    info += "pertub:\n"
    info += "\tThe command used to scale the cell, the command example:\n"
    info += "\tpwdata pertub -i input_file -f input_file_format -n output_format_name -o output_format\n\n"

    info += "convert_config:\n"
    info += "\tThe command used to scale the cell, the command example:\n"
    info += "\tpwdata convert_config -i input_file -f input_file_format -n output_format_name -o output_format\n\n"

    info += "convert_images:\n"
    info += "\tThe command used to scale the cell, the command example:\n"
    info += "\tpwdata convert_images -i input_file1 input_file2 ... input_filen -f input_file_format -n output_format_name -o output_format\n\n"

    info += "format suppport\n"
    info += "__________________________________________________________________________________________|\n"
    info += "| Software          | file             | multi-Image | label | format                     |\n"
    info += "| ----------------- | ---------------- | ----------- | ----- | -------------------------- |\n"
    info += "| PWmat             | MOVEMENT         | True        | True  | 'pwmat/movement'           |\n"
    info += "| PWmat             | OUT.MLMD         | False       | True  | 'pwmat/movement'           |\n"
    info += "| PWmat             | atom.config      | False       | False | 'pwmat/config'             |\n"
    info += "| VASP              | OUTCAR           | True        | True  | 'vasp/outcar'              |\n"
    info += "| VASP              | poscar           | False       | False | 'vasp/poscar'              |\n"
    info += "| LAMMPS            | lmp.init         | False       | False | 'lammps/lmp'               |\n"
    info += "| LAMMPS            | dump             | True        | False | 'lammps/dump'              |\n"
    info += "| CP2K              | stdout, xyz, pdb | True        | True  | 'cp2k/md'                  |\n"
    info += "| CP2K              | stdout           | False       | True  | 'cp2k/scf'                 |\n"
    info += "| PWMLFF            | \*.npy           | True        | True  | 'pwmlff/npy'               |\n"
    info += "| DeepMD (read)     | \*.npy, \*.raw   | True        | True  | 'deepmd/npy', 'deepmd/raw' |\n"
    info += "| \* (extended xyz) | \*.xyz           | True        | True  | 'extxyz'                   |\n"
    info += "__________________________________________________________________________________________|\n\n"
    print(info)