import os
import sys
from pwdata import Config
import argparse

def read_from_dirs(dirs:list[str], format:str):
    # for pwamt/movement movement or MLMD.OUT files
    
    # for outcars 

    # for pwmlff/npy search dirs 

    # for deepmd/npy search dirs

    return None

"""
convert the input dirs or files to target format files
"""
def convert_images_to(cmd_list:list[str]):
    # in_dirs:list[str], save_dir:str, in_format:str, out_format:str
    parser = argparse.ArgumentParser(description='These formats of files are converted to each other:\n pwmat/movement, vasp/outcar, cp2k/md, deepmd/npy, deepmd/raw, pwmlff/npy or extxyz files')
    parser.add_argument('--format', type=str, required=False, help='Format of the input files or dirs', default="outcar")
    parser.add_argument('--save_format', type=str, required=False, help='Format of the output file', default="config")
    parser.add_argument('--outcar_file', type=str, required=False, help='Path to the OUTCAR file')
    parser.add_argument('--movement_file', type=str, required=False, help='Path to the MOVEMENT file')
    parser.add_argument('--output_path', type=str, required=False, help='Path to the output directory', default="./")
    parser.add_argument('--output_file', type=str, required=False, help='Name of the output file', default="MOVEMENT")
    # iamges = read_from_dirs(in_dirs)
    # iamges.to(save_dir, out_format)
    return None

def convert_config_to(cmd_list:list[str]):
    pass
if __name__=="__main__":
    cmd_type = sys.argv[2]
    if cmd_type.lower() == "convert_images":
        convert_images_to(sys.argv[3:])
    if cmd_type.lower() == "convert_config":
        convert_config_to(sys.argv[3:])