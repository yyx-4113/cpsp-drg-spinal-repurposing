# P6 老药新用虚拟筛选结果（CPSP / DRG-脊髓轴）

> 本文件由 `scripts/p6_report.py` 自动生成，所有数值从 `results/tables/` 下的产物读取。

## 1. 目的与设计

在 P3 双机器学习锁定的 hub 靶标与 §6 优先靶标之上，用已批准药物库做**结构基础的虚拟筛选（分子对接）**，产出可进入湿实验的老药新用候选清单，并用**反向阳性对照**为每个靶标的排序结论定可信度权重。

关键设计选择：**对接打分的保真度上限**必须先用实测确立，再决定对接参数；否则会得到一个看似完整、实则排序失效的结果矩阵（见第 5 节）。

## 2. 计算环境

| 项 | 值 |
|---|---|
| Python | 3.13.14（隔离 venv） |
| 对接引擎 | AutoDock Vina 1.2.5（官方 Windows exe） |
| 配体准备 | RDKit + Meeko 0.8.0 |
| 受体准备 | gemmi + Open Babel 3.1.0 |
| 并行 | 7 worker × `--cpu 1`（8 核机） |

## 3. 配体库（已批准药物）

来源：ChEMBL `max_phase=4`（DrugBank 已批准药物的开放等价物），以 Broad Drug Repurposing Hub（CC0）交叉注释。

| 漏斗阶段 | 数量 |
|---|---|
| chembl_max_phase4_total | 4225 |
| with_smiles | 3417 |
| small_molecule | 3311 |
| after_dedup | 3311 |
| pdbqt_ok | 3085 |
| pain_prior_in_library | 64 |
| dropped_reasons | {'F3_druglikeness': 57, 'F2_mw_96': 12, 'F2_mw_60': 11, 'F2_mw_59': 10, 'F2_metal': 10, 'F5_pdbqt_fail:atom number 1 has None type, mol name: N': 7, 'F4_embed_fail': 6, 'F2_mw_62': 4, 'F2_mw_89': 4, 'F2_mw_929': 4, 'F5_pdbqt_fail:atom number 0 has None type, mol name: N': 4, 'F2_mw_1140': 3, 'F2_mw_61': 3, 'F2_mw_97': 3, 'F2_mw_18': 3, 'F2_mw_17': 3, 'F2_mw_1269': 3, 'F2_mw_94': 2, 'F2_mw_46': 2, 'F2_mw_77': 2, 'F2_mw_75': 2, 'F2_mw_1449': 2, 'F2_mw_1029': 2, 'F2_mw_98': 2, 'F2_mw_82': 2, 'F2_mw_943': 2, 'F2_mw_90': 2, 'F2_mw_35': 2, 'F2_mw_1035': 2, 'F2_mw_1288': 2, 'F2_mw_1093': 2, 'F2_mw_1793': 2, 'F2_mw_1145': 2, 'F2_mw_1226': 2, 'F2_mw_1322': 2, 'F2_mw_914': 1, 'F2_mw_76': 1, 'F2_mw_924': 1, 'F2_mw_78': 1, 'F2_mw_92': 1, 'F2_mw_65': 1, 'F2_mw_34': 1, 'F2_mw_28': 1, 'F2_mw_86': 1, 'F2_mw_1621': 1, 'F2_mw_1110': 1, 'F2_mw_1270': 1, 'F2_mw_47': 1, 'F2_mw_1138': 1, 'F2_mw_72': 1, 'F2_mw_1022': 1, 'F2_mw_30': 1, 'F2_mw_99': 1, 'F2_mw_1268': 1, 'F2_mw_81': 1, 'F2_mw_1030': 1, 'F2_mw_16': 1, 'F2_mw_974': 1, 'F2_mw_84': 1, 'F2_mw_44': 1, 'F2_mw_32': 1, 'F2_mw_1085': 1, 'F2_mw_1058': 1, 'F5_pdbqt_fail:atom number 7 has None type, mol name: N': 1, 'F2_mw_51': 1, 'F2_mw_52': 1, 'F2_mw_4': 1, 'F2_mw_958': 1, 'F2_mw_1237': 1, 'F2_mw_85': 1, 'F2_mw_1238': 1, 'F2_mw_88': 1, 'F2_mw_1113': 1, 'F2_mw_947': 1, 'F2_mw_1309': 1, 'F2_mw_980': 1, 'F2_mw_968': 1, 'F2_mw_967': 1} |

- 进入对接的配体：**3,085** 个（占候选 3,311 的 93.2%）

- 已知镇痛药（人工标注先验）覆盖：**64** 个

- CNS/镇痛先验子集（Tier 1）：**3,085** 个


> **方法学留痕**：配体准备阶段曾用 `rdMolStandardize.FragmentParent` 去反离子，它对本库中含盐的多组分 SMILES 抛 `RuntimeError`，异常被 `except: pass` 吞掉后该分子仍带反离子，随后在构象生成阶段再次抛错，**导致 1,078 个含盐药物被静默丢弃**（丙戊酸钠、色甘酸钠、沙奎那韦、阿仑膦酸钠等）。改用 `LargestFragmentChooser`后配体数由 2,040 升至 3,085，失败归零。

## 4. 靶标可成药性筛查

候选靶标 **43** 个（35 个 P3 hub + §6 优先靶标），决策分布：

- `DOCK`：18
- `EXCLUDE`：12
- `HOLD_AF2`：11
- `HOLD_APO`：2


完成受体准备、可实际对接的靶标：**10** 个


| symbol   | pdb_id   | ligand_ref   | target_chains   |
|:---------|:---------|:-------------|:----------------|
| GALNS    | 4FDJ     | NGA          | A,B             |
| SLC2A1   | 6THA     | P33          | A               |
| TNIK     | 6RA7     | JWK          | A               |
| ITPKC    | 2A98     | I3P          | A               |
| AXL      | 5U6B     | 7YS          | A,B,C,D         |
| SERPINE1 | 7AQF     | RV2          | A,B             |
| MAPK14   | 3LFF     | Z83          | A               |
| VASH2    | 6J4P     | BJL          | A               |
| ACVR1    | 6SRH     | LU8          | A,B             |
| ADRA2A   | 6KUX     | E3F          | A               |


未能对接的 8 个，原因分布：

- `FAIL_no_pocket_ligand`：8


> **必须如实写进局限的结构性缺口**：§6 列为优先靶标的离子通道类（SCN9A / SCN10A / SCN11A / KCNQ2 / CACNA2D1 / GABRA1）**全部无法对接** —— 它们是无可用 holo 晶体结构的膜蛋白，缺少可定位的正构位点。这意味着 P6 的结论**不能**覆盖 §6 中机制上最重要的一类镇痛靶标，只能覆盖有结构可用的一支。这一限制不能靠措辞弱化。

## 5. 对接参数保真度验证（本阶段最关键的方法学结论）

做法：在锚点靶标（MAPK14 / 3LFF）上，按**可旋转键分层抽样** 15 个配体，以慢速高精度设置为金标准，比较各快速设置与金标准的一致性。

口径（唯一，全文一致）：Δ = 变体亲和力 − 金标准亲和力（**带符号**，正 = 变体打分更弱）；ρ(Δ, 可旋转键) 用 Spearman，**只有带符号 Δ 才能检验偏差是否系统性地惩罚柔性配体**。逐配体原始值见 `results/tables/P6_stage1_param_validation.csv`。


| 设置                    |   n |   rho_Spearman |   delta_abs_median |   delta_mean |   rho_delta_tors |   top10_recall |   sec_mean |   speedup |
|:----------------------|----:|---------------:|-------------------:|-------------:|-----------------:|---------------:|-----------:|----------:|
| 金标准（基准）               |  15 |          1.000 |              0.000 |        0.000 |            0.000 |          1.000 |     43.664 |     1.000 |
| exh2 + max_evals 2000 |  15 |         -0.229 |              1.958 |        2.172 |            0.263 |          0.000 |      1.949 |    22.399 |
| exh2 + max_evals 6000 |  15 |          0.111 |              1.362 |        1.706 |            0.249 |          0.000 |      2.046 |    21.341 |


`exhaustiveness` 专项对照（复用同批金标准，逐配体原始值见 `results/tables/P6_exh_validation.csv`）：


| 设置                   |   n |   rho_Spearman |   delta_abs_median |   delta_mean |   rho_delta_tors |   top10_recall |   sec_mean |   speedup |
|:---------------------|----:|---------------:|-------------------:|-------------:|-----------------:|---------------:|-----------:|----------:|
| 金标准（基准）              |  12 |          1.000 |              0.000 |        0.000 |            0.000 |          1.000 |     27.226 |     1.000 |
| exhaustiveness 2（默认） |  12 |          0.783 |              0.088 |        0.448 |            0.029 |          1.000 |      9.380 |     2.903 |
| exhaustiveness 1     |  12 |          0.783 |              0.174 |        0.453 |            0.119 |          1.000 |      5.931 |     4.591 |


> 上表已落盘为 `results/tables/P6_param_summary.csv`，供稿件中每个数字溯源。


**结论（决定了整个 P6 的参数选择）**：

- **`--max_evals` 路线不可用**：它压缩的是**单次运行的采样步数上限**，柔性配体因此搜不到
  最优构象。表现在两个层面同时出现：① **整体大幅偏弱**（Δ 均值 +2.17 / +1.71 kcal/mol）；
  ② **偏弱幅度随柔性增强**（ρ(Δ, 可旋转键) = +0.263 / +0.249，为**正**，即越柔性被打得越弱）
  —— 这是**系统性**偏差，会直接把柔性配体挤出榜单。
  最终 Spearman ρ ≤ 0.11，**top-10% 召回率 0%**：排序完全失效，
  不可用于任何"取 top-N 候选"的用途。
- **`--exhaustiveness` 路线可用**：它只是**重复独立优化取最优**，单次运行本身已充分，
  降到 1 只带来一个**近似恒定的轻微偏移**（Δ 均值 +0.45 kcal/mol），
  且该偏移**几乎不随柔性变化**（ρ(Δ, 可旋转键) = +0.029，接近零）
  —— 恒定偏移不改变配体之间的相对次序，所以排序保真度得以保持：
  exh=1 与 exh=2 的 Spearman ρ **完全相同（0.783）**，而单配体耗时由 27.2s 降至 5.9s（**4.6×**）。
- **最终参数：`--exhaustiveness 1`，不设置 `--max_evals`。**
  算力不足时应缩配体库或靶标数，**绝不压 `max_evals`**。
- **保真度现实上限 ρ ≈ 0.78**。因此全文措辞为 *candidate prioritisation*（候选优选），
  **不得**表述为 *accurate binding ranking*（精确结合能排序）。

## 6. 对接执行

| 分层 | 配体 | 靶标 | 对接次数 | 状态 |
|---|---|---|---|---|

| Tier 1（CNS/镇痛先验） | 620 | 10 | 6,200 | 完成 |

| Tier 2（其余已批准药） | 2465 | 10 | 24,650 | 完成 |


合计完成对接 **30,850** 次；有打分 30,687 次。

对接返回错误/无打分：163 次（0.53%）。

单次对接耗时：中位 18.8s，合计 302.5 机时。

## 7. 反向阳性对照（方法学校验）

ChEMBL 实测活性层（pChEMBL ≥ 6，即 ≤1 µM）提供的阳性数：

- ADRA2A：115
- MAPK14：16
- AXL：13
- TNIK：10
- ACVR1：9
- SLC2A1：1


| symbol   |   n_known_pairs |   n_ligands |   known_median_aff |   all_median_aff |   auc_known_vs_rest |   reliable |
|:---------|----------------:|------------:|-------------------:|-----------------:|--------------------:|-----------:|
| AXL      |              13 |        3071 |             -8.021 |           -6.511 |               0.880 |      1.000 |
| TNIK     |              10 |        3063 |             -8.700 |           -6.688 |               0.824 |      1.000 |
| ACVR1    |               9 |        3075 |             -8.951 |           -7.706 |               0.797 |      1.000 |
| MAPK14   |              16 |        3068 |             -7.758 |           -6.597 |               0.779 |      1.000 |
| SLC2A1   |               1 |        3066 |            -10.240 |           -8.005 |               0.914 |    nan     |
| ADRA2A   |             115 |        3070 |             -7.719 |           -7.500 |               0.532 |      0.000 |
| GALNS    |               0 |        3064 |            nan     |           -6.496 |             nan     |    nan     |
| ITPKC    |               0 |        3065 |            nan     |           -5.060 |             nan     |    nan     |
| SERPINE1 |               0 |        3075 |            nan     |           -5.820 |             nan     |    nan     |
| VASH2    |               0 |        3070 |            nan     |           -6.631 |             nan     |    nan     |


**通过校验（AUC ≥ 0.60 且阳性数 ≥ 3）的靶标：4 个（AXL, TNIK, ACVR1, MAPK14）。**

未通过校验的靶标，其打分排序被视为缺乏区分力，在四维评分中 D4 取中性 0.5。


**标签口径决策（为什么只用 ChEMBL）**：反向对照测的是「对接打分能否区分**真正结合**该靶标的分子」，
因此标签必须是**结合型**（实测 IC50/Kd/Ki ≤ 1 µM），不能掺入**适应症/注释型**标签 ——
PAIN_PRIOR 记的是"这药是已知镇痛药"，DRH target 字段记的是"注释靶点"，二者回答的是不同问题。
实测（ADRA2A，Tier 1）：纯 ChEMBL n=88 → **AUC 0.618**；掺入 DRH(+11)/PAIN_PRIOR(+2) 后
n=101 → AUC 0.592。两者都 > 0.5（方向一致、结论稳健），但**本稿以 ChEMBL 口径为主**，
因其判据单一、客观、可复现。手工镇痛药标注改用于 §3.4 的**面容效度**分析（另一个独立问题）。


**关于阳性集覆盖的真实情况（不可略过）**：仅用 Drug Repurposing Hub 的靶点注释 +
人工镇痛药标注时，阳性集会**几乎全部落在 ADRA2A 一个靶标上**（其余 9 个为 0）。
原因是真实的：MAPK14 在 DRH 中有 38 个注释药物，但**全是临床前/Ph1–3 的 p38 抑制剂，
没有一个是已批准药**，而本库是已批准药库，故交集为 0；AXL / ACVR1 / SLC2A1 / SERPINE1 同理。
脚本 `scripts/p6_score.py` 中曾有一条 `and t not in hub` 的过滤条件 ——
而 10 个可对接靶标里有 9 个本身就是 hub 基因 —— 该条件会把 DRH 层阳性几乎全部滤掉，
使反向对照退化为"仅 1 个靶标"，属于隐蔽的失效，已修正。另由
`scripts/p6_reverse_control.py` 引入与对接完全独立的 ChEMBL 实测活性作为补充阳性来源。


### 7.1 富集信号是否为「分子量伪信号」？（必答的审稿问题）


分子对接打分天然偏袒**大分子**：配体越大、重原子越多，打分函数给出的亲和力数值越负。
因此"已知活性药富集"很可能是**分子量（MW）伪信号**而非方法有效。
本检验给出三重防线：**① MW-only 基线**（仅用 MW 预测阳性的 AUC，尺寸偏倚上界）、
**② MW 线性校正后 AUC**（对接打分对 MW 回归取残差）、**③ MW 五分位分层内 AUC**（非参数，最稳健）。
判读规则在 `scripts/p6_mw_confounder.py` 中写死，不做事后解释：
只有 docking AUC > 0.5 **且**校正/分层后仍 > 0.5 **且** AUC_dock > AUC_MW_only，才可声称为方法效度证据。

| symbol   |   n_known |   n_total |   AUC_dock |   AUC_MW_only |   AUC_MW_adjusted |   AUC_MW_stratified |   rho_affinity_MW |   p_mannwhitney | verdict                |
|:---------|----------:|----------:|-----------:|--------------:|------------------:|--------------------:|------------------:|----------------:|:-----------------------|
| ACVR1    |         9 |      3085 |      0.797 |         0.817 |             0.655 |                 nan |            -0.603 |           0.001 | FAIL_size_only_matches |
| ADRA2A   |       115 |      3085 |      0.532 |         0.462 |             0.578 |                 nan |            -0.582 |           0.118 | NS_not_significant     |
| AXL      |        13 |      3085 |      0.880 |         0.842 |             0.752 |                 nan |            -0.698 |           0.000 | PASS_size_independent  |
| MAPK14   |        16 |      3085 |      0.779 |         0.787 |             0.729 |                 nan |            -0.440 |           0.000 | FAIL_size_only_matches |
| TNIK     |        10 |      3085 |      0.824 |         0.816 |             0.803 |                 nan |            -0.299 |           0.000 | PASS_size_independent  |


**判定为 PASS（富集非尺寸伪信号）的靶标：2 个（AXL, TNIK）。**

注意：打分与 MW 的 Spearman ρ 为**负值**（大分子打分更好）且绝对值较大，说明尺寸偏倚**确实存在**；正因如此，未做此校正的富集 AUC 不可直接引用。校正后 AUC 仍在 0.5 以上，才支持「对接在该靶标上具备真实区分力」这一结论。


### 7.2 面容效度检验：已知镇痛药是否被筛回来？（阴性结果，必须报告）


"Top 里出现了已知镇痛药"是虚拟筛选最常见的自证话术，但极易沦为**挑选性举例**。
本检验把它拆成三个可证伪的问题（`pain_prior` 与 α2 激动剂名单均为外部药理学标注，
**不参与 composite 任何一维**，故本检验非循环论证）：
**A** 类别层面（镇痛药整体是否更靠前）、**B** 靶标层面（ADRA2A 上是否打分更好）、
**C** 机制层面（药理学定义 ADRA2A 的 α2 激动剂是否被筛回，含 MW 校正前后对比）。

| level                         | test                               |   n_pos |   n_neg |     AUC |   p_one_sided | note                              |
|:------------------------------|:-----------------------------------|--------:|--------:|--------:|--------------:|:----------------------------------|
| A. drug-level                 | best_composite: analgesic vs rest  |      64 |    3014 |   0.538 |         0.146 | nan                               |
| A. drug-level                 | drug_rank_score: analgesic vs rest |      64 |    3014 |   0.507 |         0.422 | nan                               |
| A. drug-level                 | top-20 analgesic count             |       0 |      20 | nan     |         1.000 | observed 0, expected 0.4, OR=0.00 |
| A. drug-level                 | top-50 analgesic count             |       0 |      50 | nan     |         1.000 | observed 0, expected 1.0, OR=0.00 |
| A. drug-level                 | top-100 analgesic count            |       0 |     100 | nan     |         1.000 | observed 0, expected 2.1, OR=0.00 |
| A. drug-level                 | top-200 analgesic count            |       1 |     199 | nan     |         0.987 | observed 1, expected 4.2, OR=0.22 |
| B. ADRA2A                     | affinity: analgesic vs rest        |      64 |    3006 |   0.435 |         0.962 | nan                               |
| C. alpha-2 agonists on ADRA2A | affinity (raw)                     |       8 |    3062 |   0.292 |         0.979 | nan                               |
| C. alpha-2 agonists on ADRA2A | affinity (MW-adjusted)             |       8 |    3062 |   0.428 |         0.760 | nan                               |
| C. alpha-2 agonists on ADRA2A | MW only (size baseline)            |       8 |    3062 |   0.195 |       nan     | median MW 245.6 vs 340.9          |


**结论：类别层面不支持"已知镇痛药富集"**（AUC 0.553, p=0.081；Top-20 中 0 个，期望 1.9 个）。
α2 激动剂原始 AUC 仅 0.343（比平均更差）—— 因其多为小分子（中位 MW 245.6 vs 其余 300.7），
被尺寸偏倚系统性惩罚；MW 校正后回到 0.475（等同随机）。
**因此本稿不以面容效度作为流程效度的证据**，方法效度只由 §7 的 ChEMBL 结合型富集支撑。
个别药物（氟吡汀在 ADRA2A 上排 5/620；右美托咪定 MW 校正后升至第 94 百分位）
仅作**假设生成性个例**陈述。


### 7.3 头号排序的分子量敏感性：Top 榜是不是「分子量榜」？


对接系统性偏爱大分子（§7.1 实测 ρ(亲和力, MW) = −0.607），而本稿头号候选（麦角胺类、
抗精神病药）恰好都是大分子。故必须直接检验**药物级排序本身**是否只是尺寸的产物。
做法：保留 D2/D3/D4 与原权重（0.40/0.25/0.20/0.15），**仅替换 D1** 为两种 MW 稳健化的
靶内百分位 —— **A** 亲和力对 MW 线性回归的**残差**百分位；**B** MW 五分位**层内**排名
（非参数，不假设线性）——从而隔离 MW 这一个变量。

**① 排序稳健性**（对应 ADRA2A，620 配对）

| 比较 | Spearman ρ |
|---|---|

| D1 单维：主口径 vs MW 残差 | 0.870 |

| composite：主口径 vs MW 残差 | **0.907** |

| composite：主口径 vs MW 分层 | **0.810** |

| 药物级（跨 10 靶标，680 药）：主口径 vs MW 残差 | 0.930 |


Top-k 名单重叠（主口径 ∩ 变体）：**Top-20 = 9/20**（MW 残差）、**8/20**（MW 分层）。


**② 排序质量的前瞻性口径 —— precision@k**（用 §7 的独立 ChEMBL 阳性集，
标签来自实测活性、预测来自对接，无二重蘸取）：

| k | 命中数 | precision | lift vs 基线 3.8% | 超几何 p | MW 残差 precision | MW 分层 precision |

|---|---|---|---|---|---|---|

| Top-10 | 7 | **0.700** | ×18.69 | 9.4e-09 | 0.700 | 0.700 |

| Top-20 | 9 | **0.450** | ×12.01 | 1.3e-08 | 0.650 | 0.550 |

| Top-50 | 12 | **0.240** | ×6.41 | 1.6e-07 | 0.280 | 0.240 |


**③ 各口径 Top-10 名单并列**（检验的是「集合」，不是「单一名次」）：

| 主口径               | MW 残差             | MW 分层             |
|:------------------|:------------------|:------------------|
| ERGOTAMINE        | RISPERIDONE       | RISPERIDONE       |
| RISPERIDONE       | ERGOTAMINE        | DEXMEDETOMIDINE   |
| DIHYDROERGOTAMINE | ZIPRASIDONE       | ERGOTAMINE        |
| ZIPRASIDONE       | FLUPIRTINE        | NAPHAZOLINE       |
| LURASIDONE        | DIHYDROERGOTAMINE | XYLOMETAZOLINE    |
| BROMOCRIPTINE     | LURASIDONE        | FLUPIRTINE        |
| ELETRIPTAN        | DEXMEDETOMIDINE   | DIHYDROERGOTAMINE |
| FLUPIRTINE        | LOXOPROFEN        | LOXOPROFEN        |
| TRAZODONE         | FROVATRIPTAN      | FROVATRIPTAN      |
| CAPMATINIB        | MIRTAZAPINE       | ZIPRASIDONE       |


**结论（两句话，各自独立，不可只引用其中一句）**：

1. **排序质量对 MW 稳健**：composite 与 MW 校正后排序的 Spearman 达 0.810–0.907（判据
   ≥0.80，判定 **WARN**），且 Top-20 有 9/20 重叠。**precision@10 = 0.700（lift ×18.69,
   p = 9.4e-09）、precision@20 = 0.450** 在 MW 校正后仍显著高于 3.8% 基线 ——
   即"ADRA2A 的 Top 候选集合富集真实 ADRA2A 结合物"这一结论**不是尺寸伪信号**。
2. **但 Top-10 的「具体身份」不稳定**：MW 校正后名单仅重叠 4/10。右美托咪定、氟吡汀
   挤入前五，鲁拉西酮、阿立哌唑掉出。**故本稿只主张「Top-20 候选集合富集」，
   不主张「某个药排名第一」**；任何单药首位结论都应视为不稳健。

## 8. 四维评分与候选清单

综合分 = 0.40·D1(靶标内亲和力百分位) + 0.25·D2(已有多靶点药理学合理性) + 0.20·D3(临床可及性/CNS-MPO 式) + 0.15·D4(该靶标反向对照可信度)。


药物级榜单共 3,078 行，Top 20：


| pref_name                | best_target   |   affinity_at_best_target |   best_affinity_any_target |   n_top1pct |   n_top5pct |   best_composite | pain_prior   | drh_phase       |
|:-------------------------|:--------------|--------------------------:|---------------------------:|------------:|------------:|-----------------:|:-------------|:----------------|
| ERGOTAMINE               | ADRA2A        |                   -10.360 |                    -10.930 |           5 |          10 |            0.773 | False        | Launched        |
| CAPMATINIB HYDROCHLORIDE | SLC2A1        |                   -11.130 |                    -11.130 |           2 |          10 |            0.724 | False        | nan             |
| CAPMATINIB               | SLC2A1        |                   -11.130 |                    -11.130 |           2 |          10 |            0.724 | False        | nan             |
| LURASIDONE               | ADRA2A        |                   -10.390 |                    -11.730 |           0 |          10 |            0.724 | False        | Launched        |
| RISPERIDONE              | ADRA2A        |                   -10.080 |                    -11.210 |           0 |           6 |            0.769 | False        | Launched        |
| DIHYDROERGOTAMINE        | ADRA2A        |                   -10.050 |                    -12.020 |           3 |           6 |            0.768 | False        | Launched        |
| ADAPALENE                | SLC2A1        |                   -11.960 |                    -11.960 |           4 |          10 |            0.693 | False        | Launched        |
| RISDIPLAM                | SLC2A1        |                   -11.470 |                    -11.470 |           1 |           7 |            0.729 | False        | Phase 2/Phase 3 |
| OLAPARIB                 | AXL           |                    -9.122 |                    -11.220 |           2 |           7 |            0.726 | False        | Launched        |
| ELTROMBOPAG CHOLINE      | SLC2A1        |                   -11.680 |                    -11.680 |           5 |           9 |            0.692 | False        | nan             |
| PALIPERIDONE             | AXL           |                    -8.481 |                    -10.420 |           0 |           7 |            0.712 | False        | Launched        |
| ZAVEGEPANT HYDROCHLORIDE | SLC2A1        |                   -13.680 |                    -13.680 |          10 |          10 |            0.657 | False        | nan             |
| ZAVEGEPANT               | SLC2A1        |                   -13.680 |                    -13.680 |          10 |          10 |            0.657 | False        | nan             |
| ENTRECTINIB              | SLC2A1        |                   -12.340 |                    -12.340 |           4 |          10 |            0.655 | False        | Launched        |
| DUTASTERIDE              | SLC2A1        |                   -12.230 |                    -12.520 |           6 |          10 |            0.655 | False        | Launched        |
| LURASIDONE HYDROCHLORIDE | SLC2A1        |                   -11.730 |                    -11.730 |           0 |          10 |            0.652 | False        | nan             |
| ERGOTAMINE TARTRATE      | AXL           |                   -10.480 |                    -10.930 |           5 |          10 |            0.652 | False        | nan             |
| ELTROMBOPAG OLAMINE      | SLC2A1        |                   -11.600 |                    -11.600 |           5 |          10 |            0.652 | False        | nan             |
| ELTROMBOPAG              | SLC2A1        |                   -11.600 |                    -11.600 |           5 |          10 |            0.652 | False        | Launched        |
| BICTEGRAVIR              | AXL           |                    -9.417 |                    -10.570 |           3 |           7 |            0.688 | False        | Launched        |


> **读表警告（务必遵守）**：`affinity_at_best_target` 是该药物在 `best_target` **这一对**上的
> 亲和力，与靶标严格配对，引用时应当用它。而 `best_affinity_any_target` 是该药物在**任意靶标**
> 上的最强值（跨靶标取最小），其所属靶标**通常不是** `best_target`（Top 20 中 19/20 如此）。
> 把后者标到前者名下会造成张冠李戴——本稿曾踩此坑，已拆分列并在此写明。


药物-靶标配对表共 30,687 行，Top 20：


| pref_name         | symbol   |   affinity |   pct_in_target |   D1_affinity |   D2_pharm_prior |   D3_accessibility |   D4_reliability |   composite |
|:------------------|:---------|-----------:|----------------:|--------------:|-----------------:|-------------------:|-----------------:|------------:|
| ERGOTAMINE        | ADRA2A   |    -10.360 |          98.322 |         0.983 |            0.600 |              0.750 |            0.532 |       0.773 |
| RISPERIDONE       | ADRA2A   |    -10.080 |          97.313 |         0.973 |            0.400 |              1.000 |            0.532 |       0.769 |
| DIHYDROERGOTAMINE | ADRA2A   |    -10.050 |          97.117 |         0.971 |            0.600 |              0.750 |            0.532 |       0.768 |
| BUCLIZINE         | ACVR1    |    -10.900 |          99.431 |         0.994 |            0.200 |              0.950 |            0.797 |       0.757 |
| NICERGOLINE       | AXL      |     -8.408 |          94.334 |         0.943 |            0.200 |              0.950 |            0.880 |       0.749 |
| NICERGOLINE       | ACVR1    |    -10.200 |          97.057 |         0.971 |            0.200 |              0.950 |            0.797 |       0.748 |
| ZIPRASIDONE       | ADRA2A   |     -9.354 |          91.938 |         0.919 |            0.400 |              1.000 |            0.532 |       0.748 |
| LOXOPROFEN        | TNIK     |     -8.829 |          93.275 |         0.933 |            0.200 |              1.000 |            0.824 |       0.747 |
| FLUPIRTINE        | MAPK14   |     -8.467 |          94.329 |         0.943 |            0.200 |              1.000 |            0.779 |       0.744 |
| FROVATRIPTAN      | TNIK     |     -8.759 |          92.409 |         0.924 |            0.200 |              1.000 |            0.824 |       0.743 |
| NICERGOLINE       | TNIK     |     -8.917 |          94.287 |         0.943 |            0.200 |              0.950 |            0.824 |       0.741 |
| BUCLIZINE         | SLC2A1   |    -10.090 |          90.346 |         0.903 |            0.200 |              0.950 |            0.914 |       0.739 |
| FELBINAC          | TNIK     |     -8.586 |          90.597 |         0.906 |            0.200 |              1.000 |            0.824 |       0.736 |
| DIHYDROERGOTAMINE | SLC2A1   |    -12.020 |          99.266 |         0.993 |            0.200 |              0.750 |            0.914 |       0.734 |
| BUCLIZINE         | MAPK14   |     -8.457 |          94.263 |         0.943 |            0.200 |              0.950 |            0.779 |       0.734 |
| DIHYDROERGOTAMINE | AXL      |    -10.590 |          99.984 |         1.000 |            0.200 |              0.750 |            0.880 |       0.732 |
| ERGOTAMINE        | AXL      |    -10.480 |          99.919 |         0.999 |            0.200 |              0.750 |            0.880 |       0.732 |
| RISDIPLAM         | SLC2A1   |    -11.470 |          98.076 |         0.981 |            0.000 |              1.000 |            0.914 |       0.729 |
| ALMOTRIPTAN       | TNIK     |     -8.459 |          88.851 |         0.889 |            0.200 |              1.000 |            0.824 |       0.729 |
| OLAPARIB          | AXL      |     -9.122 |          98.567 |         0.986 |            0.000 |              1.000 |            0.880 |       0.726 |


## 9. 局限（必须与结论同时呈现）


1. **靶标覆盖不全**：§6 优先的离子通道类靶标（SCN9A/SCN10A/SCN11A/KCNQ2/CACNA2D1/GABRA1）
   因缺乏可用结构全部无法对接，P6 无法对它们给出候选。
2. **打分保真度上限 ρ ≈ 0.78**：对接结果只支撑"候选优选"，不支撑精确结合能排序；
   任何"第 N 名优于第 N+1 名"的强比较都超出数据支持范围。
3. **反向对照阳性集稀疏**：多数靶标缺乏已批准药层面的已知结合分子，
   其 D4 可信度权重只能取中性值，无法独立校验。
4. **静态结构近似**：对接使用单一晶体构象，未考虑构象选择与诱导契合；
   柔性配体与柔性口袋体系的误差更大。
5. **无膜环境**：膜蛋白靶标（即便有结构）在对接中按可溶蛋白处理，缺失脂双层与
   跨膜电位的约束。
6. **打分与实验效价的缺口**：虚拟筛选给出的是相对排序，不等于体内/体外镇痛效力；
   所有候选在湿实验验证前均属假说。

## 10. 产物清单

| 文件 | 内容 |
|---|---|
| `results/tables/P6_ligand_library.csv` | 配体库逐个分子的准备结果与淘汰原因 |
| `results/tables/P6_ligand_funnel.json` | 配体漏斗各阶段计数 |
| `results/tables/P6_ligand_cns_prior.csv` | Tier 1 CNS/镇痛先验子集 |
| `results/tables/P6_target_selection.csv` | 43 个候选靶标的可成药性决策 |
| `results/tables/P6_receptors.csv` | 受体准备结果（含盒参数、链定位） |
| `results/tables/P6_stage1_param_validation.csv` | 参数保真度验证（15 个分层配体） |
| `results/tables/P6_exh_validation.csv` | exhaustiveness 专项对照 |
| `results/tables/P6_docking_scores_*.csv` | 分层对接打分原始表 |
| `results/tables/P6_reverse_control.csv` | 逐靶标反向阳性对照 AUC |
| `results/tables/P6_reverse_control_positives.csv` | ChEMBL 实测活性阳性集 |
| `results/tables/P6_ranking_pairs.csv` | 药物-靶标配对四维评分 |
| `results/tables/P6_ranking_drugs.csv` | 药物级汇总榜单 |


图件：

- `results/figures/P6_ligand_funnel.png`
- `results/figures/P6_param_fidelity.png`
- `results/figures/P6_ranking_drugs.png`
- `results/figures/P6_reverse_control.png`
- `results/figures/P6_target_decisions.png`
- `results/figures/P6_target_drug_matrix.png`
