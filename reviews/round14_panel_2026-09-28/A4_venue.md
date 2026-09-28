# PLOS ONE 独立合规性审查报告（A4 · 期刊编辑 / 报告规范审计视角）

**被审稿件：** *Conserved nerve-injury-associated transcriptional response of the dorsal root ganglion: spinal-cord localisation and an honest repurposing null*
**作者：** Yongxin Yang（单作者，ORCID 0009-0004-9698-6552，单位：福建中医药大学第二附属医院）
**送审包：** `submission_pack/` 重建版（Manuscript / Supporting_Information / Cover_Letter / STROBE_Checklist 四个 .docx）
**审查立场：** 当作**首次投稿**审查；不假定稿件已经过任何前期审稿或已经达到成熟状态。仅依据可读取文件独立判断。

---

## 一、总体结论（Gating 概览）

| 硬门槛 | 结果 | 说明 |
|---|---|---|
| 1. Abstract ≤ 300 词 | ✅ 通过（实测 297） | 与稿件自报一致 |
| 2. Display items ≤ 8（稿件自称 5 图 + 3 表 = 8） | ✅ 通过（实测 8，且全部枚举） | 5 个 `w:tbl` 对象实为 3 个主表（含子面板），不冲突 |
| 3. Title ≤ 20 词 | ✅ 通过（实测 16 词） | 三处文本一致 |
| 4. 图内嵌于 Manuscript.docx（非仅单独上传） | ✅ 通过（**先前"缺图"退稿触发点已修复**） | 5 图全部 inline（wp:anchor=0） |
| 5. 报告规范（STROBE）完成且与设计一致 | ⚠️ 基本通过，但存在**数字硬矛盾** | STROBE 22 项齐备；但 item 15 与 docx 表 2 注释出现稿件正文未定义的"4,055 基因核心" |
| 6. 数据可用性（带版本的真实仓库 URL，非"on request"） | ✅ 通过（三处一致 v1.4.0） | 需注意 tag 是否真正公开 |
| 7. 伦理 / IRB 声明 | ✅ 通过（适合公共去标识 GEO 再分析） |  |
| 8. 竞争利益 / 基金 / 作者贡献 / AI 披露 | ✅ 通过（单作者、无学位冒用） | 参考文献作者列表为次要技术 nit |
| 9. 参考文献 Vancouver 编号格式 | ✅ 通过（40 条编号、DOI 可解析） | 少量作者列表格式建议优化 |
| 10. 投稿信 vs 稿件一致性 | ✅ 通过（无矛盾） | 一处清单措辞可对齐 |

**最严重发现（必须修）：** STROBE 清单 item 15 与 Manuscript.docx 表 2 注释都写"4,055-gene core / 4,055-gene Stouffer meta signature"，而稿件正文**全文统一**将核心定义为 **2,750 基因**（固定效应）。"4,055"在稿件 .md 正文中**完全不存在**（grep 确认）。这是一个会在技术审查阶段被直接点名、且看起来像"旧草稿残留/复制粘贴错误"的内部矛盾，必须在送交前统一。

---

## 二、逐条发现（四段式：问题 / 证据 / 影响 / 具体修正）

### 发现 1 — Abstract 词数（硬门槛，通过）
- 【Problem】 稿件自报摘要 297 词，需核实是否 ≤300 且为结构化摘要。
- 【Evidence】 `reports/MVP_PLOSONE_submission.md` 第 12–20 行（Background/Methods/Results/Conclusions 四段）；用纯文本词数统计（去除 `**` 标记）实测 **297 词**，与自报一致；且具备 PLOS ONE 要求的四段式结构。
- 【Why it matters】 摘要超 300 词或缺少结构化分段会触发技术审查退回（technical-check fail）。此处两项均满足。
- 【Specific fix】 无需修改。保持现状即可；若后续增删文字，须重新复核 ≤300 词。

### 发现 2 — Display items 计数与枚举（硬门槛，通过）
- 【Problem】 稿件自称"5 figures + 3 tables = 8"，需核实数量与逐项枚举。
- 【Evidence】 `reports/MVP_PLOSONE_submission.md` 第 297 行标题"5 figures + 3 tables = 8 enumerated main display items"；第 299–315 行枚举 Fig.1–Fig.5；第 316–386 行枚举 Table 1（含 1a/1b）、Table 2、Table 3（含 3a/3b）。Manuscript.docx 内 `grep -c '<w:tbl>'` = **5 个表格对象**，经内容定位分别为：Table 3a Panel A、Table 3a Panel B、Table 1b（SCN 子表）、Table 2（35 hub）、Table 3b（反向对照）——即**3 个主表**（Table 3 被拆成若干子面板渲染）。补充材料 S1–S7 在 `Supporting_Information.docx` 中明确枚举，未计入主 display items，符合声明。
- 【Why it matters】 PLOS ONE 当前已不再硬性限制 8 个展示项（旧规已废止，现行政策只要求"尽量精简"），因此作者自设的"8"无论怎样都不构成退稿门槛；真正要核实的是**数量自洽且每项均被枚举**——这一点满足。
- 【Specific fix】 无需修改。注：若担心，可在 Display items 段明确写"Table 3 comprises panels 3a (A/B) and 3b rendered as separate table objects"，避免排版编辑误以为表数不符。

### 发现 3 — 标题词数（硬门槛，通过）
- 【Problem】 标题是否 ≤20 词。
- 【Evidence】 第 1 行标题实测 **16 词**（"Conserved nerve-injury-associated transcriptional response of the dorsal root ganglion: spinal-cord localisation and an honest repurposing null"）。docx `docProps/core.xml` 的 `dc:title`、投稿信、稿件三处文本**逐字一致**。
- 【Why it matters】 标题超限是技术审查 nit；此处合规。
- 【Specific fix】 无需修改。

### 发现 4 — 图内嵌于 Manuscript.docx（硬门槛，**历史退稿触发点已修复**）
- 【Problem】 PLOS ONE 要求图表嵌入稿件正文 .docx（不能仅作为单独文件上传）。已知前次送审曾因"missing figures"（图仅单独上传）被退回/拒收，需确认本次已修复。
- 【Evidence】 解包 `submission_pack/Manuscript.docx`：`word/media/` 内含 image1.png–image5.png（5 张，214–341 KB，高分辨率）；`document.xml` 中 `r:embed="rId10"`…`rId14"` 共 5 处，且 **`wp:anchor` = 0、`wp:inline` 出现 10 次（5 个图形各含开/闭标签）= 全部为行内嵌入**，无任何浮动（floating）图形。图注（Figure 1–5 legends）在 docx 末尾"Figure legends"段落完整存在。
- 【Why it matters】 这是此前被 desk-reject / 退回的**明确硬门槛**。本次 5 图已真实内嵌（inline，非浮动、非仅外链），该触发点**已闭合**。但注意：PLOS 生产环节仍要求每幅图另以单独高分辨率文件（TIFF/EPS/≥300 DPI PNG）上传，此步骤属投稿系统操作，不在本包可验证范围内（见"问题 3"）。
- 【Specific fix】 无需修改嵌入方式；上线投稿时记得在系统里**每图单独再传一份**，并复核嵌入 PNG 真实 DPI ≥ 300。

### 发现 5 — 报告规范 STROBE：完成度 OK，但存在核心数字硬矛盾（需修）
- 【Problem】 本研究为观察性 / in-silico 再分析，须完成 STROBE（或合适清单）且与稿件所述设计一致；当前 STROBE 完成但出现与正文冲突的数字。
- 【Evidence】
  - `submission_pack/STROBE_Checklist.docx` 覆盖 STROBE 2007 全部 22 项（item 1–22 均"Addressed / Partial / N/A(primary deposition)"并标注稿件章节），适用性声明合理（仅 GSE158825 为真实人类观察性队列，其余 11 个 GEO 为动物/体外，按"类比"适用 STROBE）。
  - **矛盾点：** STROBE item 15 原文写"the locked **4,055-gene** core and 35 hubs"；同时 `Manuscript.docx` 表 2 注释写"In meta core = membership in the **4,055-gene** Stouffer meta signature (the in_meta_core boolean in P3_hub_genes.csv…)"。
  - 但稿件正文（`MVP_PLOSONE_submission.md`）**全文从未出现 4,055**：核心在正文统一为 **2,750 基因**（固定效应，meta_FDR<0.05 且 consistency≥0.8；随机效应降至 508），第 18/44/46/50/56/58/140 等多处均为 2,750；grep "4055|4,055" 在 .md 中返回"NOT in manuscript md"。
- 【Why it matters】 这是会直接在技术审查 / 编辑初审被点名的**内部不一致**：同一文档里"核心基因数"出现两个互不相容的数值（2,750 vs 4,055），且 4,055 在方法学里无任何定义。编辑会认为这是旧草稿残留或 `in_meta_core` 标志实际来自一个**正文未定义的签名集**——既影响可信度，也可能被质疑"表 2 的 In-meta-core 列到底按哪个阈值算的"。属于必须消歧的硬问题。
- 【Specific fix】 二选一（推荐前者）：
  - **方案 A（对齐正文）：** 将 docx 表 2 注释与 STROBE item 15 中的"4,055-gene"全部改为"**2,750-gene core (meta_FDR < 0.05 and consistency ≥ 0.8)**"，与正文 Methods/Results 完全一致。
  - **方案 B（若 4,055 确为另一已定义集合）：** 必须在 Methods 中显式定义该 4,055 基因签名（阈值、与 2,750 的关系），并在全文统一使用，不能仅在表注/清单里凭空出现。
  - 同时核对 `P3_hub_genes.csv` 的 `in_meta_core` 布尔值到底对应 2,750 还是 4,055，保证"数据–正文–表–清单"四者一致。

### 发现 6 — 数据可用性：带版本的真实仓库（硬门槛，通过，附提醒）
- 【Problem】 须给出真实、带版本号的仓库 URL，不得"available on request"，且跨稿件/投稿信/CITATION.cff 一致。
- 【Evidence】 稿件第 283–285 行：`https://github.com/yyx-4113/cpsp-drg-spinal-repurposing`，"released as version **v1.4.0** (GitHub release tag v1.4.0)"；第 287 行明确"Data are not 'available on request'"。投稿信同样写该 URL + v1.4.0。`CITATION.cff` 第 18 行 `repository-code` 同一 URL，第 2 行 message 声明 v1.4.0 可引用存档。**三处完全一致**，且 12 个 GEO 登录号（GSE…）完整列出。
- 【Why it matters】 数据可用性语句是 PLOS 硬性政策；此处给出了可版本化、可引用的公开仓库并明确拒绝"on request"，符合要求。
- 【Specific fix】 无需修改文本。上线前**务必确认 GitHub 上的 v1.4.0 release/tag 已真正公开发布**（非本地或草稿 tag），否则该"版本化存档"承诺落空。另：稿件说明"no Zenodo snapshot has been deposited"——可接受，但 GitHub tag 必须长期存在（建议同时存一份 Zenodo 快照以免疫情/仓库变动，非强制）。

### 发现 7 — 伦理 / IRB 声明（硬门槛，通过）
- 【Problem】 对公共动物 GEO 数据的复用，是否具备恰当且自洽的伦理声明。
- 【Evidence】 稿件第 183–184 行伦理段：说明再分析 GEO 公共去标识数据；人类数据集 GSE158825（n=60 血浆 miRNA）原始 deposit 已记录 IRB 批准与知情同意（IRB 及批准号存于 GEO deposit，本再分析不再独立复现），以去标识形式获取，二级再分析无需额外伦理批准；动物数据集（GSE267799 等）原始 deposit 记录 IACUC 批准，本研究未产生新动物数据。STROBE item 5/6/13 将"原始设计/招募/场所"标为 N/A(primary deposition)，理由合理。
- 【Why it matters】 涉及人类数据（GSE158825）时 PLOS 要求声明原始伦理批准；公共去标识二级再分析按惯例可引用原始 deposit 的 IRB/ consent，本文已做到，不会触发伦理退稿。
- 【Specific fix】 无需修改。可选优化：明确写出 GSE158825 原始 deposit 的 IRB 名称/批准号（若公开可查），使"recorded in the GSE158825 data deposit"更具体；当前写法已可接受。

### 发现 8 — 竞争利益 / 基金 / 作者贡献 / AI 披露（硬门槛，通过）
- 【Problem】 四项声明是否齐备、单作者下是否冒用更高学位、AI 使用是否披露。
- 【Evidence】
  - 竞争利益（第 289–290 行）：声明无财务竞争利益；**如实披露**一项pending Fujian Natural Science Foundation 基金申请将 ADRA2A 列为候选靶标，但说明该基金未资助/未影响本分析，且 10 个靶标在 docking 流程中一视同仁。透明、具体，符合 PLOS"具体而非泛泛"的要求。
  - 基金（第 276–277 行）："received no financial support"；说明本分析作为 pending 基金申请的预备基础，但基金未资助/未影响结论——已妥善声明。
  - 作者贡献（第 279–280 行）：单作者 Y.Y. 构思、执行全部计算、解释、撰写。
  - AI 披露（第 180–181 行）：明确"generative AI language model (Claude, Anthropic) was used to assist manuscript drafting and language polishing"；科学设计/分析/结论均由作者完成，所有 AI 生成/编辑句均经作者核对，且无 AI 满足作者标准。满足 PLOS AI 使用披露政策。
  - **学位核查：** 稿件、docx、投稿信中作者署名均为"Yang Y"；docx 作者行"Yang Y¹*"、core.xml 标题区均无 MD/PhD/Dr./M.S. 等任何更高学位字样；与"作者仅持医学学士(B.M.)"的约束一致，未冒用 MD/PhD。
- 【Why it matters】 竞争利益含糊、学位冒用、AI 未披露均属 PLOS 政策红线；此处均合规。
- 【Specific fix】 无需修改。提醒：参考文献格式（见发现 9）中个别作者列表为次要 nit；另建议在 CV/简历层面也绝不出现"Dr. Yang"等暗示，保持与投稿一致。

### 发现 9 — 参考文献 Vancouver 编号（硬门槛，通过；含次要优化）
- 【Problem】 PLOS ONE 用 Vancouver（顺序编码）格式，须编号、按引用顺序、DOI 齐全；抽查前几条 DOI 有效性。
- 【Evidence】 稿件第 188–272 行共 **40 条**编号参考文献，正文用上标数字引用（如引言首引 ¹ = Macrae 2008，与文献 1 对应），编号顺序与引用顺序一致。所有条目均带 `https://doi.org/...` 格式 DOI。对前几条做**实时 DOI 解析**（HTTP HEAD）：`10.1093/bja/aen099`（ref 1）、`10.1038/nature05413`（ref 14，Cox SCN9A Nature 2006）、`10.1136/jmg.2003.012153`（ref 13，Yang SCN9A J Med Genet 2004）均返回 **HTTP 302（doi.org 正常重定向）= 可解析有效 DOI**。文献 13–15 为 SCN9A 经典论文，DOI 与真实发表完全吻合。
- 【Why it matters】 编号混乱或 DOI 失效会在技术审查被打回；此处格式统一、顺序正确、抽检 DOI 有效。
- 【Specific fix】 次要优化（非退稿门槛）：PLOS 偏好**完整作者列表**；当前对 2–4 人论文也仅列"第一作者 et al."（如 ref 13 "Yang, Y. et al."、ref 2 "Sapio, M. R. et al."）。建议：≤~10 作者的论文列出全部作者，超大作者组用"前 3 + et al."。同时建议送交前用 DOI 解析器对全部 40 条 DOI 跑一遍批量校验（本文仅抽检 3 条）。

### 发现 10 — 投稿信 vs 稿件一致性（硬门槛，通过）
- 【Problem】 投稿信与稿件在标题、核心断言、作者、版本号上是否矛盾。
- 【Evidence】 投稿信（`submission_pack/Cover_Letter.docx` 文本）标题、通讯作者"Yang Y"、GitHub v1.4.0、关键数"43.3% vs 47.1% background, perm_p = 0.0002"、"no new human or animal data"、AI 辅助撰写等，均与稿件逐一对齐；无标题/断言/作者层面的错位。
- 【Why it matters】 投稿信与正文矛盾是编辑初审常见退稿理由；此处无矛盾。
- 【Specific fix】 次要对齐：投稿信末尾自检清单写"Reporting guidelines if applicable (transcriptome reanalysis → GEO/MIAME compliance noted)"，但稿件实际主要使用 **STROBE**；建议在投稿信该条同时点名 STROBE（与 MIAME 并列），使清单措辞与正文实际使用的报告规范一致（见"问题 5/补充观察"）。

---

## 三、Stands up（合规 / 正确项，附证据，≥3）

1. **摘要合规**：结构化四段、实测 297 词 ≤300，与自报一致（`MVP_PLOSONE_submission.md:12-20`）。
2. **历史"缺图"退稿触发点已修复**：Manuscript.docx 内 5 图全部行内嵌入（word/media/image1–5.png，rId10–14，`wp:anchor=0`）——这是本次最关键的"之前被退回、现已闭合"的硬门槛。
3. **数据可用性达标**：真实、带版本（v1.4.0）的 GitHub 仓库 URL 在稿件/投稿信/CITATION.cff 三处完全一致，并显式拒绝"available on request"（`MVP_PLOSONE_submission.md:283-287`、`CITATION.cff:18`）。
4. **伦理声明适合公共去标识再分析**：对 GSE158825（人类）记录原始 IRB/consent、动物数据记录 IACUC、明确二级再分析无需新批准（`MVP_PLOSONE_submission.md:183-184`）。
5. **AI 使用披露明确**：满足 PLOS AI 政策，区分"辅助起草"与" authorship 标准"（`MVP_PLOSONE_submission.md:180-181`）。
6. **STROBE 清单完整**：22 项全部覆盖，适用性声明（仅人类观察性队列按类比适用）合理（`STROBE_Checklist.docx`）。
7. **参考文献规范**：40 条 Vancouver 顺序编号、DOI 齐全，抽检 3 条 DOI 实时可解析。
8. **作者署名无学位冒用**：稿件/docx/投稿信均仅"Yang Y"，无 MD/PhD/Dr.，与 B.M. 资格一致。
9. **补充材料枚举完整**：Supporting_Information.docx 含 Supplementary Tables S1–S7，与正文引用一致。

---

## 四、Questions for the authors（请作者回答）

1. **核心基因数 4,055 的来源是什么？** docx 表 2 注释与 STROBE item 15 写"4,055-gene core / 4,055-gene Stouffer meta signature"，但稿件正文从未定义该数（全文统一为 2,750）。请说明：(a) 4,055 是否为旧草稿残留？还是 (b) `in_meta_core` 实际来自一个正文未定义的签名集？请消歧并统一。
2. **GitHub v1.4.0 的 tag/release 是否真正公开发布？** 数据可用性声明的可信度完全依赖于此；请确认非本地/草稿 tag，且包含 README + CITATION.cff + LICENSE + 复现脚本。
3. **嵌入 PNG 的真实 DPI 是否 ≥300？** 并确认上线投稿时每幅图会作为单独文件再传一份（PLOS 生产步骤）。
4. **参考文献作者列表是否按 PLOS 偏好补全？** 当前 2–4 人论文仅列"第一作者 et al."；是否愿意补全为全部作者（或前 3 + et al.）？
5. **报告规范覆盖面：** STROBE 是"类比"适用于唯一人类队列（GSE158825），但本研究主体为转录组 meta 分析 + ML + docking 虚拟筛选。投稿信提及"GEO/MIAME compliance"，稿件是否也明确声明 MIAME / GEO 合规以覆盖转录组输入？是否考虑为计算/ docking 部分补充适用的报告规范？

---

## 五、What I actually checked（审查动作清单）

**读取的文件：**
- `reports/MVP_PLOSONE_submission.md`（全文 387 行，逐节阅读：标题/作者/摘要/正文/方法/伦理/基金/贡献/数据可用性/竞争利益/展示项/参考文献/补充）
- `CITATION.cff`（全文 29 行）
- 解包并读取内部结构：`submission_pack/Manuscript.docx`、`Cover_Letter.docx`、`STROBE_Checklist.docx`、`Supporting_Information.docx` 的 `word/document.xml`、`word/media/`、`docProps/core.xml`

**计算的计数（非估算）：**
- 摘要词数 = **297**（去除 Markdown 粗体标记后纯文本统计）
- 标题词数 = **16**
- 参考文献条数 = **40**（顺序编号）
- 展示项枚举 = **5 图（Fig.1–5）+ 3 表（Table 1/2/3）= 8**，逐项出现在稿件第 299–386 行
- Manuscript.docx 内 `w:tbl` = **5 个对象**，定位后对应 3 个主表（含子面板），与"3 表"自报不冲突
- Manuscript.docx 内 `r:embed` = 5 处（rId10–14），`wp:anchor` = 0（全部行内嵌入），`word/media/` 含 image1–5.png

**docx 媒体 / 内嵌核查：**
- 确认 5 张图真实内嵌于 Manuscript.docx（非浮动、非外链），闭合历史"missing figures"退稿触发点
- 确认 Supporting_Information.docx 枚举 S1–S7；STROBE_Checklist.docx 覆盖 STROBE 2007 全部 22 项

**一致性交叉核对：**
- 仓库 URL + v1.4.0：稿件 ↔ 投稿信 ↔ CITATION.cff 三处一致
- 作者"Yang Y"无 MD/PhD/Dr.：稿件 ↔ docx ↔ 投稿信一致；ORCID 0009-0004-9698-6552 一致
- **发现矛盾：** "4,055" 仅出现在 docx 表 2 注释 + STROBE item 15，稿件 .md 正文 grep 为"NOT in manuscript md"（正文统一 2,750）

**在线校验：**
- 3 条样本 DOI（ref 1 / 13 / 14）`https://doi.org/...` 实时 HEAD 均返回 **HTTP 302**（可解析、有效）

---

## 六、送交前最低必改清单（优先级排序）

1. **[必须]** 统一"核心基因数"：将 docx 表 2 注释与 STROBE item 15 的"4,055-gene"改为"2,750-gene core (meta_FDR<0.05 且 consistency≥0.8)"，或显式定义 4,055 并在全文一致（发现 5）。
2. **[推荐]** 投稿信自检清单中"报告规范"条同时点名 STROBE（与 MIAME 并列），使措辞与正文一致（发现 10 / 补充观察）。
3. **[推荐]** 参考文献作者列表按 PLOS 偏好补全（发现 9）。
4. **[上线动作]** 确认 GitHub v1.4.0 tag 已公开；嵌入 PNG 真实 DPI ≥300；每图单独再传一份（发现 4 / 6）。
5. **[可选]** 对全部 40 条 DOI 跑批量解析校验；考虑为转录组/ docking 部分补 MIAME 或计算可复现性声明（补充观察）。

> 说明：除上述第 1 项（数字硬矛盾）外，其余均不构成本次 desk-reject / 技术审查退回的硬门槛；第 1 项若留到编辑初审才被发现，将引发"稿件内部不一致/数据–清单脱节"的负面信号，建议在 resubmission 前主动闭合。
