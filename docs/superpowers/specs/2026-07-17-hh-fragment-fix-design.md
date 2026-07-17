# H-H 误建键与 H/H2 电荷污染修复设计

## 背景

`datacout/extend_loose` 中存在由短距离 H-H 接触触发的错误 fragment。以
`0-19/part002.xyz` 第 1612 帧为例，原始结构应为 175 个 H2O、2 个 Li+ 和
2 个 TFSI-，但当前程序把两个分别属于不同水分子的 H 连接成 H2，并留下
2 个 OH fragment。错误结果随后通过逐帧电中性方程得到 `H2 -> +2`，因此
该帧被错误标记为 resolved。

已确认全局 registry 中该 H2 signature 出现于 16 帧，其中 15 帧提供了
一致的 `+2` 投票。该一致性来自重复的 fragment 划分错误，不代表化学证据。

## 目标

1. 默认禁止 H-H 进入电解液 fragment 的共价图。
2. 禁止裸 H 和 H2 signature 仅依靠数据集电中性投票自动获得电荷。
3. 允许人工 YAML 显式注册的 H 或 H2 覆盖上述自动推断保护。
4. 从修复后的 fragment 图重新生成全局 registry、宽松中性扩展和全部
   100 个 part 的标注结果。
5. 新结果写入
   `/data/public/wuxingxing/electrolytes/decompress/datacout/extend_loose_fixed`，
   不覆盖 `extend_loose`。
6. 使用最终审计数字同步更新中文汇报 PPT。

## 非目标

- 本次不引入跨帧原子身份追踪。
- 本次不尝试识别真实气相 H2、裸质子或反应生成的 H2；如未来确认数据中
  存在这些物种，应通过人工 YAML 明确注册。
- 本次不改变 Li、Na、K、Mg、Ca、Fe、Zn 的既有电荷规则。
- 本次不改变 `extend_loose` 对已知电荷配平后未知非金属片段设为 0 的规则。

## 共价图修复

在 `fragment_graph.py` 中新增显式禁止元素对集合，初始仅包含 H-H。
`_pair_cutoff()` 在使用 ASE 共价半径回退前先检查该集合；H-H 返回 `None`，
因此不会进入候选键、价态竞争或 Union-Find。

其余显式 cutoff 和共价半径回退保持不变，避免扩大本次修改的影响范围。
若两个来自不同分子的 H 瞬时接近，它们仍保留为非共价空间接触；各自可与
正常的 O 或 C 形成共价键。

## 电荷推断保护

在 `fragment_charge_rules.yaml` 的 `inference` 节增加：

```yaml
blocked_formulas:
  - H
  - H2
```

全局和单文件推断在构造 signature catalog 后，将这些分子式对应的
signature ID 传入 `infer_signature_charges()`。自动投票循环不得接受这些
signature，但仍保留投票统计，便于审计。它们在 registry 中保持
`charge: null` 和 unresolved 状态。

人工 override 或明确的内置规则属于 seed assignment，优先级高于自动投票
保护；因此未来确有真实 H+ 或 H2 时，可以通过人工 YAML 显式启用，而不必
再次修改推断算法。

## 全量重建流程

新流水线使用修复后的代码执行以下阶段：

1. 对 100 个 part 重新收集 corrected fragment/signature 扫描结果。
2. 合并 corrected 全局基础 registry。
3. 从 corrected registry 重建高支持度拓扑 registry。
4. 使用 corrected 拓扑重新收集并合并全局电荷 registry。
5. 重新应用论文已知离子规则、中性 SMILES 规则和 `extend_loose` 的配平后
   未知非金属片段中性规则。
6. 使用最终 fixed registry 并行处理 part000-part099，写入
   `extend_loose_fixed/part000` 至 `part099`。
7. 执行全量 audit、状态转移统计和 H/H2 专项审计。

所有阶段使用新的输出目录和 SHA256 文件，避免读取或覆盖旧缓存。SLURM
数组任务继续使用 `cpu,cpu3` 分区，每个 part 独立写入自己的目录。

## 验证与回归测试

自动测试至少覆盖：

1. 两个分别具有正常 O-H 距离、但彼此距离为 0.58 A 的 H 不形成 H-H 键。
2. 上述构型得到两个 H2O，而不是 H2 加两个 OH。
3. `infer_signature_charges()` 不接受被阻断 signature 的一致自动投票。
4. 人工 seed assignment 仍可显式注册被阻断 signature。
5. `part002.xyz` 第 1612 帧得到 557 个原子、179 个 fragment、175 H2O、
   2 TFSI 和 2 Li，且不含 H、H2、OH。

全量输出必须满足：

- 100 个 part 全部通过输出完整性和逐帧电中性审计；
- 总帧数和总原子数与旧结果一致；
- 所有 `frame_charge_summary.tsv` 中 H2 fragment 数量为 0；
- 最终全局 registry 不得把 H 或 H2 标记为自动 resolved；
- 输出状态变化及 resolved/unresolved/ambiguous 总数写入汇总文件。

## PPT 更新

在保留现有模板的前提下，另存 fixed 版本 PPT。更新内容包括：

- fragment 建图规则中增加“默认禁止 H-H”；
- 电荷推断规则中增加“H/H2 不允许仅靠电中性投票自动赋荷”；
- 使用 `extend_loose_fixed` 最终审计数字替换旧统计；
- 增加第 1612 帧回归结果或在结论页注明该错误已消除；
- 保留 fragment charge loss 公式不变。

## 风险与处理

- 禁止 H-H 会改变少量帧的 signature 和 resolved 状态，因此必须重建全局
  registry，不能只重写 16 帧。
- 若数据中确有真实 H2，本次会将其拆成两个未注册 H，并保持 unresolved；
  这是有意的保守行为，后续可由人工 YAML 修正。
- 电中性只能作为电荷约束，不能反向证明 fragment 化学正确；专项审计将把
  H、H2、OH 和异常短距离接触单独统计，防止再次出现“错误但配平”的结果。
