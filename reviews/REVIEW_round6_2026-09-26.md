# 编辑合并评审报告 · Round 6（2026-09-26）

**稿件：** "Conserved nerve-injury-associated transcriptional response on the dorsal root ganglion–spinal axis: non-predictive incision translation and an honest repurposing null"
**目标期刊：** PLOS ONE（Research Article，观察性生信再分析）
**稿件版本：** `reports/MVP_ScientificReports_submission.md`（当前已按 PLOS ONE 格式改投，脱胎于被 Scientific Reports 拒稿的版本）
**评审性质：** 独立多专家同行评审（enforced-independence；各专家视为首次投稿，未读任何既往评审/回复/修订文件）
**评审团：** A1 Domain（疼痛/神经科学临床科学家）· A2 Design（设计/统计/ML 泄漏/富集方法）· A3 Implementation（数值溯源审计）· A4 Venue（PLOS ONE 政策与报告标准）
**编辑裁决：** 由主审编辑（我）对三项最严重发现做了独立复核（见 §2 裁决表）

---

## 0. 独立性声明与裁决纪律

四个专家层**未**读取任何 `REVIEW_*.md` / `RESPONSE_*.md` / `REVISION_*.md`、`reviews/round2_*/round4_*/round5_*/` 文件夹、`PROJECT_PLAN.md`、`SUBMISSION_MANIFEST.md`、`GITHUB_DEPOSIT_SOP.md`、`author_verification_statement.md`，也未互读彼此的报告。所有定量判断均直接重算自 `results/tables/` 原始表，稿件自我申报的数字一律作为"待验证断言"而非证据。

输出契约（四要件）：每条发现均含 **【Problem】/【Evidence】/【Why it matters】/【Specific fix】**。本合并报告在四专家发现之上，叠加编辑独立复核与分级裁决。

**总评：** 本稿的方法学纪律（随机效应敏感性、非循环翻译检验、bootstrap 稳定性审计、前瞻性指定的全库对接零富集）是该领域罕见的高标准。四专家 11 个数值族重算中 **10/11 精确吻合**，唯一实质数值问题为**翻译分母跨文件不一致**（provenance，非算术错误）。稿件**不存在致命科学缺陷**；待修项集中在 (a) 生物学/临床叙事的过度框定、(b) 一处未披露的 LR↔Wald 矛盾、(c) PLOS ONE 行政合规闸门。建议 **Major Revision** 后重投。

---

## 1. 评审团构成与裁决纪律

| 专家 | 层 | 核心判定 |
|---|---|---|
| A1 Domain | 疼痛/神经科学临床科学家 | 8 条发现 + 7 项 Stands-up；聚焦钠通道反向的文献对话、DAM 细胞身份、诚实零的靶标清单 |
| A2 Design | 设计/统计/ML | F1–F12；验证 Stouffer 权重、D-L 内部一致性、非循环检验、对接诚实零均精确；F10 指出 ACVR1 LR↔Wald 矛盾 |
| A3 Implementation | 数值溯源 | 11 个数值族重算，10/11 精确；F1 翻译分母不一致；F2 SCN bulk 表未交付 |
| A4 Venue | PLOS ONE 政策 | F1–F10；AI 披露不合规、数据仅 GitHub、伦理笼统、缺 STROBE、悬挂 Reporting Summary |

---

## 2. 裁决表（编辑独立复核 —— 最关键三项）

| # | 专家主张 | 编辑独立复核（重算/查源） | 裁决 |
|---|---|---|---|
| R-1 | **A1-F7**：McDonnell 2018 (ref 25) 未被引用，是"悬挂参考文献"（floating reference） | 对 `MVP_ScientificReports_submission.md` 全文 grep：正文 **line 107** 出现上标 `²⁵`（"…clinical efficacy has been limited²⁵"），**line 187** 为 ref 25 条目；源文件 `_v15_source.md` line 107 含 `{{mcdonnell2018}}`。A1 因用 `[25]`/`²⁵` 字面模式检索、漏检上标数字而误判 | **推翻（OVERRULED）**：引用确实存在。保留其有效子点——(i) 缺 Nav1.7/1.8 人类遗传学 + 临床失败文献（Yang 2004、Cox 2006、Fertleman 2006/2007、Eagles 2022、Faber 2023 vixotrigine）；(ii) 缺"老药新用万能药"/对接混杂批判文献（Pushpakom 2019、Irwin & Shoichet 2016）；(iii) DAM/补体痛觉主张应主要锚定 refs 13/19/20（Tansley 2022、Inoue 2018、Coull 2005）而非 Schafer 2012（ref 15，发育性小胶质细胞论文）。**注意**：A1-F3 的修订建议中"补 (McDonnell 2018, ref 25)"已冗余，勿重复添加 |
| R-2 | **A2-F10**：ACVR1 多元逻辑模型的 LR p=9.6e-4 与同模型亲和力 Wald p=0.172 矛盾未披露，n_pos=9（EPV≈1） | 复核 `P6_multivariate_physchem_control.csv`：ACVR1 行 `LR_dock_residual_p=0.0009567`、`Wald_neg_aff_p=0.1718236`、`n_pos=9` —— 与 A2 一致 | **确认（CONFIRMED）**：属真实未披露的内部矛盾。Tier 1，须补披露或将其移出"显著判别"列表 |
| R-3 | **A3-F1**：翻译分数分母跨文件不一致（Stouffer/NI 14,390 vs translation 文件 14,445，差 ~55 基因） | 复核两源文件：Stouffer 文件 + `_R4_nerveinjury_only_summary.json` 存 14,390/3,556；`_R4_translation_noncircular.csv` 存 14,445/3,564。两文件各自算术正确 | **确认但降级**：非印刷错误，是跨文件溯源口径不一致。归 Tier 2 provenance 修复 |

编辑复核**未**发现专家报告之外的额外错误。

---

## 3. 交叉验证表（≥2 位专家独立重算，全部精确吻合）

| 数值族 | 数值 | 复核方 | 结论 |
|---|---|---|---|
| Stouffer 权重 | 2.1909 / 1.2247 / 2.6458 / 1.4907 / 1.00 | A2-F1, A3 | 精确 |
| SCN8A/SCN9A bulk meta_Z | −4.923567 / −2.924735 | A2-F1, A3 | 精确 |
| 主分析 FE core / meta_FDR<0.05 / 基因测试数 | 4,055 / 6,869 / 16,552 | A2, A3 | 精确 |
| 随机效应 core / 中位 τ² / 中位 I² / I²>50% / τ²>0 | 1,008 / 0.2324 / 38.8% / 41.9% / 68.1% | A2-F5, A3 | 精确 |
| bulk-only core / 重叠 | 1,981 / 1,732÷4,055=42.7% | A2-F4, A3 | 精确 |
| 非循环翻译 | 背景 47.1%；NI 46.3%（−0.9pp, p=0.14） | A2-F6, A3 | 精确 |
| 基因集 BH | neuroinflammation/complement/DAM q=0.0030；OXPHOS 固定 0.020 / 随机 0.31 | A2-F7, A3 | 精确 |
| hub bootstrap | 最高 0.155（CDHR5）；0/35 ≥0.9；lasso_freq 全 0 | A2-F8, A3 | 精确 |
| 对接 | 反向对照 AUC（AXL 0.880/TNIK 0.824/ACVR1 0.797/MAPK14 0.779/ADRA2A 0.532）；广度 0.618→0.532 (p=0.118)；BH-q；face validity 0/64 | A2-F9, A3 | 精确 |
| 参考文献 | 26 条全部带 DOI 且正确 | A3, A4-F8 | 精确 |

**结论：** 量化装置实质无懈可击（唯一例外为 R-3 的 provenance 口径）。这是本稿最强资产，修订时不得改动已验证数字。

---

## 4. 分级问题清单（Tier 0–3）

### Tier 0 —— 行政退稿/送审前退回风险（PLOS ONE 闸门，须投前清零）

> 标记 **[DESK-REJECT-RISK]** 者为 PLOS ONE 主动执法项，不满足会被编辑部在送审前退回补正（非科学否决）；标 **[REVISE-BEFORE-REVIEW]** 者为大概率技术核查问询。

- **[DESK-REJECT-RISK] A4-F1｜AI 使用披露不合规**：当前披露仅写"a large language model (LLM) was used…"，未具名工具、未说明如何验证 AI 输出 —— 违反 PLOS ONE 生成式 AI 政策（须含工具名 + 用途描述 + 有效性验证 + 受影响部分）。**必修**。替换 line 154 为具名版本（如 `ChatGPT (OpenAI, GPT-4o)` 或 `Claude (Anthropic)`），并加"所有 AI 生成文本经作者对照结果表逐条核对、编辑；AI 未用于生成/筛选/解释数据"。
- **[REVISE-BEFORE-REVIEW] A4-F2｜处理数据仅存 GitHub，无 DOI 永久存档**：数据可用性仅给 GitHub tag v1.0.0，PLOS ONE 偏好 DOI 永久仓储（Zenodo/figshare/Dryad）。建议将 v1.0.0 release 镜像至 Zenodo 取得版本化 DOI 并写入 DAS；DAS 内显式列出 12 个 GEO 登录号（勿仅"见 Methods"）。
- **[REVISE-BEFORE-REVIEW] A4-F3｜伦理声明笼统**：未引用唯一人源数据集 GSE158825（n=60）的原始 IRB/同意书依据。补一句："For GSE158825 (human plasma miRNA, n=60), the original deposition documents IRB approval and informed consent; we reanalysed de-identified data and required no further approval." 动物数据集注明原始 IACUC 文档在各自 GEO 条目。
- **[REVISE-BEFORE-REVIEW] A4-F6｜缺报告指南清单**：GSE158825 人源血浆 miRNA 关联属观察性分析，PLOS ONE 大概率要求 STROBE 清单。上传完成版 STROBE checklist 作 Supporting Information（注明此为公共去标识队列的二次再分析，原始数据溯源标注"N/A — source in GEO"）。
- **A4-F5｜悬挂"Reporting Summary"引用**：line 154 写"as stated in the Reporting Summary"——这是 Nature/SR 残留，PLOS ONE 无此结构。直接删除该短语（信息已内联），或改为"as specified in the Statistical discipline paragraph above"。

### Tier 1 —— 重大科学叙事/透明度（修订必改）

- **A1-F1｜Abstract & Author Summary 残留 CPSP 过度框定**：标题/正文已改为"nerve-injury-associated, not CPSP-specific"，但 Abstract 开篇仍以 CPSP 立论、Author Summary 全程称 CPSP 而未给再框定。补一句明确"4/5 轴研究为神经损伤模型、仅 1 个切口模型，故框定为神经损伤相关而非 CPSP 特异；切口臂仅作翻译检验单独分析"。
- **A1-F2｜"neuroimmune–metabolic" 过度强调 OXPHOS，DAM 细胞身份未解**：OXPHOS 仅固定效应显著、随机效应 q=0.31 未过关；"DAM-like microglial" 在混合 bulk 组织（含驻留小胶质 + 浸润巨噬细胞）中无法区分细胞来源。将 "DAM-like microglial" 改为 "DAM-like neuroimmune"，并加一句说明该基因集信号是 bulk 推断、不能特异归因于驻留小胶质。
- **A1-F3｜钠通道反向的文献对话不足**（最悖于文献、临床负荷最重的发现）：SCN8A meta_Z −4.92 (FDR 1e-5)、四通道在唯一切口模型反向为上调。当前仅引 Ding 2019 (Nav1.6)。**须**补充 Nav1.7/1.8/Nav1.9 在损伤 DRG 伤害感受器蛋白/功能上调、人类 SCN9A 功能获得突变致痛（Yang 2004、Cox 2006、Fertleman 2006/2007）、选择性 Nav1.7/Nav1.8 阻断剂临床反复失败（McDonnell 2018 已引；另 Faber 2023 vixotrigine、Eagles 2022）的文献；并说明 bulk 下调可能反映神经元丢失/萎缩或非神经元室，而非否定神经元 Nav 上调。**勿重复添加 McDonnell**（已引）。
- **A1-F4｜"诚实零"靶标表混列无关蛋白**：SLC2A1/GALNS/VASH2/ITPKC 稿件自承"no analgesic link"却与 6 个候选并列。将 Table 3a 拆为"6 个生物学合理候选（ADRA2A/MAPK14/AXL/TNIK/ACVR1/SERPINE1；SLC2A1 有新兴 DRG-代谢依据）+ 4 个仅因有配体锚定 holo PDB 而纳入的可及性/阴性对照（GALNS/VASH2/ITPKC）"；诚实零结论适用于全部 10 个，但仅 6 个作假设生成器。
- **A1-F5｜CDHR5 作为并列候选（最可疑假阳性）**：肠上皮钙黏蛋白、无 DRG/痛觉角色，却达三法共识且是 bootstrap 最稳定 dock-eligible hub (15.5%)。将其从候选短名单与 dock-eligible 集**排除/降为 watch-list 异常值**，待正交确认。
- **A1-F6｜转化路线图夸大血可及性**：TFE3（核转录因子）、AXL（小胶质/免疫）作"blood-accessible"过度。改为仅 PBMC mRNA 或可溶/分泌因子（NPY/VIP 神经肽、SERPINE1/PAI-1）适合作血浆 qPCR/ELISA；核转录因子/小胶质标记仅为弱血标志物；强调 CSF 与人 DRG/神经瘤组织才是机制一致验证，**血浆是低产替代**（人 miRNA 层 p=0.51 已示警）。
- **A1-F7（保留子点）｜补 repurposing-panacea/对接混杂批判文献 + DAM 锚定修正**：Discussion "corrects the 'repurposing panacea' narrative" 处补 Pushpakom 2019 (Nat Rev Drug Discov)、Irwin & Shoichet 2016；DAM/补体痛觉主张主要锚定 refs 13/19/20，ref 15 (Schafer 2012) 仅作发育语境。
- **A1-F8｜Discussion 钠通道句残缺**：line 107 以 "conventiona…" 断句。补全为："Because the channels we find down-regulated in bulk nerve-injury tissue are the same Nav isoforms (Nav1.6/1.7/1.8/1.9) that conventional analgesic programmes target and that are typically up-regulated at the neuronal protein level, the present bulk direction should not be interpreted as evidence against those targets; it is a tissue-composition and model-dependent average that the single-cell and incision analyses show is non-predictive of the postsurgical setting."
- **A2-F10｜ACVR1 LR↔Wald 矛盾未披露（R-2 确认）**：Results 写"docking affinity still added statistically significant discrimination beyond chemotype for AXL, TNIK and ACVR1"，但 ACVR1 同模型 Wald p=0.172、仅 9 个阳性事件（EPV≈1）。**二选一**：(a) 从"added significant discrimination"列表移除 ACVR1，仅保留 AXL(13 事件)、TNIK(10 事件)；或 (b) 保留但加："For ACVR1 the LR test (p = 9.6e-4) disagreed with the multivariate Wald test on the affinity coefficient (p = 0.17) and rested on only 9 positive events against ~7 parameters (EPV ≈ 1); we treat it as a non-reproducible fluctuation rather than signal."
- **A2-F2｜GSE265957 两时间点当作独立对比（同动物，双重表示）**：D4/D63 各 weight 1.00，违反 Stouffer 独立性假设（联合权重 2.00≈Σw² 11.4%）。建议：(a) 将 collapse-sensitivity（合并两时间点）核心提升为共主分析；或 (b) 至少加一句声明两时间点来自同动物、非统计独立，其联合贡献由 bulk-only 与 collapse 敏感性界定。
- **A3-F2｜SCN bulk meta_Z/FDR（Table 1b）不在任何交付的逐基因表**：Table 1b 引 `META_DRG_axis_stouffer.csv`（6 对比，SCN8A=−5.11）+ `META_bulkonly_sensitivity_summary.json`（仅聚合计数），均不含 4-bulk 逐基因值。A3 已从 4 个 bulk DEG + 权重重建出 −2.92/−3.03/−3.41/−4.92（精确）。**须**交付 `META_bulkonly_meta.csv`（逐基因 meta_Z/meta_FDR）或将 Table 1b 源注改为指向 DEG 文件 + 权重并明确"此为 4-bulk 研究 Stouffer，非 6 对比"。

### Tier 2 —— 中等/溯源（修订修复）

- **A3-F1（R-3 确认）｜翻译分母跨文件不一致**：14,390/3,556（Stouffer/NI）vs 14,445/3,564（`_R4_translation_noncircular.csv`），差 ~55 基因。统一至单一"measured universe"定义：或重算 53.9%/69.5% 为 53.7%(7,751/14,445)/69.4%(2,473/3,564)，或重生成翻译文件使其分母匹配 14,390/3,556；加一句声明 overall/core/background/non-circular 各层 measured universe 一致。
- **A2-F3｜consistency≥0.8 阈值在 K=6 vs K=4 不可比**：主分析 K=6 需 ≥5/6；bulk-only K=4 实际需 4/4。声明每 K 的最小一致对比数，并考虑 K 归一化方向性指数 `(max−min)/K` 使阈值跨 meta 规模可比（非阻断）。
- **A2-F7｜18 个重叠基因集做 BH（非独立）**：声明 18 集重叠、非独立，BH 在相依下保守控 FDR（非阻断）。
- **A4-F4｜基金措辞张力**："no specific funding" 与"preliminary foundation for a pending grant" 看似矛盾。收紧为："The author received no financial support for this work. This manuscript reports completed in-silico analyses conducted as preliminary foundation for a pending Fujian Natural Science Foundation grant application; the grant did not fund and did not influence the present analyses, results, or conclusions."
- **A4-F7｜图件格式**：Display Items 称 5 图 PNG≥300 DPI；生产管线偏好 TIFF/EPS/PDF。投前导出 TIFF/EPS≥300 DPI，核图例 ≤350 词，cover letter 声明达标。
- **A4-F8｜DOI 格式**：`doi:10.xxxx` → `https://doi.org/10.xxxx`（PLOS ONE 体例，纯排版）。

### Tier 3 —— 轻微/可选

- **A2-F12（可选）**："programme" 首用加 "(descriptive)"，与因果限定段一致。
- **A2-F1（可选）**：补一句说明逆方差权重解释为大样本渐近（t→z），预判"双重计数"误解。
- **A3-F3（信息）**：`_R4_ref_DOIs.json` 按作者-年键控、非引用序，无害；可加一行注释映射 key→稿件编号。
- **A4-F9（可选）**：确认 Abstract ≤300 词、Author Summary ≤200 词。

---

## 5. 共识 / 互补 / 分歧

**共识（四专家一致）：**
- 方法学诚实度（随机效应、非循环、bootstrap、全库对接零、MW 校正、反向对照）是真实且受控的，非装饰性。
- 量化装置可重现（§3）。
- 不存在致命科学缺陷；最弱处在生物学/临床叙事框定而非计算。
- "诚实阴性"框架（人 miRNA p=0.51、全库对接零、翻译非预测）是卖点，契合 PLOS ONE 对阴性结果的明确欢迎。

**互补（各层覆盖不同面）：**
- A1（生物学）→ A2（统计）共同指向钠通道反向：A1 要求补文献，A2 补充"切口臂单研究单物种"的边界；二者合并即完整修订。
- A3（溯源）为 A1/A2 的所有数字提供独立重算背书；A3-F2 补全 A2 未触及的"SCN bulk 表未交付"缺口。
- A4（政策）独立于科学层，锁定行政闸门。

**分歧（编辑已裁决）：**
- **A1-F7 "McDonnell 未引用"** —— 编辑独立复核（§2 R-1）**推翻**：引用存在于 line 107 上标 ²⁵ 与 line 187。A1 因检索字面 `[25]`/`²⁵` 漏检上标。保留其有效子点（文献广度、DAM 锚定）。
- 其余各项无实质分歧；A2 主动验证并**推翻了启动 prompt 中关于"D-L 内部矛盾 / τ²>0 与 I²>50 矛盾"的假设**（F5 证实统计内部自洽）。

---

## 6. 优先 must-fix 列表（投前/修订必做，含 DESK-REJECT 旗标）

| 序 | 旗标 | 项 | 动作 |
|---|---|---|---|
| 1 | **[DESK-REJECT-RISK]** | A4-F1 AI 披露具名 | 替换 line 154，具名工具 + 验证说明 |
| 2 | **[REVISE-BEFORE-REVIEW]** | A4-F2 DOI 永久存档 | Zenodo 镜像 v1.0.0 + DAS 列 12 GEO |
| 3 | **[REVISE-BEFORE-REVIEW]** | A4-F3 伦理 IRB/同意 | 补 GSE158825 原始 IRB/同意引用 |
| 4 | **[REVISE-BEFORE-REVIEW]** | A4-F6 STROBE 清单 | 上传完成版 STROBE 作 SI |
| 5 | — | A4-F5 删 Reporting Summary | 删悬挂引用 |
| 6 | — | A2-F10 ACVR1 LR↔Wald | 补披露或移出"显著判别"列表 |
| 7 | — | A1-F1 Abstract/Author Summary 再框定 | 补神经/切口比例声明 |
| 8 | — | A1-F3 钠通道文献对话 | 补 Nav1.7/1.8 遗传学+临床失败文献 |
| 9 | — | A1-F4/A1-F5 靶标清单拆表 + CDHR5 降位 | 6 候选 + 4 对照；CDHR5 移出候选 |
| 10 | — | A1-F2 "DAM-like microglial"→"neuroimmune" + OXPHOS 限定 | 细胞身份澄清 |
| 11 | — | A3-F2 交付 bulk-only 逐基因 meta 表 | 或重指源 + 明确 4-bulk |
| 12 | — | A3-F1 翻译分母统一 | 单一 measured universe |

---

## 7. What stands up（经复核稳健、须保留的强项）

1. **非循环翻译检验真实非装饰**：以 5 个神经损伤对比重建签名、切口仅作一次 held-out 检验，46.3% vs 47.1%（−0.9pp, p=0.14），并主动否弃循环 69.5%——正是该领域缺失的纪律。
2. **诚实对接零真实且受控**：反向阳性对照仅作方法验证（AXL/TNIK/ACVR1/MAPK14），ADRA2A 全库 AUC 0.532 (p=0.118)、已知镇痛药 0/64 入 Top-20、无靶标同时过两道滤波；复合 Top-20 明确为知识检索而非对接证据。
3. **核心脆弱性被领述非掩**：bulk-only 敏感性显示 1,732/4,055=42.7% 重叠（57.3% 依赖 translatome），作者称其为"签名最关键的脆弱性并率先陈述"。
4. **OXPHOS 在随机效应下正确未主张**（q=0.31，仅固定效应）。
5. **hub 异常值被标注非掩盖**：ANKRD1/FLNC/CRISP3/MEG11 明确点名无 DRG/痛觉角色；bootstrap 0/35≥0.9、λ.1se=1 基因 如实报告。
6. **ML 泄漏控制典范**：LODO 跨动物下限 0.917–1.000、同动物 GSE241361 折排除、3 个退化 [1.0,1.0] CI 标为非信息、池化 CV 仅作泄漏膨胀上限（置换零 0.490±0.085）。
7. **多重检验登记与因果限定模型级**：6 个非重叠族；事后多元与复合排序 p 明确排除于推断；全文"关联非因果"一致。

---

## 8. 处理路径（建议执行顺序）

1. **先清行政闸门（Tier 0，投前）**：F1 具名 AI 披露 → F2 Zenodo DOI → F3 伦理 → F5/F6 删悬挂引用 + STROBE。这些不依赖科学改写，可并行。
2. **再修 Tier 1 科学叙事**：A1-F1/F2/F3/F4/F5/F6/F7/F8 与 A2-F10/A2-F2 多为正文增补与措辞，可一并成稿。
3. **补交付物（Tier 1/2）**：A3-F2 逐基因 bulk meta 表、A3-F1 翻译分母统一。
4. **收尾 Tier 2/3**：A2-F3/F7、A4-F4/F7/F8 等措辞与格式。
5. **回归验证**：所有已验证数字（§3）不得改动；修订后重跑 gate（consistency/word/docx）。

---

## 9. 过程教训

- **检索上标编号的陷阱**：A1 用 `[25]`/`²⁵` 字面 grep 漏检上标数字，误判"未引用"。教训：验证引用须同时检索 `{{key}}`（源）、上标 Unicode、以及 ref 列表，不能只认一种编码。编辑独立复核（grep 全文 + 源文件）已纠正。
- **跨文件溯源口径必须单一**：翻译分母 14,390 vs 14,445 的本质是两条管线对"measured universe"计数口径不同。教训：同一指标的所有呈现必须源自同一文件/同一分母定义，或在文中显式声明差异。
- **LR↔Wald 矛盾是过参数化红旗**：EPV≈1（9 事件 / ~7 参数）下 LR 显著而 Wald 不显著，是信息矩阵病态的经典信号；凡事后多元模型均须同时报告 LR 与 Wald 并核对一致性。
- **enforced-independence 的价值**：四专家未互读，A1 的误判未被其他层"传染"，编辑得以独立纠正；同时 A2 主动推翻了启动假设（D-L 矛盾），证明独立重算优于依赖 prompt 假设。

---

## 10. Reframe 注（阴性诚实框架 —— 须全程守住）

本稿的卖点不是"发现了靶点"，而是**方法学诚实 + 阴性边界**：神经炎症–DAM–补体↑·OXPHOS↓ 机制主线、人源层阴性 (p=0.51)、全库对接零、翻译非预测。修订时须守住三条红线：

1. **不以 ADRA2A 对接命中为主线**：其全库 AUC 0.532 (NS) 是 CNS 先验子集的组成伪信号（已证），仅作"方法学对照/ inconclusive"，不得升格为发现。
2. **一致性叙事**：Abstract / Author Summary / 正文 / 省自然标书 三线一致——均以"**神经损伤相关转录响应**"而非"CPSP 特异机制"为主轴；MVP 是已完成的前期基础，省自然 AIMS 须锁定 STRETCH 验证（临床 qPCR/ELISA、Visium、MD），不得把 MVP 生信筛查写成"拟做"。
3. **阴性即诚实资产**：勿为迎合期刊而淡化脆弱性（57.3% translatome 依赖、0/35 bootstrap 稳定、OXPHOS 随机效应未过关）。这些恰是 PLOS ONE sound-science  criterion 所奖励的。

---

*本合并报告由编辑在四份独立专家报告（A1_domain / A2_design / A3_implementation / A4_venue，均存于 `reviews/round6_2026-09-26/`）基础上撰写，并叠加编辑对 R-1/R-2/R-3 三项的最严重发现的独立复核。四专家报告与本条合并报告遵循 enforced-independence 纪律，视为首次投稿评审。*
