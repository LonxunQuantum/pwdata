#!/bin/bash
cd ../../examples
# test convert_config
pwdata cvt_config -i ./pwmat_data/lisi_atom.config -f pwmat/config -s ./test_workdir/cvtcnf_atom.config -o pwmat/config -c
pwdata cvt_config -i ./pwmat_data/lisi_atom.config -f pwmat/config -s ./test_workdir/cvtcnf_POSCAR -o vasp/poscar -c
pwdata cvt_config -i ./pwmat_data/lisi_atom.config -f pwmat/config -s ./test_workdir/cvtcnf_lammps.lmp -o lammps/lmp -c
pwdata cvt_config -i ./pwmat_data/LiGePS_atom.config -f pwmat/config -s ./test_workdir/cvtcnf_atom.config -o pwmat/config -c
pwdata cvt_config -i ./pwmat_data/LiGePS_atom.config -f pwmat/config -s ./test_workdir/cvtcnf_POSCAR -o vasp/poscar -c
pwdata cvt_config -i ./pwmat_data/LiGePS_atom.config -f pwmat/config -s ./test_workdir/cvtcnf_lammps.lmp -o lammps/lmp -c
pwdata cvt_config -i ./lmps_data/HfO2/96.lmp -f lammps/lmp -s ./test_workdir/cvtcnf_atom.config -o pwmat/config -c -t Hf O
pwdata cvt_config -i ./lmps_data/HfO2/96.lmp -f lammps/lmp -s ./test_workdir/cvtcnf_POSCAR -o vasp/poscar -c -t Hf O
pwdata cvt_config -i ./lmps_data/HfO2/96.lmp -f lammps/lmp -s ./test_workdir/cvtcnf_lammps.lmp -o lammps/lmp -c -t Hf O
pwdata cvt_config -i ./vasp_data/Si_POSCAR -f vasp/poscar -s ./test_workdir/cvtcnf_atom.config -o pwmat/config -c
pwdata cvt_config -i ./vasp_data/Si_POSCAR -f vasp/poscar -s ./test_workdir/cvtcnf_POSCAR -o vasp/poscar -c
pwdata cvt_config -i ./vasp_data/Si_POSCAR -f vasp/poscar -s ./test_workdir/cvtcnf_lammps.lmp -o lammps/lmp -c
pwdata cvt_config -i ./vasp_data/LiSi_POSCAR -f vasp/poscar -s ./test_workdir/cvtcnf_atom.config -o pwmat/config -c
pwdata cvt_config -i ./vasp_data/LiSi_POSCAR -f vasp/poscar -s ./test_workdir/cvtcnf_POSCAR -o vasp/poscar -c
pwdata cvt_config -i ./vasp_data/LiSi_POSCAR -f vasp/poscar -s ./test_workdir/cvtcnf_lammps.lmp -o lammps/lmp -c

# test scale_cell
pwdata scale_cell -r 0.98 0.99 0.97 0.95 -i ./pwmat_data/lisi_atom.config -f pwmat/config -s ./test_workdir/scale_atom.config -o pwmat/config -c
pwdata scale_cell -r 0.98 0.99 0.97 0.95 -i ./pwmat_data/lisi_atom.config -f pwmat/config -s ./test_workdir/scale_POSCAR -o vasp/poscar -c
pwdata scale_cell -r 0.98 0.99 0.97 0.95 -i ./pwmat_data/lisi_atom.config -f pwmat/config -s ./test_workdir/scale_lammps.lmp -o lammps/lmp -c
pwdata scale_cell -r 0.98 0.99 0.97 0.95 -i ./pwmat_data/LiGePS_atom.config -f pwmat/config -s ./test_workdir/scale_atom.config -o pwmat/config -c
pwdata scale_cell -r 0.98 0.99 0.97 0.95 -i ./pwmat_data/LiGePS_atom.config -f pwmat/config -s ./test_workdir/scale_POSCAR -o vasp/poscar -c
pwdata scale_cell -r 0.98 0.99 0.97 0.95 -i ./pwmat_data/LiGePS_atom.config -f pwmat/config -s ./test_workdir/scale_lammps.lmp -o lammps/lmp -c
pwdata scale_cell -r 0.98 0.99 0.97 0.95 -i ./lmps_data/HfO2/96.lmp -f lammps/lmp -s ./test_workdir/scale_atom.config -o pwmat/config -c -t Hf O
pwdata scale_cell -r 0.98 0.99 0.97 0.95 -i ./lmps_data/HfO2/96.lmp -f lammps/lmp -s ./test_workdir/scale_POSCAR -o vasp/poscar -c -t Hf O
pwdata scale_cell -r 0.98 0.99 0.97 0.95 -i ./lmps_data/HfO2/96.lmp -f lammps/lmp -s ./test_workdir/scale_lammps.lmp -o lammps/lmp -c -t Hf O
pwdata scale_cell -r 0.98 0.99 0.97 0.95 -i ./vasp_data/Si_POSCAR -f vasp/poscar -s ./test_workdir/scale_atom.config -o pwmat/config -c
pwdata scale_cell -r 0.98 0.99 0.97 0.95 -i ./vasp_data/Si_POSCAR -f vasp/poscar -s ./test_workdir/scale_POSCAR -o vasp/poscar -c
pwdata scale_cell -r 0.98 0.99 0.97 0.95 -i ./vasp_data/Si_POSCAR -f vasp/poscar -s ./test_workdir/scale_lammps.lmp -o lammps/lmp -c
pwdata scale_cell -r 0.98 0.99 0.97 0.95 -i ./vasp_data/LiSi_POSCAR -f vasp/poscar -s ./test_workdir/scale_atom.config -o pwmat/config -c
pwdata scale_cell -r 0.98 0.99 0.97 0.95 -i ./vasp_data/LiSi_POSCAR -f vasp/poscar -s ./test_workdir/scale_POSCAR -o vasp/poscar -c
pwdata scale_cell -r 0.98 0.99 0.97 0.95 -i ./vasp_data/LiSi_POSCAR -f vasp/poscar -s ./test_workdir/scale_lammps.lmp -o lammps/lmp -c

# test super_cell
pwdata super_cell -m 2 3 4 -i ./pwmat_data/lisi_atom.config -f pwmat/config -s ./test_workdir/super_atom.config -o pwmat/config 
pwdata super_cell -m 2 3 4 -i ./pwmat_data/lisi_atom.config -f pwmat/config -s ./test_workdir/super_POSCAR -o vasp/poscar 
pwdata super_cell -m 2 3 4 -i ./pwmat_data/lisi_atom.config -f pwmat/config -s ./test_workdir/super_lammps.lmp -o lammps/lmp 
pwdata super_cell -m 2 3 4 -i ./pwmat_data/LiGePS_atom.config -f pwmat/config -s ./test_workdir/super_atom.config -o pwmat/config 
pwdata super_cell -m 2 3 4 -i ./pwmat_data/LiGePS_atom.config -f pwmat/config -s ./test_workdir/super_POSCAR -o vasp/poscar 
pwdata super_cell -m 2 3 4 -i ./pwmat_data/LiGePS_atom.config -f pwmat/config -s ./test_workdir/super_lammps.lmp -o lammps/lmp 
pwdata super_cell -m 2 3 4 -i ./lmps_data/HfO2/96.lmp -f lammps/lmp -s ./test_workdir/super_atom.config -o pwmat/config  -t Hf O
pwdata super_cell -m 2 3 4 -i ./lmps_data/HfO2/96.lmp -f lammps/lmp -s ./test_workdir/super_POSCAR -o vasp/poscar  -t Hf O
pwdata super_cell -m 2 3 4 -i ./lmps_data/HfO2/96.lmp -f lammps/lmp -s ./test_workdir/super_lammps.lmp -o lammps/lmp  -t Hf O
pwdata super_cell -m 2 3 4 -i ./vasp_data/Si_POSCAR -f vasp/poscar -s ./test_workdir/super_atom.config -o pwmat/config 
pwdata super_cell -m 2 3 4 -i ./vasp_data/Si_POSCAR -f vasp/poscar -s ./test_workdir/super_POSCAR -o vasp/poscar 
pwdata super_cell -m 2 3 4 -i ./vasp_data/Si_POSCAR -f vasp/poscar -s ./test_workdir/super_lammps.lmp -o lammps/lmp 
pwdata super_cell -m 2 3 4 -i ./vasp_data/LiSi_POSCAR -f vasp/poscar -s ./test_workdir/super_atom.config -o pwmat/config 
pwdata super_cell -m 2 3 4 -i ./vasp_data/LiSi_POSCAR -f vasp/poscar -s ./test_workdir/super_POSCAR -o vasp/poscar 
pwdata super_cell -m 2 3 4 -i ./vasp_data/LiSi_POSCAR -f vasp/poscar -s ./test_workdir/super_lammps.lmp -o lammps/lmp 

#test pertub
pwdata perturb -e 0.01 -d 0.04 -n 20 -i ./pwmat_data/lisi_atom.config -f pwmat/config -s ./test_workdir/perturb_atom -o pwmat/config -c
pwdata perturb -e 0.01 -d 0.04 -n 20 -i ./pwmat_data/lisi_atom.config -f pwmat/config -s ./test_workdir/perturb_POSCAR -o vasp/poscar -c
pwdata perturb -e 0.01 -d 0.04 -n 20 -i ./pwmat_data/lisi_atom.config -f pwmat/config -s ./test_workdir/perturb_lammps -o lammps/lmp -c
pwdata perturb -e 0.01 -d 0.04 -n 20 -i ./pwmat_data/LiGePS_atom.config -f pwmat/config -s ./test_workdir/perturb_atom -o pwmat/config -c
pwdata perturb -e 0.01 -d 0.04 -n 20 -i ./pwmat_data/LiGePS_atom.config -f pwmat/config -s ./test_workdir/perturb_POSCAR -o vasp/poscar -c
pwdata perturb -e 0.01 -d 0.04 -n 20 -i ./pwmat_data/LiGePS_atom.config -f pwmat/config -s ./test_workdir/perturb_lammps -o lammps/lmp -c
pwdata perturb -e 0.01 -d 0.04 -n 20 -i ./lmps_data/HfO2/96.lmp -f lammps/lmp -s ./test_workdir/perturb_atom -o pwmat/config -c -t Hf O
pwdata perturb -e 0.01 -d 0.04 -n 20 -i ./lmps_data/HfO2/96.lmp -f lammps/lmp -s ./test_workdir/perturb_POSCAR -o vasp/poscar -c -t Hf O
pwdata perturb -e 0.01 -d 0.04 -n 20 -i ./lmps_data/HfO2/96.lmp -f lammps/lmp -s ./test_workdir/perturb_lammps -o lammps/lmp -c -t Hf O
pwdata perturb -e 0.01 -d 0.04 -n 20 -i ./vasp_data/Si_POSCAR -f vasp/poscar -s ./test_workdir/perturb_atom -o pwmat/config -c
pwdata perturb -e 0.01 -d 0.04 -n 20 -i ./vasp_data/Si_POSCAR -f vasp/poscar -s ./test_workdir/perturb_POSCAR -o vasp/poscar -c
pwdata perturb -e 0.01 -d 0.04 -n 20 -i ./vasp_data/Si_POSCAR -f vasp/poscar -s ./test_workdir/perturb_lammps -o lammps/lmp -c
pwdata perturb -e 0.01 -d 0.04 -n 20 -i ./vasp_data/LiSi_POSCAR -f vasp/poscar -s ./test_workdir/perturb_atom -o pwmat/config -c
pwdata perturb -e 0.01 -d 0.04 -n 20 -i ./vasp_data/LiSi_POSCAR -f vasp/poscar -s ./test_workdir/perturb_POSCAR -o vasp/poscar -c
pwdata perturb -e 0.01 -d 0.04 -n 20 -i ./vasp_data/LiSi_POSCAR -f vasp/poscar -s ./test_workdir/perturb_lammps -o lammps/lmp -c

# test convert_images
pwdata convert_configs -i ./pwmlff_data/LiSiC -f pwmlff/npy -s ./test_workdir/0_0_configs_PWdata -o pwmlff/npy -p 0.8 -r -g 1
pwdata convert_configs -i ./pwmlff_data/LiSiC -f pwmlff/npy -s ./test_workdir/0_1_configs_extxyz -o extxyz -p 0.8 -r -g 1
pwdata convert_configs -i ./pwmlff_data/LiSiC/Si217 ./pwmlff_data/LiSiC/C2 ./pwmlff_data/LiSiC/Si1 ./pwmlff_data/LiSiC/C64Si32 ./pwmlff_data/LiSiC/Li1Si24 ./pwmlff_data/LiSiC/C64Si32 -f pwmlff/npy -s ./test_workdir/1_0_configs_PWdata -o pwmlff/npy -p 0.8 -r -g 1
pwdata convert_configs -i ./pwmlff_data/LiSiC/Si217 ./pwmlff_data/LiSiC/C2 ./pwmlff_data/LiSiC/Si1 ./pwmlff_data/LiSiC/C64Si32 ./pwmlff_data/LiSiC/Li1Si24 ./pwmlff_data/LiSiC/C64Si32 -f pwmlff/npy -s ./test_workdir/1_1_configs_extxyz -o extxyz -p 0.8 -r -g 1
pwdata convert_configs -i ./pwmat_data/50_LiGePS_movement -f pwmat/movement -s ./test_workdir/2_0_configs_PWdata -o pwmlff/npy -p 0.8 -r -g 1
pwdata convert_configs -i ./pwmat_data/50_LiGePS_movement -f pwmat/movement -s ./test_workdir/2_1_configs_extxyz -o extxyz -p 0.8 -r -g 1
pwdata convert_configs -i ./pwmat_data/50_LiGePS_movement ./pwmat_data/lisi_50_movement -f pwmat/movement -s ./test_workdir/3_0_configs_PWdata -o pwmlff/npy -p 0.8 -r -g 1
pwdata convert_configs -i ./pwmat_data/50_LiGePS_movement ./pwmat_data/lisi_50_movement -f pwmat/movement -s ./test_workdir/3_1_configs_extxyz -o extxyz -p 0.8 -r -g 1
pwdata convert_configs -i ./vasp_data/Si_OUTCAR -f vasp/outcar -s ./test_workdir/4_0_configs_PWdata -o pwmlff/npy -p 0.8 -r -g 1
pwdata convert_configs -i ./vasp_data/Si_OUTCAR -f vasp/outcar -s ./test_workdir/4_1_configs_extxyz -o extxyz -p 0.8 -r -g 1
pwdata convert_configs -i ./xyz_data/PbPt.xyz ./xyz_data/gap_c.xyz ./xyz_data/metal_1.xyz -f extxyz -s ./test_workdir/5_0_configs_PWdata -o pwmlff/npy -p 0.8 -r -g 1
pwdata convert_configs -i ./xyz_data/PbPt.xyz ./xyz_data/gap_c.xyz ./xyz_data/metal_1.xyz -f extxyz -s ./test_workdir/5_1_configs_extxyz -o extxyz -p 0.8 -r -g 1
pwdata convert_configs -i ./deepmd_data/alloy/IrNi_POSCAR/deepmd -f deepmd/npy -s ./test_workdir/6_0_configs_PWdata -o pwmlff/npy -p 0.8 -r -g 1
pwdata convert_configs -i ./deepmd_data/alloy/IrNi_POSCAR/deepmd -f deepmd/npy -s ./test_workdir/6_1_configs_extxyz -o extxyz -p 0.8 -r -g 1
pwdata convert_configs -i ./deepmd_data/alloy/IrNi_POSCAR/deepmd ./deepmd_data/alloy/IrPdNi_POSCAR/deepmd ./deepmd_data/alloy/RhIrPdNi_POSCAR/deepmd -f deepmd/npy -s ./test_workdir/7_0_configs_PWdata -o pwmlff/npy -p 0.8 -r -g 1
pwdata convert_configs -i ./deepmd_data/alloy/IrNi_POSCAR/deepmd ./deepmd_data/alloy/IrPdNi_POSCAR/deepmd ./deepmd_data/alloy/RhIrPdNi_POSCAR/deepmd -f deepmd/npy -s ./test_workdir/7_1_configs_extxyz -o extxyz -p 0.8 -r -g 1
pwdata convert_configs -i ./cp2k_data/dft.log -f cp2k/md -s ./test_workdir/8_0_configs_PWdata -o pwmlff/npy -p 0.8 -r -g 1
pwdata convert_configs -i ./cp2k_data/dft.log -f cp2k/md -s ./test_workdir/8_1_configs_extxyz -o extxyz -p 0.8 -r -g 1
pwdata convert_configs -i ./lmps_data/HfO2/0.lammpstrj ./lmps_data/HfO2/10.lammpstrj ./lmps_data/HfO2/20.lammpstrj ./lmps_data/HfO2/30.lammpstrj -f lammps/dump -s ./test_workdir/9_0_configs_PWdata -o pwmlff/npy -p 0.8 -r -g 1 -t Hf O
pwdata convert_configs -i ./lmps_data/HfO2/0.lammpstrj ./lmps_data/HfO2/10.lammpstrj ./lmps_data/HfO2/20.lammpstrj ./lmps_data/HfO2/30.lammpstrj -f lammps/dump -s ./test_workdir/9_1_configs_extxyz -o extxyz -p 0.8 -r -g 1 -t Hf O
pwdata convert_configs -i ./meta_data/alex_val/alex_go_aao_001.aselmdb ./meta_data/alex_val/alex_go_aao_002.aselmdb -f meta -s ./test_workdir/10_0_configs_PWdata -o pwmlff/npy -p 0.8 -r -g 1 -t Pt Ge
pwdata convert_configs -i ./meta_data/alex_val/alex_go_aao_001.aselmdb ./meta_data/alex_val/alex_go_aao_002.aselmdb -f meta -s ./test_workdir/10_1_configs_extxyz -o extxyz -p 0.8 -r -g 1 -t Pt Ge
