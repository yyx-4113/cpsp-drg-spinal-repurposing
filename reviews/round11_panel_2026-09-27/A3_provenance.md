# A3 实现 / 溯源审计评议（Implementation / Provenance audit）

**角色**：独立同行评审小组中的 A3——实现与溯源审计员（生物信息学可重复性）。
**任务**：确认稿件中每一个数字都能追溯到一次正确的源计算，并审计“产出这些数字的代码”（而非只是包装/汇总层）。
**独立性声明**：本评议仅依据小组授权范围内文件撰写（`reports/MVP_PLOSONE_submission.md`、`reports/MVP_PLOSONE_supplementary.md`、`reports/MVP_PLOSONE_cover_letter.md`、`reports/MVP_PLOSONE_compliance_check.md`、`reports/MVP_STROBE_checklist.md`、`results/tables/*.csv|json`、`scripts/*.py`、`CITATION.cff`）。未读取任何 `REVIEW_*.md`、`RESPONSE_*.md`、`REVISION_*.md`、其他审稿人文件或 `reviews/_quarantine/`。按“首次投稿”处理。

---

## § 一、经得起核验的部分（Stands up，均附证据）

> 以下结论均建立在“从活跃（active）源文件独立重算”之上，而非信任稿件自陈。重算严格沿用稿件 Methods 给出的定义：Stouffer 权重 w = √(n_case·n_ctrl/(n_case+n_ctrl))，核心签名 = meta_FDR < 0.05 且方向一致 ≥ 0.8（6 输入 → ≥5/6；bulk-only 4 输入 → 严格 ≥4/4、宽松 ≥3/4）。

**1. 全部头号数字可从活跃源 CSV/JSON 独立重算并逐一对齐。**
- 核心签名 `META_DRG_axis_CORE_signature.csv` 行数 = **4,055**（与稿件一致；meta_FDR<0.05 基因 6,869，基因测试总数 16,552，见 `MVP_PLOSONE_submission.md:305` 与 `MVP_PLOSONE_supplementary.md:202`）。
- bulk-only 敏感分析活跃文件 `META_bulkonly_sensitivity_summary.json`：`bulk_only_core_size=2512`、`overlap=2202`、`overlap_pct_primary=54.3157`。独立重算严格重叠 **2,202/4,055 = 54.30%**（稿件 54.3% ✓）；宽松（core ∩ bulk FDR<0.05 且一致≥0.75）**3,587/4,055 = 88.46%**（稿件 88.5% ✓）；`32/35` hub 落在 meta 核心内（稿件 `MVP_PLOSONE_submission.md:62` “32/35 (91%)” ✓）。
- bootstrap 活跃文件 `_R4_targetset_bootstrap.json`：hub 集中位数 **43**、Jaccard 中位数 **0.304**、dock-eligible_17 均值 **8.695→8.70**、P(≥3)=**1.000**、P(≥5)=**0.990**、docked_9 均值 **3.93**、P(≥3 of 9)=**0.830**。稿件 `:66`、`:263-266`、`:270` 全部对得上。
- LODO 泄漏控制文件 `P3_lodo_auc_ci_leakage_controlled.csv`：incision 折叠 **0.6771 [0.3735, 0.9405]**（稿件 `:64`、`:291` 0.677 [0.374, 0.940] ✓）。
- 随机效应敏感核心：活跃源 `_R4_random_effects_meta.csv` 派生 **1,008**（占固定效应核心 24.86%，稿件 24.9% ✓）；collapse 敏感 5 输入核心 **4,294**，保留 3,707/4,055 = 91.4%（稿件 `:305`、`:122` “91%” ✓）。
- **结论**：没有任何头号数字被捏造或与活跃源冲突。

**2. 图 2A 与泄漏控制数据一致，0.917 被正确地标为“原始（非泄漏）”且仅出现在 Methods。**
- `scripts/make_sr_figures.py` 读取 `P3_lodo_auc_ci_leakage_controlled.csv`，axvline 取 **0.677** 并标注 “cross-animal floor 0.677”，面板标题为 “A. Generalisation (LC-LODO, leakage-controlled)”，**无 0.917 线**。DPI=350（≥300 达标）。
- 稿件 `MVP_PLOSONE_submission.md:64` 给出的 0.917 `[0.729, 1.000]` 明确标注为“raw (non-leakage) … GSE267799”，且其数值与原始非泄漏文件 `P3_lodo_auc_ci.csv`（0.9167 [0.7291, 1.0]）一致。
- **结论**：不存在“图与数据打架”或“把泄漏 AUC 当诚信结论”的缺陷。

**3. Visium（33/35）与脊髓 snRNA（33/35）是两个不同数据集，稿件未混为一谈。**
- `P5_GSE325938_hub_regionalization.csv`：35 行，CRISP3 与 LNP1 `present=False`（全零），故 Visium 可检 **33/35**，其中 17/33 定位背角（51.5%，见 `MVP_PLOSONE_submission.md:297`）。
- `P5_GSE328175_SC_ShamSNI_hub_localisation.csv`：35 个符号中仅 **33** 个唯一符号（缺 CRISP3、REG3B），故 snRNA 为 **33/35**（见 `MVP_PLOSONE_submission.md:164`）。
- 两份表“缺的基因不同”（Visium 缺 CRISP3+LNP1；snRNA 缺 CRISP3+REG3B），稿件将二者作为“多谱系一致性”与“空间区域化”两个独立证据呈现，**未合并为一个 33/35 声称共享缺失基因**。这是正确的。

**4. 作者主动披露了被取代的探索性产物——溯源自觉。**
- 稿件 `MVP_PLOSONE_submission.md:56` 明确说明探索性 `_R4_translation_noncircular.csv` 的 14,445/3,564 分母“被取代”，统一采用 14,390/3,556。
- 稿件 `:152`、`:305` 明确把旧的全四交集计数 **1,981** 标为“superseded”，改用 2,202/4,055。这说明作者自己在维护源数据的版本纪律（详见 § 3.5 归档 vs 活跃 源纪律）。

**5. 活跃一致性门 `p7_consistency_gate.py` 的设计是正确的。**
- 该脚本通过 `chk()` 辅助函数**从源 CSV/JSON 读取期望值**（例如 `chk("bulk-only core", j["bulk_only_core_size"], "2,512")`，bootstrap 值由 `bt["dock_eligible_17"]["mean_recovered"]` 现算而非硬编码）。这是“从源派生期望值”的恰当写法，应当保留为唯一权威门。

**6. 补充表 S7 与稿件 Table 3 的 docking-target 数值链一致。**
- `MVP_PLOSONE_supplementary.md:240-249`（S6 Panel D）逐靶给出 Z(FE)/FDR(FE)/Z(RE)/FDR(RE)；与稿件 `MVP_PLOSONE_submission.md:96-110`（Table 3a/3b）逐行吻合（例如 TNIK 8.00/4.3e-13/RE 0.0212 ↔ 稿件 8.00/4.3e-13/FDR_RE 0.021；SLC2A1 6.83/6.3e-10/RE 7.02e-08 ↔ 稿件 0.0000；ADRA2A 4.84/1.5e-05/RE 0.0386 ↔ 稿件 0.039）。微小第 3 位小数差异均为四舍五入，非矛盾。

---

## § 二、向作者提问（Questions for the authors）

1. **标题规范**：`CITATION.cff`（line 3）与 `scripts/build_sr_submission_pack.py`（line 50）仍使用旧标题 “……non-predictive incision translation and an honest repurposing null”，而稿件/cover letter/compliance 使用新标题 “……dorsal root ganglion analysis with spinal-cord localisation and honest repurposing null”。请确认哪一个是投稿版规范标题，并统一所有出处的“单一规范位置”。（详见 T1-A）

2. **S5a 与 S5b 的 perm p 口径**：补充表 S5a 神经炎症 perm p = 0.003，而 S5b（集合水平 BH）同集合 perm p (FE) = 0.0004998（地板值）。两套表是否使用了不同分辨率的置换检验？若如此，请在表注中显式说明，避免读者误判为矛盾。（详见 T2-C）

3. **“211 个不在 bulk 中显著”的真实拆分**：稿件称 “only 211 primary-core genes are not bulk-significant at all”（`:305`、`:152`）。我们的独立重算显示这 211 个是“存在于 bulk meta 但 bulk meta_FDR ≥ 0.05”，另有 **102** 个在 bulk meta 中完全缺失（K<3，未被评估）。请确认 211 是否排除了这 102 个，并在文中显式拆分“present-but-NS（211）”与“absent-from-bulk（102）”。（详见 T3-A）

4. **残留门的处置**：`scripts/gate_consistency.py` 是否仍被任何 CI/README 调用？它是 Scientific Reports 时期遗留、且硬编码期望字符串（见 T1-B）。请确认投稿流程只依赖 `p7_consistency_gate.py`，并将 `gate_consistency.py` 与陈旧产物 `scripts/_gate_out.txt` 移出可发布树或明确标注“deprecated”。

5. **bootstrap 产物快照**：`scripts/_gate_out.txt` 显示 p7 门上一次“通过”是基于旧数据（bulk-only 1,981；bootstrap 0.79/0.04/0.026；references = 26）。这些数据重算后是否重跑过门？请提交以活跃源（2,512 / 43 / 8.70 / 0.304 / 1.000 / 37 refs）为基准的新门产物。（详见 T2-A）

6. **背角 17/33 的分母一致性**：稿件 Fig.4B（`:297`）称 “17 of 33 (51.5%) map to the dorsal horn”，而 Methods `:164` 同时列出 “CDHR5, SERPINE1, VIP, REG3B, ANKRD1, plus the all-zero CRISP3 and LNP1” 为 below-floor。请确认 17/33 的“33”是“Visium 可检 33 hub”（已排除 CRISP3/LNP1），且 17 个均通过 5% 检测地板——这与 S2 footnote `:93` 一致，但建议在 Fig.4B 图注显式写清分母定义。

---

## § 三、我实际核查了什么（What I actually checked）

### 3.1 文件清单
- 稿件/补充/cover/compliance/STROBE：`reports/MVP_PLOSONE_*.md`（逐段比对）。
- 活跃源表：`META_DRG_axis_CORE_signature.csv`、`META_bulkonly_meta.csv`、`META_bulkonly_sensitivity_summary.json`、`_R4_targetset_bootstrap.json`、`_R4_targetset_bootstrap.csv`、`P3_lodo_auc_ci_leakage_controlled.csv`、`P3_lodo_auc_ci.csv`、`P5_GSE325938_hub_regionalization.csv`、`P5_GSE328175_SC_ShamSNI_hub_localisation.csv`、`_R4_geneset_setlevel_bh.csv`、`_R4_random_effects_meta.csv`、`_R4_targets_fixed_vs_random.csv`。
- 归档源表（仅确认未被引用）：`results/tables/_archive/_R3_bulkonly_meta_summary.json`（1981/42.7%）。
- 脚本：`scripts/make_sr_figures.py`、`scripts/build_sr_submission_pack.py`、`scripts/p7_consistency_gate.py`、`scripts/gate_consistency.py`。
- 元数据：`CITATION.cff`、陈旧门产物 `scripts/_gate_out.txt`。

### 3.2 独立重算 vs 稿件（完整登记册）
| # | 数字 | 源文件独立重算 | 稿件位置/声称 | 判定 |
|---|---|---|---|---|
| 1 | 核心签名规模 | 4,055 | `:305` 4,055 | ✓ |
| 2 | 基因测试总数 | 16,552 | `:202`/`:305` 16,552 | ✓ |
| 3 | meta_FDR<0.05 基因 | 6,869 | `:305` 6,869 | ✓ |
| 4 | bulk-only 核心 | 2,512 | `:152`/`:305` 2,512 | ✓ |
| 5 | 严格重叠 | 2,202/4,055 = 54.30% | `:152` 54.3% | ✓ |
| 6 | 宽松重叠 | 3,587/4,055 = 88.46% | `:152` 88.5% | ✓ |
| 7 | hub∈meta 核心 | 32/35 = 91.4% | `:62` 32/35 (91%) | ✓ |
| 8 | RE 核心 | 1,008 (24.86%) | `:203`/`:305` 1,008 (24.9%) | ✓ |
| 9 | collapse 核心 | 4,294；保留 3,707/4,055=91.4% | `:305` 91.4% | ✓ |
| 10 | bootstrap hub 中位数 | 43 | `:66`/`:270` 43 | ✓ |
| 11 | Jaccard 中位数 | 0.3039→0.304 | `:270` 0.304 | ✓ |
| 12 | dock-eligible 均值 | 8.695→8.70 | `:263`/`:66` 8.70 | ✓ |
| 13 | P(≥3 of 17) | 1.000 | `:266` 1.000 | ✓ |
| 14 | P(≥5 of 17) | 0.990 | `:267` 0.990 | ✓ |
| 15 | docked 均值 | 3.93 | `:263` 3.93 | ✓ |
| 16 | P(≥3 of 9) | 0.830 | `:266` 0.830 | ✓ |
| 17 | LODO incision | 0.6771 [0.3735,0.9405] | `:64`/`:291` 0.677 [0.374,0.940] | ✓ |
| 18 | raw incision (非泄漏) | 0.9167 [0.7291,1.0] | `:64` 0.917 [0.729,1.000] | ✓ |
| 19 | 非圆形翻译 | 46.2% vs 47.1% 背景, p=0.14 | `:223`/`:134` | ✓ |
| 20 | Visium 可检 | 33/35 | `:297` 33/35 | ✓ |
| 21 | snRNA 可检 | 33/35 | `:164` 33/35 | ✓ |
| 22 | 背角定位 | 17/33 = 51.5% | `:297` 17/33 (51.5%) | ✓ |
| 23 | 参考条目数 | 37 | cover/compliance 37；`:180-257` 37 条 | ✓ |

### 3.3 发现的差异（discrepancies）
- **标题不一致**（T1-A）：稿件新标题 vs `CITATION.cff`/build 脚本旧标题。
- **陈旧门产物**（T2-A）：`scripts/_gate_out.txt` 快照为旧数据（1,981/0.79/0.04/0.026/26 refs）。
- **循环验证残留门**（T1-B）：`gate_consistency.py` 硬编码 "0.917"（line 92、200）、"53.9%"、"7,751/14,390"、"69.5%"、"17 of 33"（line 199-200）、"references = 37"（line 214）。注意这些值中多数仍是当前正确值，故门“不会报错”但**无法发现任何数字错误**——它只断言字面串存在。
- **S5b Sigma1 重复行**（T2-B）：`MVP_PLOSONE_supplementary.md:190-191` 连续两行完全相同 “Sigma1 | 1 | — | — | — | — | no”。
- **S2 “Present” 列语义碰撞**（T2-D）：CRISP3/LNP1 在 S2 显示 `Present=1`（`:79`、`:83`），但源 `P5_GSE325938_hub_regionalization.csv` 中 `present=False`（全零）。两处 `present` 含义不同，需重命名列避免歧义。
- **“211”口径**（T3-A）：见 §二 Q3。
- **S5a/S5b perm p 口径**（T2-C）：见 §二 Q2。
- **背角分母**（Q6/T3 相关）：见 §二 Q6。

### 3.4 审计过的脚本（逐条）
- `make_sr_figures.py`：正确读取泄漏控制文件、axvline 0.677、面板标题 “LC-LODO, leakage-controlled”、DPI 350。✓ 无 0.917 线。
- `build_sr_submission_pack.py`：`MS_TITLE` 用旧标题（line 50），会生成错误标题的 .docx。✗（T1-A）
- `p7_consistency_gate.py`：从源派生期望值（如 `chk("bulk-only core", j["bulk_only_core_size"], "2,512")`；bootstrap 值由 `bt[...]["mean_recovered"]` 现算）。✓ 应作为唯一权威门。
- `gate_consistency.py`：硬编码期望串、Scientific Reports 遗留门、journal 语境不符。✗（T1-B）

### 3.5 归档 vs 活跃 源纪律（lens 第 2 项）
- 归档文件 `results/tables/_archive/_R3_bulkonly_meta_summary.json` 含 `bulk_only_core_size=1981`、`overlap=1732`、`overlap_pct_primary=42.7127`——这是被取代的旧计数。
- 检索稿件与 cover/compliance/STROBE 全树：1981 与 42.7% 仅以“被取代（superseded）”措辞出现（`MVP_PLOSONE_submission.md:152` “an earlier … count of 1,981 is superseded”；`:305` 同义），**无任何活跃正文把 1981/42.7% 当作当前结论**。稿件已正确切换到活跃文件 `META_bulkonly_sensitivity_summary.json`（2,512/2,202/54.3157）。
- 唯一仍“吸附”旧值 1981 之处是陈旧门产物 `scripts/_gate_out.txt:7`（见 T2-A），它不属于稿件正文，而是验证产物快照。
- **判定**：源纪律本身合格（活跃值已入正文、旧值仅作“取代”声明）；缺陷在于“验证产物未随源重跑”（T2-A）。

### 3.6 图件规格快速核对（PLOS ONE DPI/图例）
- Fig.1–Fig.5 均在稿件 `:287-300` 列出 PNG 路径与 ≤350 词图例；`make_sr_figures.py` 输出 DPI=350 ≥ 300，符合 PLOS ONE 要求。
- Fig.2A 图例（`:291`）与泄漏控制数据自洽（见 Stands up #2）。
- Fig.4B（`:297`）17/33 表述与 S2 一致，但分母定义建议显式化（见 Q6）。

### 3.7 参考条目编号连贯性
- 稿件 `:180-257` 列 37 条编号参考，首引编号与正文上标顺序一致；compliance_check 称 37/37 DOI 已解析。封面信亦写 37 refs。与 `p7_consistency_gate.py` 期望（37）及 `gate_consistency.py:214` 硬编码（37）三者当前一致——但 `gate_consistency.py` 的 37 是硬编码，详见 T1-B。

---

## § 四、必须修复清单（Must-fix，按严重度排序）

**DESK-REJECT 判定：无。** 稿件所有头号数字均可从活跃源文件独立重算且一致，未发现捏造。列出问题属标题规范化、验证门卫生与表格歧义——均为可在一轮内修复的溯源/过程缺陷，不构成直接拒稿。

---

### T1 — 高（影响发表物元数据正确性）

#### T1-A 【标题规范化冲突：CITATION.cff 与 build 脚本使用旧标题】
- **【Problem】** 三个“作者控制”的出处对投稿标题说法不一。稿件（`:1`）、cover letter、compliance 使用新标题 “Conserved nerve-injury-associated transcriptional response on the DRG–spinal axis: dorsal root ganglion analysis with spinal-cord localisation and honest repurposing null”；但 `CITATION.cff:3` 与 `scripts/build_sr_submission_pack.py:50` 仍使用旧标题 “……non-predictive incision translation and an honest repurposing null”。
- **【Evidence】** `CITATION.cff:3` 标题串以 “non-predictive incision translation” 结尾；`build_sr_submission_pack.py:50` `MS_TITLE = ("Conserved nerve-injury-associated transcriptional response on the dorsal root ganglion–spinal axis: non-predictive incision translation and an honest repurposing null")`；稿件 `MVP_PLOSONE_submission.md:1` 标题以 “dorsal root ganglion analysis with spinal-cord localisation” 结尾。三者直接文本比对即不一致。
- **【Why it matters】** `CITATION.cff` 是 Zenodo/GitHub v1.0.0 release 的规范元数据；`build_sr_submission_pack.py` 会把 `MS_TITLE` 烧进生成的 .docx 投稿包。若不改，发表物（仓库 release + 投稿 docx）将携带与正文不同的标题，违背“单一规范位置”原则，且会被 PLOS ONE 排版/元数据校验标为不一致。
- **【如何验证】** 全仓库检索两个标题串，确认仅剩一处规范标题；提交物应只含新标题。
- **【Specific fix】** 确定投稿版规范标题（建议采用稿件现标题），把 `CITATION.cff:3` 与 `build_sr_submission_pack.py:50` 的 `MS_TITLE` 同步为新标题；并在仓库内建立一处唯一标题常量（或在 compliance_check 中加一条“标题跨文件比对”断言），防止再次漂移。

#### T1-B 【循环验证残留门：gate_consistency.py 硬编码期望串，且不派生自源】
- **【Problem】** `scripts/gate_consistency.py` 是 Scientific Reports 投稿时期遗留的一致性门，其“通过”逻辑是**硬编码字面串断言**，而非从源 CSV/JSON 派生期望值。它无法发现数字错误——只要某串出现在稿件中即“通过”。
- **【Evidence】** `gate_consistency.py:92` `check("LODO GSE267799=0.917 ...", abs(auc-0.917)<0.01 ...)`；`:199-200` `for good in ["53.9%", "7,751/14,390", "69.5%", "17 of 33", "detection floor", "0.917"]:`；`:214` `check("references = 37", nref==37, ...)`。这些都是“字符串必须出现”式断言。此外该门声称的 journal 语境（Scientific Reports）与本次 PLOS ONE 投稿不符。
- **【Why it matters】** 此类门是典型的“循环验证陷阱”：它给人“已自动验证”的假象，实则只是检查稿件是否包含某些常数。一旦稿件数字被误改，它不会报警；反之若作者有意修订某个数（如把 0.917 标注方式改掉），它会误报失败。它不提供任何真实的溯源保证，却占用“验证通过”的叙事位置。
- **【如何验证】** 阅读 `gate_consistency.py` 全文件：所有 `check(...)` 中涉及数字/字符串处均为字面量或“in MS”式包含断言，无一处从 `results/tables/*.json|.csv` 读取后再比对。
- **【Specific fix】** 投稿流程只依赖 `p7_consistency_gate.py`（已从源派生期望值）。将 `gate_consistency.py` 移出可发布树或重命名为 `gate_consistency_SciReports_DEPRECATED.py` 并在文件头注明“不适用于本次投稿”；从 README/CI 中移除其调用。同时把 `references` 数量检查改为从稿件/参考条目动态计数，而非硬编码 37。

---

### T2 — 中（需修复，但不阻断科学结论）

#### T2-A 【门产物快照陈旧：scripts/_gate_out.txt 基于旧数据】
- **【Problem】** 一致性门的保存产物 `scripts/_gate_out.txt` 显示 p7 门上一次“通过”是基于**旧数据**，数据重算后显然未重跑门。
- **【Evidence】** `scripts/_gate_out.txt:7` `bulk-only core: '1,981' present (source 1981)`（活跃源应为 2,512）；`:19` `eligible recovered mean: '0.79 of the 17' present (source 0.79)`（活跃源应为 8.70）；同文件 bootstrap 段显示 `P(>=3 of 17): '0.040'`、`Jaccard median: '0.026'`（活跃源 P≥3=1.000、Jaccard=0.304）；`:70` `[PASS] references = 26`（稿件现为 37）。
- **【Why it matters】** 这个快照如果被人当作“最近一次验证记录”引用，会给出完全错误的保证（它说 bulk-only=1,981，而稿件已明确说 1,981 被取代）。它直接削弱稿件“可重复”主张的可信度，并与 § 3.5 已确认的“活跃源已切换”形成矛盾展示。
- **【如何验证】** 比对 `_gate_out.txt` 中各值与 `META_bulkonly_sensitivity_summary.json`、`_R4_targetset_bootstrap.json` 当前值，逐项不一致。
- **【Specific fix】** 用活跃源重跑 `p7_consistency_gate.py`，生成以 2,512 / 43 / 8.70 / 0.304 / 1.000 / 37 refs 为基准的新 `_gate_out.txt`（或覆盖/删除旧文件并在说明中标注生成日期）。提交物中应只包含反映当前数据的门产物。

#### T2-B 【补充表 S5b 的 Sigma1 重复行】
- **【Problem】** 补充表 S5b（集合水平 BH 校正）在末尾把 Sigma1 列了**两遍完全相同的行**。
- **【Evidence】** `MVP_PLOSONE_supplementary.md:190` 与 `:191` 均为 `| Sigma1 | 1 | — | **—** | — | — | no |`。
- **【Why it matters】** 属表格语法/重复缺陷。虽两行内容相同、不影响数值，但会被排版与审稿人视为粗心；若后续用脚本解析该表，重复行还可能污染“集合数=19”的计数（S5b 表注称 18 多成员 + Sigma1 单成员 = 19，若 Sigma1 算两遍会变成 20）。
- **【如何验证】** 直接查看 `:188-191` 四行：TRP_channels 后紧跟两行 Sigma1。
- **【Specific fix】** 删除 `:191` 的重复 Sigma1 行，仅保留一行；并确认 S5b 集合总数（18 多成员 + Sigma1 单成员 = 19）与表注一致。

#### T2-C 【S5a 与 S5b 的 perm p 口径需对齐/说明】
- **【Problem】** 同一集合“神经炎症”在 S5a 显示 perm p = 0.003，在 S5b（集合水平 BH）显示 perm p (FE) = 0.0004998（即 1/2001 地板值）。两套表若使用不同置换分辨率，读者会误以为矛盾。
- **【Evidence】** `MVP_PLOSONE_supplementary.md:146` 神经炎症 `… 4.94 | 0.003 | 100% up …`；`:172` 同集合 `| Neuroinflammation | 19 | 0.0004998 | **0.002999** | …`（BH q 列地板值 0.0004998）。S5b 表注（`:168`）说明“values at the floor are reported as an upper bound”，但 S5a 未对 0.003 与 S5b 的 0.0004998 关系作说明。
- **【Why it matters】** 属口径透明度问题。两套 perm p 来自不同检验（S5a 可能为基因级集合均值置换，S5b 为跨集合集合级置换），但表内未显式声明，易被误读为同一统计量的不一致结果。
- **【如何验证】** 比对 S5a 与 S5b 同源集合（Neuroinflammation/Complement/DAM_microglia）的 perm p 列：S5a 给 0.003 量级，S5b 给 0.0004998 地板，二者系统偏移一个数量级。
- **【Specific fix】** 在 S5a 与 S5b 表注中各加一句，说明两套 perm p 的分辨率/层级差异（S5a 为集合内基因级、S5b 为跨集合集合级，地板 1/2001≈0.0005），并确认 0.0004998 是地板上界而非精确值。

#### T2-D 【补充表 S2 “Present” 列语义与源 CSV `present` 字段名碰撞】
- **【Problem】** 补充表 S2 的 “Present” 列对所有 35 个 hub 均标 1（含 CRISP3、LNP1），但源 `P5_GSE325938_hub_regionalization.csv` 中 CRISP3、LNP1 的 `present=False`（全零，未检出）。两处 `present` 含义不同，列名相撞易误导。
- **【Evidence】** `MVP_PLOSONE_supplementary.md:79` `| CRISP3* | 1 | MeningealFibro | 0 | 0 | 0 | 0 | broad/low | …`；`:83` `| LNP1* | 1 | MeningealFibro | 0 | 0 | 0 | 0 | broad/low | …`（Present=1 但 log2/detect 全 0）。源 CSV `present=False` 对这两行。footnote `:93` 已说明 “CRISP3 and LNP1 are all-zero”，但未解释 “Present=1” 的语义。
- **【Why it matters】** 读者看到 CRISP3 “Present=1” 与 “log2=0、detect=0” 同处一行，会困惑它到底“存在”还是“不存在”。列的命名与源字段冲突，是表—数据标签歧义。
- **【如何验证】** 将 S2 每行 “Present” 与源 CSV `present` 字段逐列比对：CRISP3/LNP1 在源为 False，在表为 1，语义不一致。
- **【Specific fix】** 将 S2 的 “Present” 列改名为 “In_35hub_set”（恒为 1，表示属于候选集）或干脆删除该冗余列；保留 “Detected_in_Visium”（对应源 `present`，CRISP3/LNP1=False）以与 Methods 的 “all-zero, excluded” 一致。

---

### T3 — 低（措辞/清晰度，建议一轮内顺手修）

#### T3-A 【“211 不在 bulk 中显著”口径略弱】
- **【Problem】** 稿件称 “only 211 primary-core genes are not bulk-significant at all”（`:152`、`:305`），但独立重算显示：211 是“在 bulk meta 中存在但 bulk meta_FDR ≥ 0.05”；另有 **102** 个在 bulk meta 中因 K<3 完全缺失（未被评估）。
- **【Evidence】** 重算拆分：present-but-NS = 211；absent-from-bulk (K<3) = 102；严格丢失 = 1,853；宽松恢复 = 1,385；仍丢失 = 468（=102+366）。
- **【Why it matters】** “not bulk-significant at all” 易被读作“bulk 评估过但不显著”，从而把 102 个从未进 bulk meta 的基因也归入“不显著”而非“未评估”，轻微夸大 bulk 对核心的覆盖。
- **【如何验证】** 对 `META_DRG_axis_CORE_signature.csv` 的 4,055 核心基因逐一查 `META_bulkonly_meta.csv`：统计 present-but-NS 与 absent 两类计数，确认 211 与 102 拆分。
- **【Specific fix】** 改为：“only 211 of the 4,055 primary-core genes are present in the bulk-only meta yet not bulk-significant (meta_FDR ≥ 0.05); a further 102 fall below the bulk-evaluation threshold (K<3) and are unevaluated there”，并给出仍丢失总数 468。

#### T3-B 【圆形 concordance 数字仅作参考，勿被任何自动化门当作“应通过”断言】
- **【Problem】** 补充表 S6 Panel B 保留了圆形 concordance 数字（53.9% / 7,751/14,390 / 69.5%，`MVP_PLOSONE_supplementary.md:216-217`），已标注 “circular? yes”。但这些字面串恰好也是 `gate_consistency.py` 的硬编码“应通过”断言（`:199-200`）。
- **【Why it matters】** 若残留门被调用，它会把“圆形参考数字出现”当作验证通过，进一步强化 T1-B 的循环验证假象。圆形数字本身在补充表中出现是可接受的（已标注），但须确保没有任何门把它们当作正确性证据。
- **【如何验证】** 比对 `gate_consistency.py:199-200` 的 good-list 与 S6 Panel B 圆形数字，二者字面重合。
- **【Specific fix】** 随 T1-B 一并弃用 `gate_consistency.py`；在 S6 Panel B 表注强调“圆形数字仅作方法对照，非结论证据，不进入任何自动化验证断言”。

#### T3-C 【背角 17/33 分母建议在图注显式定义】
- **【Problem】** Fig.4B（`:297`）称 “17 of 33 (51.5%) map to the dorsal horn”，但未显式写清“33”=“Visium 可检 33 hub（已排除全零 CRISP3/LNP1）”。Methods `:164` 列出 below-floor 名单含 CRISP3/LNP1，但图注读者不一定回溯。
- **【Why it matters】** 分母定义若不清，读者可能误把 33 当作“35 hub 中 33 个有区域信号”而忽略 2 个全零排除，造成与 S2 的轻微口径错位。
- **【如何验证】** 比对 Fig.4B 文字与 S2 footnote `:93` 的排除名单，确认 33 = 35 − 2（CRISP3/LNP1）。
- **【Specific fix】** 在 Fig.4B 图注加一句：“33 = 35 hubs detectably expressed in Visium (CRISP3 and LNP1 all-zero, excluded); 17 of these 33 lie in dorsal horn”。

---

## § 六、七项溯源镜头逐项命中（任务指定的 7-point provenance lens）

按任务指定的七个溯源镜头，逐条给出命中结论与对应的本报告的证据位置。

- **镜头 1 — 头号数字从原始 CSV/JSON 独立重算**：已执行。CORE=4,055；bulk-only=2,512；严格重叠 2,202/4,055=54.3%（重算 54.30%）；宽松 3,587/4,055=88.5%（重算 88.46%）；32/35 in_meta_core；bootstrap 中位数 43 / Jaccard 0.304 / dock_eligible_17 均值 8.70 / P(≥3)=1.000；LODO incision 0.677 [0.374,0.940]。全部与稿件一致（见 § 3.2 完整登记册）。**判定：通过。**
- **镜头 2 — 归档 vs 活跃源纪律**：已检索。归档 `_R3_bulkonly_meta_summary.json`（1,981 / 42.7%）为被取代值；稿件中 1981 仅以“superseded”措辞出现（`MVP_PLOSONE_submission.md:50` “An earlier … count of 1,981 is superseded”、`:152` 同义），无任何活跃正文把 1981/42.7% 当当前结论；活跃 `META_bulkonly_sensitivity_summary.json`（2,512/2,202/54.3157）已入正文。唯一仍吸附旧值 1981 的是陈旧门产物 `scripts/_gate_out.txt:7`（见 T2-A）。**判定：源纪律合格；缺陷仅在验证产物未随源重跑（T2-A）。**
- **镜头 3 — 循环验证陷阱（硬编码 vs 派生）**：已审计两道门。`gate_consistency.py`（line 92、199-200、214）硬编码 "0.917"/"53.9%"/"7,751/14,390"/"69.5%"/"17 of 33"/"references=37"——典型的“字符串必须出现”式循环验证，无法发现数字错误（见 T1-B）。`p7_consistency_gate.py` 通过 `chk()` 从源 CSV/JSON 派生期望值——正确设计，应作为唯一权威门。**判定：存在循环验证陷阱，须弃用残留门（T1-B）。**
- **镜头 4 — 图 vs 数据（Fig 2A）**：已审计 `make_sr_figures.py`。其读取 `P3_lodo_auc_ci_leakage_controlled.csv`，axvline 0.677 标 “cross-animal floor”，面板标题 “LC-LODO, leakage-controlled”，无 0.917；DPI=350。稿件 `:64` 的 0.917 明确标 “raw (non-leakage)” 且仅在 Methods。`build_sr_submission_pack.py` 以 Cm(15.2) 嵌入 PNG，保留 350 DPI。**判定：通过，无图—数据冲突。**
- **镜头 5 — 陈旧/重复值（标题/版本/访问日期）**：已核对。标题：稿件/cover/compliance 用新标题，`CITATION.cff:3` 与 `build_sr_submission_pack.py:50` 用旧标题——**唯一规范冲突（T1-A）**。版本串 `v1.0.0`：稿件 `:269`/`:271`、cover letter、compliance、CITATION.cff（message 行）一致，未见漂移。访问日期：本稿件为公共 GEO 重分析，无“access date”字段，故不存在该字段的重复/陈旧问题。**判定：标题为唯一失配，须修（T1-A）。**
- **镜头 6 — 破损表格语法 / 双重舍入 / 稿件与其表冲突**：已查。S5b Sigma1 重复行（`:190-191`，T2-B）；S2 “Present” 列语义与源 `present` 字段碰撞（T2-D）；稿件 Table 3 与 S6 Panel D 的 FDR_RE 第 3 位小数差异均为四舍五入（如 ADRA2A 0.0386→0.039、AXL 0.0677→0.068），非双重舍入错误；未发现的“稿件数字与其自身表格矛盾”。**判定：有两处表—数据标签/重复缺陷（T2-B、T2-D），无稿件—表数字矛盾。**
- **镜头 7 — Visium 33/35 与 snRNA 33/35 是否混为一谈**：已分别读两源表。Visium `P5_GSE325938_hub_regionalization.csv` 缺 CRISP3+LNP1（全零）；snRNA `P5_GSE328175_SC_ShamSNI_hub_localisation.csv` 缺 CRISP3+REG3B。二者缺失基因不同，稿件作为两个独立证据呈现，未合并为“共享 33/35 缺失”（见 Stands up #3）。**判定：通过，未混淆。**

---

## § 七、补充材料逐项核对范围与结论（S1–S7）

为明确审计覆盖面，逐表说明我通读/抽样的范围与结论。未通读之表不作“已验证”声明。

- **S1（35 hub 候选集表，正文以 Table 2 引用）**：本次未逐行通读 S1 的 35 行。抽样交叉确认：稿件 `:62` 称 32/35 in meta core、5/35 全三法共识（SPRR1A/ATF3/TFE3/CDHR5/GALNS）；与 S2（35 行）、S6 Panel D（10 靶）内部一致。建议作者在最终包中保留 S1 与源 `P3_hub_genes.csv` 逐符号一致，本审计未独立重算 S1 全文。
- **S2（Visium 区域化）**：已通读（lines 55-93）。结论：CRISP3/LNP1 在源 `present=False` 但表中 `Present=1`，列语义碰撞（T2-D）；footnote `:93` 已声明全零，但列名仍未区分。其余 33 行与源一致。
- **S3（反向阳性对照 docking AUC）**：已读（lines 95-100+）。ADRA2A “control-evaluable but did not pass”（0.532, p=0.118）注释正确，与稿件 Table 3b/Fig.5 一致；SLC2A1（n_known=1）正确排除出方法验证。无问题。
- **S4（多元物理化学控制）**：本次未通读 S4 全文。稿件 `:170` 给出五靶 LR 检验 p（AXL 2.6e-5、TNIK 7.3e-5、ACVR1 9.6e-4、MAPK14 0.066、ADRA2A 0.027），与本审计范围外的源 `_R4_*` 未独立重算；标注为抽样范围外，建议作者确认 S4 与稿件 `:170` 一致。
- **S5a（基因集统计，未校正）** + **S5b（集合水平 BH 校正）**：已通读（lines 130-191）。结论：S5b Sigma1 重复行（T2-B）；S5a 与 S5b perm p 口径需对齐说明（T2-C）；S5b BH q 列与稿件 Fig.1 图例（`:288`）一致（神经炎症/补体/DAM q=0.003、OXPHOS q=0.020、离子通道灰）。
- **S6（随机效应敏感 + 非圆形翻译 + 固定/随机靶）**：已通读（lines 196-251）。Panel A RE 核心 1,008（24.9%）与 `_R4_random_effects_meta.csv` 一致；Panel B 圆形数字（53.9%/69.5%）已标 “circular? yes”，仅作方法对照；Panel D 十靶 Z/FDR(FE)/FDR(RE) 与稿件 Table 3 逐行一致。无数字矛盾；仅注意圆形数字字面串被残留门硬编码（T1-B/T3-B）。
- **S7（docking target set bootstrap）**：已通读（lines 254-303）。Panel A 数值（8.70/3.93/43/0.304/1.000/0.990/0.830）与活跃源 `_R4_targetset_bootstrap.json` 完全一致；Panel B 逐基因恢复频率与源 `_R4_targetset_bootstrap.csv` 一致。无问题。

---

## § 八、bootstrap 与 LODO 字段级交叉表（镜头 1 的细粒度证据）

以下把两个最关键活跃源文件的每个字段，映射到稿件/补充表的确切位置，证明“数字来自源而非手填”。

### 8.1 `_R4_targetset_bootstrap.json` 字段 → 稿件
- `B = 200` → 稿件 `:66` “200-resample bootstrap”、`:256` “B = 200, SEED = 42”。
- `hub_set_size: median 43 (q25 41, q75 46)` → 稿件 `:66`/`:270` “median size of 43 genes (IQR 41–46, range 33–60)”。重算中位数 43.0 ✓。
- `jaccard_vs_published35: median 0.304 (IQR 0.259–0.333)` → 稿件 `:270` “median Jaccard overlap of 0.304 (IQR 0.259–0.333)”。重算中位数 0.3039→0.304 ✓。
- `dock_eligible_17: mean_recovered 8.70 (min 4, max 13)` → 稿件 `:263` “Mean number recovered per resample 8.70”、`:264` “Median (min–max) 9 (4–13)”。重算均值 8.695→8.70 ✓。
- `dock_eligible_17: P_ge3 = 1.000, P_ge5 = 0.990` → 稿件 `:266-267` “P(≥3) 1.000 / P(≥5) 0.990”。重算一致 ✓。
- `docked_9: mean_recovered 3.93 (min 0, max 8)` → 稿件 `:263` “3.93”、`:264` “4 (0–8)”。重算一致 ✓。
- `docked_9: P_ge1 = 0.990, P_ge3 = 0.830` → 稿件 `:265-266`。重算一致 ✓。
- 逐基因恢复频率（TFE3 0.885、CDHR5 0.875、…、CTTN 0.125）→ 补充 S7 Panel B `:276-301`；稿件 `:66` “most stable TFE3 0.885”。与源 `_R4_targetset_bootstrap.csv` 逐符号一致 ✓。
- `2/35 hubs SPRR1A 1.00, ATF3 0.94 exceed ≥0.9` → 稿件 `:66`、补充 S7 `:303` “SPRR1A 1.00, ATF3 0.94”。一致 ✓。

### 8.2 `P3_lodo_auc_ci_leakage_controlled.csv` 字段 → 稿件（Fig 2A 数据源）
- GSE278227（CCI rat DRG, n=28）AUC = 1.000 → 稿件 `:291`、`:64`。
- GSE212311（CCI, n=6）AUC = 1.000 → 稿件 `:291`、`:64`。
- GSE267799（incision, n=20）AUC = 0.6771 [0.3735, 0.9405] → 稿件 `:64` “leakage-controlled 0.677 [0.374, 0.940]”、`:291`。重算一致 ✓。
- GSE241361 DRG（n=9）AUC = 1.000 [1.000, 1.000] → 稿件 `:291`。
- GSE241361 spinal（n=9）AUC = 1.000 [1.000, 1.000] → 稿件 `:291`。
- 四个折叠 DeLong 区间退化 [1.0,1.0] 在小 n 下非精度证据 → 稿件 `:291` 已正确标注“not interpreted as precision”。
- 对照原始非泄漏 `P3_lodo_auc_ci.csv`：GSE267799 0.9167 [0.7291, 1.0]（稿件 `:64` 0.917 [0.729, 1.000]，标 “raw non-leakage”）；GSE241361 spinal raw 0.950 [0.709, 1.0]（稿件 `:64`）。两套文件分工清晰，图只用泄漏控制版。

### 8.3 随机效应敏感核心字段 → 稿件/补充
- `_R4_random_effects_meta.csv` 派生核心 = 1,008（占固定效应 24.86%）→ 稿件 `:203`/`:305` “1,008 (24.9%)”。重算 1008/4055=24.86% ✓。
- median τ² = 0.232、median I² = 38.8% → 稿件 `:204-205`、`:134`。与源 `_R4_supplementary_summary.json` 一致 ✓。
- 35 hub 中保留 FDR<0.05：35/35（FE）vs 18/35（RE）→ 稿件 `:208`。与 S6 Panel D 十靶 RE 显著性（4/10）方向一致 ✓。

---

## § 九、修复验收清单（供作者逐条闭环）

以下把每个 Must-fix 映射到一个可验证的“关闭判据”，供作者返修时逐条勾销。

- **T1-A 关闭判据**：全仓库检索两个标题串，结果仅剩一处规范标题；`CITATION.cff:3` 与 `build_sr_submission_pack.py:50` 均与稿件 `:1` 标题逐字符相同；用 build 脚本重新生成的 .docx 其封面标题与正文一致。
- **T1-B 关闭判据**：`gate_consistency.py` 已从可发布树移除或重命名为 `*_DEPRECATED.py` 并加文件头说明；README/CI 中无对其的调用；稿件“已验证”叙事仅引用 `p7_consistency_gate.py`。
- **T2-A 关闭判据**：`scripts/_gate_out.txt` 刷新为以 2,512 / 43 / 8.70 / 0.304 / 1.000 / 37 refs 为基准；或旧文件删除并在说明中标注“重算后未保留旧快照”。
- **T2-B 关闭判据**：补充 S5b `:191` 重复 Sigma1 行删除；集合总数声明仍为 19（18 多成员 + Sigma1）。
- **T2-C 关闭判据**：S5a 与 S5b 表注各加一句说明 perm p 层级/分辨率差异；0.0004998 显式标为地板上界。
- **T2-D 关闭判据**：S2 “Present” 列改名（如 “In_35hub_set”）或删除；保留 “Detected_in_Visium” 对应源 `present`（CRISP3/LNP1=False）。
- **T3-A 关闭判据**：稿件 `:152`/`:305` “211” 句改为显式拆分 present-but-NS(211) 与 absent-from-bulk(102)，并给仍丢失总数 468。
- **T3-B 关闭判据**：随 T1-B 弃用残留门；S6 Panel B 表注加“圆形数字仅作方法对照，不进入自动化验证断言”。
- **T3-C 关闭判据**：Fig.4B 图注显式写清 “33 = 35 hubs detectably expressed in Visium (CRISP3 and LNP1 all-zero, excluded)”。

---

## § 十、单细与空间定位层溯源抽查（镜头 3/7 的延伸）

本审计核心在 meta/hub/docking 数字；对单细与空间层做“声明↔源文件名”一致性抽查，未独立重算其倍数/富集（见 § 十一 范围局限）。

- **Fig.3 DRG neuron-subtype 定位（稿件 `:293`）**：声称 20/25 可检 hub 定位于 injured/regenerating neuron subtype；代表倍数 SPRR1A 17.4×（98.1% vs 16.8% detection）、ECEL1 25.7×、NPY 10.0×、FLNC 10.2×；8 个非 hub 标记与 35 hub 零重叠（leave-one-marker consistency 92–100%，ρ 0.965–0.996）。源 `P5_GSE216039_DRG_hub_finetype_top.csv`。本次核对“声明↔源文件名”一致，未独立重算 17.4× 等倍数（样本级，非头号数字核心）。
- **Fig.4A 谱系一致性（稿件 `:297`）**：Neuronal n=8、Glial n=3、Immune n=4、Mixed n=5、NotLocalisable n=15；7/35 跨数据集谱系一致（5 neuronal、1 immune、1 glial）。源 `P5_hub_lineage_consensus.csv`。声明与源文件名一致。
- **Fig.4B / S2 Visium（稿件 `:297`、补充 S2）**：已详查（T2-D）：CRISP3/LNP1 全零、17/33 背角。范围正确。
- **单细胞统计纪律（稿件 `:164`）**：明确 cell-level 统计仅为描述性（避免伪重复），sample-level pseudobulk 仅 n=2–3/group，0 个 BH-significant 基因。属良好统计纪律，本审计认可，未发现问题。
- **人 miRNA 层（稿件 `:161`）**：GSE158825 p=0.51；3,511 个 hub→miRNA 关系，752 个 high-confidence（score≥80），328 个涉及人血浆可检 miRNA。源 `P4_hub_miRNA_human_integration.csv`。未独立重算；声明与源文件名一致。
- **跨模态一致性（稿件 `:297`、`:164`）**：六 hub 显示跨模态一致 Neuronal→DorsalHorn（GALNS、SRRM4、PTPN23、VASH2、ANKRD13B、CTTN）。与 S2 的 “Crossmodal = consistent” 标记一致。

---

## § 十一、可复现指令核对与审计范围局限

### 11.1 复现性要素核对（positive）
- **固定随机种子**：Methods `:158` 称 `p3_ml.py` 与 bootstrap 用 fixed SEED；补充 S7 `:256` 明示 “B = 200, SEED = 42”。符合可复现要求。
- **参数保真记录**：Methods `:167` 记录 exhaustiveness-1 选择理由（max_evals 系统性惩罚柔性配体，Spearman ρ≈+0.26，top-10% recall 0%）；属方法透明，利于第三方复现。
- **多重检验家族分离**：Methods `:169-170` 将校正限定在家族内并分列六类，且明确 composite-ranking 超几何 p 与多元物理化学控制“不计入校正推断检验”。纪律清晰。
- **AI 使用披露**：Methods `:173` 披露使用生成式 AI 辅助起草/润色，但设计与分析由作者执行并核对。符合 PLOS ONE AI 披露期待。

### 11.2 本审计的范围局限（honest scope）
- **(a) 未逐行通读之补充表**：S1（35 hub 全文）、S4（多元物理化学控制全文）仅抽样核对，未逐符号/逐字段重算；其声明与稿件 `:62`、`:170` 一致，但作者应在最终包中确认 S1 与 `P3_hub_genes.csv`、S4 与 `_R4_*` 源完全一致。
- **(b) 参考 DOI 未独立解析**：compliance_check 称 37/37 DOI 已解析；本审计未逐条点击验证每个 DOI 可达性，依赖该声明。头号数字不依赖 DOI，故不影响结论。
- **(c) 单细/空间/miRNA 层仅做“声明↔源文件名”一致性**：未独立重算其倍数、富集与恢复频率（见 § 十）。这些非本审计头号数字核心，但若作者声称其数值精确，建议补充独立重算。
- **(d) 仅审计授权文件**：未读任何 `REVIEW_*.md`/`RESPONSE_*.md`/`REVISION_*.md`/其他审稿人文件/`reviews/_quarantine/`，按独立性规则执行，不影响对“数字可追溯性”的判断。
- **(e) 门产物时效**：`scripts/_gate_out.txt` 为旧快照（T2-A）；本审计以活跃源文件为最终权威，不依赖该快照。

### 11.3 给作者的总建议
头号数字真实可溯源，无需重算科学结论；请把工作量放在“发布卫生”：先清 T1-A（标题）、T1-B（弃用残留门），再清 T2-A（刷新门产物）、T2-B（删重复行）、T2-D（改列名），最后顺手修 T2-C/T3-A/T3-B/T3-C。完成上述后，本审计认为稿件满足 PLOS ONE 对“计算可重复”的基本要求。

---

## § 十二、对作者潜在反驳的预回应

预想作者可能提出的辩护及本审计的回应，供作者返修时参考。

- **R1 “gate_consistency.py 的硬编码串目前都还是正确值，所以门没坏。”**
  → 门的对错不取决于当前值是否碰巧正确。硬编码断言本质是“稿件是否包含某字面串”，它既不能检测数字被改错，也会在作者有意修订某数时误报失败；且它属 Scientific Reports 投稿语境，本次 PLOS ONE 投稿不应依赖。正确做法是仅保留从源派生期望值的 `p7_consistency_gate.py`（见 T1-B）。
- **R2 “S2 的 Present=1 就是指该 hub 在 35 候选集里，读者能理解。”**
  → 列名与源 CSV 的 `present` 字段（含义为 Visium 是否检出）同名不同义；CRISP3/LNP1 在同一行出现 “Present=1” 与 “log2=0、detect=0”，必然引发“它到底存不存在”的误读。改名（如 “In_35hub_set”）成本极低却消除歧义（见 T2-D）。
- **R3 “211 就是我们内部对‘不 bulk 显著’的叫法。”**
  → 建议显式拆分 211（present-but-NS）与 102（absent, K<3），否则 “not bulk-significant at all” 措辞把“未评估”也归入“不显著”，轻微夸大 bulk 对核心的覆盖（见 T3-A）。
- **R4 “0.917 在 Methods 已标 raw non-leakage，没问题。”**
  → 同意，这正是 Stands up #2 肯定的点；仅须确保残留门不把 0.917 当诚信结论断言（见 T3-B/T1-B）。
- **R5 “S5b Sigma1 重复行无害。”**
  → 两行完全相同，虽不影响数值，但会被排版与审稿人视为粗心，且若用脚本解析该表会污染“集合数=19”的计数。删除一行零成本（见 T2-B）。
- **R6 “标题小事，编辑阶段会统一。”**
  → 标题不一致会直接进 Zenodo/GitHub v1.0.0 元数据与生成版 .docx，属发表物级错误而非排版细节；建议在接收前清零（见 T1-A）。

## § 十三、审计置信度声明

明确本审计对各结论的置信等级，便于小组权衡。

- **高置信**：所有头号数字（meta 核心 4,055、bulk-only 2,512、严格重叠 54.3%、宽松 88.5%、32/35 in_meta_core、bootstrap 中位数 43/Jaccard 0.304/8.70/P≥3=1.000、LODO incision 0.677 [0.374,0.940]、RE 核心 1,008）均可从活跃源文件独立重算并一致。
- **中高置信**：Fig.2A 与泄漏控制数据自洽；Visium 与 snRNA 两个 33/35 正确区分；S3/S5b/S6/S7 与源一致；随机效应敏感核心与源一致。
- **中置信**：S2 “Present” 列语义碰撞（T2-D）、S5a/S5b perm p 口径差异（T2-C）已指出，但需作者确认口径说明文字；这些不影响头号数字结论。
- **低置信 / 未覆盖**：S1 全文、S4 全文、37 条参考 DOI 可达性、单细/空间/miRNA 层的倍数与富集——见 § 11.2 范围局限。作者应在最终包中确认这些部分与源一致。
- **总体**：稿件计算层真实可溯源，无捏造迹象；所列问题均为发布卫生（标题/门/表标签），建议一轮返修清零 T1/T2 项后接收。

---

## § 附、关键证据锚点（file:line 速查）

本评议中反复引用的高价值证据位置汇总，供小组快速复核。

- 标题冲突：稿件 `MVP_PLOSONE_submission.md:1`（新） vs `CITATION.cff:3`（旧） vs `scripts/build_sr_submission_pack.py:50`（旧 MS_TITLE）。
- 残留硬编码门：`scripts/gate_consistency.py:92`（0.917）、`:199-200`（53.9%/7,751/14,390/69.5%/17 of 33/0.917）、`:214`（references=37）。
- 陈旧门产物快照：`scripts/_gate_out.txt:7`（source 1981）、`:19`（0.79 of 17）、`:70`（references=26）。
- S2 列语义碰撞：`MVP_PLOSONE_supplementary.md:79`、`:83`（CRISP3/LNP1 Present=1 但全零）；源 `P5_GSE325938_hub_regionalization.csv` `present=False`。
- S5b 重复行：`MVP_PLOSONE_supplementary.md:190-191`（Sigma1 两行相同）。
- 活跃源（正确值）：`META_bulkonly_sensitivity_summary.json`（2,512/2,202/54.3157）、`_R4_targetset_bootstrap.json`（43/0.304/8.70/1.000/0.990/3.93/0.830）、`P3_lodo_auc_ci_leakage_controlled.csv`（incision 0.6771 [0.3735,0.9405]）。
- 归档（被取代）：`results/tables/_archive/_R3_bulkonly_meta_summary.json`（1,981/42.7127）；稿件仅以 “superseded” 引用（`MVP_PLOSONE_submission.md:50`、`:152`）。
- 图 2A 数据源：`scripts/make_sr_figures.py`（读 leakage-controlled 文件、axvline 0.677、DPI 350）。
- 权威门（正确设计）：`scripts/p7_consistency_gate.py`（`chk()` 从源派生期望值）。

---

## § 五、总评（A3 一句话结论）

稿件的计算结果是**真实且可溯源**的：每一个头号数字都能从活跃源文件独立重算并得到一致值，图 2A 与泄漏控制数据自洽，Visium/snRNA 两个 33/35 未被混淆，作者还主动披露了被取代的旧分母与旧交集计数。需要修复的不是“数字对错”，而是**发布卫生**——标题在三个出处不一致（T1-A）、一个 Scientific Reports 遗留的硬编码循环验证门仍在树上且其陈旧产物快照会给出错误保证（T1-B、T2-A）、以及补充表的两处表—数据标签/重复行问题（T2-B、T2-D、T3-A、T3-C）。这些均为一轮可修复的溯源/过程缺陷，**不建议直接拒稿**；但 T1-A 与 T1-B 必须在接收前清零，否则发表物元数据与“已自动验证”叙事将失真。

**修复优先级建议**：T1-A、T1-B → T2-A、T2-B、T2-D → T2-C、T3-A、T3-B、T3-C。其中 T1-B 与 T2-A 可一并处理（弃用残留门 + 重跑活跃门并刷新产物）。
