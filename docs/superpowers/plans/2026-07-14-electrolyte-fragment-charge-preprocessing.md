# 电解液 Fragment 与电荷预处理 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 为 `part000.xyz` 的每个原子生成与顺序无关的 fragment ID 和按 fragment 重复的目标总电荷，并对无法唯一推断的内容给出明确报告。

**Architecture:** 采用两遍流式处理。第一遍通过 ASE 周期性邻居表构建共价连通分量、生成拓扑 signature，并利用每帧独立电中性方程建立 charge 注册表；第二遍重新识别 fragment，写出标注 XYZ、逐帧汇总和元数据。人工覆盖、固定规则和自动推断彼此分离。

**Tech Stack:** Python 3.9、NumPy、ASE neighbor list、PyYAML、标准库 `unittest`。

## Global Constraints

- 生产代码只能新增在 `pwdata/electrolytes/`。
- 输入暂时只处理 `/data/public/wuxingxing/electrolytes/decompress/0-19/part000.xyz`。
- 输出写入 `/data/public/wuxingxing/electrolytes/decompress/datacout/part000`。
- 默认每帧总电荷为 0，且每帧分别满足电中性。
- 不构造全原子距离矩阵，不把金属配位关系加入共价 fragment 图。
- `charge` 是 fragment 总电荷，在组内每个原子上重复；训练和验证按 `fragment` 去重。
- 自动推断只接受唯一、整数、范围为 -4 至 +4 且精确满足方程的 signature 电荷。

---

## 文件结构

- `pwdata/electrolytes/__init__.py`：公开预处理接口。
- `pwdata/electrolytes/models.py`：帧、fragment、signature、推断结果数据结构。
- `pwdata/electrolytes/extxyz_io.py`：流式读取和保留原字段的标注写出。
- `pwdata/electrolytes/fragment_graph.py`：周期邻居表、价态约束、union-find。
- `pwdata/electrolytes/signatures.py`：分子式、拓扑不变量和稳定哈希。
- `pwdata/electrolytes/charge_inference.py`：规则、YAML、方程求解、Fe/Zn 守恒。
- `pwdata/electrolytes/preprocess.py`：两遍处理 CLI、目录和报告。
- `pwdata/electrolytes/fragment_charge_rules.yaml`：固定元素价态、拓扑规则和推断范围。
- `pwdata/electrolytes/fragment_charge_overrides.yaml`：人工精确覆盖，初始为空。
- `tests/electrolytes/test_extxyz_io.py`：流式 I/O 和新增列测试。
- `tests/electrolytes/test_fragment_graph.py`：周期图、金属隔离、乱序和氢键测试。
- `tests/electrolytes/test_charge_inference.py`：规则、唯一解、欠定、Fe/Zn 测试。
- `tests/electrolytes/test_zn_regression.py`：`Zn.xyz` 回归测试。

### Task 1: Extended XYZ 流式模型与 I/O

**Files:**
- Create: `pwdata/electrolytes/models.py`
- Create: `pwdata/electrolytes/extxyz_io.py`
- Create: `tests/electrolytes/test_extxyz_io.py`

**Interfaces:**
- Produces: `iter_extxyz(path) -> Iterator[XYZFrame]`
- Produces: `write_annotated_frame(handle, frame, fragment_ids, fragment_charges, status)`
- `XYZFrame` 保存 `symbols`、`positions`、`cell`、`comment`、原子字段和 property schema。

- [ ] **Step 1: 写失败测试**

```python
class ExtxyzIOTest(unittest.TestCase):
    def test_writer_preserves_fields_and_repeats_fragment_charge(self):
        frame = next(iter_extxyz(self.fixture))
        write_annotated_frame(self.output, frame, [0, 0, 1], [0.0, 0.0, 1.0], "resolved")
        text = self.output.getvalue()
        self.assertIn("fragment:I:1:charge:R:1", text)
        reread = next(iter_extxyz(io.StringIO(text)))
        self.assertEqual(reread.extra_arrays["fragment"].tolist(), [0, 0, 1])
        self.assertEqual(reread.extra_arrays["charge"].tolist(), [0.0, 0.0, 1.0])
```

- [ ] **Step 2: 确认测试因模块不存在而失败**

Run: `conda run -n mlff_typ python -m unittest tests.electrolytes.test_extxyz_io -v`
Expected: `ModuleNotFoundError: pwdata.electrolytes`

- [ ] **Step 3: 实现最小模型和 I/O**

实现 `PropertySpec(name, kind, width, offset)`、`XYZFrame`、comment 键值解析、动态
`Properties` offset、一般 3x3 `Lattice`、可选 frame charge 读取，以及追加两列的 writer。
writer 必须逐行复用原 atom fields，并验证数组长度等于原子数。

- [ ] **Step 4: 运行测试通过**

Run: `conda run -n mlff_typ python -m unittest tests.electrolytes.test_extxyz_io -v`
Expected: `OK`

### Task 2: 周期性共价图与稳定 Signature

**Files:**
- Create: `pwdata/electrolytes/fragment_graph.py`
- Create: `pwdata/electrolytes/signatures.py`
- Create: `tests/electrolytes/test_fragment_graph.py`

**Interfaces:**
- Consumes: `XYZFrame`
- Produces: `build_fragments(frame, config) -> FragmentGraphResult`
- Produces: `make_signature(symbols, atom_indices, edges) -> FragmentSignature`

- [ ] **Step 1: 写周期图和顺序无关测试**

```python
class FragmentGraphTest(unittest.TestCase):
    def test_periodic_water_and_short_zn_contact(self):
        frame = make_frame(["O", "H", "H", "Zn"], positions, skew_cell)
        result = build_fragments(frame)
        self.assertEqual(sorted(map(len, result.components)), [1, 3])
        self.assertEqual(result.components[result.atom_to_fragment[3]], [3])

    def test_signature_is_unchanged_by_atom_permutation(self):
        first = analyze_fixture(order=[0, 1, 2])
        second = analyze_fixture(order=[2, 0, 1])
        self.assertEqual(first.signature_id, second.signature_id)

    def test_hydrogen_bond_is_not_covalent(self):
        result = build_fragments(two_waters_with_1_7_angstrom_oh_contact())
        self.assertEqual(sorted(map(len, result.components)), [3, 3])
```

- [ ] **Step 2: 确认测试因接口不存在而失败**

Run: `conda run -n mlff_typ python -m unittest tests.electrolytes.test_fragment_graph -v`
Expected: import failure for `build_fragments` or `make_signature`

- [ ] **Step 3: 实现局部邻居图和 signature**

使用 `ase.neighborlist.neighbor_list("ijd", atoms, max_cutoff)` 获得周期候选；按
`1.20 * (covalent_radius_i + covalent_radius_j)` 过滤，O-H 截断不超过 1.25 A，
并排除 Li/Na/K/Mg/Ca/Fe/Zn 的全部共价边。按归一化距离排序，在
`H/F/Cl/Br/I=1, O=2, C=4, N=4, B=4, P=6, S=6` 的最大 degree 内选边；
竞争最后一个价键且距离差不超过 0.03 A 时记录 ambiguous。使用 union-find 生成组件。

signature 使用 Hill 分子式、元素-degree 计数、元素对边计数和迭代至稳定的
Weisfeiler-Lehman node labels，最终 SHA-256 截取 24 个十六进制字符。

- [ ] **Step 4: 运行图测试通过并运行原 Zn 回归测试**

Run: `conda run -n mlff_typ python -m unittest tests.electrolytes.test_fragment_graph -v`
Expected: `OK`

### Task 3: 三层电荷注册表与每帧联立推断

**Files:**
- Create: `pwdata/electrolytes/charge_inference.py`
- Create: `pwdata/electrolytes/fragment_charge_rules.yaml`
- Create: `pwdata/electrolytes/fragment_charge_overrides.yaml`
- Create: `tests/electrolytes/test_charge_inference.py`

**Interfaces:**
- Produces: `match_builtin_rule(fragment) -> Optional[ChargeAssignment]`
- Produces: `infer_signature_charges(frame_equations, seed_assignments, limits) -> InferenceResult`
- Produces: `resolve_frame_charges(fragments, registry, frame_total_charge) -> FrameChargeResult`

- [ ] **Step 1: 写规则、唯一解、欠定和金属守恒失败测试**

```python
class ChargeInferenceTest(unittest.TestCase):
    def test_uses_each_frame_as_an_independent_equation(self):
        equations = [equation({"A": 1}, -1), equation({"B": 1}, -2)]
        result = infer_signature_charges(equations, {})
        self.assertEqual(result.charges, {"A": -1, "B": -2})

    def test_does_not_label_underdetermined_signatures(self):
        result = infer_signature_charges([equation({"A": 1, "B": 1}, -1)], {})
        self.assertEqual(result.charges, {})
        self.assertEqual(result.unresolved, {"A", "B"})

    def test_zn_receives_the_residual_average(self):
        result = resolve_frame_charges(known_minus_fourteen_plus_seven_zn(), {}, 0)
        self.assertEqual(result.zn_total_charge, 14)
        self.assertEqual(result.zn_average_charge, 2.0)
```

- [ ] **Step 2: 确认测试因函数不存在而失败**

Run: `conda run -n mlff_typ python -m unittest tests.electrolytes.test_charge_inference -v`
Expected: import failure for inference interfaces

- [ ] **Step 3: 实现规则和推断**

YAML 固定规则包括单原子金属/卤素，以及基于 formula、元素-degree 和边计数的
H2O、DMF、SO4、TFSI、FSI、BF4、PF6、DMSO、DMSO2。人工 overrides 只接受
`signature_id -> {charge, note}`。

推断先循环处理单未知方程，再构造 signature-equation 二部图的连通子系统。
对子系统构造整数矩阵 `A` 和 `b`；仅当 `matrix_rank(A) == n_unknowns` 时使用
`numpy.linalg.lstsq`，将结果取整后用 `A @ q == b` 做精确复核。范围、整数性或已有
赋值冲突都会进入 conflict 报告。含 Fe/Zn 的帧不进入 signature 推断。

- [ ] **Step 4: 运行推断测试通过**

Run: `conda run -n mlff_typ python -m unittest tests.electrolytes.test_charge_inference -v`
Expected: `OK`

### Task 4: 两遍 CLI、结果文件和 Zn 回归

**Files:**
- Create: `pwdata/electrolytes/preprocess.py`
- Create: `pwdata/electrolytes/__init__.py`
- Create: `tests/electrolytes/test_zn_regression.py`

**Interfaces:**
- Produces: `preprocess_file(input_path, output_dir, rules_path=None, overrides_path=None) -> RunSummary`
- CLI: `python -m pwdata.electrolytes.preprocess INPUT --output-dir OUTPUT`

- [ ] **Step 1: 写 `Zn.xyz` 和小型两帧端到端失败测试**

```python
class ZnRegressionTest(unittest.TestCase):
    def test_element_sorted_zn_fixture(self):
        analysis = analyze_first_pass(ZN_XYZ)
        self.assertEqual(analysis.fragment_formula_counts,
                         {"H2O": 67, "C3H7NO": 23, "O4S": 7, "Zn": 7})
        resolved = resolve_analysis(analysis)
        self.assertEqual(resolved.zn_total_charge, 14)
        self.assertEqual(resolved.zn_average_charge, 2.0)
        self.assertEqual(resolved.n_fragments, 104)
```

- [ ] **Step 2: 确认端到端接口缺失导致失败**

Run: `conda run -n mlff_typ python -m unittest tests.electrolytes.test_zn_regression -v`
Expected: import failure for preprocessing interfaces

- [ ] **Step 3: 实现第一遍目录、第二遍 writer 和报告**

第一遍保存每帧 signature Counter、fragment 状态、catalog 计数和示例帧；输出自动 YAML
注册表。第二遍重新计算 fragment，确认 signature 未漂移，构造每原子 fragment ID 和
重复 charge，写 XYZ、TSV、JSONL 和压缩 NPZ。所有写入先使用同目录 `.tmp` 文件，
成功后用 `os.replace` 原子替换；异常时保留旧结果。

- [ ] **Step 4: 运行全部新增测试和现有 Zn 测试**

Run: `conda run -n mlff_typ python -m unittest discover -s tests/electrolytes -v`
Expected: all tests `OK`

### Task 5: 运行 part000 并做完成前验证

**Files:**
- Output: `/data/public/wuxingxing/electrolytes/decompress/datacout/part000/*`

- [ ] **Step 1: 在 mlff_typ 环境运行完整预处理**

Run:
```bash
conda run -n mlff_typ python -m pwdata.electrolytes.preprocess \
  /data/public/wuxingxing/electrolytes/decompress/0-19/part000.xyz \
  --output-dir /data/public/wuxingxing/electrolytes/decompress/datacout/part000
```
Expected: CLI 完成两遍扫描并输出 1675 帧汇总。

- [ ] **Step 2: 验证输出结构与电荷不变量**

Run:
```bash
conda run -n mlff_typ python -m pwdata.electrolytes.preprocess \
  --verify-output /data/public/wuxingxing/electrolytes/decompress/datacout/part000/part000_fragment_charge.xyz
```
Expected: 1675 帧；每个原子一个非负 fragment ID；组内 charge 相同；所有 resolved 帧
按 fragment 去重后的电荷和为 0；无 source hash 不匹配。

- [ ] **Step 3: 重新运行完整测试并检查工作树**

Run: `conda run -n mlff_typ python -m unittest discover -s tests/electrolytes -v`
Expected: all tests `OK`

Run: `git status --short`
Expected: 只出现本计划新增的 `pwdata/electrolytes/`、`tests/electrolytes/`，以及开始任务前已存在的未跟踪文件。
