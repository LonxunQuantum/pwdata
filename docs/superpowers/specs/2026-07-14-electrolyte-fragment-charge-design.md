# 电解液 Fragment 与电荷预处理设计

## 一、范围

针对以下数据文件实现预处理流程：

`/data/public/wuxingxing/electrolytes/decompress/0-19/part000.xyz`

生产代码放在 `pwdata/electrolytes/` 目录下，处理结果写入：

`/data/public/wuxingxing/electrolytes/decompress/datacout/part000`

源文件共 1675 帧，每帧包含 148 至 3068 个原子。原子属性只有
`species`、`pos` 和 `forces`，没有帧总电荷字段，因此默认每帧目标总电荷为 0。

## 二、输出列的语义

标注后的 extended XYZ 保留源文件的全部字段，并增加：

- `fragment:I:1`：当前帧内从 0 开始编号的 fragment ID。
- `charge:R:1`：该 fragment 的目标总电荷，在 fragment 所属的每个原子行中重复保存。

训练时必须按 `fragment` 对原子分组，将组内预测的原子电荷求和，然后与该组唯一的
`charge` 标签计算损失。重复保存的 `charge` 标签只能读取一次，不能在组内累加。
无法解析电荷的 fragment 写为 `charge=nan`。

## 三、Fragment 构建

逐帧流式读取 extended XYZ。使用周期性邻居表和一般的 3x3 晶胞矩阵搜索共价键，
不得构造全原子距离矩阵。候选共价键采用可配置的元素对截断半径，默认由共价半径
生成，同时施加元素最大价态约束。H、F、Br 和 I 的最大共价 degree 为 1；
Cl 默认最大 degree 为 1，只有同一 Cl 同时存在至少 3 个短 Cl-O 候选时，
才允许按含氧酸根中心原子处理并提高到 degree 4。
如果出现超过价态限制或多个等价候选解，则将该 fragment 标记为 ambiguous 并输出报告。

Li、Na、K、Mg、Ca、Fe 和 Zn 不参与共价 fragment 图。即使它们与其他原子距离很短，
也必须保持为单原子 fragment，不得把金属配位键当作分子内部共价键。

共价图的连通分量使用 union-find 提取。每个原子必须恰好属于一个 fragment，不能遗漏，
也不能重复分配。

## 四、Fragment Signature

Fragment 的身份不依赖原子排列顺序，也不要求预先知道物种名称。稳定 signature 由以下内容组成：

- Hill 顺序分子式；
- 带元素标签的 Weisfeiler-Lehman 拓扑哈希；
- 节点 degree 直方图；
- 元素对键类型计数。

目录文件同时保存未哈希的拓扑不变量，用于检查哈希碰撞。如果相同 signature 对应不兼容的
拓扑不变量，则报告冲突，不能将两者合并。

## 五、电荷解析

电荷配置分为三个文件，避免自动结果覆盖人工确认内容：

- `fragment_charge_rules.yaml`：人工维护的通用化学规则，例如固定金属价态和已验证物种拓扑。
- `fragment_charge_registry.generated.yaml`：程序扫描数据后自动生成的精确
  `signature -> charge` 注册表，记录来源、状态、出现次数和示例帧。
- `fragment_charge_overrides.yaml`：人工确认或修正的精确 signature 电荷，优先级最高，
  程序只读取、不自动改写。

首次运行时程序先生成 signature 目录，再用固定规则和电中性方程填充自动注册表。
仍然无法确定的 signature 在自动注册表中保留 `charge: null` 和 `status: needs_review`，
人工只需要把确认结果写入 overrides 文件。

电荷解析严格按照以下优先级处理：

1. 人工维护的 YAML 注册表中，以精确 signature 配置的电荷。
2. 已验证 fragment 的确定性规则：单原子 Li、Na、K 为 +1，Mg、Ca 为 +2，
   单原子 F、Cl、Br、I 为 -1。初始拓扑规则覆盖 H2O（0）、DMF（0）、
   SO4（-2）、TFSI（-1）、FSI（-1）、BF4（-1）、PF6（-1）、
   DMSO（0）、DMSO2（0）、ClO4（-1）、Cp/C5H5（-1）、NO3（-1）、
   TFA（-1）、OH（-1）和甲醇（0）。只有分子式和拓扑同时匹配时才能自动赋值，
   不能仅凭分子式赋值。
3. 对不含 Fe 和 Zn 的帧，利用 `part000` 中每帧分别电中性的约束，联立推断未知 signature：
   `sum(fragment_count * signature_charge) = frame_target_charge`。

这里的“全数据集”表示同时使用 `part000` 中所有适用帧各自的独立方程，并让相同 signature
在不同帧共享同一个电荷值；不是把所有帧的 fragment 合并后只要求总和为零。

自动推断首先传播只含一个未知 signature 的方程，然后对剩余相互关联的方程组按连通子系统求解。
只有同时满足以下条件时才接受结果：

- 解唯一；
- 解为整数；
- 电荷位于配置范围 -4 至 +4；
- 能精确满足所有参与推断的帧。

欠定、非整数或互相冲突的方程组保持 unresolved。启发式规则或先验信息只能用于报告排序，
不能据此生成训练标签。

当一帧中所有非 Fe/Zn fragment 的电荷都已确定后，再用电荷守恒处理 Fe 和 Zn：

- 单个 Fe 获得该帧剩余总电荷；
- 所有 Zn 获得该帧剩余总电荷的平均值，每个 Zn 仍是独立 fragment；
- 同一帧同时含 Fe 和 Zn、含多个 Fe，或仍有未知非金属 fragment 时，该帧保持 unresolved。

## 六、代码组件

- `pwdata/electrolytes/extxyz_io.py`：流式解析源 XYZ，并写出增加标注列的 XYZ。
- `pwdata/electrolytes/fragment_graph.py`：周期性邻居搜索、价态约束建键和 union-find 连通分量。
- `pwdata/electrolytes/signatures.py`：分子式和与原子顺序无关的拓扑 signature。
- `pwdata/electrolytes/charge_inference.py`：注册表、固定规则、电中性方程、Fe/Zn 剩余电荷处理和验证。
- `pwdata/electrolytes/preprocess.py`：两遍流式处理的命令行入口和报告生成。
- `pwdata/electrolytes/fragment_charge_rules.yaml`：已验证的通用规则和推断限制。
- `pwdata/electrolytes/fragment_charge_overrides.yaml`：人工确认或修正的精确 signature 电荷。
- `tests/electrolytes/`：共价图、signature、电荷推断、输入输出和 Zn 回归测试。

第一遍扫描所有帧，构建 fragment 和 signature 目录；第二遍解析电荷、验证电中性，
并写出标注后的 XYZ 和各类报告。

第一遍开始前保存源文件 SHA-256、大小和纳秒修改时间；第一遍结束后、第二遍结束后均重新检查，
并逐帧比较两遍 signature 计数。任一项变化都中止处理。多结果文件替换采用备份和异常回滚，
如果某个 `os.replace` 失败，已经替换的文件会删除，旧版本会全部恢复。

## 七、结果文件

输出目录包含：

- `part000_fragment_charge.xyz`；
- `fragment_signature_catalog.tsv`；
- `fragment_charge_registry.generated.yaml`；
- `frame_charge_summary.tsv`；
- `charge_inference_report.tsv`；
- `unresolved_fragments.jsonl`；
- `fragment_charge_summary.txt`；
- `fragment_charge_metadata.npz`。

报告中保存源文件路径、SHA-256、文件大小和修改时间。汇总文件记录已解析与未解析帧数量、
signature 数量、电中性异常、Fe/Zn 电荷分布和原子分配检查结果。

## 八、测试与验收

自动测试覆盖：

- 一般晶胞下的跨周期共价键；
- 打乱原子顺序后结果不变；
- 金属始终保持单原子 fragment；
- 氢键不能识别成共价键；
- signature 与原子排列无关；
- 唯一方程解和欠定方程报告；
- Fe/Zn 电荷守恒处理；
- fragment 内重复 charge 标签的语义；
- 多帧流式输入输出；
- 未知和 ambiguous fragment 的错误报告。

现有 `Zn.xyz` 回归测试必须继续得到：67 个 H2O、23 个 DMF、7 个 SO4、
7 个 Zn、Zn 总形式电荷 +14、Zn 平均形式电荷 +2。

完整运行 `part000.xyz` 后，必须满足：

- 每个原子恰好得到一个 fragment ID；
- 每个已解析 fragment 内的重复 charge 标签完全一致；
- 每个已解析帧按 fragment 去重后的电荷总和在 `1e-8` 误差内等于 0。
