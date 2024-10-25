#!/bin/bash
cd ../examples
# test convert_config
pwdata convert_config -i ./pwmat_data/lisi_atom.config -f pwmat/config -s ./test_workdir/atom.config -o pwmat/config -d
pwdata convert_config -i ./pwmat_data/lisi_atom.config -f pwmat/config -s ./test_workdir/POSCAR -o vasp/poscar -d
pwdata convert_config -i ./pwmat_data/lisi_atom.config -f pwmat/config -s ./test_workdir/lammps.lmp -o lammps/lmp -d
pwdata convert_config -i ./pwmat_data/LiGePS_atom.config -f pwmat/config -s ./test_workdir/atom.config -o pwmat/config -d
pwdata convert_config -i ./pwmat_data/LiGePS_atom.config -f pwmat/config -s ./test_workdir/POSCAR -o vasp/poscar -d
pwdata convert_config -i ./pwmat_data/LiGePS_atom.config -f pwmat/config -s ./test_workdir/lammps.lmp -o lammps/lmp -d
pwdata convert_config -i ./lmps_data/HfO2/96.lmp -f lammps/lmp -s ./test_workdir/atom.config -o pwmat/config -d -t Hf O
pwdata convert_config -i ./lmps_data/HfO2/96.lmp -f lammps/lmp -s ./test_workdir/POSCAR -o vasp/poscar -d -t Hf O
pwdata convert_config -i ./lmps_data/HfO2/96.lmp -f lammps/lmp -s ./test_workdir/lammps.lmp -o lammps/lmp -d -t Hf O
pwdata convert_config -i ./vasp_data/Si_POSCAR -f vasp/poscar -s ./test_workdir/atom.config -o pwmat/config -d
pwdata convert_config -i ./vasp_data/Si_POSCAR -f vasp/poscar -s ./test_workdir/POSCAR -o vasp/poscar -d
pwdata convert_config -i ./vasp_data/Si_POSCAR -f vasp/poscar -s ./test_workdir/lammps.lmp -o lammps/lmp -d
pwdata convert_config -i ./vasp_data/LiSi_POSCAR -f vasp/poscar -s ./test_workdir/atom.config -o pwmat/config -d
pwdata convert_config -i ./vasp_data/LiSi_POSCAR -f vasp/poscar -s ./test_workdir/POSCAR -o vasp/poscar -d
pwdata convert_config -i ./vasp_data/LiSi_POSCAR -f vasp/poscar -s ./test_workdir/lammps.lmp -o lammps/lmp -d

# test scale_cell
pwdata scale_cell -r 0.98 -i ./pwmat_data/lisi_atom.config -f pwmat/config -s ./test_workdir/scale_cell_atom.config -o pwmat/config -d
pwdata scale_cell -r 0.98 -i ./pwmat_data/lisi_atom.config -f pwmat/config -s ./test_workdir/scale_cell_POSCAR -o vasp/poscar -d
pwdata scale_cell -r 0.98 -i ./pwmat_data/lisi_atom.config -f pwmat/config -s ./test_workdir/scale_cell_lammps.lmp -o lammps/lmp -d
pwdata scale_cell -r 0.98 -i ./pwmat_data/LiGePS_atom.config -f pwmat/config -s ./test_workdir/scale_cell_atom.config -o pwmat/config -d
pwdata scale_cell -r 0.98 -i ./pwmat_data/LiGePS_atom.config -f pwmat/config -s ./test_workdir/scale_cell_POSCAR -o vasp/poscar -d
pwdata scale_cell -r 0.98 -i ./pwmat_data/LiGePS_atom.config -f pwmat/config -s ./test_workdir/scale_cell_lammps.lmp -o lammps/lmp -d
pwdata scale_cell -r 0.98 -i ./lmps_data/HfO2/96.lmp -f lammps/lmp -s ./test_workdir/scale_cell_atom.config -o pwmat/config -d -t Hf O
pwdata scale_cell -r 0.98 -i ./lmps_data/HfO2/96.lmp -f lammps/lmp -s ./test_workdir/scale_cell_POSCAR -o vasp/poscar -d -t Hf O
pwdata scale_cell -r 0.98 -i ./lmps_data/HfO2/96.lmp -f lammps/lmp -s ./test_workdir/scale_cell_lammps.lmp -o lammps/lmp -d -t Hf O
pwdata scale_cell -r 0.98 -i ./vasp_data/Si_POSCAR -f vasp/poscar -s ./test_workdir/scale_cell_atom.config -o pwmat/config -d
pwdata scale_cell -r 0.98 -i ./vasp_data/Si_POSCAR -f vasp/poscar -s ./test_workdir/scale_cell_POSCAR -o vasp/poscar -d
pwdata scale_cell -r 0.98 -i ./vasp_data/Si_POSCAR -f vasp/poscar -s ./test_workdir/scale_cell_lammps.lmp -o lammps/lmp -d
pwdata scale_cell -r 0.98 -i ./vasp_data/LiSi_POSCAR -f vasp/poscar -s ./test_workdir/scale_cell_atom.config -o pwmat/config -d
pwdata scale_cell -r 0.98 -i ./vasp_data/LiSi_POSCAR -f vasp/poscar -s ./test_workdir/scale_cell_POSCAR -o vasp/poscar -d
pwdata scale_cell -r 0.98 -i ./vasp_data/LiSi_POSCAR -f vasp/poscar -s ./test_workdir/scale_cell_lammps.lmp -o lammps/lmp -d

# test super_cell
pwdata super_cell -m 2 3 4 -i ./pwmat_data/lisi_atom.config -f pwmat/config -s ./test_workdir/super_atom.config -o pwmat/config -d
pwdata super_cell -m 2 3 4 -i ./pwmat_data/lisi_atom.config -f pwmat/config -s ./test_workdir/super_POSCAR -o vasp/poscar -d
pwdata super_cell -m 2 3 4 -i ./pwmat_data/lisi_atom.config -f pwmat/config -s ./test_workdir/super_lammps.lmp -o lammps/lmp -d
pwdata super_cell -m 2 3 4 -i ./pwmat_data/LiGePS_atom.config -f pwmat/config -s ./test_workdir/super_atom.config -o pwmat/config -d
pwdata super_cell -m 2 3 4 -i ./pwmat_data/LiGePS_atom.config -f pwmat/config -s ./test_workdir/super_POSCAR -o vasp/poscar -d
pwdata super_cell -m 2 3 4 -i ./pwmat_data/LiGePS_atom.config -f pwmat/config -s ./test_workdir/super_lammps.lmp -o lammps/lmp -d
pwdata super_cell -m 2 3 4 -i ./lmps_data/HfO2/96.lmp -f lammps/lmp -s ./test_workdir/super_atom.config -o pwmat/config -d -t Hf O
pwdata super_cell -m 2 3 4 -i ./lmps_data/HfO2/96.lmp -f lammps/lmp -s ./test_workdir/super_POSCAR -o vasp/poscar -d -t Hf O
pwdata super_cell -m 2 3 4 -i ./lmps_data/HfO2/96.lmp -f lammps/lmp -s ./test_workdir/super_lammps.lmp -o lammps/lmp -d -t Hf O
pwdata super_cell -m 2 3 4 -i ./vasp_data/Si_POSCAR -f vasp/poscar -s ./test_workdir/super_atom.config -o pwmat/config -d
pwdata super_cell -m 2 3 4 -i ./vasp_data/Si_POSCAR -f vasp/poscar -s ./test_workdir/super_POSCAR -o vasp/poscar -d
pwdata super_cell -m 2 3 4 -i ./vasp_data/Si_POSCAR -f vasp/poscar -s ./test_workdir/super_lammps.lmp -o lammps/lmp -d
pwdata super_cell -m 2 3 4 -i ./vasp_data/LiSi_POSCAR -f vasp/poscar -s ./test_workdir/super_atom.config -o pwmat/config -d
pwdata super_cell -m 2 3 4 -i ./vasp_data/LiSi_POSCAR -f vasp/poscar -s ./test_workdir/super_POSCAR -o vasp/poscar -d
pwdata super_cell -m 2 3 4 -i ./vasp_data/LiSi_POSCAR -f vasp/poscar -s ./test_workdir/super_lammps.lmp -o lammps/lmp -d

#test pertub
pwdata pertub -c 0.01 -a 0.04 -n 20 -i ./pwmat_data/lisi_atom.config -f pwmat/config -s ./test_workdir/pertub_atom -o pwmat/config -d
pwdata pertub -c 0.01 -a 0.04 -n 20 -i ./pwmat_data/lisi_atom.config -f pwmat/config -s ./test_workdir/pertub_POSCAR -o vasp/poscar -d
pwdata pertub -c 0.01 -a 0.04 -n 20 -i ./pwmat_data/lisi_atom.config -f pwmat/config -s ./test_workdir/pertub_lammps -o lammps/lmp -d
pwdata pertub -c 0.01 -a 0.04 -n 20 -i ./pwmat_data/LiGePS_atom.config -f pwmat/config -s ./test_workdir/pertub_atom -o pwmat/config -d
pwdata pertub -c 0.01 -a 0.04 -n 20 -i ./pwmat_data/LiGePS_atom.config -f pwmat/config -s ./test_workdir/pertub_POSCAR -o vasp/poscar -d
pwdata pertub -c 0.01 -a 0.04 -n 20 -i ./pwmat_data/LiGePS_atom.config -f pwmat/config -s ./test_workdir/pertub_lammps -o lammps/lmp -d
pwdata pertub -c 0.01 -a 0.04 -n 20 -i ./lmps_data/HfO2/96.lmp -f lammps/lmp -s ./test_workdir/pertub_atom -o pwmat/config -d -t Hf O
pwdata pertub -c 0.01 -a 0.04 -n 20 -i ./lmps_data/HfO2/96.lmp -f lammps/lmp -s ./test_workdir/pertub_POSCAR -o vasp/poscar -d -t Hf O
pwdata pertub -c 0.01 -a 0.04 -n 20 -i ./lmps_data/HfO2/96.lmp -f lammps/lmp -s ./test_workdir/pertub_lammps -o lammps/lmp -d -t Hf O
pwdata pertub -c 0.01 -a 0.04 -n 20 -i ./vasp_data/Si_POSCAR -f vasp/poscar -s ./test_workdir/pertub_atom -o pwmat/config -d
pwdata pertub -c 0.01 -a 0.04 -n 20 -i ./vasp_data/Si_POSCAR -f vasp/poscar -s ./test_workdir/pertub_POSCAR -o vasp/poscar -d
pwdata pertub -c 0.01 -a 0.04 -n 20 -i ./vasp_data/Si_POSCAR -f vasp/poscar -s ./test_workdir/pertub_lammps -o lammps/lmp -d
pwdata pertub -c 0.01 -a 0.04 -n 20 -i ./vasp_data/LiSi_POSCAR -f vasp/poscar -s ./test_workdir/pertub_atom -o pwmat/config -d
pwdata pertub -c 0.01 -a 0.04 -n 20 -i ./vasp_data/LiSi_POSCAR -f vasp/poscar -s ./test_workdir/pertub_POSCAR -o vasp/poscar -d
pwdata pertub -c 0.01 -a 0.04 -n 20 -i ./vasp_data/LiSi_POSCAR -f vasp/poscar -s ./test_workdir/pertub_lammps -o lammps/lmp -d

# test convert_images
pwdata convert_images -i ./pwmlff_data/LiSiC -f pwmlff/npy -s ./test_workdir/0_0_images_PWdata -o pwmlff/npy -r 0.8 -u -g 1
pwdata convert_images -i ./pwmlff_data/LiSiC -f pwmlff/npy -s ./test_workdir/0_1_images_extxyz -o extxyz -r 0.8 -u -g 1
pwdata convert_images -i ./pwmlff_data/LiSiC/Si217 ./pwmlff_data/LiSiC/C2 ./pwmlff_data/LiSiC/Si1 ./pwmlff_data/LiSiC/C64Si32 ./pwmlff_data/LiSiC/Li1Si24 ./pwmlff_data/LiSiC/C64Si32 -f pwmlff/npy -s ./test_workdir/1_0_images_PWdata -o pwmlff/npy -r 0.8 -u -g 1
pwdata convert_images -i ./pwmlff_data/LiSiC/Si217 ./pwmlff_data/LiSiC/C2 ./pwmlff_data/LiSiC/Si1 ./pwmlff_data/LiSiC/C64Si32 ./pwmlff_data/LiSiC/Li1Si24 ./pwmlff_data/LiSiC/C64Si32 -f pwmlff/npy -s ./test_workdir/1_1_images_extxyz -o extxyz -r 0.8 -u -g 1
pwdata convert_images -i ./pwmat_data/50_LiGePS_movement -f pwmat/movement -s ./test_workdir/2_0_images_PWdata -o pwmlff/npy -r 0.8 -u -g 1
pwdata convert_images -i ./pwmat_data/50_LiGePS_movement -f pwmat/movement -s ./test_workdir/2_1_images_extxyz -o extxyz -r 0.8 -u -g 1
pwdata convert_images -i ./pwmat_data/50_LiGePS_movement ./pwmat_data/lisi_50_movement -f pwmat/movement -s ./test_workdir/3_0_images_PWdata -o pwmlff/npy -r 0.8 -u -g 1
pwdata convert_images -i ./pwmat_data/50_LiGePS_movement ./pwmat_data/lisi_50_movement -f pwmat/movement -s ./test_workdir/3_1_images_extxyz -o extxyz -r 0.8 -u -g 1
pwdata convert_images -i ./vasp_data/Si_OUTCAR -f vasp/outcar -s ./test_workdir/4_0_images_PWdata -o pwmlff/npy -r 0.8 -u -g 1
pwdata convert_images -i ./vasp_data/Si_OUTCAR -f vasp/outcar -s ./test_workdir/4_1_images_extxyz -o extxyz -r 0.8 -u -g 1
pwdata convert_images -i ./xyz_data/PbPt.xyz ./xyz_data/gap_c.xyz ./xyz_data/metal_1.xyz -f extxyz -s ./test_workdir/5_0_images_PWdata -o pwmlff/npy -r 0.8 -u -g 1
pwdata convert_images -i ./xyz_data/PbPt.xyz ./xyz_data/gap_c.xyz ./xyz_data/metal_1.xyz -f extxyz -s ./test_workdir/5_1_images_extxyz -o extxyz -r 0.8 -u -g 1
pwdata convert_images -i ./deepmd_data/alloy/IrNi_POSCAR/deepmd -f deepmd/npy -s ./test_workdir/6_0_images_PWdata -o pwmlff/npy -r 0.8 -u -g 1
pwdata convert_images -i ./deepmd_data/alloy/IrNi_POSCAR/deepmd -f deepmd/npy -s ./test_workdir/6_1_images_extxyz -o extxyz -r 0.8 -u -g 1
pwdata convert_images -i ./deepmd_data/alloy/IrNi_POSCAR/deepmd ./deepmd_data/alloy/IrPdNi_POSCAR/deepmd ./deepmd_data/alloy/RhIrPdNi_POSCAR/deepmd -f deepmd/npy -s ./test_workdir/7_0_images_PWdata -o pwmlff/npy -r 0.8 -u -g 1
pwdata convert_images -i ./deepmd_data/alloy/IrNi_POSCAR/deepmd ./deepmd_data/alloy/IrPdNi_POSCAR/deepmd ./deepmd_data/alloy/RhIrPdNi_POSCAR/deepmd -f deepmd/npy -s ./test_workdir/7_1_images_extxyz -o extxyz -r 0.8 -u -g 1
pwdata convert_images -i ./cp2k_data/dft.log -f cp2k/md -s ./test_workdir/8_0_images_PWdata -o pwmlff/npy -r 0.8 -u -g 1
pwdata convert_images -i ./cp2k_data/dft.log -f cp2k/md -s ./test_workdir/8_1_images_extxyz -o extxyz -r 0.8 -u -g 1
pwdata convert_images -i ./lmps_data/HfO2/0.lammpstrj ./lmps_data/HfO2/10.lammpstrj ./lmps_data/HfO2/20.lammpstrj ./lmps_data/HfO2/30.lammpstrj -f lammps/dump -s ./test_workdir/9_0_images_PWdata -o pwmlff/npy -r 0.8 -u -g 1 -t Hf O
pwdata convert_images -i ./lmps_data/HfO2/0.lammpstrj ./lmps_data/HfO2/10.lammpstrj ./lmps_data/HfO2/20.lammpstrj ./lmps_data/HfO2/30.lammpstrj -f lammps/dump -s ./test_workdir/9_1_images_extxyz -o extxyz -r 0.8 -u -g 1 -t Hf O