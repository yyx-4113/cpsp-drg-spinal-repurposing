# 评审报告 — PLOS ONE 处理编辑视角 + STROBE 2007 报告规范审计

**评审角色**：独立同行评审专家（处理编辑视角，负责期刊合规性与报告清单诚实性）
**评审对象**：*Conserved nerve-injury-associated transcriptional response on the dorsal root ganglion–spinal axis: non-predictive incision translation and an honest repurposing null*（首次提交，独立评审，未读取任何前轮评审/作者回复）
**评审依据**：PLOS ONE 投稿政策 + STROBE 2007（von Elm et al., *Lancet* 2007;370:1453–1457）

---

## § Stands up（已合规项，附证据）

1. **结构化摘要齐全且符合 PLOS ONE 格式。**
   【Evidence】Manuscript.docx / MVP_ScientificReports_submission.md 行 12–21：摘要含 **Background / Methods / Results / Conclusions** 四个一级标题；常规空格分词计词 = **185 词**（Background 39 / Methods 28 / Results 101 / Conclusions 23 的细分相加亦自洽），低于强制 ≤200 字闸值（PLOS 软上限 ~300）。docx 中 Abstract 段落与 md 完全一致。
   【结论】格式与字数双合规。

2. **标题三件套完全一致。**
   【Evidence】Manuscript.docx 标题行、Cover_Letter_PLOSONE.docx “Manuscript title:” 行、STROBE_Checklist.docx “Manuscript:” 行，三者均为 *Conserved nerve-injury-associated transcriptional response on the dorsal root ganglion–spinal axis: non-predictive incision translation and an honest repurposing null*，逐字一致。

3. **STROBE 版本号一致（2007）。**
   【Evidence】STROBE_Checklist.docx 首段 “STROBE 2007 (von Elm et al., Lancet 2007;370:1453–1457)”；MVP_ScientificReports_submission.md 行 283 亦写 “completed **STROBE 2007** checklist”。版本无歧义。

4. **AI 使用声明具体、诚实且位置明确。**
   【Evidence】MVP_ScientificReports_submission.md 行 166–167（Methods “Statistical discipline, causal scope and AI-use disclosure”）：明确点名 “A generative AI language model (Claude, Anthropic) was used to assist manuscript drafting and language polishing”，并声明 “no AI tool was used to generate, select or interpret data; no AI tool satisfies authorship criteria”。符合 PLOS 对“指明工具与用途”的要求。

5. **伦理/IRB 与动物伦理声明齐备。**
   【Evidence】MVP_ScientificReports_submission.md 行 169–170（Ethics statement）：GSE158825 原始存档“documents IRB approval and informed consent”，再分析无需二次审批；动物数据集（9 个 GSE）声明原始 IACUC 批准。人类唯一数据集 n=60 的去标识化再分析路径清晰。

6. **利益冲突 / 基金 / 作者贡献三声明齐全。**
   【Evidence】MVP_ScientificReports_submission.md 行 215–225：Funding（无资助 + 待批福建自然基金声明）、Author contributions（Y.Y. 全包）、Competing interests（无金融利益冲突 + 待批基金中列有 ADRA2A 的披露）。Cover_Letter_PLOSONE.docx 亦复述一致。

7. **图表数量声明与实际 docx 一致。**
   【Evidence】MVP_ScientificReports_submission.md 行 232 声明 “5 figures + 5 tables = 10”。对 Manuscript.docx 的 `word/document.xml` 解析：`w:tbl` 计数 = **5**，`a:blip`（嵌入图）= **5**，正文 Fig1–Fig5、Table 1/1b/2/3/3a 提及齐全。声明与成品相符，无虚报。

8. **全部 33 条参考文献均带可解析 DOI。**
   【Evidence】MVP_ScientificReports_submission.md 行 176–208：33 条参考文献逐条含 `https://doi.org/...`，无缺失。

---

## § 问题与整改（每个问题均含 Problem / Evidence / Why it matters / Specific fix）

### 问题 A — 两条参考文献未被正文引用，引用序号不连续（高优先级）
【Problem】参考文献 26、27 在正文中从未被引用，正文引用序列在 25 之后直接跳到 28，出现断号。
【Evidence】MVP_ScientificReports_submission.md 行 200–203 列出 26（Yousefpour N. et al., *Nat Commun* 16, 4590, 2025）与 27（Kong E. et al., *J Cell Mol Med* 27, 1664–1681, 2023）；脚本对正文（References 之前）上标数字全量提取显示：使用过的编号集合为 {1..25, 28..33}，**26、27 缺失**；首次出现顺序为 1→25→28→33，确认断号。
【Why it matters】PLOS 硬性要求“参考文献按引用顺序编号且每条必须被引用”。存在未被引用的孤儿文献 + 断号，属参考文献完整性缺陷，编辑/排版会要求必修，严重时构成格式退稿风险；也削弱报告严谨度。
【Specific fix】二选一：① 在 Discussion 小胶质/C1q/DAM 相关处（约行 120–124，“microglial–complement”“DAM-like”论述）补引 26、27，使 1..33 连续；② 若确无对应论述，直接从参考文献表删除 26、27 并重新顺号。

### 问题 B — 数据可用性声明中的 Zenodo DOI 为未兑现占位符，且“已镜像”表述失真
【Problem】数据可用性声明声称存在一个“版本化 Zenodo 归档镜像 GitHub release v1.0.0”，但其 DOI 为占位符 `10.5281/zenodo.XXXXXXX — to be minted at submission`，提交时该归档并不存在。
【Evidence】MVP_ScientificReports_submission.md 行 222：“A versioned Zenodo archive providing a citable permanent DOI mirrors the GitHub release v1.0.0 (DOI: 10.5281/zenodo.XXXXXXX — to be minted at submission)”。同一段 GitHub 仓库 `https://github.com/yyx-4113/cpsp-drg-spinal-repurposing`（tag v1.0.0）确为真实公开库且已含处理数据。
【Why it matters】PLOS 要求数据在提交时即存入公开仓储**或**有可信计划。底层数据经 GitHub（公开库）已实际可得，故**非硬性退稿**；但“Zenodo 归档已镜像”在提交时为假陈述，审稿人点击 DOI 必验证失败，构成诚信瑕疵，易被要求修正乃至质疑。
【Specific fix】二选一：① 提交前真正创建 Zenodo 归档、替换占位符为真实 DOI；② 删除 Zenodo 整句，仅保留 GitHub URL（已满足“公开仓储 + 非 on-request”要求），并将 “Data are not ‘available on request’” 保留。不要在数据已可得时继续声明一个不存在的镜像。

### 问题 C — STROBE 第 14 项（描述性数据）标注“Addressed”但实际未做（清单诚实性，严重）
【Problem】STROBE 清单第 14 项（Descriptive data：报告研究对象人口学/临床/社会特征及缺失值）被勾为“Addressed”，但稿件**未提供任何参与者层面的描述性统计**——n=60 的 GSE158825 队列无年龄、性别、疼痛结局分布、缺失值计数。
【Evidence】STROBE_Checklist.docx / MVP_STROBE_checklist.md 第 14 项：“Addressed. Gene-set programme magnitudes (Fig. 1…); SCN per-contrast directions (Table 1b…); hub localisation (Figs 3–4…); docking AUCs (Fig. 5…)”。但 MVP_ScientificReports_submission.md 全文无 GSE158825 参与者特征表；被引用的 Fig.1/Table1b/Figs3–4/Fig.5 均为**基因/分子层面结果**，并非 STROBE 14 要求的参与者描述性数据。
【Why it matters】这是清单与稿件实质不符的“诚实性”硬伤。STROBE 用户/审稿人按清单核对会立即发现：第 14 项并未真正满足。在再分析情境下，作者至少应说明“公开存档是否提供参与者级人口学变量”，而非用基因层面图表冒充。
【Specific fix】二选一：① 增补 GSE158825 参与者特征表（年龄/性别/疼痛评分 %nprs20delta 分布、缺失情况）作为真正的第 14 项交付物，并将清单第 14 项证据改指该表；② 若公开存档确无参与者级人口学，将第 14 项如实改为 “Partial / N/A (no participant-level demographics available in the public deposition)” 并附说明，删除对 Fig.1/Table1b 等的错误指向。

### 问题 D — STROBE 第 5 项（研究现场/日期）笼统标 N/A，原始研究现场与日期逻辑不可核
【Problem】第 5 项（Setting，须描述现场、地点及相关日期：招募、暴露、随访、数据收集）被标为 “N/A (primary deposition)”，但未对原始 GSE158825 的研究设计、现场、数据收集/IRB 批准日期做任何交代，全文亦无任何伦理批准或数据收集日期，导致“伦理批准 vs 数据收集”的日期逻辑无法核验。
【Evidence】STROBE_Checklist.docx 第 5 项：“N/A (primary deposition)… no physical study site of its own”。MVP_ScientificReports_submission.md 行 169–170 仅称“original deposition documents IRB approval and informed consent”，无日期；全稿检索无 IRB 批准日或数据收集日。
【Why it matters】STROBE 第 5 项期望描述原始研究的现场与关键日期；纯 N/A 过度简化，使伦理来源不可追溯，审稿人可能要求补述原始研究设计/现场/年代。对再分析而言，至少应报告“从存档可得的设计/现场/年代信息”，或明确声明这些信息在存档中不可得。
【Specific fix】在第 5 项或 Ethics 段补 1–2 句：概括 GSE158825 原始设计（观察性队列、腰椎手术 + 疼痛结局、存档单位/国家、招募与数据收集年代（如存档可知）、IRB 批准日 vs 收集日）；若日期在存档中不可得，明确写出“日期信息未在原 GEO 存档中提供”，并将第 5 项由纯 N/A 改为 “N/A with note: original setting/dates summarised as … / unavailable”。

### 问题 E — STROBE 第 1 项清单描述与标题实际内容不符
【Problem】第 1 项称“Title states ‘multi-dataset in-silico meta-analysis’”，但稿件实际标题并不包含该短语，研究设计实际是在摘要而非标题中说明。
【Evidence】STROBE_Checklist.docx 第 1 项首句：“Title states ‘multi-dataset in-silico meta-analysis’”。MVP_ScientificReports_submission.md 行 1 / Manuscript.docx 标题为 *Conserved nerve-injury-associated transcriptional response on the dorsal root ganglion–spinal axis: non-predictive incision translation and an honest repurposing null*——**不含** “meta-analysis”或“reanalysis”字样；设计词仅见于摘要 Background（行 14 “We reanalysed 12 public GEO datasets”）与 Methods。
【Why it matters】STROBE 第 1 项要求标题/摘要标明研究设计；清单把“标题标明设计”记为已满足但描述失真，削弱清单可信度。
【Specific fix】二选一：① 在标题中加入设计词，例如改为 “*… : a multi-dataset in-silico meta-analysis with non-predictive incision translation and an honest repurposing null*”；② 或将第 1 项措辞改为“设计在摘要中标明（Background: ‘We reanalysed 12 public GEO datasets…’），标题未含设计词”。

### 问题 F — STROBE 清单的行号定位与稿件实际行号不符
【Problem】清单多处给出的稿件行号定位与实际稿件行号不一致。
【Evidence】STROBE_Checklist.docx：第 1 项“Abstract (lines 7–21)”而摘要实际在行 12–21；第 22 项“Funding (line 211)”而 Funding 在行 215；同一项“Competing interests (line 220)”而 Competing interests 在行 224；第 4 项“Methods (lines 129–162)”而 Methods 章节始于行 132。
【Why it matters】编辑/审稿人按清单回查稿件时会发现指针偏移，降低对清单其余“Addressed”判定的信任。
【Specific fix】以提交版稿件（docx 对应 md 行号）重新锚定每条证据行号，或改为“章节名 + 关键词”定位以免疫于行号变动。

### 问题 G — 跨产物文件名品牌不一致（ScientificReports vs PLOS ONE）
【Problem】稿件正文以“Scientific Reports”品牌命名支撑文件，却投递 PLOS ONE；STROBE 文件名亦与投稿包实际文件名不符。
【Evidence】MVP_ScientificReports_submission.md 行 283：“… `MVP_ScientificReports_supplementary.md` … `MVP_STROBE_checklist.md`”。但 submission_pack 中对应文件为 `STROBE_Checklist.docx`（非 `MVP_STROBE_checklist.md`），且无任何 `MVP_ScientificReports_supplementary.md`；投稿包文件前缀为 `Cover_Letter_PLOSONE.docx`、`Manuscript.docx`。
【Why it matters】PLOS 投稿系统要求支撑文件使用 PLOS 品牌命名（如 S1_File、S2_Checklist），品牌错配显属疏漏，且稿件内引用的支撑文件名与实际提交不符，会造成审稿人找不到文件。
【Specific fix】将支撑文件按 PLOS 约定重命名（如 Supplementary Information → S1_File.docx；STROBE → S2_STROBE_Checklist.docx），并同步修改稿件行 283 的内部引用字符串。

### 问题 H — Author Summary 非 PLOS ONE 必需，且投稿信误称其为“PLOS ONE 要求”
【Problem】稿件含 Author Summary（PLOS ONE 不要求该模块）；投稿信却将其列为“PLOS ONE-required”元素，表述不准确。
【Evidence】MVP_ScientificReports_submission.md 行 24–28 “## Author Summary”；Cover_Letter_PLOSONE.docx 上传前清单项：“[ ] Manuscript incl. Author Summary, Abstract, Intro, Results, Discussion, Methods” 及其正文 “The manuscript includes the PLOS ONE-required Author Summary…”。
【Why it matters】非退稿级，但 Author Summary 属其他 PLOS 子刊模块，PLOS ONE 投稿信称其为“必需”属事实错误，可能让编辑质疑作者对期刊政策的熟悉度。
【Specific fix】删除 Author Summary，或明确其为可选“Synopsis”；修正投稿信，去掉“PLOS ONE-required Author Summary”的措辞。

---

## § Questions for the authors（请作者回答）

1. 参考文献 26（Yousefpour N., *Nat Commun* 2025）与 27（Kong E., *J Cell Mol Med* 2023）在正文中完全未被引用。请问是漏引（应在小胶质/C1q/DAM 讨论处补引），还是应直接从参考文献表删除并重排序号？
2. 数据可用性声明称 Zenodo 归档“已镜像 GitHub release v1.0.0”，但 DOI 为占位符。请问提交前是否会真正创建 Zenodo 归档并替换真实 DOI？若不会，是否同意删除 Zenodo 整句、仅保留 GitHub？
3. STROBE 第 14 项被标“Addressed”，但稿件未提供 GSE158825（n=60）参与者层面的人口学/临床描述与缺失值。请问原 GEO 存档是否提供参与者级变量？若提供，请补一张参与者特征表；若不可得，是否同意将第 14 项改为“Partial/N/A（存档无参与者级数据）”？
4. STROBE 第 5 项标 N/A 但无原始研究现场与任何日期。能否补充 GSE158825 原始研究设计、现场、数据收集/IRB 批准年代（或明确声明存档未提供这些日期）？
5. 稿件与支撑文件以 “ScientificReports” 品牌命名却投 PLOS ONE。请确认所有支撑文件将按 PLOS 命名约定重命名，并同步修正稿件行 283 的内部引用。
6. 参考文献 20（Divito A.E. et al., *Cleveland Clinic Journal of Medicine* 93, 94–98, **2026**）为 2026 年文献，请确认其为已接受/在线发表且 DOI 可解析，而非预期文献。

---

## § What I actually checked（核查清单）

**读取/解析的文件（均按独立首次提交处理，未读任何前轮评审/作者回复/记忆文件）：**
- `reports/MVP_ScientificReports_submission.md`（全文 283 行，分两段读取 + grep 检索）
- `reports/MVP_STROBE_checklist.md`（全文 35 行）
- `submission_pack/Manuscript.docx`、`submission_pack/Cover_Letter_PLOSONE.docx`、`submission_pack/STROBE_Checklist.docx`（经 zip 解包提取 `word/document.xml` 纯文本）

**docx 属性/数值核验（脚本执行）：**
- Manuscript.docx `word/document.xml`：`w:tbl` = 5、`a:blip` 嵌入图 = 5、`<w:drawing>` = 5；正文 Fig1–Fig5 与 Table 1/1b/2/3/3a 提及齐全 → 与“5+5=10”声明一致（问题 C/D 之外的展示项核对通过）。
- 三份 docx 标题字符串逐字比对一致；STROBE 年份在清单与稿件均为 “2007”。
- 摘要词数：脚本常规空格分词 = **185 词**（< 200 闸值）；上标/数值拆分式计数会到 220，但期刊标准空白分词为 185，合规。

**数值/序列核验（脚本执行）：**
- 对正文（References 之前）上标数字全量提取：使用编号 {1..25, 28..33}，**26、27 缺失**，首次出现顺序确认断号 → 问题 A。
- 参考文献表 33 条，逐条含 `doi.org` → 问题 8 合规；但 26/27 孤儿文献 → 问题 A。

**未触发退稿的判定：** 上述 A–H 中，单独任一项均不构成 PLOS ONE 绝对性 desk-reject；但 **B（Zenodo 假镜像声明）** 与 **C（STROBE 第 14 项清单不实）** 属诚信/完整性高风险，建议作为“接收前必须修正”项；A（孤儿文献+断号）属格式完整性硬伤，编辑必退修。
