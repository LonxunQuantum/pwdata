from pwdata.config import Config

# std ext
# xyz =    Config(data_path="/data/home/wuxingxing/codespace/pwdata_dev/examples/xyz_data/metal_1.xyz", format="extxyz")
# pwnpy1 = Config(data_path="/data/home/wuxingxing/codespace/pwdata_dev/examples/pwmlff_data/LiSiC/Si1", format="pwmlff/npy")
# pwnpy2 = Config(data_path="/data/home/wuxingxing/codespace/pwdata_dev/examples/pwmlff_data/LiSiC/C2", format="pwmlff/npy")

# xyz.to(data_path="/data/home/wuxingxing/codespace/pwdata_dev/examples/test_workdir", format="pwmlff/npy", data_name="test")
# xyz.to(data_path="/data/home/wuxingxing/codespace/pwdata_dev/examples/test_workdir", format="extxyz", data_name="test")
# xyz.to(data_path="/data/home/wuxingxing/codespace/pwdata_dev/examples/test_workdir", format="extxyz")
# pwnpy2.to(data_path="/data/home/wuxingxing/codespace/pwdata_dev/examples/test_workdir", format="pwmlff/npy", data_name="test")
# pwnpy2.to(data_path="/data/home/wuxingxing/codespace/pwdata_dev/examples/test_workdir", format="pwmlff/npy")

mvm    = Config(data_path="/data/home/wuxingxing/codespace/pwdata_dev/examples/pwmat_data/50_LiGePS_movement", format="pwmat/movement")
config = Config(data_path="/data/home/wuxingxing/codespace/pwdata_dev/examples/pwmat_data/LiGePS_atom.config", format="pwmat/config")
# mvm.to(data_path="/data/home/wuxingxing/codespace/pwdata_dev/examples/test_workdir", format="pwmlff/npy", data_name="test")
# mvm.to(data_path="/data/home/wuxingxing/codespace/pwdata_dev/examples/test_workdir", format="pwmlff/npy")
# mvm.to(data_path="/data/home/wuxingxing/codespace/pwdata_dev/examples/test_workdir", format="pwmat/movement", data_name="tmp_mvm")
# mvm.to(data_path="/data/home/wuxingxing/codespace/pwdata_dev/examples/test_workdir", format="pwmat/movement")
# config.to(data_path="/data/home/wuxingxing/codespace/pwdata_dev/examples/test_workdir", format="pwmat/config", data_name="tmp_pwmat.config")
# config.to(data_path="/data/home/wuxingxing/codespace/pwdata_dev/examples/test_workdir", format="pwmat/config")

vasp_poscar=Config(data_path="/data/home/wuxingxing/codespace/pwdata_dev/examples/vasp_data/LiSi_POSCAR", format="vasp/poscar")
vasp_outcar=Config(data_path="/data/home/wuxingxing/codespace/pwdata_dev/examples/vasp_data/Si_OUTCAR",  format="vasp/outcar")
# vasp_poscar.to(data_path="/data/home/wuxingxing/codespace/pwdata_dev/examples/test_workdir", format="vasp/poscar", data_name="tmp_poscar")
# vasp_outcar.to(data_path="/data/home/wuxingxing/codespace/pwdata_dev/examples/test_workdir", format="pwmat/movement", data_name="out_movement")
# vasp_outcar.to(data_path="/data/home/wuxingxing/codespace/pwdata_dev/examples/test_workdir", format="pwmlff/npy", data_name="outonpy")
# vasp_outcar.to(data_path="/data/home/wuxingxing/codespace/pwdata_dev/examples/test_workdir", format="extxyz", data_name="outxyz")

cp2k_md = Config(data_path="/data/home/wuxingxing/codespace/pwdata_dev/examples/cp2k_data/dft.log", format="cp2k/md")
# cp2k_md.to(data_path="/data/home/wuxingxing/codespace/pwdata_dev/examples/test_workdir", format="pwmat/movement", data_name="cp2kto_movement")
# cp2k_md.to(data_path="/data/home/wuxingxing/codespace/pwdata_dev/examples/test_workdir", format="pwmlff/npy", data_name="cp2ktoonpy")
# cp2k_md.to(data_path="/data/home/wuxingxing/codespace/pwdata_dev/examples/test_workdir", format="extxyz")

lmps_lmp= Config(data_path="/data/home/wuxingxing/codespace/pwdata_dev/examples/lmps_data/HfO2/96.lmp", format="lammps/lmp")
lmps_md = Config(data_path="/data/home/wuxingxing/codespace/pwdata_dev/examples/lmps_data/HfO2/0.lammpstrj", format="lammps/dump", atom_names=["Hf", "O"])
# # error lmps_md.to(data_path="/data/home/wuxingxing/codespace/pwdata_dev/examples/test_workdir", format="pwmat/movement", data_name="lmpto_movement")
# lmps_md.to(data_path="/data/home/wuxingxing/codespace/pwdata_dev/examples/test_workdir", format="pwmlff/npy", data_name="lmptoonpy")
# lmps_md.to(data_path="/data/home/wuxingxing/codespace/pwdata_dev/examples/test_workdir", format="extxyz", data_name="lmpxyz")

dpmd_npy = Config(data_path="/data/home/wuxingxing/codespace/pwdata_dev/examples/deepmd_data/alloy/IrNi_POSCAR/deepmd", format="deepmd/npy")
dpmd_raw = Config(data_path="/data/home/wuxingxing/codespace/pwdata_dev/examples/deepmd_data/alloy/IrNi_POSCAR/deepmd", format="deepmd/raw")
# dpmd_npy.to(data_path="/data/home/wuxingxing/codespace/pwdata_dev/examples/test_workdir", format="pwmat/movement", data_name="dpnpyto_movement")
# dpmd_npy.to(data_path="/data/home/wuxingxing/codespace/pwdata_dev/examples/test_workdir", format="pwmlff/npy", data_name="dpnpytoonpy")
# dpmd_npy.to(data_path="/data/home/wuxingxing/codespace/pwdata_dev/examples/test_workdir", format="extxyz", data_name="dpnpyxyz")
# dpmd_raw.to(data_path="/data/home/wuxingxing/codespace/pwdata_dev/examples/test_workdir", format="pwmat/movement", data_name="dprawto_movement")
# dpmd_raw.to(data_path="/data/home/wuxingxing/codespace/pwdata_dev/examples/test_workdir", format="pwmlff/npy", data_name="dprawtoonpy")
# dpmd_raw.to(data_path="/data/home/wuxingxing/codespace/pwdata_dev/examples/test_workdir", format="extxyz", data_name="dprawxyz")

# meta
meta_data = Config(data_path="/data/home/wuxingxing/codespace/pwdata_dev/examples/meta_data/alex_val/alex_go_aao_001.aselmdb", format="meta")
# meta_data.to(data_path="/data/home/wuxingxing/codespace/pwdata_dev/examples/test_workdir", format="pwmat/movement", data_name="metato_movement")
# meta_data.to(data_path="/data/home/wuxingxing/codespace/pwdata_dev/examples/test_workdir", format="pwmlff/npy", data_name="metatoonpy")
# meta_data.to(data_path="/data/home/wuxingxing/codespace/pwdata_dev/examples/test_workdir", format="extxyz", data_name="metaxyz")

# pwnpy1 = Config(data_path="/data/home/wuxingxing/codespace/pwdata_dev/examples/pwmlff_data/LiSiC/Si1", format="pwmlff/npy")
# pwnpy2 = Config(data_path="/data/home/wuxingxing/codespace/pwdata_dev/examples/pwmlff_data/LiSiC/C2", format="pwmlff/npy")

print()

# vasp outcar
# voutcar = Config(data_path="", format="vasp/outcar")
# # vasp poscar
# vposcar = Config(data_path="", format="vasp/poscar")

