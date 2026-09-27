# A2 独立评审意见（设计 / 统计视角）

**评审人角色：** A2 — Design / Statistics expert（meta-analysis, machine learning, causal inference）
**评审日期：** 2026-09-27
**稿件（视作首次投稿）：** `reports/MVP_PLOSONE_submission.md`（《Conserved nerve-injury-associated transcriptional response on the DRG–spinal axis…》）
**独立性声明：** 本评审仅依据 `reports/` 下的主稿、补充材料、cover letter、compliance check、STROBE checklist，以及 `results/tables/*`、`scripts/*` 中的原始产物。未读取任何其他评审人、作者回应或任务状态文件。所有数字均按原始输入重新核算。

---

## 0. 总体判断（bottom line）

这是一篇**方法学自律程度高于多数同类计算重分析**的稿件：它主动披露了非独立性、循环性、异质性和对接零结果，并给出了 bulk-only / collapse / 非循环翻译 / 反向阳性对照等多重敏感性分析。在「诚实阴性结果」这一点上值得肯定。

但是，从设计/统计角度，稿件存在 **4 个必须修改的实质性问题**，其中两个是可直接由原始表复算证实的**内部算术不一致**（"211" 基因数、以及 "strict 4/4" 的错标），另外两个是**对证据强度的过度解读**（nerve-injury-specific 结论建立在零精度 CI 上；缺少显式 EPV 声明）。这些问题均可修，不构成立即拒稿（无 DESK-REJECT 触发），但 T1 项不修正将影响结论可信度与可接收性。

**DESK-REJECT 标志：否。** 理由：无学术不端、无不可复现的捏造（所有复算数字与 `results/tables/` 一致）、核心缺陷均为可更正的描述/解释层面问题。

---

## 1. 站得住的地方（Stands up，证据支撑）

**S1. 循环性被正确处理，且非循环翻译检验做得对。**
【证据】稿件第 56 行明确承认 53.9%（7,751/14,390）与 69.5%（2,473/3,556）这两个方向一致率"由循环设计产生……不以 50% 为零假设检验"。我复算 `_R4_nerveinjury_only_summary.json`：`NI_FDR05_AND_NIcons>=0.8` 层 k=2,266 / n=4,899，rate=0.4625，CI[0.4486, 0.4765]，perm_p=0.1396；background `all_measured` 6,779/14,390=0.4711，CI[0.4629, 0.4793]；强 vs 背景风险差 −0.9 pp。与正文 "46.2% vs 47.1%，p=0.14" 完全一致。分母 14,390 与正文一致（早期合并的 14,445 已显式标注为被取代）。
【为什么重要】这是很多"轴一致性"论文会踩的坑；作者不仅没踩，还把 50% 错误零假设替换成了经验置换零假设（5,000 次重标），是真正的统计纪律。

**S2. 敏感性分析框架（bulk-only + collapse + RE）齐备且主体数字可复算。**
【证据】`META_bulkonly_sensitivity_summary.json`：bulk_only_core=2,512，primary_core=4,055，overlap=2,202（=54.3%）。`META_collapse_meta.csv`：retained_fraction=0.9142（3,707/4,055）。我独立复算：primary_core 4,055 行全部满足 `meta_FDR<0.05 & consistency≥0.8`；bulk-only core(FDR<0.05 & consistency≥0.8)=2,512；`primary ∩ bulk-only core`=2,202（=54.3%）；relaxed(≥3/4)=3,587（=88.5%）；collapse 保留 91.4%。三数全部吻合。
【为什么重要】在标题承诺"DRG–spinal axis"而 meta 核心实为 DRG-only 的情况下（见 F5），这套敏感性分析是把"轴"的稳健性边界说清楚的主要依仗，且数字诚实。

**S3. DeLong 在 AUC=1.0 处方差塌缩被识别并标注为"非信息性"。**
【证据】第 158 行（方法）与第 64 行（结果）均声明四个泄漏控制折的 CI 退化为 `[1.0,1.0]`、"作为非信息性报告，而非精度的证据"。我已用 DeLong 方差恒等式验证：AUC=1.0 时 `Q1=1/(2−1)=1, Q2=2·1²/(1+1)=1`，故 `Var=(AUC(1−AUC)+(n₊−1)(Q1−AUC²)+(n₋−1)(Q2−AUC²))/(n₊n₋)=0`，CI 必然为 `[1.0,1.0]` 与 n 无关。作者没有把 `[1.0,1.0]` 当精度吹嘘，统计素养合格。

**S4. 对接零结果的"全库广度 + 反向阳性对照 + MW 校正"三件套是真实的，不是装饰。**
【证据】ADRA2A Tier-1 AUC 0.618 → 全库 0.532（p=0.118），作者明确"non-informative 而非干净的富集"，且对 10 个靶一视同仁、不Privilege 也不排除 ADRA2A（尽管作者声明自己在研基金含 ADRA2A，并说明未影响分析）。这种"诚实阴性"是稿件最大贡献。
【为什么重要】多数虚拟筛选文章止步于 Tier-1，本稿把双 dipping 的假阳性风险正面拆穿，方向正确。

---

## 2. 给作者的问题（Questions for the authors）

1. **"211" 这个数字的来源定义是什么？** 它既不是 relaxed 重叠的补集（4,055−3,587=468），也不是"完全不在 bulk-only meta 中"的基因数（102）。请指明 211 = 哪一类集合的计数，或将其更正为 468（并区分"缺席 102"与"在场但 <3/4 显著 366"）。
2. **GSE278227（n=28, AUC=1.0）折的 CI 是 `[0.9999999999999999, 1.0]`，实质即 `[1.0,1.0]`。** 既然正文说"nerve-injury-specific 结论主要落在 GSE278227 上"，而该折 CI 与 n=6 折一样零宽度，您如何区分"真正的泛化"与"小测试集上的完全分离假象（过拟合指纹）"？是否同意将该结论降级为"候选的 nerve-injury 富集信号"？
3. **EPV 是否应显式声明？** LODO 每折 `n_selected`=139–164 个特征，而测试集 n=6–28。是否同意在正文补一句："这些 AUC 来自严重欠参数化的分类器，仅供候选生成，不可读作预测精度估计"？
4. **严格重叠的真实 K 构成？** 2,202 个重叠基因中 495 个（22.5%）是 K=3（仅 3/4 对比一致），并非正文所称"all four bulk contrasts concordant, 4/4"。您是否接受将标签改为"≥4/4 或 3/3"，或单独报告纯 4/4 重叠（我复算为 1,707）？
5. **主标题的"DRG–spinal axis"是否应弱化？** 六输入 meta 全部为 DRG/DRG 翻译组；脊髓维度由单独的 LODO SC 折与 Visium 提供。是否同意把主标题改为"DRG-centred … with spinal-cord localisation"，把"–spinal axis"保留在副标题？

---

## 3. 我实际核查了什么（文件、命令、复算 vs 稿件、偏差）

### 3.1 读取的文件
- `reports/MVP_PLOSONE_submission.md`（主稿，行 1–251 及方法/讨论）
- `reports/MVP_PLOSONE_supplementary.md`（S5 基因集、对接目标集恢复表）
- `reports/MVP_PLOSONE_cover_letter.md`、`MVP_PLOSONE_compliance_check.md`、`MVP_STROBE_checklist.md`
- `results/tables/META_DRG_axis_CORE_signature.csv`（4,055 核心）、`META_bulkonly_meta.csv`（15,735 行）、`META_bulkonly_sensitivity_summary.json`、`META_collapse_meta.csv`
- `results/tables/P3_lodo_auc_ci_leakage_controlled.csv`、`P3_hub_bootstrap.csv`、`P3_hub_genes.csv`、`P5_hub_lineage_consensus.csv`
- `results/tables/_R4_targetset_bootstrap.json` / `.csv` / `_R4_targetset_bootstrap_resamples.csv`（200 行）
- `results/tables/_R4_nerveinjury_only_summary.json`、`_R4_translation_noncircular.json`
- `results/tables/META_DRG_axis_stouffer.csv`（用于核实 16,552 基因）

### 3.2 复算命令与结果（均用托管 Python `C:\Users\Administrator\.workbuddy\binaries\python\versions\3.13.12\python.exe`，stdlib csv/json）
**权重与 Σw²（核对正文第 44 行 "11.4%"）：**
```
w = sqrt(n_case*n_ctrl/(n_case+n_ctrl))
GSE267799 (12,8)=2.19089; GSE212311 (3,3)=1.22474; GSE278227 (14,14)=2.64575;
GSE241361_DRG (4,5)=1.49071; GSE265957_D4 (2,2)=1.0; GSE265957_D63 (2,2)=1.0
Sigma w^2 = 17.5222 ; translatome 两时间点合计 = (1+1)/17.5222 = 11.41%
```
→ 与正文 "2.00/17.52≈11.4%"、"GSE241361_DRG 12.7%"、"GSE212311 8.6%" 全部吻合。✅

**核心与重叠（核对正文第 44、50 行）：**
- primary core = 4,055（全部满足 `FDR<0.05 & consistency≥0.8`，min consistency=0.8）。✅
- bulk-only core（FDR<0.05 & consistency≥0.8）= 2,512。✅
- `primary ∩ bulk-only core` = 2,202 = 54.3%。✅
- relaxed（FDR<0.05 & consistency≥0.75）= 3,587 = 88.5%。✅
- **`primary − relaxed` = 468；`primary` 完全缺席于 bulk-only meta = 102。** ❌ 与正文"only 211 … are not bulk-significant at all"不符（见 F1）。
- bulk-only core 的 K 构成：K=4 有 1,951，K=3 有 561；overlap 2,202 中 K=4=1,707、K=3=495。❌ 与正文"all four bulk contrasts concordant, 4/4"不符（见 F2）。

**hub–核心重叠 32/35（核对正文第 62 行）：**
- `P3_hub_genes.csv` 的 `in_meta_core` 列：35 行中 True=32、False=3（REG3B、ANKRD1、MEGF11）→ 32/35=91.4%。✅
- 注：任务指向的 `P5_hub_lineage_consensus.csv` 仅含细胞定位，**不含核心归属标志**；正确来源是 `P3_hub_genes.csv`。稿件若引用该 32/35 应指向后者（见 F8）。

**LODO 泄漏控制 AUC/CI（核对正文第 64 行）：**
`P3_lodo_auc_ci_leakage_controlled.csv`：
- GSE278227_1W_ratDRG: AUC=1.0, CI[0.9999999999999999, 1.0], n=28, n_selected=164
- GSE267799_incision: AUC=0.67708, CI[0.3735, 0.9405], n=20, n_selected=142
- GSE241361_mouseDRG: AUC=1.0, CI[1.0,1.0], n=9, n_selected=139
- GSE241361_mouseSC: AUC=1.0, CI[1.0,1.0], n=9, n_selected=150
- GSE212311_CCI: AUC=1.0, CI[1.0,1.0], n=6, n_selected=158
→ 与正文 "nerve-injury folds=1.000；incision=0.677[0.374,0.940]" 一致。✅ 但 GSE278227 的 `[0.9999999999999999,1.0]` 实质为 `[1.0,1.0]`（见 F3）。

**Bootstrap B=200（核对正文第 66 行与 `_R4_targetset_bootstrap.json`）：**
由 `_R4_targetset_bootstrap_resamples.csv`（200 行）复算：
- hub_set_size 中位 43，IQR[41,46]，range[33,60]；jaccard 中位 0.304（IQR[0.259,0.333]）
- dock_eligible_17 平均恢复 8.70（中位 9，min 4，max 13）；P(≥3)=1.000，P(≥5)=0.990
→ 与 JSON 摘要逐项一致。✅ 用法属稳定性分析，未见误用（见 F9）。

**非循环翻译（核对正文第 58 行）：** 见 S1，全部吻合。✅

**基因集 BH（正文第 48 行 q=0.003）：** `META_bulkonly_sensitivity_summary.json` 中 Neuroinflammation/DAM/Complement 的 `perm_p=0.00049975`（=1/2001 分辨率下限），经 18 集 BH 校正得 q=0.003。→ q 值实为 BH 调整后的分辨率下限，**是上界而非精确 q**（见 F7）。

### 3.3 复算发现的关键偏差（汇总）
| 稿件陈述 | 稿件数字 | 我复算数字 | 判定 |
|---|---|---|---|
| 严格重叠 "all four … 4/4" | 2,202 | 2,202 中 495 为 K=3（3/3） | **错标**（F2） |
| "only 211 … not bulk-significant at all" | 211 | 468（补集）/ 102（缺席） | **不一致**（F1） |
| 松弛重叠 88.5% | 3,587 | 3,587 | ✅ |
| bulk-only 核心 2,512 / 54.3% | 2,202 / 54.3% | 同 | ✅ |
| collapse 保留 91.4% | 91.4% | 同 | ✅ |
| 权重 11.4% | 11.4% | 11.41% | ✅ |
| 32/35 hub 在核心 | 32/35 | 32/35 | ✅ |
| LODO AUC/CI | 见上 | 见上 | ✅（但 F3） |
| Bootstrap 中位数 43 / Jaccard 0.304 / P≥5=0.99 | 同 | 同 | ✅ |

---

## 4. 必须修改清单（按严重度排序；T0/T1/T2/T3）

### F1 — 【T1】"211 个基因完全无 bulk 信号"是内部算术不一致
【Problem】正文称 4,055 核心中"仅 211 个完全无 bulk 显著性（translatome 特异性贡献）"，但该数与稿件自身分区不自洽，低估了真实的 translatome 特异性贡献约 2.2 倍。
【Evidence】`META_DRG_axis_CORE_signature.csv`(4,055) 与 `META_bulkonly_meta.csv`(15,735) 复算：`primary ∩ relaxed(FDR<0.05 & consistency≥0.75)`=3,587，故 `primary − relaxed`=**468**；`primary` 完全不在 bulk-only meta 中的基因=**102**。稿件分区 2,202+1,385+211=3,798≠4,055，缺失 257；而正确的补集应为 4,055−3,587=468。211 既不等于 468 也不等于 102，且稿件未给出其定义（submission.md 第 50 行）。
【Why it matters】这直接削弱第 1 个审阅要点（同动物双时间点是否夸大有效样本量）：若真实"无 bulk 支持"的核心基因是 468（11.5%）而非 211（5.2%），则 GSE265957 翻译组对核心的**独特**驱动被低估了一倍多，与"11.4% 方差权重"叠加后，非独立性对核心成员资格的实质影响比正文暗示的更大。
【Specific fix】二选一（推荐前者）：
- 改为："在松弛 ≥3/4 门槛下仍有 **468/4,055（11.5%）** 核心基因无任何 bulk 支持；其中 102 个根本未进入 bulk-only meta（仅在 ≤2 个 bulk 对比中出现），其余 366 个虽进入 bulk meta 但未达 ≥3/4 的 FDR 一致性门槛。这 468 个才是翻译组的真实特异性贡献。"
- 或明确定义 211 为"在 4 个 bulk 对比中**逐一**均不显著（per-contrast FDR≥0.05）的基因"，并补充该定义所需的逐对比显著性来源文件，同时说明其与 468 的关系。

### F2 — 【T1】"strict 4/4" 重叠标签错标，低估了门槛的宽松度
【Problem】正文将 54.3% 严格重叠描述为"all four bulk contrasts concordant, 4/4"，但该重叠实际包含 22.5% 仅 3/4 对比一致（K=3）的基因，并非"全部四个"。
【Evidence】`META_bulkonly_meta.csv`：bulk-only core（FDR<0.05 & consistency≥0.8）共 2,512，其中 K=4=1,951、K=3=561；`primary ∩ bulk-only core`=2,202，其中 K=4=1,707、K=3=**495**。即 495/2,202=22.5% 是 3/3 一致（只出现在 3 个 bulk 对比中），不满足"all four"。submission.md 第 50 行。
【Why it matters】"4/4"措辞让读者以为严格门槛极紧；实际 bulk-only core 定义允许 K=3 基因以 3/3 计入，门槛为"≥4/4 或 3/3"。这夸大了保守边界的严格程度，与 F1 共同让人误判核心对翻译组的依赖程度。
【Specific fix】改为："严格重叠 = primary core ∩ bulk-only core（FDR<0.05 且 consistency≥0.8，即 **4/4 或 3/3**），2,202/4,055=54.3%。其中纯 4/4（K=4 且四对比全一致）为 1,707；其余 495 为 K=3（3/3）。" 或单独报告纯 4/4=1,707 作为最严格下界。

### F3 — 【T1】"nerve-injury-specific" 结论建立在零精度 CI 上，且易被过拟合解释
【Problem】四折"AUC=1.0"的 DeLong CI 均为 `[1.0,1.0]`（含正文称为"主要依仗"的 GSE278227 n=28 折，其 CI 为 `[0.9999999999999999,1.0]`，即 `[1.0,1.0]`）；整条 nerve-injury-specific 证据链实质只由"一个 n=28 的无区间点估计 + 一个 n=6 的设计下限"支撑。
【Evidence】`P3_lodo_auc_ci_leakage_controlled.csv`：GSE278227 n=28 AUC=1.0 CI≈[1.0,1.0]；GSE212311 n=6 AUC=1.0 CI=[1.0,1.0]，正文承认其精确 MW p=0.10（单侧 0.05）为设计下限；GSE241361 DRG/SC n=9 同动物、CI=[1.0,1.0] 被排除于跨动物均值。DeLong 方差在 AUC=1.0 处恒为 0（已用方差恒等式证明），故 CI 必然零宽度——此为完全分离的**数学必然**，与 n 无关。submission.md 第 64 行。
【Why it matters】AUC=1.0 在 n=6/9/28 测试集上、且每折选入 139–164 个特征时，是"高 VR 分类器在小测试集上轻易完全分离"的典型指纹，与"稳健泛化"无法区分。把结论"主要落在 GSE278227 上"却不提供该折任何精度区间，等于把点估计当证据。这会直接抬高评审与读者对"nerve-injury 特异性信号"的信心，而统计上它等价于设计下限 + 过拟合假象。
【Specific fix】将"Honest evaluation confirmed a nerve-injury-specific … LODO signal"降级为："LODO 提示一个**候选的** nerve-injury 富集信号；但跨动物证据仅限于 GSE278227（n=28，点 AUC=1.0，**无可估计 CI**，因 DeLong 在完全分离处方差塌缩）与 GSE212311（n=6，精确 MW p=0.10 即设计下限）。四折 AUC=1.0 的零宽度 CI 与高特征数共同提示其可能反映小测试集上的完全分离而非已验证泛化，故不读作预测精度证据。" 并保留 incision 折 0.677[0.374,0.940]（含机会）作为"既不支持也不反驳"的诚实陈述。

### F4 — 【T1】未显式声明 EPV（事件/参数比）违规
【Problem】稿件提及"small test n""same-animal folds not independent""λ.1se=1 gene"，但从未给出 EPV 比值，也未把分类器显式框定为"候选生成而非校准分类"。
【Evidence】`P3_lodo_auc_ci_leakage_controlled.csv` 的 `n_selected`=139–164，`n`（测试集）=6–28。EPV = 事件数 / 参数数 ≈ 6–28 / 139–164 ≪ 1（约 0.04–0.20）。全文（含 supplementary）无 "EPV"/"events-per-parameter"/"candidate generation" 的显式表述（grep submission.md 仅命中"leakage-controlled""calibrat-ed"等，无 EPV 声明）。submission.md 第 64、66、158 行。
【Why it matters】EPV≪1 是这类高维 ML 的根本局限：即便做了特征选择的外折重算（leakage-controlled），分类器仍严重欠参数化，AUC 不应被读作精度。不声明会让读者把 LODO AUC 当成"模型能区分 nerve-injury vs 其他"的验证，而它只是候选筛选。
【Specific fix】在 Methods（Dual-ML 段）或 Discussion 增补一句："Each LODO fold selected 139–164 features against test sets of n=6–28, giving events-per-parameter ≪1; the LODO AUCs are therefore reported as **hypothesis-generating candidate discrimination, not as estimates of predictive accuracy**, and the 35 hubs are a candidate set for prospective validation." 并把 F3 的降级表述与本条呼应。

### F5 — 【T2】主标题 "DRG–spinal axis" 夸大整合程度（正文已部分补救）
【Problem】主标题承诺"DRG–spinal axis"，但六输入 Stouffer meta 核心全部为 DRG / DRG 翻译组；脊髓维度由单独的 LODO SC 折（GSE241361）与 Visium 空间映射独立提供，并非 meta 轴的产物。
【Evidence】submission.md 第 44 行自陈："The Stouffer meta core is thus a DRG-axis product (all six inputs are DRG or DRG translatome); the spinal-cord dimension … is supplied independently by the LODO spinal fold and the Visium." 但主标题（第 1 行）仍写"on the DRG–spinal axis"。六输入构成见第 44、146 行（GSE267799/GSE212311/GSE278227/GSE241361_DRG/GSE265957 D4/D63，全 DRG）。
【Why it matters】标题是读者第一印象；把"DRG 核心 + 独立脊髓定位"说成"DRG–spinal 轴 meta"会让人误以为脊髓也被同法整合。正文虽诚实，但标题领读仍属过度宣称。
【Specific fix】主标题改为："Conserved nerve-injury-associated transcriptional response in the DRG, with spinal-cord localisation …"；保留副标题中的"honest repurposing null"。或在主标题用 "DRG-centred … axis" 并将 "–spinal" 限定词移至副标题。

### F6 — 【T2/T3】主 meta_Z 把同动物双翻译组时间点当独立，SE 略偏乐观
【Problem】primary FE meta_Z 将 GSE265957 D4 与 D63（同一批 4 只动物、n_eff=4/时间点）作为两个独立对比加权，二者相关但未相关建模；11.4% 方差权重使主 meta_Z 的标准误轻微反保守。
【Evidence】复算 Σw²=17.5222，翻译组两时间点合计 11.41%；`META_bulkonly_sensitivity_summary.json` 标注二者"from the same animals … not statistically independent"。bulk-only/collapse 敏感性绑定的是**成员资格**，不绑定主 meta_Z 的**效应量 SE**。submission.md 第 44 行。
【Why it matters】对核心成员资格影响已由敏感性分析 bound（54.3%/88.5%/91.4%），但主效应量（meta_Z、meta_FDR）的精度被同动物相关性轻微夸大。由于核心结论多读 FDR 与一致性而非点估计精度，实际影响有限，但仍应声明。
【Specific fix】在第 44 行补充："Because the two translatome timepoints are from the same animals, treating them as independent inputs renders the primary FE meta_Z standard error marginally anti-conservative; the practical impact on gene-level membership is bounded by the bulk-only (54.3%) and collapse (91.4%) sensitivities, and gene-level claims remain FE-conditional as stated."

### F7 — 【T3】基因集 q=0.003 实为 BH 调整后的分辨率下限（上界）
【Problem】Neuroinflammation/DAM/Complement 的 q=0.003 由原始置换 p 钉在 0.0005（1/2001 分辨率下限）经 18 集 BH 得到，是上界而非精确 q；正文称 p"reported as an upper bound"但随后把 q=0.003 当作精确值陈述。
【Evidence】`META_bulkonly_sensitivity_summary.json`：三集 `perm_p=0.00049975`；submission.md 第 48 行声明分辨率下限 1/2001≈0.0005 并"reported as an upper bound"，但同段给出"q=0.003"未标注为上界。
【Why it matters】三位点效应量极大（mean_Z +4.94/+3.88/+3.44），结论稳健；但把地板 q 当精确 q 会让人高估集合水平推断的刻度精度。属轻度过度陈述。
【Specific fix】将 q=0.003 改为"q≤0.003（BH 调整后的置换分辨率下限，上界）"，并说明协调轴的结论依赖效应量大小而非 q 的精确刻度；保留"effective number of independent discoveries ≈ 1"的合并表述。

### F8 — 【T3】32/35 核心重叠的标志文件指向偏差（文档小错）
【Problem】任务与读者若按"P5_hub_lineage_consensus.csv"查找 32/35 核心重叠会落空——该文件仅含细胞定位，无核心归属标志；真正的 `in_meta_core` 在 `P3_hub_genes.csv`。
【Evidence】`P5_hub_lineage_consensus.csv` 列：`symbol,n_methods,n_datasets,celltypes,consensus_lineage,confident,mean_enrich,tiers,lineages`（无核心标志）；`P3_hub_genes.csv` 含 `in_meta_core`（32 True / 3 False）。我据此复算 32/35=91.4%，与正文第 62 行一致。
【Why it matters】不影响数字正确性（32/35 已验证），但会误导方法复现者去找错文件。
【Specific fix】在 Methods/Supplementary 明确："hub–meta-core 重叠（32/35）取自 `P3_hub_genes.csv` 的 `in_meta_core` 列"；`P5_hub_lineage_consensus.csv` 仅用于单细胞/空间定位共识。

### F9 — 【T3，已确认无滥用】Bootstrap 用法正确，仅建议补一句分辨率说明
【Problem】Bootstrap（B=200）被用于稳定性分析（中位集大小 43、Jaccard 0.304、dock_eligible_17 平均恢复 8.70、P≥3=1.0、P≥5=0.99），属恰当的稳定性而非显著性检验；未误用。
【Evidence】`_R4_targetset_bootstrap.json` 与 `_R4_targetset_bootstrap_resamples.csv`（200 行）逐项吻合（见 §3.2）。正文第 66 行将其框为"candidate set whose two strongest members are resampling-stable"，定位准确。
【Why it matters】无缺陷；仅提示 B=200 的分位数分辨率约 0.5%（P≥5=0.99 即 200 次中仅 2 次 <5），属可接受。
【Specific fix】可不改；若改，补一句"B=200 下比例估计的分辨率约 0.5%，P(≥5)=0.99 应读作'≥5 的恢复在 ≤2/200 次中失败'"。

### F10 — 【T3，已确认是优势】incision 臂异质性已披露
【Problem】无问题。GSE267799 合并 SMIR+LPI 且把 day-10 与 day-32（Flatters 报告 day-32 已消退）合并为"chronic"，作者已显式标注为保守且异质，并把 incision→nerve-injury 翻译作为单一异质 arm 的保守下界。
【Evidence】submission.md 第 152 行。
【Why it matters】这是透明处理的范例，保留即可。

---

## 5. 结论性建议（给编辑）

- **不拒稿**。核心方法合理、敏感性分析齐备、阴性结果诚实，复算数字（除 F1/F2 外）与主稿一致。
- **T1（必改，修后方可接收）：** F1（211→468）、F2（4/4 错标）、F3（nerve-injury-specific 降级 + 零精度 CI 声明）、F4（显式 EPV 声明）。
- **T2（强烈建议）：** F5（标题弱化）、F6（主 meta_Z SE 反保守声明）。
- **T3（小修）：** F7（q 上界标注）、F8（文件指向）、F9/F10（确认无误）。
- 修回时请作者提供 F1 中 211 的定义来源或采用 468 的更正版，并给出纯 4/4 重叠（1,707）与松弛 88.5% 的并列表，以消除对"核心对翻译组依赖程度"的歧义解读。
