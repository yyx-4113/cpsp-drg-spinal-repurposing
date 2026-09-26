# A4 — Venue / Reporting-Standard Review (Scientific Reports)

**Reviewer role:** A4 — venue / reporting-standard editor (Nature/*Scientific Reports* submission standards, reporting-checklist honesty, format hard-fails, cover-letter↔manuscript consistency).
**Manuscript version reviewed:** v1.4 rendered text (`MVP_ScientificReports_submission.md`, `_supplementary.md`, `_cover_letter.md`, `_reporting_summary.md`). Treated as a first submission; no other reviewers' files read.

---

## 1. Nature / *Scientific Reports* format hard-fails

### 1.1 Title length — PASS
【Problem】 Title 词数需 ≤ 20；实测 18 词，合规。
【Evidence】 `submission.md:1` — "Conserved nerve-injury-associated transcriptional response on the dorsal root ganglion–spinal axis: non-predictive incision translation and an honest repurposing null"。按空白分词（连字符复合词计 1 词）计为 18 词；即便把 `ganglion–spinal` 拆开也仅 19 词，仍 ≤ 20。
【Why it matters】 标题超限是格式硬伤，触发退回；此处无风险。
【Specific fix】 无需修改。保持当前标题。

### 1.2 Abstract length — BORDERLINE（建议删减，非干净通过）
【Problem】 摘要按最宽松分词法 195 词（≤200 通过），但余量仅 5 词；按拆分连字符复合词的口径计为 221 词，已超限。
【Evidence】 `submission.md:14`。空白分词（hyphenated compounds = 1 词）：**195 词**；拆分连字符/斜杠（`nerve-injury-associated`、`dorsal root ganglion–spinal`、`random-effects`、`non-circular`、`set-level`、`size-independent`、`4,055-gene`、`SCN9A/10A/11A/8A` 等各自拆开）：**221 词**。摘要内无任何括号引用或 author-year 引用（命中 0 条），满足"no citations"要求。
【Why it matters】 *Scientific Reports* 严格执行 ≤200 词且为 unstructured。195 词仅留 5 词缓冲，一旦投稿系统的分词口径偏向拆词（许多期刊计数器对连字符复合词按多词计），即逾限被退。边界摘要还会被编辑重点审查，增加被挑刺概率。
【Specific fix】 将摘要删减至 **≤185 词**，优先删除冗余修饰：如 "drug-repurposing screen reported as a methodological boundary"（已被标题与正文覆盖）、"(median I² = 38.8%)" 可缩为 "(I² = 38.8%)"、"directional agreement with the incision model was 46.3% versus a 47.1% background (difference −0.9 pp, permutation p = 0.14)" 可缩为 "46.3% vs 47.1% background (−0.9 pp, p = 0.14)"。删 10–15 词即可建立安全余量。

### 1.3 Display items ≤ 8 (main text) — PASS
【Problem】 主文展示项须 ≤ 8；实测恰好 8。
【Evidence】 `submission.md:201` 自述 "5 figures + 3 tables = 8"。核对：Fig.1–Fig.5（5 图，:205/:208/:211/:214/:217）；Table 1（含 1a/1b，:222–231）、Table 2（:235）、Table 3（含 3a/3b，3a 内联于 :80–91，3b 于 :242）——计为 3 表。5+3=8，未超。
【Why it matters】 超 8 项须挪入补充材料，属格式硬伤；此处合规。
【Specific fix】 无需修改。确认投稿系统将 3a/3b 作为 Table 3 子表而非独立展示项计数（当前处理正确）。

### 1.4 Figure legends ≤ 350 words each — PASS
【Problem】 每幅图注须 ≤ 350 词；五幅图注均远低于上限。
【Evidence】 逐图统计（按科学词元）：Fig.1 `:206` = 187 词；Fig.2 `:209` = 165 词；Fig.3 `:212` = 118 词；Fig.4 `:215` = 166 词；Fig.5 `:218` = 174 词。最大值 187 < 350。
【Why it matters】 图注超 350 词为格式问题，可退回；此处无风险。
【Specific fix】 无需修改。

### 1.5 Figure resolution ≥ 300 DPI — PASS（已核验文件元数据）
【Problem】 图须 ≥300 DPI；五张 PNG 元数据均记录 350 DPI。
【Evidence】 `figures/Fig1–Fig5_*.png` 文件头 DPI = (350.012, 350.012) ×5。投稿包 `submission_pack/` 内含同一组 PNG（:Fig1–Fig5）。
【Why it matters】 低于 300 DPI 会被要求重交；此处达标。
【Specific fix】 无需修改。上传前再次确认投稿系统读到的为该 350 DPI 版本（勿误传草稿低分辨率图）。

### 1.6 References — Nature style, ≤60, numbered by first citation, all cited — PASS
【Problem】 参考文献须为 Nature 样式、≤60 条、按首次引用编号、无未引用条目；实测 24 条，全合规。
【Evidence】 `submission.md:157–180` 共 24 条。样式示例 `Macrae, W. A. Chronic postsurgical pain: 10 years on. *Br. J. Anaesth.* **119** (Suppl. 1), i3–i4 (2017)` 符合 Nature 样式。编号顺序：1–9 首引于引言（:20–24），10–14 首引于结果（:40/:70/:72/:93），15–24 首引于讨论（:101，其中 15–20 以范围 `¹⁵–²⁰` 一次性引用，16–19 因而被涵盖）。逐条核验 1–24 均在正文出现，无"幽灵引用"。
【Why it matters】 未引用文献或编号错序是低级硬伤；此处无。
【Specific fix】 无需修改。仅建议确认 `¹⁵–²⁰` 范围引用在排版后不被误拆为独立上标。

---

## 2. Data Availability statement honesty（重点）

### 2.1 核心声明"GitHub 仓库已包含所有处理数据"——当前本地仓库状态下**不成立**
【Problem】 稿件称 GitHub 仓库"already contains all processed data"并点名 5 个文件，但按当前本地仓库状态，这些文件并不在版本控制中，声明若今日投稿即为不实。
【Evidence】 `submission.md:191` 列举：`META_bulkonly_sensitivity_summary.json`、`P6_target_plausibility.json`、`_R4_random_effects_meta.csv`、`_R4_nerveinjury_only_meta.csv`、`_R4_targetset_bootstrap.csv`，外加 `figures/` 五图与 `scripts/p7_targetset_bootstrap.py`/`p3_hub_bootstrap.py`。核验 Git 跟踪状态：上述 5 个命名数据文件 **NOT TRACKED**（仅 `scripts/p3_ml.py` 被跟踪）；`figures/` 目录被 `.gitignore:11` 显式忽略（`figures/` 一行），故五张图**永不会被提交**；`scripts/p7_targetset_bootstrap.py` 与 `scripts/p3_hub_bootstrap.py` 亦为未跟踪。仓库内 `results/tables/` 另有 109 个被跟踪文件，但稿件点名的这 5 个核心文件恰不在其中。
【Why it matters】 *Scientific Reports* 要求 Data Availability 如实且可验证；编辑/审稿人会点击仓库链接核验。当前状态下公开仓库（除非作者已单独特例强制推送）**不含图表、不含稿件点名的 5 个 JSON/CSV、不含 p7 脚本**——声明与事实不符，轻则被要求补存后接受，重则被视为数据可用性不实。这是本次审查最高优先级的诚信风险。
【Specific fix】 二选一，且须在投稿前落地：(a) 实际入库——`git add -f figures/`（因被忽略需 `-f`）并提交那 5 个命名文件与 p7/p3_hub 脚本，确认已 `git push` 到公开仓库，再保留原声明；或 (b) 若暂不公开，将声明改为"processed data will be deposited in the public GitHub repository upon acceptance / mirrored to Zenodo with a citable DOI"，并删除"already contains"这一现在时态断言。严禁保留"already contains all processed data"却不实际推送。

### 2.2 Reporting Summary 的 Data Availability 与主文一致——PASS（但依赖 2.1 修正）
【Problem】 Reporting Summary 的 Data Availability 段与主文措辞一致，本身无矛盾；但其真实性同样取决于 2.1 的入库动作。
【Evidence】 `reporting_summary.md:25`："All code/tables/figures in the public GitHub repository … processed data mirrored to Zenodo (DOI on acceptance); not 'available on request'。" 与主文 `:191` 口径一致。
【Why it matters】 两处一致性好，但若 2.1 文件未实际入库，两处会同时失真。
【Specific fix】 随 2.1 一并落地；推送后建议在两处均保留"not available on request"的强硬措辞（符合期刊偏好）。

---

## 3. Cover letter ↔ manuscript mismatches

### 3.1 标题完全一致、无夸大、无撤回性矛盾——PASS
【Problem】 投稿信标题须与稿件标题逐字一致，且不得比稿件（现为诚实零结果框架）更夸大；实测一致且克制。
【Evidence】 `cover_letter.md:3` 标题与 `submission.md:1`、`supplementary.md:3` 三者完全相同（18 词长标题）。投稿信 :11 称"honest null"、:13 明示随机效应下核心由 4,055 缩至 1,008、57.3% 主核心依赖 translatome、对接靶集不可复现，:15 明言"we draw no therapeutic priority from the screen"——与稿件诚实零结果框架一致，未宣称疗效或优先级。
【Why it matters】 投稿信夸大或标题不符会触发编辑对全文可信度的质疑；此处无。
【Specific fix】 无需修改。

### 3.2 投稿信自检清单断言"无 [truncated]/版本/轮次残留"——与事实一致（见第 6 节）
【Problem】 投稿信 :27 自检项含 "No `[truncated]` / version / round tokens remaining"，该断言对渲染稿件成立。
【Evidence】 见第 6 节：四份渲染文件中确实无 `[truncated]`、`Round-3`、`v1.3`、`v1.4`、`REVIEW_`、`RESPONSE_` 残留。
【Why it matters】 若渲染稿含此类残留而清单谎称无，属诚信问题；此处清单如实。
【Specific fix】 无需修改；保留该自检项。

---

## 4. Reporting Summary completeness

### 4.1 必填模块齐备、AI 使用披露一致——PASS
【Problem】 Nature Reporting Summary 要求覆盖 Statistics / Software / Data / 人/动物/特定材料 / Competing interests / AI 披露；实测齐备且 AI 披露跨文档一致。
【Evidence】 `reporting_summary.md`：Statistics(:8–18)、Software and code(:20–22)、Data(:24–26)、Human participants(:28–33)、Animal research(:35–36)、Field-specific(:38–43)、Specific materials(:45–48)、Competing interests(:50–52)、AI disclosure(:54–55)。AI 披露："An LLM assisted manuscript drafting/language polishing; scientific content … authored and verified by Y.Y. No LLM is an author." 与主文 `submission.md:148` 的"large language model (LLM) was used to assist manuscript drafting and language polishing … no LLM satisfies authorship criteria"一致。
【Why it matters】 缺失必填模块或 AI 披露不一致会被退回补表；此处合规。
【Specific fix】 无需修改。补充提示：Statistics 段(:40)引用内部文件 `P5_RESULTS.md §1` 作为数据排除依据——可接受，但确保该文件在仓库中可查（见 2.1 入库纪律，避免再次因未跟踪而失联）。

### 4.2 负向披露充分——PASS
【Problem】 生命科学研究中动物/人/抗体等项须作负向披露而非留白；实测规范。
【Evidence】 `reporting_summary.md:35–36` "We performed no new animal experiments"；:45–46 "Antibodies / Eukaryotic cell lines … N/A (public data)"；:47 "Clinical data: human miRNA data are public de-identified"。均用负向措辞，未写"n/a"留白。
【Why it matters】 模板禁止在禁填处写 n/a；此处处置正确。
【Specific fix】 无需修改。

---

## 5. Internal consistency of derived artefacts

### 5.1 CITATION.cff 标题与稿件标题**不一致**——FINDING
【Problem】 仓库内 `CITATION.cff` 的 title 字段与稿件标题不同，属派生产物一致性门控失败。
【Evidence】 `CITATION.cff` 中 `title: "Multi-dataset target lock-in and structure-based drug repurposing for chronic postsurgical pain"`，而稿件标题（`submission.md:1`、`supplementary.md:3`、`cover_letter.md:3`）为 "Conserved nerve-injury-associated transcriptional response on the dorsal root ganglion–spinal axis: non-predictive incision translation and an honest repurposing null"。两者完全不同。稿件 Data Availability(:191) 明确称仓库含 "README + CITATION.cff + MIT LICENSE"，故 CITATION.cff 是读者/引文会看到的元数据。
【Why it matters】 引文元数据标题与发表标题不符会造成引文错配、被质疑稿仓管理粗糙；若期刊或 Zenodo 直接读取 CITATION.cff 生成引文，将产生错误题名。
【Specific fix】 将 `CITATION.cff` 的 `title` 改为与稿件标题逐字一致；同步核对 `CITATION.cff` 的 `authors`、`date`、`license`(MIT) 与稿件署名/声明一致。

### 5.2 标题跨三份渲染稿一致；无版本/日期二次出现不符——PASS
【Problem】 标题在 submission / supplementary / cover letter 三处一致；渲染稿内无第二处版本串或访问日期需核对。
【Evidence】 标题字符串在 `submission.md`、`supplementary.md`、`cover_letter.md` 中三者完全相同；`reporting_summary.md` 不重复标题（非必需）。渲染四稿中均无 "v1.4"/"Round-"/访问日期在多处出现而彼此冲突的情形。
【Why it matters】 派生题名/版本二次出现不一致是常见低级错误；此处仅 5.1 一处破口。
【Specific fix】 仅修 5.1 的 CITATION.cff。

---

## 6. Leftover internal-version artefacts

### 6.1 四份渲染稿无 `[truncated]`/Round-3/v1.3/v1.4/REVIEW_/RESPONSE_ 残留——PASS
【Problem】 渲染稿件不得含内部版本/轮次残留标记，否则 desk-reject；实测四份渲染稿均干净。
【Evidence】 对 `submission.md`/`supplementary.md`/`cover_letter.md`/`reporting_summary.md` 全文检索 `[truncated]`、`Round-3`、`v1.3`、`v1.4`、`REVIEW_`、`RESPONSE_`、`Round N`：仅命中 `cover_letter.md:27` 自检清单中"作为文本提及"的 `No `[truncated]` …`，并非真实残留标记。注：审阅初读时稿件 :93 与 :101 显示 "[truncated]"，经复核此为长行显示截断伪影；真实文件该行末尾为完整句（"...outside the structure-based screen." 与 "...not a therapeutic recommendation."），非稿件内容截断。
【Why it matters】 真实残留版本/轮次标记是即时退稿触发项；此处渲染稿无。
【Specific fix】 无需修改渲染稿。但见 6.2 关于投稿包内部分内部文件的提示。

### 6.2 投稿包含内部清单文件（带 v1.4 名）——建议勿入公开仓库
【Problem】 `submission_pack/` 内含 `GITHUB_PUSH_LIST_v1.4.md` 与 `SUBMISSION_MANIFEST.md`（文件名/内容带版本号），若一并提交至公开 GitHub 仓库会泄露内部轮次信息。
【Evidence】 `submission_pack/` 目录含 `GITHUB_PUSH_LIST_v1.4.md`、`SUBMISSION_MANIFEST.md`（按独立性约束未读取其内容，仅据文件名与第 6.1 检索确认渲染稿件本身干净）。
【Why it matters】 公开仓库出现 "v1.4"/"push list"/"manifest" 类文件虽非稿件硬伤，但会被视作稿仓卫生差，且与 Data Availability 声明的"干净公开仓库"印象冲突。
【Specific fix】 仅将 `Manuscript.docx`、`Supporting_Information.docx`、`Cover_Letter.docx`、`Reporting_Summary.md` 与 `Fig1–Fig5.png` 作为投稿/公开产物；`GITHUB_PUSH_LIST_v1.4.md`、`SUBMISSION_MANIFEST.md` 等内部清单留在本地，勿 `git add` 进公开仓库。

---

## § Stands up（成立项，附证据）

1. **标题合规且三稿一致**：`submission.md:1`/`supplementary.md:3`/`cover_letter.md:3` 18 词长标题完全相同，≤20 词（实测 18），无标题不符风险。
2. **展示项与图注合规**：主文 5 图 + 3 表 = 8 项（`:201`），五图注最高 187 词 < 350（:206/:209/:212/:215/:218），五图 PNG 元数据 350 DPI，均满足硬限。
3. **参考文献合规**：24 条 Nature 样式、编号按首次引用、1–24 全部被引（15–20 以范围引用涵盖），无未引/错序（`:157–180`）。
4. **投稿信与稿件框架一致且无夸大**：`:3` 标题一致，`:11–15` 维持诚实零结果框架、明确"不抽取治疗优先级"，无撤回性矛盾。
5. **Reporting Summary 齐备且 AI 披露跨文档一致**：必填模块全覆盖（:8–55），AI 使用披露与 `submission.md:148` 一致。
6. **渲染稿无版本/轮次残留**：四稿检索无 `[truncated]`/`Round-3`/`v1.3`/`v1.4`/`REVIEW_`/`RESPONSE_` 真实标记（6.1）。

---

## § Questions for the authors

1. Data Availability 声称为"already contains all processed data"，但 `figures/` 被 `.gitignore` 忽略、点名的 5 个 JSON/CSV 与 p7 脚本均未跟踪——请确认公开 GitHub 仓库**实际**已含这些文件（含强制 `git add -f figures/`），还是需改为"upon acceptance"措辞？
2. 摘要按空白分词 195 词、按拆连字符 221 词——贵方投稿时采用哪种分词口径？是否接受删至 ≤185 词建立安全余量？
3. `CITATION.cff` 标题与稿件标题不同，是否为旧版本遗留？是否计划改为与稿件逐字一致？
4. `submission_pack/GITHUB_PUSH_LIST_v1.4.md` 与 `SUBMISSION_MANIFEST.md` 是否会被一并推入公开仓库？建议仅公开六类产物（见 6.2）。

---

## § What I actually checked

**读取文件（4 份目标稿，按独立性约束未读其他审稿人文件）：**
- `reports/MVP_ScientificReports_submission.md`（253 行）
- `reports/MVP_ScientificReports_supplementary.md`（302 行）
- `reports/MVP_ScientificReports_cover_letter.md`（27 行）
- `reports/MVP_ScientificReports_reporting_summary.md`（56 行）
- 附带只读（非禁读清单内）：`CITATION.cff`、`.gitignore`（用于一致性/数据可用性核验）

**实测计数与核验：**
- 标题词数：18（空白分词）。
- 摘要词数：195（空白分词）/ 221（拆连字符）；引用命中：0。
- 主文展示项：5 图 + 3 表 = 8；图注词数：187/165/118/166/174（均 ≤350）。
- 五图 PNG DPI：(350.012, 350.012) ×5。
- 参考文献：24 条，全部被引（15–20 范围引用涵盖 16–19）。
- 数据可用性核验（Git 层）：`figures/` 被 `.gitignore:11` 忽略；稿件点名的 `META_bulkonly_sensitivity_summary.json`、`P6_target_plausibility.json`、`_R4_random_effects_meta.csv`、`_R4_nerveinjury_only_meta.csv`、`_R4_targetset_bootstrap.csv`、`scripts/p7_targetset_bootstrap.py`、`scripts/p3_hub_bootstrap.py` 均 **NOT TRACKED**；`results/tables/` 有 109 个被跟踪文件但上述 5 个命名文件不在其列。
- CITATION.cff 标题："Multi-dataset target lock-in and structure-based drug repurposing for chronic postsurgical pain"（与稿件标题不符）。
- 残留标记检索（四稿）：仅 `cover_letter.md:27` 自检文本提及 `[truncated]`，无真实残留；`:93`/`:101` 看似截断实为长行显示伪影，真实文件行尾为完整句。
- 投稿包检索：含 `GITHUB_PUSH_LIST_v1.4.md`、`SUBMISSION_MANIFEST.md`（内部文件，建议勿入公开仓库）；渲染稿件本身无版本/轮次残留。

**与预期的主要偏差（discrepancies）：**
- 预期数据可用性声明可成立，实则当前仓库状态下不成立（figures 被忽略 + 命名文件未跟踪）→ 列为最高优先级诚信风险（第 2.1 节）。
- 预期 CITATION.cff 与稿件标题一致，实则不同（第 5.1 节）。
- 预期摘要干净 ≤200，实则边界（195/221 取决于分词口径）→ 建议删减（第 1.2 节）。
- 初读稿件 :93/:101 的 "[truncated]" 经复核为显示伪影，非真实内容截断，故第 6.1 判定为 PASS 而非硬伤。
