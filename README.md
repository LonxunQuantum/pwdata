# pwdata

pwdata 是 PWMLFF 系列机器学习力场软件的**训练数据转换工具**。它把各第一性原理 / 分子动力学软件的输出文件统一转换为 PWMLFF 训练所需的 `pwmlff/npy` 数据集或 `extxyz` 轨迹文件，并提供结构文件的互转、扩胞、缩放、微扰、切表面等预处理功能。

- 官网文档：<http://doc.lonxun.com/PWMLFF/Appendix-2/>

---

## 1. 安装

```bash
git clone <repo-url> pwdata
cd pwdata
pip3 install .
```

安装后获得命令行工具 `pwdata`（入口 `pwdata.main:main`）。

依赖：`ase >= 3.25.0`、`ase-db-backends`、`lmdb`、`numpy`、`orjson`、`PyYAML`、`setuptools`、`tqdm`、`typing_extensions`。

---

## 2. 支持的格式

### 2.1 可读取的格式

| 格式名 (`-f` / `format=`) | 输入文件 | 说明 |
|---|---|---|
| `pwmat/config` | `atom.config` | PWmat 单结构文件 |
| `pwmat/movement` | `MOVEMENT` | PWmat AIMD / 驰豫轨迹 |
| `vasp/poscar` | `POSCAR` | VASP 单结构文件 |
| `vasp/outcar` | `OUTCAR` | VASP AIMD / 驰豫轨迹（只取收敛的离子步） |
| `lammps/lmp` | `lammps.lmp` | LAMMPS data 文件，需 `-t` 指定元素类型顺序 |
| `lammps/dump` | `*.lammpstrj` | LAMMPS dump 轨迹，需 `-t` 指定元素类型顺序 |
| `cp2k/scf` | CP2K 输出日志（如 `dft.log`） | 单点 / 结构优化输出 |
| `cp2k/md` | CP2K 输出日志 + 同目录 `*-pos*`（轨迹）与 `*-frc*`（力）文件 | AIMD 轨迹 |
| `castep/scf` | `<seed>.castep` | CASTEP 单点 / 结构优化输出（兼容新版与 ≤6.x 旧版格式） |
| `castep/geom` | `<seed>.geom` | CASTEP 结构优化轨迹 |
| `castep/md` | `<seed>.md` | CASTEP AIMD 轨迹 |
| `deepmd/npy` | `energy.npy` 等所在目录 | DeepMD npy 数据集 |
| `deepmd/raw` | `energy.raw` 等所在目录 | DeepMD raw 数据集 |
| `pwmlff/npy` | `energies.npy` 等所在目录 | PWMLFF 训练数据集 |
| `extxyz` | `*.xyz`（extxyz 格式，含 `Lattice`、`energy`、`forces` 等属性） | 扩展 xyz 轨迹 |
| `meta` | `*.aselmdb`（ASE SQLite/JSON 数据库） | 支持 `-q` 查询语句、`-n` 多进程读取 |

格式名省略 `-f` 时会根据文件内容 / 扩展名自动推断（`castep/*.castep|.geom|.md`、`vasp/outcar`、`pwmat/movement` 等均可自动识别）。

### 2.2 可写入的格式

| 格式名 | 输出文件 | 说明 |
|---|---|---|
| `pwmlff/npy` | `PWdata/<组成>/` 目录（energies.npy、forces.npy、lattice.npy、position.npy、virials.npy、ei.npy、atom_type.npy、image_type.npy） | PWMLFF 训练数据，默认输出格式 |
| `extxyz` | `*.xyz`（默认合并为一个文件） | 通用轨迹格式 |
| `pwmat/config` | `atom.config` | 单结构 |
| `vasp/poscar` | `POSCAR` | 单结构 |
| `lammps/lmp` | `lammps.lmp` | 单结构 |

---

## 3. 命令行使用

### 3.1 转换轨迹数据为训练集（核心命令）

```bash
# VASP AIMD -> PWMLFF 训练数据（默认格式）
pwdata convert_configs -i ./Si_OUTCAR -f vasp/outcar -s ./PWdata

# CP2K AIMD -> extxyz
pwdata convert_configs -i ./cp2k_data/dft.log -f cp2k/md -s ./out_xyz -o extxyz

# CASTEP 结构优化轨迹 / AIMD
pwdata convert_configs -i ./castep_data/dft.geom -f castep/geom -s ./PWdata
pwdata convert_configs -i ./castep_data/dft.md   -f castep/md   -s ./PWdata

# 目录批量转换（自动识别目录中的文件）
pwdata convert_configs -i ./multi_data_dir -s ./PWdata
```

参数说明：

| 参数 | 说明 |
|---|---|
| `-i` | 输入文件或目录，可多个；也可用 JSON 文件列出路径（见 3.6） |
| `-f` | 输入格式（见 2.1 表），省略时自动推断 |
| `-s` | 输出目录，默认 `./` |
| `-o` | 输出格式：`pwmlff/npy`（默认）或 `extxyz` |
| `-g` | 从轨迹中每隔 `gap` 步取一帧（默认 1） |
| `-m` | `-m 1` 时 extxyz 输出合并为一个文件（默认），否则按元素组成分目录保存 |
| `-r` | 保存前随机打乱数据顺序（不划分 train/valid 集） |
| `-t` | 元素类型列表（`lammps/*` 必需；`meta` 用作元素过滤） |
| `-q` / `-n` | 仅 `meta` 格式：ASE 查询语句 / 多进程读取核数 |

> `pwmlff/npy` 保存时原子会按原子序数排序（O 在前、Si 在后），这是 pwdata 全格式统一的保存行为。

### 3.2 单结构文件互转

```bash
# POSCAR -> atom.config（PWmat），分数坐标
pwdata cvt_config -i ./POSCAR -f vasp/poscar -o pwmat/config -s ./atom.config

# atom.config -> POSCAR
pwdata cvt_config -i ./atom.config -f pwmat/config -o vasp/poscar -s ./POSCAR

# 输出 lammps.lmp 需给出元素类型顺序
pwdata cvt_config -i ./atom.config -f pwmat/config -o lammps/lmp -s ./lammps.lmp -t Hf O
```

`-c` 表示使用笛卡尔坐标输出（默认分数坐标）。`-o` 为必选参数；通过 Python API（`do_convert_config`）调用且不指定输出格式时，`cp2k/scf`、`castep/scf` 输入默认重映射为 `pwmat/config`（`atom.config`）。

### 3.3 统计结构数量

```bash
pwdata count -i ./Si_OUTCAR
pwdata count -i ./castep_data/dft.md -f castep/md
pwdata count -i ./multi_data_dir
```

### 3.4 结构预处理

```bash
# 晶胞缩放（可多个因子，输出文件名加因子前缀，如 0.99_atom.config）
pwdata scale_cell -i ./atom.config -f pwmat/config -r 0.99 0.98 -o pwmat/config -s ./atom.config

# 扩胞（3 个数为对角矩阵，9 个数为完整矩阵）
pwdata super_cell -i ./atom.config -f pwmat/config -m 2 2 2 -o pwmat/config -s ./super_atom.config
pwdata super_cell -i ./atom.config -f pwmat/config -m 2 0 0 0 2 0 0 0 2 -o vasp/poscar -s ./POSCAR

# 扰动结构（原子位移 0.01 Å，晶胞形变 3%，生成 10 个）
pwdata perturb -i ./atom.config -f pwmat/config -d 0.01 -e 0.03 -n 10 -o pwmat/config -s ./perturb

# 切表面（更多真空层参数见 -h）
pwdata surface_config -i ./atom.config -f pwmat/config -e 1 1 1 -n 3 -v 12 -o vasp/poscar -s ./surf_POSCAR
```

### 3.5 帮助

```bash
pwdata -h           # 查看所有子命令
pwdata convert_configs -h
```

### 3.6 JSON 配置模式

`pwdata convert_configs` 与 `pwdata count` 支持用 JSON 文件组织输入（与 PWMLFF 训练配置文件兼容）：

```json
{
  "raw_files": ["./vasp_data/Si_OUTCAR", "./castep_data/dft.md"],
  "format": "vasp/outcar",
  "save_format": "pwmlff/npy",
  "trainSetDir": "./PWdata",
  "valid_shuffle": true
}
```

```bash
pwdata convert_configs <config.json>
pwdata count extract.json        # extract.json 使用 "datapath": [...] 列出路径
```

---

## 4. Python API

```python
from pwdata import Config

# 读取（format 省略时自动推断；index 支持切片选择帧，如 '::2'、'-1'、'1::2'）
config = Config(format="castep/md", data_path="./castep_data/dft.md", index="::2")
print(len(config.images))            # Image 列表
image = config.images[0]
print(image.Ep, image.force.shape, image.lattice)   # 能量(eV)、力(eV/Å)、晶格(Å)

# 单结构转换
config = Config(format="vasp/poscar", data_path="./POSCAR")
config.to(data_path="./", data_name="atom.config", format="pwmat/config", direct=True, sort=True)

# 轨迹 -> 训练集
config = Config(format="vasp/outcar", data_path="./Si_OUTCAR")
config.to(data_path="./PWdata", format="pwmlff/npy",
          data_name="PWdata", random=True, seed=2024, retain_raw=False)
```

`Config.to` 常用关键字：`data_name`（输出文件名/数据集名）、`sort`（保存前按原子序数排序）、`direct`（分数坐标）、`wrap`（按周期边界包裹原子）；`pwmlff/npy` 格式支持 `data_name` / `random` / `seed` / `retain_raw`（数据随机打乱、随机种子、是否保留 raw 文件）。如需 train/valid 划分，请使用 `Save_Data` 类（见 [config.py](pwdata/config.py)）。

更多示例见 [examples/interface_call.py](examples/interface_call.py)。

---

## 5. 各格式输入文件说明

- **VASP**：`vasp/poscar` 读 `POSCAR`；`vasp/outcar` 读 `OUTCAR`（仅保留 SCF 收敛的离子步，能量取 TOTEN，原子类型从 POTCAR 头解析）。
- **PWmat**：`pwmat/movement` 读 `MOVEMENT`；`pwmat/config` 读 `atom.config`（类型为原子序数，1 基）。
- **LAMMPS**：`lammps/lmp` 与 `lammps/dump` 均需 `-t Hf O` 按文件中类型顺序给出元素（dump 支持 `metal` 等单位，`-f lammps/dump` 时可用 `unit`、`style` 关键字）。dump 轨迹每帧一个 `ITEM: TIMESTEP` 块。
- **CP2K**：`cp2k/md` 传输出日志文件路径，晶格/周期性/应力取自日志，位置/力取自同目录的 `*-pos*`（pdb/xyz）与 `*-frc*` 文件；`cp2k/scf` 读日志中 `CELL_TOP`、`TOTAL NUMBERS`、`ATOMIC COORDINATES`、`ENERGY| Total FORCE_EVAL`、`ATOMIC FORCES`、`STRESS` 等段落。
- **CASTEP**：
  - `castep/scf` 读 `<seed>.castep`，兼容新版（`Final energy, E`、`Cartesian components of stress tensor (GPa)`）与 ≤6.x / Materials Studio 旧版（`Final energy`、`Cartesian components (GPa)`）标记；旧版每个 BFGS 迭代会打印多次能量（截断能收敛扫描），仅"能量 + 完整力表"齐全的步才会生成一帧，其余为中间结果不输出；
  - `castep/geom` 读 `<seed>.geom`、`castep/md` 读 `<seed>.md`，均为原子单位（Hartree/Bohr），自动转换为 eV/Å；兼容经典 `<-- E` 标签布局与新版 `BEGIN/END header` 块布局；速度、温度、压力不读取。
- **extxyz**：每帧带 `Lattice`、`energy`、`forces` 等属性行，属性名可含冒号前缀。
- **meta**：ASE 数据库（`.aselmdb`），`-t` 过滤元素、`-q` 高级查询。

---

## 6. 测试

仓库自带各格式示例数据与冒烟测试脚本：

```bash
cd examples
bash test.sh                # 全格式转换冒烟测试（需先安装 pwdata 到 PATH）
python3 ../pwdata/test.py   # 等价驱动脚本（含 config.json 测试矩阵）
python3 interface_call.py   # Python API 往返测试
```

示例数据位于 `examples/<format>_data/`，测试输出写入 `examples/test_workdir/`（已 gitignore）。

---

## 7. 发布（维护者）

```bash
pip3 install setuptools wheel twine
rm dist/ -r
python3 setup.py sdist bdist_wheel
twine upload dist/* --verbose
```
