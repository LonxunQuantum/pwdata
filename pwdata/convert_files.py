import os
import sys
def read_from_dirs(dirs:list[str], format:str):
    # for pwamt/movement movement or MLMD.OUT files
    
    # for outcars 

    # for pwmlff/npy search dirs 

    # for deepmd/npy search dirs

    return None

"""
convert the input dirs or files to target format files
"""
def convert_files_to(in_dirs:list[str], save_dir:str, in_format:str, out_format:str):
    iamges = read_from_dirs(in_dirs)
    iamges.to(save_dir, out_format)
    return None