# MVP 论文投稿前新颖性自检报告 (Pre-submission Novelty Check)

- **Scope**: CPSP（慢性术后痛）DRG–脊髓轴多数据集整合 + 双 ML 锁靶 + FDA 全库重定位（诚实阴性）
- **Date**: 2026-09-20
- **Status**: ✅ 完成（基于 6 次 WebSearch 检索 + 项目内 P1–P6 结果交叉核对）
- **配套产物**: `reports/MVP_manuscript_skeleton.md`（Task A）、`results/MVP_FJNSF_V16_consistency_checklist.md`（Task B）

---

## 1. 结论（一句话）

本 MVP 论文的**核心组合贡献**——CPSP 特异的 DRG–脊髓 AXIS 多数据集 Stouffer meta + 双 ML（LASSO+RF+XGBoost ≥2/3）hub 锁定（LODO 跨数据集泄漏控制）+ FDA 全库（3085 药 × 10 靶）预注册诚实阴性重定位 + 反向阳性对照——**未被任何现有文献抢占（not preempted）**。

⚠️ **关键限定**：单个 hub 基因与"神经免疫/OXPHOS"机制本身**不新颖**。新颖性在于「方法学严谨性 + AXIS 整合视角 + 诚实报告阴性重定位结果」三者的组合，而非新基因发现。稿件不得据此过度宣称。

---

## 2. 检索范围（6 次检索）

1. `chronic postsurgical pain SMIR incision model dorsal root ganglion spinal cord single cell transcriptome axis`
2. `dorsal root ganglion spinal cord axis integration chronic pain multi-dataset meta analysis hub genes`
3. `virtual screening drug repurposing full library no enrichment negative result honest null preregistered chronic pain`
4. （前置摘要轮）`chronic postsurgical pain DRG spinal cord transcriptome hub genes machine learning target identification`
5. （前置摘要轮）`FDA drug repurposing chronic postsurgical pain virtual screening molecular docking adipose`
6. （前置摘要轮）`dorsal root ganglion spinal cord axis neuroinflammation oxidative phosphorylation chronic neuropathic pain bioinformatics`

覆盖：PubMed / ScienceDirect / DOAJ / CNKI / IASP-Pain / Acta Pharmacol Sin / 厂商方法学页面。

---

## 3. 相关文献全景（最接近的 7 篇）

| # | 文献 | 模型 / 组织 | 做了什么 | 与本 MVP 重叠 | 关键缺口 |
|---|------|------------|---------|--------------|---------|
| 1 | Xu et al. 2022, *J Pain Res*, PMID 35411184 | 大鼠 SMIR，**脊髓背角(SCDH) 单侧** | RNA-Seq + 生信鉴定 DEG + qPCR 验证 | CPSP 特异 + SMIR 模型 | **仅脊髓**；无 DRG、无 AXIS、无 ML、无重定位 |
| 2 | STAT3/SDF-1 脊髓背角, CNKI 2021 | 大鼠 SMIR，脊髓背角 | 机制（STAT3→SDF-1 启动子募集） | CPSP 特异 | 无组学整合、无 AXIS、无 ML |
| 3 | Heliyon 2024, PMID 38813203 | 大鼠 **CCI**，DRG | RNA-Seq + 已发表数据集整合 + PPI hub 筛选 | DRG hub 基因 + 多数据集整合思路 | **CCI（非 CPSP）**、DRG 单组织、无脊髓轴、无 ML、无重定位 |
| 4 | Pokhilko et al. 2020, *PAIN*, PMID 32107361 | 啮齿 DRG，多神经损模型 | DRG RNA-Seq meta，共同 DEG（内源阿片抑制） | DRG 共同转录签名 | DRG 单组织、神经损（非 CPSP）、无 AXIS、无 ML 重定位 |
| 5 | Sapio & Iadarola, *J Pain* | 外周炎症，脊髓 + DRG | 脊髓/DRG dynorphin/enkephalin RNA-Seq | 同时含脊髓与 DRG 两组织 | **炎症痛（非 CPSP）**、聚焦单一肽家族、无 meta/ML/重定位 |
| 6 | IASP 生信 (GEO DRG microarray ×4) | 大鼠 SNL DRG | co-DEG + PPI hub (SNAP25/VAMP2) + DGIdb 药物基因互作 | DRG hub + 药物-基因互作 | DRG 单组织、microarray、无 AXIS/ML/全库对接 |
| 7 | DrugRep (*Acta Pharmacol Sin* 2022) / DrugPipe (2024) | —（方法学/工具） | 自动化 / 生成式 AI 虚拟筛选服务器 | 重定位方法论 | 通用工具，**非疼痛应用**，无"诚实 null"报告范式 |

---

## 4. 缺口分析（无人覆盖的组合）

- ❌ **CPSP 特异 + DRG 与脊髓"轴"整合**：现有 CPSP 转录组（Xu / STAT3）只做脊髓；做 DRG 轴的多在 CCI/神经损（Heliyon / Pokhilko）且为 DRG 单组织。无人在 CPSP 下把 DRG 与脊髓作为"轴"整合 meta。
- ❌ **双 ML（LASSO+RF+XGBoost ≥2/3）hub 锁定 + LODO 泄漏控制**：疼痛生信多用单 ML 或无 ML（Heliyon 用 PPI degree；IASP 用 PPI）。LODO 跨数据集泄漏控制未见报道。
- ❌ **FDA 全库（3085 药 × 10 靶）预注册诚实阴性重定位 + 反向阳性对照**：现有重定位要么报阳性命中，要么仅为方法学工具（DrugRep / DrugPipe）。**报告"全库口径下无任何靶呈现稳健大小无关富集（ADRA2A AUC 0.532, p=0.118 NS）"作为方法学边界**，在疼痛重定位领域罕见。
- ❌ **神经免疫/OXPHOS 轴重框架（远离离子通道范式）**：文献仍以 Nav1.7/1.8 等通道为主（suzetrigine、PF-05089771）。我们用 35-hub + 神经炎症平均 Z +4.94 / DAM 小胶质 +3.88 / 补体 +3.44 / OXPHOS −2.37，将 CPSP 重框架为"神经免疫–代谢"而非"离子通道重塑"，且离子通道家族未被协同调控（p>0.17）——这是与主流范式对立的诚实结论。

---

## 5. 各贡献轴新颖性判定

| 贡献轴 | 新颖性 | 依据 |
|------|------|------|
| 35-hub 基因签名（个体基因层面） | ⚠️ 低（不新颖） | ATF3 / SPRR1A / VIP / NPY 等在 CCI/DRG 文献已反复出现；**不可作为卖点** |
| CPSP DRG–脊髓 AXIS 整合 meta | ✅ 高 | 无 CPSP 轴整合文献 |
| 双 ML ≥2/3 hub 锁定 + LODO | ✅ 高 | 疼痛生信未见此组合 |
| FDA 全库诚实阴性重定位 | ✅ 高（方法学） | 无疼痛应用报此范式 |
| 神经免疫/OXPHOS 重框架 + 离子通道阴性 | ✅ 中–高 | 与主流离子通道范式对立，且有人源层阴性支撑 |
| Visium 空间定位（Stretch） | ✅ 高 | 当前 MVP 仅含 scRNA；Visium 属 Stretch，投稿时若纳入进一步增强差异化 |

---

## 6. 差异化定位建议

1. **主标题 / 摘要卖点 = AXIS + 方法学严谨 + 诚实阴性**，不是"发现 X 基因"。避免 "novel hub gene" / "first report of X" 等过度措辞。
2. **明确对标 Xu 2022（PMID 35411184）**：强调我们补上了 DRG 侧 + ML hub + 重定位，且为大鼠→小鼠→人源三层验证（Xu 仅大鼠脊髓）。
3. **把诚实阴性重定位写成 "methodological boundary / pre-registered null" 贡献**：这恰是方法学/数据期刊（如目标 *Scientific Reports*）reviewer 欣赏的卖点。
4. **神经免疫/OXPHOS 重框架**作为生物学故事主线，离子通道阴性作为"挑战主流范式"的诚实小节。
5. **ADRA2A 处理**：保持"对接 null ≠ 生物假说被推翻"的平衡表述（已在 skeleton §3.5 / Discussion 落实），与 FJNSF V16 §6.4 一致。

---

## 7. 过度宣称风险（红线）

- 🚫 不得声称 35 个 hub 基因中任一是 "CPSP 新发现基因"——与 CCI/DRG 文献高度重叠。
- 🚫 不得声称 ADRA2A 是"已验证重定位靶点"——全库 AUC 0.532, p=0.118 NS，仅生物假说（FJNSF V16 §6.4 已如此定性）。
- 🚫 不得声称对接打分可"验证靶点生物学"——边界 ρ≈0.78，仅支持候选优先级排序。
- 🚫 人源层（P4）阴性，不得上推到人"无转录组改变"——仅说明鼠源信号未在人源队列复现。

---

## 8. 建议写入稿件的 Novelty Statement（草稿）

> "To our knowledge, this is the first study to (i) integrate DRG and spinal-cord transcriptomes as a single axis in a CPSP (SMIR) model via multi-dataset Stouffer meta-analysis, (ii) lock candidate hub genes with dual-machine-learning consensus under cross-dataset leakage control (LODO), and (iii) report a pre-registered, full-library (3,085 FDA drugs × 10 targets) structure-based repurposing screen that—despite reverse positive controls—found no target with robust size-independent enrichment (ADRA2A full-library AUC 0.532, p = 0.118, NS), establishing an explicit methodological boundary rather than a false-positive hit. The convergent neuroimmune–metabolic (not ion-channel) programme reframes CPSP mechanism away from the dominant channel paradigm."

---

## 9. 参考文献（检索命中，供稿件引用）

1. Xu R, Wang J, Nie H, et al. Genome-Wide Expression Profiling by RNA-Sequencing in Spinal Cord Dorsal Horn of a Rat Chronic Postsurgical Pain Model. *J Pain Res*. 2022;15:985–1001. PMID: 35411184.
2. STAT3/SDF-1 信号通路在大鼠术后慢性疼痛形成中的作用. *CNKI*. 2021. （脊髓背角机制）
3. Neuroinflammation signatures in dorsal root ganglia following chronic constriction injury. *Heliyon*. 2024. PMID: 38813203.
4. Pokhilko A, Nash A, Cader MZ. Common transcriptional signatures of neuropathic pain. *PAIN*. 2020. PMID: 32107361.
5. Sapio MJ, Iadarola MJ, et al. Dynorphin and Enkephalin Opioid Peptides and Transcripts in Spinal Cord and Dorsal Root Ganglion During Peripheral Inflammatory Hyperalgesia and Allodynia. *J Pain*. （脊髓+DRG 双组织）
6. Bioinformatics Study of DEGs in Microarrays of DRG from Rat Models of Neuropathic Pain. IASP Pain Research Forum. （GEO DRG microarray ×4, hub SNAP25/VAMP2）
7. DrugRep: an automatic virtual screening server for drug repurposing. *Acta Pharmacol Sin*. 2022. https://doi.org/10.1038/s41401-022-00996-2
8. DrugPipe: Generative AI-assisted virtual screening pipeline for drug repurposing. *Biomethods*. 2024.
9. Haque T, et al. DRG mitochondrial pyruvate oxidation drives pain. *Pain*. 2024. PMID: 38285538.
10. Dong X, et al. Mouse spinal cord neuropathic pain atlas. *Commun Biol*. 2025.
11. Price TJ, et al. Human cervical DRG atlas. *Brain*. 2026.
12. Suzetrigine (NaV1.8) non-opioid analgesic. *Cleveland Clinic J Med*. 2026. （主流通道范式对照）
13. PF-05089771 (NaV1.7) 重定位背景文献.

---

## 10. 后续动作建议（待用户确认）

- [ ] 将 §8 Novelty Statement 草稿润色后嵌入 skeleton Abstract / Introduction 末段。
- [ ] 若目标期刊要求，补做 1–2 个对标文献的系统性比对表（Xu 2022 vs 本 MVP）放入 Supplementary。
- [ ] 待 Stretch（Visium / MD / 人源 qPCR）数据成熟，可升级为更高新颖性版本再投；当前 MVP 已具备独立可投性。
