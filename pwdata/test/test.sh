scale_cell -r 1.2 1.1 1.0 0.99 0.98 -i ./pwmat_data/lisi_atom.config -s ./test_workdir/scale_0_0_atom.config -o pwmat/config -c
 pwdata scale_cell -r 1.2 1.1 1.0 0.99 0.98 -i ./pwmat_data/lisi_atom.config -s ./test_workdir/scale_0_1_POSCAR -o vasp/poscar -c
 pwdata scale_cell -r 1.2 1.1 1.0 0.99 0.98 -i ./pwmat_data/lisi_atom.config -s ./test_workdir/scale_0_2_lammps.lmp -o lammps/lmp -c
 pwdata scale_cell -r 1.2 1.1 1.0 0.99 0.98 -i ./pwmat_data/LiGePS_atom.config -s ./test_workdir/scale_1_0_atom.config -o pwmat/config -c
 pwdata scale_cell -r 1.2 1.1 1.0 0.99 0.98 -i ./pwmat_data/LiGePS_atom.config -s ./test_workdir/scale_1_1_POSCAR -o vasp/poscar -c
 pwdata scale_cell -r 1.2 1.1 1.0 0.99 0.98 -i ./pwmat_data/LiGePS_atom.config -s ./test_workdir/scale_1_2_lammps.lmp -o lammps/lmp -c
 pwdata scale_cell -r 1.2 1.1 1.0 0.99 0.98 -i ./lmps_data/HfO2/96.lmp -s ./test_workdir/scale_2_0_atom.config -o pwmat/config -c -t Hf O
 pwdata scale_cell -r 1.2 1.1 1.0 0.99 0.98 -i ./lmps_data/HfO2/96.lmp -s ./test_workdir/scale_2_1_POSCAR -o vasp/poscar -c -t Hf O
 pwdata scale_cell -r 1.2 1.1 1.0 0.99 0.98 -i ./lmps_data/HfO2/96.lmp -s ./test_workdir/scale_2_2_lammps.lmp -o lammps/lmp -c -t Hf O
 pwdata scale_cell -r 1.2 1.1 1.0 0.99 0.98 -i ./vasp_data/Si_POSCAR -s ./test_workdir/scale_3_0_atom.config -o pwmat/config -c
 pwdata scale_cell -r 1.2 1.1 1.0 0.99 0.98 -i ./vasp_data/Si_POSCAR -s ./test_workdir/scale_3_1_POSCAR -o vasp/poscar -c
 pwdata scale_cell -r 1.2 1.1 1.0 0.99 0.98 -i ./vasp_data/Si_POSCAR -s ./test_workdir/scale_3_2_lammps.lmp -o lammps/lmp -c
 pwdata scale_cell -r 1.2 1.1 1.0 0.99 0.98 -i ./vasp_data/LiSi_POSCAR -s ./test_workdir/scale_4_0_atom.config -o pwmat/config -c
 pwdata scale_cell -r 1.2 1.1 1.0 0.99 0.98 -i ./vasp_data/LiSi_POSCAR -s ./test_workdir/scale_4_1_POSCAR -o vasp/poscar -c
 pwdata scale_cell -r 1.2 1.1 1.0 0.99 0.98 -i ./vasp_data/LiSi_POSCAR -s ./test_workdir/scale_4_2_lammps.lmp -o lammps/lmp -c
 pwdata super_cell -m 2 3 4 -i ./pwmat_data/lisi_atom.config -s ./test_workdir/super_0_0_atom.config -o pwmat/config -c
 pwdata super_cell -m 2 3 4 -i ./pwmat_data/lisi_atom.config -s ./test_workdir/super_0_1_POSCAR -o vasp/poscar -c
 pwdata super_cell -m 2 3 4 -i ./pwmat_data/lisi_atom.config -s ./test_workdir/super_0_2_lammps.lmp -o lammps/lmp -c
 pwdata super_cell -m 2 3 4 -i ./pwmat_data/LiGePS_atom.config -s ./test_workdir/super_1_0_atom.config -o pwmat/config -c
 pwdata super_cell -m 2 3 4 -i ./pwmat_data/LiGePS_atom.config -s ./test_workdir/super_1_1_POSCAR -o vasp/poscar -c
 pwdata super_cell -m 2 3 4 -i ./pwmat_data/LiGePS_atom.config -s ./test_workdir/super_1_2_lammps.lmp -o lammps/lmp -c
 pwdata super_cell -m 2 3 4 -i ./lmps_data/HfO2/96.lmp -s ./test_workdir/super_2_0_atom.config -o pwmat/config -c -t Hf O
 pwdata super_cell -m 2 3 4 -i ./lmps_data/HfO2/96.lmp -s ./test_workdir/super_2_1_POSCAR -o vasp/poscar -c -t Hf O
 pwdata super_cell -m 2 3 4 -i ./lmps_data/HfO2/96.lmp -s ./test_workdir/super_2_2_lammps.lmp -o lammps/lmp -c -t Hf O
 pwdata super_cell -m 2 3 4 -i ./vasp_data/Si_POSCAR -s ./test_workdir/super_3_0_atom.config -o pwmat/config -c
 pwdata super_cell -m 2 3 4 -i ./vasp_data/Si_POSCAR -s ./test_workdir/super_3_1_POSCAR -o vasp/poscar -c
 pwdata super_cell -m 2 3 4 -i ./vasp_data/Si_POSCAR -s ./test_workdir/super_3_2_lammps.lmp -o lammps/lmp -c
 pwdata super_cell -m 2 3 4 -i ./vasp_data/LiSi_POSCAR -s ./test_workdir/super_4_0_atom.config -o pwmat/config -c
 pwdata super_cell -m 2 3 4 -i ./vasp_data/LiSi_POSCAR -s ./test_workdir/super_4_1_POSCAR -o vasp/poscar -c
 pwdata super_cell -m 2 3 4 -i ./vasp_data/LiSi_POSCAR -s ./test_workdir/super_4_2_lammps.lmp -o lammps/lmp -c
 pwdata perturb -e 0.01 -d 0.04 -n 20 -i ./pwmat_data/lisi_atom.config -s ./test_workdir/perturb_0_0_atom -o pwmat/config -c
 pwdata perturb -e 0.01 -d 0.04 -n 20 -i ./pwmat_data/lisi_atom.config -s ./test_workdir/perturb_0_1_POSCAR -o vasp/poscar -c
 pwdata perturb -e 0.01 -d 0.04 -n 20 -i ./pwmat_data/lisi_atom.config -s ./test_workdir/perturb_0_2_lammps -o lammps/lmp -c
 pwdata perturb -e 0.01 -d 0.04 -n 20 -i ./pwmat_data/LiGePS_atom.config -s ./test_workdir/perturb_1_0_atom -o pwmat/config -c
 pwdata perturb -e 0.01 -d 0.04 -n 20 -i ./pwmat_data/LiGePS_atom.config -s ./test_workdir/perturb_1_1_POSCAR -o vasp/poscar -c
 pwdata perturb -e 0.01 -d 0.04 -n 20 -i ./pwmat_data/LiGePS_atom.config -s ./test_workdir/perturb_1_2_lammps -o lammps/lmp -c
 pwdata perturb -e 0.01 -d 0.04 -n 20 -i ./lmps_data/HfO2/96.lmp -s ./test_workdir/perturb_2_0_atom -o pwmat/config -c -t Hf O
 pwdata perturb -e 0.01 -d 0.04 -n 20 -i ./lmps_data/HfO2/96.lmp -s ./test_workdir/perturb_2_1_POSCAR -o vasp/poscar -c -t Hf O
 pwdata perturb -e 0.01 -d 0.04 -n 20 -i ./lmps_data/HfO2/96.lmp -s ./test_workdir/perturb_2_2_lammps -o lammps/lmp -c -t Hf O
 pwdata perturb -e 0.01 -d 0.04 -n 20 -i ./vasp_data/Si_POSCAR -s ./test_workdir/perturb_3_0_atom -o pwmat/config -c
 pwdata perturb -e 0.01 -d 0.04 -n 20 -i ./vasp_data/Si_POSCAR -s ./test_workdir/perturb_3_1_POSCAR -o vasp/poscar -c
 pwdata perturb -e 0.01 -d 0.04 -n 20 -i ./vasp_data/Si_POSCAR -s ./test_workdir/perturb_3_2_lammps -o lammps/lmp -c
 pwdata perturb -e 0.01 -d 0.04 -n 20 -i ./vasp_data/LiSi_POSCAR -s ./test_workdir/perturb_4_0_atom -o pwmat/config -c
 pwdata perturb -e 0.01 -d 0.04 -n 20 -i ./vasp_data/LiSi_POSCAR -s ./test_workdir/perturb_4_1_POSCAR -o vasp/poscar -c
 pwdata perturb -e 0.01 -d 0.04 -n 20 -i ./vasp_data/LiSi_POSCAR -s ./test_workdir/perturb_4_2_lammps -o lammps/lmp -c
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
 pwdata convert_configs -i ./deepmd_data -s ./test_workdir/0_0_deepmd_npy_PWdata -o pwmlff/npy -r -g 1 -m 1
 pwdata convert_configs -i ./deepmd_data -s ./test_workdir/0_1_deepmd_npy_extxyz -o extxyz -r -g 1 -m 1
 pwdata convert_configs -i ./vasp_data/Si_OUTCAR -s ./test_workdir/1_0_vasp_outcar_PWdata -o pwmlff/npy -r -g 1 -m 1
 pwdata convert_configs -i ./vasp_data/Si_OUTCAR -s ./test_workdir/1_1_vasp_outcar_extxyz -o extxyz -r -g 1 -m 1
 pwdata convert_configs -i ./pwmat_data/50_LiGePS_movement -s ./test_workdir/2_0_pwmat_movement_PWdata -o pwmlff/npy -r -g 1 -m 1
 pwdata convert_configs -i ./pwmat_data/50_LiGePS_movement -s ./test_workdir/2_1_pwmat_movement_extxyz -o extxyz -r -g 1 -m 1
 pwdata convert_configs -i ./pwmat_data/50_LiGePS_movement ./pwmat_data/lisi_50_movement -s ./test_workdir/3_0_pwmat_movement_PWdata -o pwmlff/npy -r -g 1 -m 1
 pwdata convert_configs -i ./pwmat_data/50_LiGePS_movement ./pwmat_data/lisi_50_movement -s ./test_workdir/3_1_pwmat_movement_extxyz -o extxyz -r -g 1 -m 1
 pwdata convert_configs -i ./xyz_data -s ./test_workdir/4_0_extxyz_PWdata -o pwmlff/npy -r -g 1 -m 1
 pwdata convert_configs -i ./xyz_data -s ./test_workdir/4_1_extxyz_extxyz -o extxyz -r -g 1 -m 1
 pwdata convert_configs -i ./deepmd_data/alloy/IrNi_POSCAR/deepmd ./deepmd_data/alloy/IrPdNi_POSCAR/deepmd ./deepmd_data/alloy/RhIrPdNi_POSCAR/deepmd -s ./test_workdir/5_0_deepmd_npy_PWdata -o pwmlff/npy -r -g 1 -m 1
 pwdata convert_configs -i ./deepmd_data/alloy/IrNi_POSCAR/deepmd ./deepmd_data/alloy/IrPdNi_POSCAR/deepmd ./deepmd_data/alloy/RhIrPdNi_POSCAR/deepmd -s ./test_workdir/5_1_deepmd_npy_extxyz -o extxyz -r -g 1 -m 1
 pwdata convert_configs -i ./cp2k_data/dft.log -s ./test_workdir/6_0_cp2k_md_PWdata -o pwmlff/npy -r -g 1 -m 1
 pwdata convert_configs -i ./cp2k_data/dft.log -s ./test_workdir/6_1_cp2k_md_extxyz -o extxyz -r -g 1 -m 1
 pwdata convert_configs -i ./lmps_data/HfO2/0.lammpstrj ./lmps_data/HfO2/10.lammpstrj ./lmps_data/HfO2/20.lammpstrj ./lmps_data/HfO2/30.lammpstrj -s ./test_workdir/7_0_lammps_dump_PWdata -o pwmlff/npy -r -g 1 -m 1 -t Hf O
 pwdata convert_configs -i ./lmps_data/HfO2/0.lammpstrj ./lmps_data/HfO2/10.lammpstrj ./lmps_data/HfO2/20.lammpstrj ./lmps_data/HfO2/30.lammpstrj -s ./test_workdir/7_1_lammps_dump_extxyz -o extxyz -r -g 1 -m 1 -t Hf O
 pwdata convert_configs -i ./xyz_data/PbPt.xyz ./xyz_data/gap_c.xyz ./xyz_data/metal_1.xyz -s ./test_workdir/8_0_extxyz_PWdata -o pwmlff/npy -r -g 1 -m 1
 pwdata convert_configs -i ./xyz_data/PbPt.xyz ./xyz_data/gap_c.xyz ./xyz_data/metal_1.xyz -s ./test_workdir/8_1_extxyz_extxyz -o extxyz -r -g 1 -m 1
 pwdata convert_configs -i ./pwmlff_data/LiSiC -s ./test_workdir/9_0_pwmlff_npy_PWdata -o pwmlff/npy -r -g 1 -m 1
 pwdata convert_configs -i ./pwmlff_data/LiSiC -s ./test_workdir/9_1_pwmlff_npy_extxyz -o extxyz -r -g 1 -m 1
 pwdata convert_configs -i ./pwmlff_data/LiSiC/Si217 ./pwmlff_data/LiSiC/C2 ./pwmlff_data/LiSiC/Si1 ./pwmlff_data/LiSiC/C64Si32 ./pwmlff_data/LiSiC/Li1Si24 ./pwmlff_data/LiSiC/C64Si32 -s ./test_workdir/10_0_pwmlff_npy_PWdata -o pwmlff/npy -r -g 1 -m 1
 pwdata convert_configs -i ./pwmlff_data/LiSiC/Si217 ./pwmlff_data/LiSiC/C2 ./pwmlff_data/LiSiC/Si1 ./pwmlff_data/LiSiC/C64Si32 ./pwmlff_data/LiSiC/Li1Si24 ./pwmlff_data/LiSiC/C64Si32 -s ./test_workdir/10_1_pwmlff_npy_extxyz -o extxyz -r -g 1 -m 1
 pwdata convert_configs -i ./meta_data/alex_val/alex_go_aao_001.aselmdb ./meta_data/alex_val/alex_go_aao_002.aselmdb -s ./test_workdir/11_0_meta_PWdata -o pwmlff/npy -r -g 1 -m 1 -t Pt Ge
 pwdata convert_configs -i ./meta_data/alex_val/alex_go_aao_001.aselmdb ./meta_data/alex_val/alex_go_aao_002.aselmdb -s ./test_workdir/11_1_meta_extxyz -o extxyz -r -g 1 -m 1 -t Pt Ge
 pwdata count -i ./deepmd_data
 pwdata count -i ./deepmd_data
 pwdata count -i ./vasp_data/Si_OUTCAR
 pwdata count -i ./vasp_data/Si_OUTCAR
 pwdata count -i ./pwmat_data/50_LiGePS_movement
 pwdata count -i ./pwmat_data/50_LiGePS_movement
 pwdata count -i ./pwmat_data/50_LiGePS_movement ./pwmat_data/lisi_50_movement
 pwdata count -i ./pwmat_data/50_LiGePS_movement ./pwmat_data/lisi_50_movement
 pwdata count -i ./xyz_data
 pwdata count -i ./xyz_data
 pwdata count -i ./deepmd_data/alloy/IrNi_POSCAR/deepmd ./deepmd_data/alloy/IrPdNi_POSCAR/deepmd ./deepmd_data/alloy/RhIrPdNi_POSCAR/deepmd
 pwdata count -i ./deepmd_data/alloy/IrNi_POSCAR/deepmd ./deepmd_data/alloy/IrPdNi_POSCAR/deepmd ./deepmd_data/alloy/RhIrPdNi_POSCAR/deepmd
 pwdata count -i ./cp2k_data/dft.log
 pwdata count -i ./cp2k_data/dft.log
 pwdata count -i ./lmps_data/HfO2/0.lammpstrj ./lmps_data/HfO2/10.lammpstrj ./lmps_data/HfO2/20.lammpstrj ./lmps_data/HfO2/30.lammpstrj -t Hf O
 pwdata count -i ./lmps_data/HfO2/0.lammpstrj ./lmps_data/HfO2/10.lammpstrj ./lmps_data/HfO2/20.lammpstrj ./lmps_data/HfO2/30.lammpstrj -t Hf O
 pwdata count -i ./xyz_data/PbPt.xyz ./xyz_data/gap_c.xyz ./xyz_data/metal_1.xyz
 pwdata count -i ./xyz_data/PbPt.xyz ./xyz_data/gap_c.xyz ./xyz_data/metal_1.xyz
 pwdata count -i ./pwmlff_data/LiSiC
 pwdata count -i ./pwmlff_data/LiSiC
 pwdata count -i ./pwmlff_data/LiSiC/Si217 ./pwmlff_data/LiSiC/C2 ./pwmlff_data/LiSiC/Si1 ./pwmlff_data/LiSiC/C64Si32 ./pwmlff_data/LiSiC/Li1Si24 ./pwmlff_data/LiSiC/C64Si32
 pwdata count -i ./pwmlff_data/LiSiC/Si217 ./pwmlff_data/LiSiC/C2 ./pwmlff_data/LiSiC/Si1 ./pwmlff_data/LiSiC/C64Si32 ./pwmlff_data/LiSiC/Li1Si24 ./pwmlff_data/LiSiC/C64Si32
 pwdata count -i ./meta_data/alex_val/alex_go_aao_001.aselmdb ./meta_data/alex_val/alex_go_aao_002.aselmdb -t Pt Ge
 pwdata count -i ./meta_data/alex_val/alex_go_aao_001.aselmdb ./meta_data/alex_val/alex_go_aao_002.aselmdb -t Pt Ge