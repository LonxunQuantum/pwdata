# H-H Fragment Fix Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 消除短距离 H-H 接触导致的 H2/OH 错误 fragment，阻止 H/H2 自动投票赋荷，并生成一致的 `extend_loose_fixed` 全量结果与更新后的 PPT。

**Architecture:** 在共价图入口禁止 H-H，在电荷推断入口按 signature ID 阻断 H/H2 自动投票；人工 seed 仍可覆盖。随后从修正图重新生成基础 registry、可信拓扑、extend registry、宽松中性 registry 和 100 个 part 输出。

**Tech Stack:** Python 3.10、NumPy、ASE neighbor list、PyYAML、unittest/pytest、SLURM、artifact-tool。

## Global Constraints

- 旧目录 `datacout/extend_loose` 不得覆盖。
- 新最终目录固定为 `/data/public/wuxingxing/electrolytes/decompress/datacout/extend_loose_fixed`。
- H-H 默认禁止；H/H2 自动投票禁止；人工 YAML seed 允许覆盖。
- Li/Na/K/Mg/Ca/Fe/Zn 和 `extend_loose` 中性规则保持不变。
- 所有 100 个 part 必须使用同一 registry SHA256 和 topology SHA256。
- 修改必须先有失败测试，再实现最小修复。

---

### Task 1: H-H 共价候选回归测试

**Files:**
- Modify: `tests/electrolytes/test_fragment_graph.py`
- Modify: `pwdata/electrolytes/fragment_graph.py`

**Interfaces:**
- Consumes: `build_fragments(frame) -> FragmentGraphResult`
- Produces: `FORBIDDEN_COVALENT_PAIRS`，供 `_pair_cutoff()` 在半径回退前检查。

- [ ] **Step 1: 写入失败测试**

构造两个水分子，使两个异分子 H 的距离为 0.58 A，但各自 O-H 距离为 1.02-1.06 A；断言得到两个 `H2O` 连通分量且不存在 H-H bond。

- [ ] **Step 2: 验证 RED**

Run: `python -m pytest tests/electrolytes/test_fragment_graph.py -q`

Expected: 新测试失败，旧实现生成 `H2 + 2 HO`。

- [ ] **Step 3: 最小实现**

在 `fragment_graph.py` 添加：

```python
FORBIDDEN_COVALENT_PAIRS = frozenset({tuple(sorted(("H", "H")))})
```

并在 `_pair_cutoff()` 的金属检查之后返回 `None`。

- [ ] **Step 4: 验证 GREEN**

Run: `python -m pytest tests/electrolytes/test_fragment_graph.py -q`

Expected: 全部通过。

### Task 2: H/H2 自动投票保护

**Files:**
- Modify: `pwdata/electrolytes/fragment_charge_rules.yaml`
- Modify: `pwdata/electrolytes/charge_inference.py`
- Modify: `pwdata/electrolytes/preprocess.py`
- Modify: `pwdata/electrolytes/dataset_preprocess.py`
- Modify: `tests/electrolytes/test_charge_inference.py`
- Modify: `tests/electrolytes/test_dataset_preprocess.py`

**Interfaces:**
- Consumes: `infer_signature_charges(..., blocked_signature_ids=())`
- Produces: blocked signature 保留 vote stats，但不会进入 `charges`；seed assignment 不受影响。

- [ ] **Step 1: 写入失败测试**

增加20条一致 `H -> +1` 或 `H2 -> +2` 方程，传入 blocked ID 后断言其仍 unresolved；再用人工 seed 断言显式 charge 仍 resolved。

- [ ] **Step 2: 验证 RED**

Run: `python -m pytest tests/electrolytes/test_charge_inference.py tests/electrolytes/test_dataset_preprocess.py -q`

Expected: 当前 API 不接受 `blocked_signature_ids` 或错误地自动 resolved。

- [ ] **Step 3: 最小实现**

在规则 YAML 增加：

```yaml
inference:
  blocked_formulas: [H, H2]
```

`infer_signature_charges()` 在接受自动投票前跳过 blocked ID。`preprocess.py` 从本文件 catalog 计算 blocked ID；`dataset_preprocess.py` 从合并后的 signatures 计算 blocked ID，并把未赋荷条目标记为 `blocked_inference`/`inference_blocked_formula`。

- [ ] **Step 4: 验证 GREEN 与全套回归**

Run: `python -m pytest tests/electrolytes -q`

Expected: 全部通过。

### Task 3: part002 第1612帧真实数据回归

**Files:**
- Create: `tests/electrolytes/test_part002_frame1612_regression.py`

**Interfaces:**
- Consumes: `iter_extxyz()`、`analyze_frame()`
- Produces: 可在数据文件存在时执行的服务器回归测试。

- [ ] **Step 1: 写测试并先验证旧代码失败**

读取 `/data/public/wuxingxing/electrolytes/decompress/0-19/part002.xyz` 第1612帧，断言557原子、179 fragments、175 H2O、2 TFSI、2 Li，且 H/H2/HO 均为0。

- [ ] **Step 2: 在修复后验证通过**

Run: `python -m pytest tests/electrolytes/test_part002_frame1612_regression.py -q`

Expected: PASS。

### Task 4: 宽松 registry 排除 H/H2

**Files:**
- Modify: `/data/public/wuxingxing/electrolytes/build_extend_loose_registry.py`
- Modify: `/data/public/wuxingxing/electrolytes/test_build_extend_loose_registry.py`
- Create: `/data/public/wuxingxing/electrolytes/count_zero_balance_unknown_signatures_fixed.py`

**Interfaces:**
- Consumes: corrected extend 输出和 corrected base registry。
- Produces: final loose registry；Fe/Zn/H/H2 均不会被宽松中性规则赋0。

- [ ] **Step 1: 写失败测试**

断言目标中的 H、H2 被排除并保留 null，普通非金属 solvent 被赋0。

- [ ] **Step 2: 验证 RED**

Run: `python /data/public/wuxingxing/electrolytes/test_build_extend_loose_registry.py`

Expected: H/H2 当前会被错误赋0。

- [ ] **Step 3: 实现与验证**

新增 `BLOCKED_FORMULAS={"H", "H2"}`，输出排除原因；fixed 计数脚本接受 `--input-root` 和 `--output`，不硬编码旧统计。

### Task 5: 新建 SLURM 全量流水线

**Files:**
- Create: `/data/public/wuxingxing/electrolytes/submit_extend_loose_fixed_pipeline.sh`
- Create: `/data/public/wuxingxing/electrolytes/extend_loose_fixed_*.slurm`
- Create: `/data/public/wuxingxing/electrolytes/summarize_extend_loose_fixed_results.py`

**Interfaces:**
- Consumes: part000-part099、修复代码、paper registry。
- Produces: `extend_loose_fixed/work/*` 中间缓存、最终 registry、part000-part099、audit 和 statistics JSON。

- [ ] **Step 1: 创建阶段脚本**

依赖链：base collect -> base merge -> topology build -> fixed collect -> extend merge -> neutral build -> final extend merge -> extend write/audit -> loose target/build -> final write/audit -> summary。

- [ ] **Step 2: 静态检查**

Run: `sh -n /data/public/wuxingxing/electrolytes/submit_extend_loose_fixed_pipeline.sh /data/public/wuxingxing/electrolytes/extend_loose_fixed_*.slurm`

Expected: 无语法错误；所有输出路径均在 `extend_loose_fixed`。

- [ ] **Step 3: 提交并记录 job ID**

Run: `/data/public/wuxingxing/electrolytes/submit_extend_loose_fixed_pipeline.sh`

Expected: 每个阶段返回 job ID，并由 `afterok` 串联。

### Task 6: 全量审计

**Files:**
- Output: `datacout/extend_loose_fixed/audit/*`
- Output: `datacout/extend_loose_fixed/extend_loose_fixed_statistics.json`

- [ ] **Step 1: 等待最终任务完成并检查队列/日志**

Run: `sacct -j <job_ids> --format=JobID,State,ExitCode,Elapsed`

Expected: 全部 COMPLETED/0:0。

- [ ] **Step 2: 验证数据不变量**

检查100 parts、167461帧、112412315原子、0 audit failures、统一 SHA；精确解析 formula JSON，断言 H2 fragment 总数0；检查 H/H2 registry charge 均非自动 resolved。

- [ ] **Step 3: 验证第1612帧**

检查 `part002/frame_charge_summary.tsv` 第1612帧为179 fragments、175 H2O、2 TFSI、2 Li、总电荷0。

### Task 7: 同步 PPT

**Files:**
- Source: `outputs/electrolyte_fragment_charge_report_cn_extend_loose.pptx`
- Create: `outputs/electrolyte_fragment_charge_report_cn_extend_loose_fixed.pptx`

- [ ] **Step 1: 使用最终统计更新页面**

更新封面版本、fragment 建图规则、电荷推断保护、最终 resolved/unresolved/ambiguous、registry 数量、1612帧回归和结论；charge loss 公式保持不变。

- [ ] **Step 2: 渲染与检查**

运行 artifact-tool 全页导出、`slides_test.py`、模板保真检测，逐页检查无溢出或旧统计残留。

- [ ] **Step 3: 最终交付**

报告修改文件、测试命令、SLURM job 状态、全量统计、1612帧结果及 PPT 路径。
