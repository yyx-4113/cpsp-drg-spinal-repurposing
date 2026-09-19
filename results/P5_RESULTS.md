# P5 结果 · 单细胞层 hub 定位（DRG 神经元亚型 · 脊髓多谱系 · 脊髓小胶质）

> 生成日期：2026-09-16 ｜ 脚本：`scripts/p5_sc.py`（主流程，通用：`<GSE> <DRG|SC> [样本过滤]`）、`p5_subtype.py`（DRG 神经元亚型细化）、`p5_summarize.py`（判读与假信号剔除）、`p5_microglia_tc.py`（小胶质时程）
> 数据源：GSE216039（小鼠 DRG scRNA）· GSE328175（小鼠腰段脊髓 snRNA）· GSE246288（小鼠脊髓背角 Cd11b+ scRNA）
> 产物：`results/tables/P5_*.csv`、`results/figures/P5_*.png`

---

## 0. 一句话结论

**35 个 hub 不是"单一细胞类型签名"，而是一个跨 DRG-脊髓轴的多细胞程序**：在 DRG 侧，hub 高度集中于 **CCI 诱导的损伤/再生神经元亚型**（可检出的 25 个 hub 中 **20 个**，其中 SPRR1A 在该亚型检出率 98.1%，其它亚型仅 17.8%，富集 17.4 倍）；在脊髓侧，hub 分散于**神经元、小胶质、星形胶质、OPC** 四类，仅 **7/35** 在两个独立数据集上获得**同谱系一致定位**——这本身就是"轴两端分工"的证据，而不是定位失败。

---

## 1. 三个数据集的实验设计（逐条核实，含两处必须剔除的陷阱）

| 数据集 | 真实设计 | QC 后细胞 × 基因 | 细胞类型构成 | 在本层的角色 |
|---|---|---|---|---|
| **GSE216039** | 小鼠双侧 L4-5 DRG，**Pirt-EGFP FACS 神经元富集** scRNA；Sham / CCI-7d × 雄/雌，各 1 只 | 22,063 × 22,086 | Neuron 17,562（79.6%）· Erythrocyte 2,058 · Schwann 1,492 · SatelliteGlia 847 · Immune 73 · Endothelial 31 | DRG 侧 **神经元亚型**定位 |
| **GSE328175** | 小鼠腰段脊髓 **FANS snRNA**；Sham1-3 vs SNI1-3（entrenched 神经病理痛）；**另有 SNI+Transplant1-2 为 hg19 人源移植细胞** | 54,312 × 25,506 | Neuron 46,349 · Oligodendrocyte 5,749 · Microglia 1,017 · Astrocyte 527 · OPC 415 · Fibroblast_Meninges 125 · Ependymal 87 · Endothelial 43 | 脊髓侧**多谱系**定位（唯一 n≥3 的样本级对比） |
| **GSE246288** | 小鼠脊髓背角 (L4-6) **Cd11b+ FACS** scRNA；Sham PID0 / SNI PID3 / PID7 / PID14，**每时间点 1 只** | 14,582 × 17,438 | Microglia 8,501（58%）+ **ambient RNA 伪簇**（Neuron 4,103 等，见 §5） | 脊髓小胶质表达/时程（**仅描述性**） |

### ⚠️ 两个必须写进 Limitations 的陷阱

1. **GSE328175 的 Transplant 两库是 hg19 人源注释**——它们是"人源移植细胞"，与小鼠样本的基因空间不重叠，**绝不能合并**。本层只取小鼠六样本臂。顺带确认 **GSE325938 是同一研究的 Visium 空间配套数据**（同标题、8 样本、物种含人+鼠），留给 P5-Stretch。
2. **GSE246288 用的是全量 10x 条形码白名单**（6,794,880 barcode/样本，绝大多数全零），4 样本合并名义上 27,179,520 个"细胞"，QC 后仅 14,582 个真实细胞（99.95% 被丢弃）。若不在载入时剔除全零列，会直接打爆内存。

---

## 2. DRG 侧：hub 集中在损伤/再生神经元亚型（本层最强结果）

### 2.1 先做细胞类型级定位（GSE216039）

数据集本身是**神经元富集**的（`characteristics: cell type: neuron`），所以"hub 在神经元"几乎无信息量。细胞类型级只给出 16/25 个可定位 hub，且 **ATF3 落在 Schwann（1.030）与 Neuron（1.029）几乎完全并列** → 判为 `broad`（广泛表达）。

> 这个"并列"暴露了一个通用陷阱：**log-normalized 均值随该细胞类型的检出基因数系统性升高**（神经元核中位 6,389 基因 vs 卫星胶质 1,795 基因）。仅比均值会把 ATF3 误判成 Schwann 特异。因此本层判读要求**均值富集与检出率富集同时达标**（见 §4）。

### 2.2 再做神经元亚型级定位（关键设计）

**三条防循环论证（double-dipping）红线：**

1. **亚型注释只用非 hub marker**。Injured_Regen 亚型仅用 `GAL / GAP43 / SOX11 / VGF / MMP16 / CDK5R1 / SCG2 / NCAM1`；脚本硬性剔除任何同时属于 hub 的基因（本次实际剔除 **0 个**，即这 8 个 marker 与 hub 完全不相交，逐条打印留痕）。
2. **hub 来自完全不同的数据集**（bulk：GSE278227 / 267799 / 241361 / 212311），与 GSE216039 的无监督聚类相互独立 → 聚类过程不含 hub 信息。
3. 同时给出**无监督 cluster 级**与**亚型级**两套富集，并做留一 marker 稳健性。

**四个神经元亚型**（Pirt-EGFP 富集数据，共 16 个神经元 cluster）：

| 亚型 | 细胞数 | 判定使用的非 hub marker |
|---|---|---|
| Injured_RegenNeuron | 4,470 | GAL, GAP43, SOX11, VGF, MMP16, CDK5R1, SCG2, NCAM1 |
| Peptidergic_Nociceptor | 4,612 | CALCA, CALCB, TAC1, TRPV1, SST, TACR1, NTRK1, ADCYAP1 |
| NonPeptidergic_Noci | 4,812 | MRGPRD, P2RX3, MRGPRA3, CTNNA2, SLC10A4, RET |
| Myelinated_Proprio | 3,668 | PVALB, RUNX3, NEFH, ETV1, SLC17A6, MAFA |

### 2.3 结果：20/25 可检出 hub 归于损伤/再生神经元亚型

35 个 hub 中 34 个在该数据集中存在（`CRISP3` 缺失），**25 个达到检出门槛**（top 亚型检出率 ≥5% 且均值 >0.05），其中：

| top 亚型 | hub 数 |
|---|---|
| **Injured_RegenNeuron** | **20** |
| Immune | 2（TFE3, AXL） |
| Endothelial | 2（AGRN, WBP1L） |
| SatelliteGlia | 1（TNS3） |

判读分层（仅可检出的 25 个）：**restricted 19 · enriched 6 · broad 0** ——即**没有一个 hub 只是"广泛表达"**。

**代表性富集（top 亚型 vs 其它亚型）：**

| 基因 | 方法数 | 亚型内均值 | 亚型内检出率 | 其它亚型检出率 | log2 富集(均值) | 倍数 |
|---|---|---|---|---|---|---|
| **SPRR1A** | 3 | 3.091 | **0.981** | 0.168 | 4.11 | **17.4×** |
| **ATF3** | 3 | 2.470 | **0.994** | 0.523 | 1.81 | 3.5× |
| FLRT3 | 2 | 1.354 | 0.972 | 0.258 | 3.12 | 8.8× |
| CHL1 | 2 | 1.321 | 0.938 | 0.420 | 1.97 | 3.9× |
| TNIK | 2 | 1.047 | 0.951 | 0.344 | 2.47 | 5.6× |
| **ECEL1** | 2 | 0.989 | 0.879 | 0.054 | 4.65 | **25.7×** |
| CTTN | 2 | 0.918 | 0.960 | 0.512 | 1.47 | 2.8× |
| SLC2A1 | 2 | 0.486 | 0.864 | 0.302 | 1.48 | 2.8× |
| ANKRD13B | 2 | 0.485 | 0.876 | 0.337 | 1.71 | 3.3× |
| SRRM4 | 2 | 0.417 | 0.835 | 0.250 | 2.20 | 4.7× |
| **NPY** | 2 | 0.380 | 0.436 | 0.037 | 3.29 | **10.0×** |
| **FLNC** | 2 | 0.385 | 0.527 | 0.047 | 3.32 | **10.2×** |
| ACVR1 | 2 | 0.248 | 0.653 | 0.231 | 1.42 | 2.7× |
| VASH2 | 2 | 0.139 | 0.482 | 0.076 | 2.67 | 6.6× |
| ITPKC | 2 | 0.152 | 0.516 | 0.097 | 1.98 | 4.0× |

（完整表：`results/tables/P5_GSE216039_DRG_hub_finetype_top.csv`）

**ATF3 的两级结论并不矛盾**：在细胞类型级它是 `broad`（神经元与 Schwann 并列），在神经元**亚型**级它是损伤亚型高度特异（亚型内检出率 99.4% vs 其它 52.3%）——正确的表述是"**ATF3 由损伤神经元与去分化 Schwann 共同表达；但在 DRG 神经元内部，它标记损伤/再生亚型**"。这正是先做粗定位、再做亚型细化的价值。

### 2.4 亚型划定的稳健性（留一 marker）

逐个剔除 Injured_Regen 亚型的单个注释 marker 后重算划分：

| 剔除的 marker | cluster 划分一致率 | 与全量得分的 Spearman ρ | Injured cluster 数（基线 3） |
|---|---|---|---|
| GAL | 0.96 | 0.985 | 4 |
| GAP43 | 1.00 | 0.983 | 3 |
| SOX11 | 1.00 | 0.995 | 3 |
| VGF | 0.92 | 0.988 | 5 |
| MMP16 | 1.00 | 0.996 | 3 |
| CDK5R1 | 1.00 | 0.965 | 3 |
| SCG2 | 1.00 | 0.970 | 3 |
| NCAM1 | 1.00 | 0.980 | 3 |

→ **一致率 92–100%、ρ 0.965–0.996**：损伤/再生亚型不是靠某一个 marker 撑起来的。
（`results/tables/P5_GSE216039_DRG_subtype_marker_LOO.csv`）

---

## 3. 脊髓侧：hub 分散在神经元 / 小胶质 / 星形胶质 / OPC

GSE328175 是唯一有功效的样本级对比（Sham n=3 vs SNI n=3）。QC 后 54,312 个核、25,506 个基因。**MEG3 / SNHG11 这类泛核 lncRNA 已从 Neuron marker 中移除**（否则会系统性抬高所有核的神经元得分）。

33/35 个 hub 在本数据集存在（`CRISP3`、`REG3B` 缺失），24 个可检出，**16 个可定位**：

| 基因 | 方法数 | top 细胞类型 | 均值 | 检出率 | log2 富集(均值) | log2 富集(检出率) | ambient_index |
|---|---|---|---|---|---|---|---|
| TFE3 | 3 | **Microglia** | 0.286 | 0.198 | 2.45 | 1.69 | 0.62 |
| GALNS | 3 | Neuron | 0.153 | 0.229 | 1.57 | 2.30 | 0.43 |
| **MEGF11** | 2 | **OPC** | 1.888 | 0.851 | 4.67 | 3.86 | 0.51 |
| SRRM4 | 2 | Neuron | 0.754 | 0.670 | 3.27 | 3.18 | 0.31 |
| VASH2 | 2 | Neuron | 0.082 | 0.151 | 2.77 | 3.22 | 0.24 |
| CHL1 | 2 | **Astrocyte** | 1.853 | 0.884 | 2.61 | 1.94 | 0.43 |
| WDR81 | 2 | Microglia | 0.110 | 0.077 | 2.02 | 1.31 | 0.87 |
| ANKRD13B | 2 | Neuron | 0.150 | 0.247 | 1.91 | 2.60 | 0.41 |
| RNF19B | 2 | Microglia | 0.218 | 0.150 | 1.76 | 1.02 | 0.60 |
| MAPK14 | 2 | Microglia | 0.867 | 0.504 | 1.38 | 0.79 | 0.60 |
| TNIK | 2 | Astrocyte | 2.612 | 0.972 | 1.30 | 0.78 | 0.53 |
| FLRT3 | 2 | OPC | 0.208 | 0.190 | 1.29 | 1.04 | 0.36 |
| CTTN | 2 | Neuron | 0.244 | 0.375 | 0.95 | 1.72 | 0.36 |
| WBP1L | 2 | Microglia | 0.389 | 0.262 | 0.93 | 0.44 | 0.74 |
| PTPN23 | 2 | Neuron | 0.147 | 0.244 | 0.87 | 1.80 | 0.49 |
| RUBCN | 2 | OPC | 0.464 | 0.361 | 0.71 | 0.52 | 0.54 |

**被降级、不计入结论的三类（可审计清单见 `P5_hub_localisation_dropped.csv`）：**

| 类别 | 基因 | 原因 |
|---|---|---|
| `ambient_caution` | **ATF3**（2.59）· **AXL**（3.11）· TNS3（1.77） | ambient_index > 1.5，即最空的 10% 核比全局高 1.8–3.1 倍 → 细胞归属不可采信 |
| `rare_compartment` | SLC2A1（Endothelial, 43 核）· AGRN（Endothelial, 43）· FLNC（Ependymal, 87）· CCDC160（Ependymal, 87） | 落在 <135 核的小簇。**方向可信但样本量不足**：SLC2A1→内皮正是生物学正确结论，故保留指派、标注为"罕见区室"而非丢弃 |
| `broad` | MAPK14 之外的弱富集项（1 个） | 富集不足 1.5 倍 |

> **ATF3 在脊髓 snRNA 中 ambient_index = 2.59**，即它的"小胶质信号"很可能是**环境 RNA**（ATF3 在 DRG 高丰度，且脊椎管内解剖相邻）。同一逻辑下 AXL 的脊髓定位也被降级。这类判读若不写出来，会变成假阳性。

---

## 4. 跨数据集谱系一致性（Hub 定位主结论表）

只让**横跨多谱系**的两个数据集（GSE216039 DRG + GSE328175 脊髓）参与共识；GSE246288 是 Cd11b+ 单谱系数据，纳入共识会**人为制造 Mixed（假不一致）**，故单列。

判读分层定义（**先验设定，不随数据调参**）：

| tier | 条件 | 含义 |
|---|---|---|
| `restricted` | log2 富集(均值) ≥ 1.0 **且** log2 富集(检出率) ≥ 0.58 | 细胞类型特异 |
| `enriched` | log2 富集(均值) ≥ 0.58 | 有富集但不严格 |
| `broad` | 富集 < 1.5 倍 | 广泛表达，不做定位声明 |
| `undetected` | top 均值 ≤0.05 或检出率 <5% | 该数据集中近乎不表达 |
| `rare_compartment` | top 落在小簇 | 方向可信、功效不足 |
| `ambient_caution` | ambient_index > 1.5 | 环境 RNA 主导，归属不可信 |

**结果：**

| 谱系 | hub 数 | 基因 |
|---|---|---|
| **Neuronal**（两数据集一致） | 5 | ANKRD13B · CTTN · PTPN23 · SRRM4 · VASH2 |
| **Immune**（两数据集一致） | 1 | **TFE3** |
| **Glial**（两数据集一致） | 1 | CHL1 |
| Mixed（谱系不一致） | 5 | FLRT3(Neuron\|OPC) · MAPK14(Microglia\|Schwann) · RNF19B(Microglia\|Neuron) · RUBCN(Neuron\|OPC) · TNIK(Astrocyte\|Neuron) |
| 单数据集可定位 | 8 | GALNS · SPRR1A · AXL · ECEL1 · MEGF11 · TNS3 · WBP1L · WDR81 |
| **NotLocalisable** | 15 | ATF3 · CDHR5 · ACVR1 · AGRN · ANKRD1 · CCDC160 · CRISP3 · FLNC · ITPKC · LNP1 · NPY · REG3B · SERPINE1 · SLC2A1 · VIP |

**必须点明的三条：**

1. 只有 **7/35** 在两个独立数据集上得到同谱系一致定位。**这不是失败**——它是"DRG-脊髓轴两端分工"的直接证据：DRG 侧的枢纽是损伤神经元程序，脊髓侧的枢纽分散在神经元/小胶质/星形胶质/OPC。若强行要求单细胞类型归属，反而会掩盖这一点。
2. **TFE3 是唯一跨数据集一致定位到免疫谱系的 hub**，且它同时是 3 方法 hub。
3. NPY 与 SPRR1A 在 DRG 亚型级高度特异，却在脊髓侧 `NotLocalisable`/单数据集——符合"它们是 DRG 侧损伤程序、并非脊髓驱动因素"的预期。

---

## 5. 脊髓小胶质（GSE246288）：诚实的弱结果 + 一个必须剔除的伪簇问题

**伪簇问题**：本集是 **Cd11b+ FACS 分选**的背角细胞，理论上只含小胶质/巨噬。但无监督聚类"找到"了 Neuron 4,103 / Oligodendrocyte 1,045 / OPC / Pericyte / Ependymal / Astrocyte 等簇——**这是 ambient RNA 造的伪簇**：本集 HVG 头部是 `S100A8 / S100A9 / RETNLG / MKI67 / TOP2A / HIST1H1B`（纯髓系+增殖特征），且这些"其它细胞"的 marker 得分 margin 普遍 <0.5。**因此本集的跨细胞类型定位结论全部作废**，只保留小胶质内部的时间趋势。

**小胶质表达 / 时程（每时间点 1 只，纯描述性，不做任何检验）：**

- 27 个存在的 hub 中 **14 个在小胶质中可检出**（global mean >0.05）。
- **无时间趋势**：13 个 `flat`、1 个 `down`（PTPN23, ρ=−1.0）、0 个上调（|Δ(PID14−PID0)| > 0.10）。
- 两个有信息量的点：**TFE3 全程高表达**（0.686–0.811，与 §4 的 Immune 一致定位互证）；**AXL 在 PID3 达峰**（0.043 → **0.141** → 0.121 → 0.087），即损伤后 3 天诱导、随后回落。

> 这符合该研究自身的发现逻辑：小胶质在 PID3→7 发生**亚群**转变（pro-inflammatory → pruning），而全小胶质 pseudobulk 会把这个转变平均掉。**本层不宣称任何小胶质亚群结论**；亚群级分析超出本层范围（且 n=1/时间点从统计上就不允许推断）。
> 表：`results/tables/P5_GSE246288_microglia_timecourse.csv`

---

## 6. 样本级统计（pseudobulk）：两集均无 BH 显著

| 数据集 | 对比 | 细胞类型数 | 每组样本数 | 检验基因数 | **BH<0.05** |
|---|---|---|---|---|---|
| GSE216039 | CCI-7d vs Sham | 5（Erythrocyte/Immune/Neuron/SatelliteGlia/Schwann） | 2 vs 2 | 34 | **0** |
| GSE328175 | SNI vs Sham | 6（Astrocyte/Fibroblast_Meninges/Microglia/Neuron/OPC/Oligodendrocyte） | 2–3 vs 2–3 | 33 | **0** |

**这是设计层面的必然，不是意外**：每细胞类型仅 2–3 个样本、仅 33–34 个基因做 BH 校正，功效极低。按 §4 统计铁律，**本层所有定位结论一律标注为"方向提示"，不写成确证**。真正有功效的样本级推断在 P2 的 bulk 层（n=6–62/对比）。

---

## 7. 本层局限（直接进 Limitations）

1. **无功效**：所有单细胞对比 n=2–3/组，BH 后 0 显著；定位只是方向提示。
2. **GSE216039 神经元富集** 由 FACS 造成 → 胶质/免疫区室被系统性稀释（Immune 仅 73 细胞、Endothelial 31），这两类的定位在本集**不可信**，已由 min_cells 门与 rare_compartment 标注处理。
3. **GSE328175 的 Neuron 占比 85.3%**（神经元核 RNA 含量约为胶质核 2.5 倍）→ 神经元基因的 log-norm 均值被系统性抬高，故必须用"均值+检出率双门"判读；且本集**不含** SNI+Transplant（人源注释）与 GSE325938 Visium（留给 Stretch）。
4. **ambient RNA**：ATF3/AXL/TNS3 在脊髓 snRNA 的归属已降级；GSE246288 的非小胶质簇全部作废。
5. **跨物种/跨模型**：hub 来自大鼠+小鼠 bulk，本层为小鼠；人源相应细胞类型未验证（P4 已诚实报告人源层阴性）。
6. **单细胞级差异表达一律未做推断**（规避伪重复）。细胞级统计只作描述。

---

## 8. 产物清单

**表（`results/tables/`）**

| 文件 | 内容 |
|---|---|
| `P5_hub_lineage_consensus.csv` | **主结论表**：35 hub × 谱系一致性 + confident 标记 |
| `P5_hub_localisation_summary.csv` | 94 行逐数据集定位明细（含全部诊断列） |
| `P5_hub_localisation_dropped.csv` | 49 行被降级/剔除明细（可审计） |
| `P5_GSE216039_DRG_hub_finetype_top.csv` | DRG 亚型级 top（含检出门槛与 tier） |
| `P5_GSE216039_DRG_neuron_subtype_scores.csv` | 25 cluster × 4 亚型得分与指派 |
| `P5_GSE216039_DRG_subtype_marker_LOO.csv` | 亚型划定留一稳健性 |
| `P5_GSE216039_DRG_hub_localisation_by_cluster.csv` | cluster 级 hub 富集（无监督层） |
| `P5_GSE216039_DRG_pseudobulk_stats.csv` / `P5_GSE328175_SC_ShamSNI_pseudobulk_stats.csv` | 样本级 Welch + BH |
| `P5_GSE246288_microglia_timecourse.csv` | 小胶质 hub 时程（描述性） |
| `P5_*_cluster_annotation.csv` / `P5_*_celltype_composition.csv` / `P5_*_cellmeta.csv.gz` | 注释、构成、逐细胞元数据 |

**图（`results/figures/`）**

| 文件 | 内容 |
|---|---|
| `P5_hub_lineage_consensus.png` | A 逐数据集 top 谱系热图（粗体=两数据集一致）；B 共识谱系条形图 |
| `P5_GSE216039_DRG_subtype_localisation.png` | A cluster 级富集；B 亚型级富集；C hub top 亚型分布 |
| `P5_GSE216039_DRG_localisation.png` / `P5_GSE328175_SC_ShamSNI_localisation.png` / `P5_GSE246288_SC_localisation.png` | 各数据集 UMAP + hub 富集 |
