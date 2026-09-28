# A3 — 实证复算与溯源审计报告 (Implementation / Provenance Audit)

**稿件：** `reports/MVP_PLOSONE_submission.md`（单作者 PLOS ONE 重投，按首次投稿对待）
**审计角色：** A3，溯源 / 复算审计员
**审计原则：** 不信任转录数字；所有关键数值均从原始 `results/tables/*.csv|*.json` 重新计算，并与稿件逐条比对。
**未读取（按分工禁读）：** 任何 `reviews/REVIEW_*.md`、`RESPONSE_*.md`、`REVISION_*.md`、round12/round13 panel 目录、`SUBMISSION_MANIFEST.md`、`GITHUB_PUSH_LIST_v1.4.md`、`GITHUB_DEPOSIT_SOP.md`、`author_verification_statement.md`、`_quarantine/`，以及同目录 `A1_*`/`A2_*`/`A4_*` 文件。

---

## 执行摘要（Bottom line）

我对稿件中可复算的核心数值做了独立重算。**一致性与随机效应、LODO、基因集、bootstrap、图件 DPI 这一大类数字基本全部对得上**；但发现 **3 处实质性数值/口径矛盾**与 **1 处轻微不一致**，其中两处直接动摇稿件的自我一致性与结论表述：

| # | 严重度 | 问题 | 稿件声称 | 我重算 / 溯源结果 |
|---|--------|------|----------|-------------------|
| F1 | 高 | 35 hub 中满足 meta-core gate 的比例被高估 | 32/35（91%） | 26/35（74%）；任何口径都不是 32 |
| F2 | 高 | 同一翻译检验结果在文中自相矛盾（significant vs non-significant） | 摘要/结论称"non-significant" | 同一数字 perm_p=0.0002 在 Results 段被作者自己标注为"(significant)" |
| F3 | 中 | Discussion 引用一个无法从任何原始文件复现的翻译统计量 | 46.2% vs 47.1%，p=0.14 | 两个 JSON 源均无 46.2%；且与 43.3%/p=0.0002 互相矛盾 |
| F4 | 低 | 摘要与正文/图注的基因集 q 值不一致 | 摘要 q=0.003 | 正文/图注/数据均为 q=0.0022 |

此外，稿件与 gate 都宣称"0 failure, 0 warning, 47 passed"——我**实际重跑了 gate**，**确认 47/0/0 属实**。但必须指出：该 gate 的检查范围是"数字是否出现 / 能否从源文件再派生"，它**并不覆盖** F1–F3 这类口径与显著性标注问题；我的独立复算正是 gate 未覆盖的部分。

---

## 一、发现（每条含四要素）

### F1 — 35 个 hub 中"满足 meta-core gate"的比例被高估，与稿件自身 Table 2 直接矛盾

**【Problem】** 稿件正文声称 35 个候选 hub 中"32/35（91%）也满足 meta-core gate"，但该数字与稿件自己的 Table 2 以及源文件 `P3_hub_genes.csv`、源 `META_DRG_axis_stouffer.csv` 全部不符。

**【Evidence】**
- 稿件 L124："The dual-ML candidate hub set (35 genes; **32/35, 91%**, also satisfy the meta core gate…)"
- 稿件 Table 2（L333–L369）"In meta core"列：我逐行清点得 **26 个 "Yes"**（SPRR1A, ATF3, CDHR5, GALNS, TFE3, MEGF11, SLC2A1, CCDC160, SRRM4, VIP, LNP1, ITPKC, TNIK, FLRT3, CHL1, AXL, FLNC, RNF19B, CRISP3, SERPINE1, TNS3, MAPK14, ACVR1, NPY, VASH2, WBP1L），其余 9 个为 "No"。
- 源 `P3_hub_genes.csv` 的 `in_meta_core` 列：`True` 计数 = **26**（与 Table 2 一致）。
- 我按稿件给的口径定义（Table 2 注："meta core gate = meta_FDR < 0.05 且 consistency ≥ 0.8"）从 `META_DRG_axis_stouffer.csv` 重算：35 hub 中满足者 = **26**；其中不满足的全部 9 个为 consistency < 0.8（ECEL1, PTPN23, WDR81, ANKRD13B, AGRN, REG3B, ANKRD1, CTTN, RUBCN）。
- 为排除"32 是另一种 gate"的可能，我额外检查了两种相邻口径：
  - meta FDR<0.05 且 **meta** consistency≥0.8 → 26；
  - **nerve-injury** consistency≥0.8（来自 `_R4_random_effects_meta.csv` 的 `nerve_injury_consistency`）→ **28**；
  - 仅 meta FDR<0.05（不限一致性）→ 35。
  **没有任何一种口径得到 32。**

**【Why it matters】**
1. 这是稿件内部的硬矛盾：同一篇文章的 Table 2 与正文数字不一致，最容易被审稿人/编辑在 30 秒内抓到，直接导致"数字不可靠"印象。
2. 真正的比例是 26/35（74%），而非 91%。虽然稿件随后正确地指出"该重叠不是独立佐证"，但把 74% 写成 91% 放大了 meta 与 ML 之间的表观一致性，削弱了后文"non-independent"自省的可信度。
3. 9 个一致性失败的 hub（如 ECEL1、ANKRD1、CTTN、RUBCN、AGRN）是方向在 6 个对比中反复翻转的基因，这一 caveat 本应被强调，却被错误的 91% 稀释。

**【Specific fix】** 把 L124 的 "32/35, 91%" 改为 "26/35 (74%)"。同时建议在该句补充说明：所有 35 个 hub 均满足 meta FDR<0.05（即 35/35 在 FDR 层面显著），但仅 26/35 通过一致性≥0.8 的 core gate；若作者希望保留一个"宽松"口径，应明确写"28/35 满足 nerve-injury consistency≥0.8"，而非含糊的 32/35。

---

### F2 — 同一翻译检验结果在文中自我矛盾："significant" 与 "non-significant" 并存

**【Problem】** 稿件对 incision-arm 翻译检验（43.3% vs 47.1% background, perm_p = 0.0002）的显著性判定，在 Results 段与 Abstract/Conclusions 段互相矛盾。

**【Evidence】**
- Results（L58，作者原话）："…the agreement rate was 43.3% (1,660/3,830; …) (…), a risk difference of −3.7 pp versus background, permutation p = 0.0002 **(significant)**."
- Abstract（L20）："The nerve-injury signature did not predict that arm (43.3% vs 47.1% background, perm_p = 0.0002; **non-informative rather than negative** given the lesion-class mismatch)". 此处把同一 p=0.0002 的结果表述为"non-significant / non-informative"。
- Conclusions（L140）："the translation test to the sole surgical-incision arm was **non-significant** (43.3% vs 47.1% background, perm_p = 0.0002 - … this test is **non-informative rather than negative**)".
- 该数值对得上源文件 `_R4_nerveinjury_only_summary.json` 的 `NI_FDR05_AND_NIcons>=0.8` 层：`rate=0.4334`（43.3%），`n=3830, k=1660`；`perm_p=0.00019996`（≈0.0002）；background `all_measured`：`rate=0.4706`（47.1%），`n=14390, k=6772`。即**数字本身正确**，矛盾出在"significant / non-significant"的判定上。
- p=0.0002 在任一常规解读下都是**显著**（即使按两侧置换 p，也远小于 0.05）。作者在 L58 已自认 "(significant)"，因此 L20/L140 的 "non-significant" 与该作者自己的标注直接冲突。

**【Why it matters】**
1. 同一 p 值在同一稿件里既"significant"又"non-significant"，是审稿人必挑的逻辑硬伤，且会让读者无法判断作者到底想表达什么。
2. 实质结论也写反了方向：观测值 43.3% **低于**背景 47.1%（−3.7pp）且 perm_p=0.0002，正确读法应是"nerve-injury core 在 incision arm 中 concordance 显著低于背景"，即一次**显著的"不翻译 / 耗竭"**。稿件用"non-informative rather than negative"淡化它，但 p=0.0002 不是 non-informative——它是显著负向。lesion-class 差异确实支持"这一显著负向对 CPSP 特异性无信息量"的 caveat，但 caveat 不能把显著结果改写成"non-significant"。

**【Specific fix】** 统一三处的显著性表述。建议改为（以 L140 为例）：
> "the translation test to the sole surgical-incision arm was significantly depleted (43.3% vs 47.1% background, perm_p = 0.0002 — a significant non-translation); because the two arms differ in lesion class, this significant non-translation is non-informative about CPSP specificity rather than evidence against the programme."
Abstract（L20）与 L58 同步。关键是：不要把 p=0.0002 称作 "non-significant"；要保留"lesion-class caveat"作为**解释性**限制，而非作为"结果不显著"的借口。

**【方法学补充（避免二次误读）】** 当前 `perm_p = 0.0002` 究竟对应单侧还是双侧置换检验，稿件方法部分未显式声明。若该 p 为**双侧**（观测 −3.7pp 偏离背景的任何方向），则"显著"是正确结论（耗竭显著）。若作者本意是检验"核心是否富集（正向翻译）"的**单侧**假设，则正确写法应是"one-sided test of enrichment p ≈ 1.0 (non-significant for enrichment)"，同时仍须说明**双侧** p=0.0002 表明显著耗竭——绝不能只写"non-significant"而隐去双侧显著。建议作者在 Methods 明确置换检验的方向性与零分布定义，并在 Results 同步给出两侧 p 与（如适用）富集单侧 p，避免任何方向的误读。

---

### F3 — Discussion 引用一个无法从任何源文件复现的翻译统计量（46.2% vs 47.1%, p=0.14）

**【Problem】** Discussion（L122）给出一组与 Results 段完全不同的翻译数字："46.2% versus a 47.1% background; difference −0.9 pp, p = 0.14"，该数字不对应任何提供的 JSON/CSV 源，且与 L58 的 43.3%/p=0.0002 互相矛盾。

**【Evidence】**
- 稿件 L122："The nerve-injury signature does not predict incision direction (**46.2% versus a 47.1% background; difference −0.9 pp, p = 0.14**)…"
- 我在两个声明为翻译检验源的文件里逐一核对：
  - `_R4_nerveinjury_only_summary.json` 各层 rate：`all_measured` 0.4706（47.1%）、`NI_FDR05_any_consistency` 0.4443（44.4%）、`NI_FDR05_AND_NIcons>=0.8` 0.4334（43.3%）、`NI_FDR05_AND_NIcons<0.8` 0.4577（45.8%）、`NI_FDRRE05_AND_NIcons>=0.8` 0.4186（41.9%）。**无 46.2%。**
  - `_R4_translation_noncircular.json` 各层：`all_measured` 0.5378、`meta_FDR05_NIcons_ge08` 0.524、`meta_FDR05_NIcons_lt08` 0.616、`meta_FDR05_pooled_ge08` 0.769。**无 46.2%，且背景率是 53.8% 而非 47.1%。**
- 我进一步在 `results/tables/*.csv` 全量检索字面 "0.462 / 46.2"，命中全部是 DEG 表的无关浮点（如 logFC 0.462…，或分子量 146.2），**没有任何一处生成 46.2% 的翻译一致性率**。
- 因此 46.2% / −0.9pp / p=0.14 既不来自声明源，也无法由提供的脚本产物复现；同时它与 L58/L140 的 43.3% / −3.7pp / p=0.0002 直接冲突（同一"incision 预测"主题出现两组不可调和的数字）。

**【Why it matters】**
1. 读者/审稿人若交叉核对 Results 与 Discussion，会看到"翻译到底成不成功"出现两个相差悬殊的答案（43.3% 显著 vs 46.2% 不显著），直接摧毁结论的可信度。
2. 若 46.2%/p=0.14 来自某个未归档的管线或旧版本，则属于"声明源无法复现"的溯源缺陷，正好撞上本次审计的主题。

**【Specific fix】** 二选一：(a) 删除 L122 的 46.2%/p=0.14 表述，统一到 L58 的非循环翻译结果（43.3% vs 47.1%, −3.7pp, perm_p=0.0002）；(b) 若作者确有另一条合法管线得到 46.2%，必须**指明其源文件与计算定义**（哪个 JSON/CSV 的哪一行、分母是哪组基因），并在 Data availability 中提供该产物。在源文件未补齐前，建议直接采用 (a)。

---

### F4 — 摘要与正文/图注的基因集 set-level BH q 值不一致（q=0.003 vs q=0.0022）

**【Problem】** 摘要把四个核心基因集的 set-level BH q 写成 0.003，而正文（L48）、图 1 图注（L302）与源 `_R4_geneset_setlevel_bh.csv` 均为 0.0022。

**【Evidence】**
- 摘要 L18："Gene-set tests recapitulated a coordinated neuroimmune/complement and DAM-like programme (set-level BH **q = 0.003** each, an upper bound at the 2,000-permutation resolution floor)".
- 正文 L48 与图注 L302："neuroinflammation (… q = **0.0022**)、DAM microglia (… q = **0.0022**)、complement (… q = **0.0022**)、Mitochondria_OXPHOS (… q = **0.0022**)".
- 源 `_R4_geneset_setlevel_bh.csv`：`Neuroinflammation / Complement / Mitochondria_OXPHOS / DAM_microglia` 在 fixed 与 random 两种 scale 下 `perm_q` 均为 **0.0022488755622188904 ≈ 0.0022**。`0.003` 与 `0.0022` 不符。
- 附带核验：该四组的 `mean_Z` 也与稿件一致（Neuroinflammation 5.0749≈5.075、DAM 3.833、Complement 3.700、OXPHOS −2.9218≈−2.922），`frac_up` 一致（1.0 / 0.875 / 0.944 / 0.211→78.9% down），因此**只有 q 的呈现不一致**，统计量本身正确。

**【Why it matters】** 单看是小数位的轻微出入，但它与 F2 同属"同一指标在稿件不同位置写法不一"的家族问题；PLOS ONE 对数值一致性较敏感，且摘要与正文冲突会在技术核查（technical check）阶段被标记。

**【Specific fix】** 把摘要 L18 的 "q = 0.003" 改为 "q = 0.0022"，或统一为 "q ≤ 0.0025" 这类对分辨率下限安全的写法，但须与正文/图注一致。

---

### F5（说明项，非稿件错误）— "P=0.000" 在我被要求核验的清单里，但稿件/源文件中并无字面 "P=0.000" 主张

**【Problem】** 审计简报要求核验 "Jaccard 0.304, P=0.000"。我未能在稿件或源文件中找到任何字面 "P=0.000" 的主张。

**【Evidence】**
- 与 0.304 同段落的 bootstrap 主张来自 `_R4_targetset_bootstrap_resamples.csv`：Jaccard 中位数 = **0.30395 ≈ 0.304** ✓；dock-eligible 17 hub 的恢复数均值 = **8.695 ≈ 8.70**、中位数 9 ✓；`P(≥3 of 17) = 200/200 = 1.000`（稿件写 "P(≥3 of 17) = 1.000"），**不是 0.000**。
- 全文中与 "0.000" 接近的 p 值是翻译检验的 `perm_p = 0.0002`（见 F2），以及 ADRA2A 的 size-independent ΔAUC p = 0.0005（Table 3b, L380）。
- 结论：被要求核验的 "P=0.000" 很可能是对 "perm_p=0.0002" 或 "P(≥3)=1.000" 的误记。**两项实际数值均经我复算确认无误**（见 Stands up）。请在定稿时明确：若指 bootstrap 恢复概率，应为 P=1.000；若指翻译显著性，应为 perm_p=0.0002。

---

## 二、Stands up（经我独立复算确认正确的部分）

以下每一项均由我从原始 CSV/JSON 重算，并与稿件声称值一致：

1. **基因检验总量与 core 规模（META_DRG_axis_stouffer.csv，16,552 行）**
   - 稿件：genes tested 16,552；meta_FDR<0.05 = 6,558；core (FDR<0.05 & consistency≥0.8) = 2,750。
   - 我重算：行数 16,552；`meta_FDR<0.05` 计数 **6,558** ✓；core 计数 **2,750** ✓。完全吻合。

2. **CACNA2D1 行（fig 1 图注主张）**
   - 稿件：CACNA2D1 up-regulated in 4/6 contrasts, meta_FDR 2.3×10⁻¹⁰。
   - 我重算（按 6 个 lfc 列符号）：`meta_Z=7.088`、`meta_FDR=2.322e-10`（≈2.3e-10）✓、`consistency=0.6667`、`n_up=4 / n_dn=2` ✓。吻合。

3. **随机效应敏感性（_R4_random_effects_meta.csv，16,552 行）**
   - 稿件：median τ²=0.266，median I²=41.8%；RE core (FDR_RE<0.05 & consistency≥0.8) = 508（=18.5% of 2,750）；35 hub 中 median I²=79.1%，7/35 保留 FDR_RE<0.05。
   - 我重算：median τ² = **0.2664** ✓；median I² = **41.77** ✓；RE core = **508** ✓（508/2750 = 18.5% ✓）；35 hub median I² = **79.06** ✓；35 hub 中 FDR_RE<0.05 = **7** ✓。全部吻合。

4. **LODO 泄漏受控交叉验证（P3_lodo_auc_ci_leakage_controlled.csv，5 行）**
   - 稿件：5 折中 4 折 AUC=1.000，incision 折 0.677；n_selected 范围 140–169。
   - 我重算：5 折 AUC 分别为 1.000(GSE278227, n=28, n_sel=169)、0.6771(GSE267799, n=20, n_sel=142)、1.000(GSE241361_DRG, n=9, n_sel=140)、1.000(GSE241361_SC, n=9, n_sel=166)、1.000(GSE212311, n=6, n_sel=161)。AUC=1.000 共 **4** 折 ✓；incision AUC=0.6771 ✓；`n_selected` 最小 **140**、最大 **169** → 范围 140–169 ✓。完全吻合。

5. **Hub 集合规模与一致性来源、bootstrap（P3_hub_genes.csv=35 行；_R4_targetset_bootstrap_resamples.csv=200 行）**
   - hub 计数 = **35** ✓（与 Table 2、35-hub 主张一致）。
   - Jaccard 中位数 = **0.30395 ≈ 0.304** ✓；dock-eligible 17 hub 恢复均值 = **8.695**（稿件 8.70）✓、中位数 9；`P(≥3 of 17) = 200/200 = 1.000` ✓。
   - 三方法共识：`n_methods=3` 的 hub = **5**（SPRR1A, ATF3, CDHR5, GALNS, TFE3），`n_methods=2` = **30**（稿件 L305："5/35 reach full three-method consensus, the remaining 30 by exactly two"）✓。

6. **基因集 set-level BH q 值（_R4_geneset_setlevel_bh.csv）**
   - 四核心集 perm_q = 0.0022（见 F4 说明），mean_Z / frac_up 与稿件逐项吻合（见 F4 证据）。稿件 L48/302 的 q=0.0022 正确，仅摘要写错。

7. **Bulk-only 敏感性 core（META_bulkonly_sensitivity_summary.json）**
   - 稿件：bulk-only core = 2,512。
   - 源 `bulk_only_core_size = 2512` ✓。

8. **图 4A 脊髓谱系数（P5_hub_lineage_consensus.csv，35 行）**
   - 稿件：Neuronal n=8, Glial n=3, Immune n=4, Mixed n=5, NotLocalisable n=15。
   - 我按 `consensus_lineage` 重算：NotLocalisable 15、Neuronal 8、Immune 4、Glial 3、Mixed 5（合计 35）✓。

9. **Visium 背角定位（P5_GSE325938_hub_regionalization.csv，35 行）**
   - 稿件：33/35 可检测，其中 17/33（51.5%）定位于背角。
   - 我重算：present=33，其 `top_region` 含 dorsal horn 者 = **17**，17/33 = **51.5%** ✓。

10. **图件 DPI 与 docx 嵌入（submission_pack/Manuscript.docx）**
    - 5 个 PNG（image1–5）均存在于 `word/media/`，且 `document.xml` 中 `<wp:inline>` 计数 = **5**（5 个内嵌图形）✓。
    - 5 个 PNG 的 pHYs chunk 均给出 **350.0 DPI**（350.0118 ≈ 350）✓，满足稿件"≥300 DPI"主张，且稿件正文明确写"350 DPI"。
    - docx 文本核验：`within-animal paired` 存在 ✓；`not independent corroboration` 存在 ✓；矛盾旧表述 `genuinely independent cross-animal` **不存在** ✓；`v1.4.0` 存在 ✓。说明 v1.4.0 的新措辞已正确进入投稿 docx，旧措辞已清除。

11. **一致性 gate 实跑结果（scripts/p7_consistency_gate.py）**
    - 我**实际运行**了该 gate：输出 `RESULT: 0 failure(s), 0 warning(s), 47 check(s) passed`，与稿件/gate 宣称的"0 failure, 0 warning, 47 passed"**完全一致**。
    - 但需重申（见下）：gate 的 47 项多为"数字是否出现 / 能否从源再派生"的核查，其通过的"NI-only strong pct 43.3 / NI background 47.1 / risk diff −3.7"仅确认这些数字被写入，并**不**核查 F2 的"significant vs non-significant"措辞，也**不**核查 F1 的 32/35 与 F3 的 46.2%。所以 gate 绿 ≠ 稿件无问题。

12. **Bulk-only OXPHOS 下调比例（META_bulkonly_sensitivity_summary.json → setcalls.Mitochondria_OXPHOS）**
    - 稿件（gate 项 "bulk-only OXPHOS down pct: 72.2"）主张 bulk-only 元分析中 OXPHOS 下调成员占 72.2%。
    - 我复算：该文件 `setcalls["Mitochondria_OXPHOS"]["frac_up"] = 0.2777778` → 下调比例 = 1 − 0.2778 = **0.7222 = 72.2%** ✓。与主张吻合。
    - 补充核对 bulk-only 核心集 Neuroinflammation/Complement/DAM_microglia/Neuroinflammation 的 `frac_up` 分别为 1.0 / 0.9375 / 0.875 / 1.0，`perm_p` 均为 0.0005（置换分辨率下限），与正文"协调上调"叙述一致。

13. **核心一致性 77.2%（1,822/2,361）（_R4_translation_concordance_effectsize.csv）**
    - 稿件 L56："77.2% (1,822/2,361)"——六对比循环核心中 incision 方向一致的比例。
    - 我复算：该文件 `core_FDR05_c08` 行 `k=1822, n=2361, rate=0.7717` → **77.2%** ✓；且 `NI_FDR05_AND_NIcons>=0.8` 非循环层（即 F2 主数）`k=1660, n=3830, rate=0.4334` → 43.3% ✓，与 `_R4_nerveinjury_only_summary.json` 完全对应。说明稿件 L56/L58 的数字均能从具名源复现，问题仅出在 F2 的"显著性措辞"与 F3 的"46.2%"。

14. **ADRA2A 两滤子规则数值（Table 3b / _R4_targets_fixed_vs_random.csv 等）**
    - 稿件 Table 3b：ADRA2A 全库 AUC 0.532、p=0.118（NS）、size-independent BH q=0.0025（通过滤子 2）→ 结论"inconclusive"。
    - 我核对 `P3_lodo_auc_ci_leakage_controlled.csv` 不直接含 ADRA2A；但 `META_DRG_axis_stouffer.csv` 中 ADRA2A 行：`meta_Z` 与 `meta_FDR` 等可用于 plausibility 表。ADRA2A 的具体 AUC 来自 docking 产物（不在我本次强制复算清单内），但稿件将其定性为"inconclusive"与公开描述（full-library AUC NS、size-indep q 通过）在逻辑上自洽，且 gate 已对 "ADRA2A size-indep BH q = 0.0025" 做了存在性核对。此项标记为"逻辑一致、未独立重跑 docking AUC"。

---

## 三、Questions for the authors（请作者澄清/处理）

1. **F1：** 请确认 L124 的 "32/35" 是笔误还是来自某个未归档口径。若保留"宽松"口径，请明确写"28/35 满足 nerve-injury consistency≥0.8"或"35/35 满足 meta FDR<0.05"，并让 Table 2 的 "In meta core" 列与正文一致（当前为 26 Yes）。
2. **F2：** 翻译检验的显著性判定，请以 p=0.0002 为准统一为"significant (depletion)"，并保留 lesion-class caveat 作为**解释性**限制；请勿再称其为 "non-significant"。
3. **F3：** L122 的 46.2% / p=0.14 来自何处？请提供其源文件与计算定义，或删除该句并统一到 L58 的非循环结果。在源补齐前，建议直接删除。
4. **F4：** 摘要的 q=0.003 请改为 0.0022，与正文/图注/数据一致。
5. **方法学澄清（非错误，但影响解读）：** L58 的 perm_p=0.0002 是两侧还是单侧置换 p？若作者想强调"对富集（正向翻译）不显著"，应在文中明确写"two-sided p=0.0002 (significant depletion)；one-sided test of enrichment p≈1.0"，避免读者误读。请在方法部分补一句置换检验的方向性定义。
6. **可复现性（流程层面）：** 我复算 F1/F3 时发现，稿件声称的翻译检验源（`_R4_nerveinjury_only_summary.json`）与讨论段引用的数字不一致。请确认 `reports/MVP_PLOSONE_submission.md` 的每一处统计量都对应一个具名源文件中的具名字段；建议在稿件最终版附一张"claim → source file → field"对照表，便于审稿人核查（这正是本次审计做的工作）。

---

## 四、What I actually checked（我实际读过的文件与跑过的核验，逐值列示）

**读取并核验的稿件：** `reports/MVP_PLOSONE_submission.md`（重点 L14–L140、L299–L387、Table 1/2/3 及图注）。

**读取并作为源重算的文件：**
- `results/tables/META_DRG_axis_stouffer.csv`（16,552 行×16 列）
- `results/tables/_R4_random_effects_meta.csv`（16,552 行×18 列）
- `results/tables/P3_lodo_auc_ci_leakage_controlled.csv`（5 行）
- `results/tables/P3_hub_genes.csv`（35 行）
- `results/tables/P3_geneset_stats.csv`（19 行）
- `results/tables/_R4_geneset_setlevel_bh.csv`（固定+随机两组，含 Sigma1 空行）
- `results/tables/_R4_targetset_bootstrap_resamples.csv`（200 行）
- `results/tables/_R4_translation_noncircular.json`
- `results/tables/_R4_nerveinjury_only_summary.json`
- `results/tables/META_bulkonly_sensitivity_summary.json`
- `results/tables/P5_hub_lineage_consensus.csv`（35 行）
- `results/tables/P5_GSE325938_hub_regionalization.csv`（35 行）
- `submission_pack/Manuscript.docx`（zip：word/media 5 PNG、document.xml 内嵌形状与文本）
- `scripts/p7_consistency_gate.py`（实际执行）

**逐项复算值与稿件声称值对照（含差异）：**

| 稿件主张 | 稿件值 | 我重算值 | 来源字段 | 结论 |
|---|---|---|---|---|
| genes tested | 16,552 | 16,552 | 行数 | ✓ |
| meta_FDR<0.05 计数 | 6,558 | 6,558 | `meta_FDR<0.05` | ✓ |
| core (FDR<0.05 & cons≥0.8) | 2,750 | 2,750 | 同上两条件 | ✓ |
| CACNA2D1 meta_FDR | 2.3e-10 | 2.322e-10 | `meta_FDR` | ✓（四舍五入一致） |
| CACNA2D1 up/6 | 4/6 | 4/6 | 6 个 lfc 符号 | ✓ |
| CACNA2D1 consistency | （未明示数值） | 0.6667 | `consistency` | — |
| RE median τ² | 0.266 | 0.2664 | `tau2` 中位数 | ✓ |
| RE median I² | 41.8% | 41.77% | `I2` 中位数 | ✓ |
| RE core | 508 | 508 | `FDR_RE<0.05 & cons≥0.8` | ✓ |
| RE core / FE core | 18.5% | 18.5% | 508/2750 | ✓ |
| 35 hub median I² | 79.1% | 79.06% | 35 hub `I2` 中位数 | ✓ |
| 35 hub FDR_RE<0.05 | 7/35 | 7/35 | `FDR_RE<0.05` | ✓ |
| hub 总数 | 35 | 35 | 行数 | ✓ |
| hub 满足 meta-core gate | **32/35 (91%)** | **26/35 (74%)** | `in_meta_core` 与重算 | ✗ **F1** |
| hub 满足 NI-consistency≥0.8 | （未主张） | 28/35 | `nerve_injury_consistency` | 供参考，≠32 |
| LODO 4 折 AUC=1.000 | 4 | 4 | `auc==1.0` 计数 | ✓ |
| incision 折 AUC | 0.677 | 0.6771 | GSE267799 行 | ✓ |
| n_selected 范围 | 140–169 | 140–169 | `n_selected` min/max | ✓ |
| Jaccard（bootstrap） | 0.304 | 0.30395（中位数） | `jaccard_vs_published35` | ✓ |
| dock-eligible 恢复均值 | 8.70 | 8.695 | `n_dock_eligible_17_recovered` | ✓ |
| P(≥3 of 17) | 1.000 | 1.000（200/200） | 同上 | ✓（非 0.000） |
| 三方法共识 5/35 | 5 | 5 | `n_methods==3` | ✓ |
| 基因集 q（4 核心集） | 0.0022（正文）/ **0.003（摘要）** | 0.0022 | `perm_q` | 正文✓；摘要✗ **F4** |
| bulk-only core | 2,512 | 2,512 | `bulk_only_core_size` | ✓ |
| 图 4A 谱系计数 | N8/G3/I4/M5/NL15 | N8/G3/I4/M5/NL15 | `consensus_lineage` | ✓ |
| 背角 17/33 | 51.5% | 51.5%（17/33） | `top_region` | ✓ |
| 翻译 43.3% vs 47.1%, pd=0.0002 | 43.3/47.1/0.0002 | 0.4334/0.4706/0.0002 | `NI_FDR05_AND_NIcons>=0.8` & `all_measured` | 数字✓；但显著性标注自相矛盾 **F2** |
| 翻译 46.2% vs 47.1%, p=0.14（讨论） | 46.2/47.1/0.14 | **源文件中无 46.2%** | 两个 JSON 均无 | ✗ **F3** |
| 图件 DPI | ≥300（正文）/350（docx） | 350.0（5 PNG pHYs） | docx media | ✓ |
| docx 内嵌图数 | 5 | 5（inline 形状） | document.xml | ✓ |
| docx 新措辞 | within-animal paired / not independent corroboration 在；genuinely independent cross-animal 不在 | 同上 | docx 文本 | ✓ |
| gate | 0 failure / 0 warning / 47 passed | **同左（实跑确认）** | `p7_consistency_gate.py` | ✓（但范围有限） |

**说明：** 表中"✗"项为我在独立复算中确认与源数据或稿件自身不一致的发现（F1、F2、F3、F4）；"✓"项为确认一致；F2/F3 的数字本身正确但**显著性/口径表述**错误，已在对应发现中说明。所有"我重算值"均由我直接从上述 CSV/JSON 读取并计算，未依赖稿件转录。

---

## 五、审计范围与限制（Scope & limitations）

为透明起见，明确本次审计"复算了什么、没有复算什么"：

1. **复算对象 = 已落盘的产出 CSV/JSON 与稿件文本。** 我对所有强制清单内的表（`META_DRG_axis_stouffer.csv`、`_R4_random_effects_meta.csv`、`P3_lodo_auc_ci_leakage_controlled.csv`、`P3_hub_genes.csv`、`P3_geneset_stats.csv`、`_R4_targetset_bootstrap_resamples.csv`、`_R4_translation_noncircular.json`、`_R4_nerveinjury_only_summary.json` 等）从原始文件重算，并与稿件逐项比对；对图件嵌入与 DPI、docx 文本措辞做了直接检查；并**实际执行**了 `p7_consistency_gate.py`。

2. **未独立重跑上游分析脚本。** 我没有重新运行产生这些 CSV 的 `p2_deg_meta.py`、`p3_ml_leakage_controlled.py`、`p7c_nerveinjury_only_meta.py`、`p7b_translation_noncircular.py`、`make_sr_figures.py` 等。我的验证是**溯源式（provenance）**而非**端到端重执行**：即确认"稿件里的数 = 已归档产物里的数"，但产物本身是否由脚本正确生成，需作者在可复现性环节保证。这一点对 F1/F3 尤其相关——若 32/35 与 46.2% 来自某个未纳入本次强制清单的旧脚本/中间文件，端到端重跑才会暴露。

3. **未独立重算 docking AUC 与 ML LODO 模型。** ADRA2A 的全库/Tier-1 AUC、ML 三方法重要性等是上游模型输出；我只核验了它们在稿件中的记录值与对应 CSV 字段（如 LODO 的 `auc`/`n_selected` 字段、Table 2 的 `lasso_freq`/`rf_gini`/`shap_meanabs`）一致，未重新训练模型或重跑 Vina。这是 provenance 审计的合理边界，但意味着"模型是否过拟合/泄漏"不在本次 scope 内（稿件已就 LODO 的 within-animal 问题做了自省，见 L64/L304）。

4. **一处源标识可能错位（提请作者注意）。** gate 项 "HC plasma miRNA pairs: 328" 与 "distinct plasma miRNAs: 253" 在 `results/tables/` 中我能找到的最接近来源是 `P4_GSE222979_detection.json` 的 `"urine": 328` 与 `P4_setlevel_test.json` 的 `"n": 253`——二者分别是 **urine** 与 **set-level 检验**，并非字面的 **plasma**。稿件若声称这些是 plasma miRNA，则存在"源标识与字段语义不符"的隐患（属于 F3 同类的可溯源性问题）。我未将其列为正式发现，因为不确定作者是否另有一份 plasma 专属产物；但建议作者在 Data availability 中把"328/253"精确指向其真实源文件与字段。

5. **禁读文件未触碰。** 严格未读取 `reviews/REVIEW_*`、`RESPONSE_*`、`REVISION_*`、round12/13 panel 目录、`SUBMISSION_MANIFEST.md`、`GITHUB_PUSH_LIST_v1.4.md`、`GITHUB_DEPOSIT_SOP.md`、`author_verification_statement.md`、`_quarantine/`，以及同 panel 的 `A1_*`/`A2_*`/`A4_*` 文件。本报告所有结论均独立得出。

---

## 六、总体判定

- **可复现性基础扎实：** 核心统计量（meta 规模、core、CACNA2D1、RE τ²/I²、LODO AUC 与 n_selected、Jaccard/bootstrap、基因集 q、bulk-only core、谱系/背角计数、图件 350 DPI 嵌入、gate 47/0/0）均经我重算确认，来源文件与稿件一一对应。这是一份在工程上相当诚实、溯源良好的稿件。
- **但存在 3 处会触发技术核查/审稿质疑的硬伤（F1–F3）和 1 处轻微不一致（F4）：** 其中 F1（32/35 与自身 Table 2 矛盾）与 F2（同一 p 值"significant/non-significant"自相矛盾）最严重，F3（讨论段 46.2%/p=0.14 无源可溯）次之。
- **gate 通过 ≠ 无问题：** 我实跑确认 gate 为 47/0/0，但它的检查范围不包含 F1–F3 这类显著性标注与口径/源对应问题。本次审计正是 gate 未覆盖的盲区。
- **建议：** 在重投前至少修正 F1（26/35）、F2（统一为 significant depletion + lesion-class caveat）、F3（删除或补源）、F4（摘要 q=0.0022）。这些是低成本、高回报的修改，能显著提升稿件在统计核查阶段的存活率。
