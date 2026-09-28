# REVIEW — Round 15 (v1.5.0, 2026-09-28)

## 委员会结论（强制独立四专家，互不读前轮报告，从产物重算）

| 专家 | 角色 | 裁决 | 一句话 |
|---|---|---|---|
| A1 | 领域/临床科学 | **minor-revision**（1 个硬门） | 主线机制自洽、诚实阴性是卖点；唯一硬门 = B1 陈旧核心数自相矛盾 |
| A2 | 设计/统计 | **minor-revision** | 统计稳健、可复现；旧 XGBoost 索引错配 bug 已修复；仅措辞级小项 |
| A3 | 实现/溯源/复算 | **minor-revision** | 代码—手稿主体一致；F1 版本号漂移、F2 gate 弱化为真缺陷 |
| A4 | 期刊/合规 | **minor-revision** | 图已内嵌（修复了 SR 致命伤）；**结构化摘要是技术检查硬 blocker** |

**四人均未建议 reject / major-revision；无科学缺陷，均为诚实阴性边界论文框架内的小修。**

## 信任核验（主编独立复算，非仅采信面板）

我（主编）在把 A1 的 B1、A4 的结构化摘要、A3 的 F1 列为"真 bug"前，逐条独立核验：

- **B1 属实**：`results/tables/META_bulkonly_sensitivity_summary.json` 仍含 `primary_core_size: 4055`、`overlap: 2202`、`overlap_pct_primary: 54.3157`；`results/tables/META_collapse_meta.csv` 仍含 `orig_core: 4055.0`。稿件 L44 写 "overlap 54.3% / retention 91.4%"，与同稿 L50/L321 权威数 **bulk 重叠 63.2%（1,737/2,750）**、**collapse 保留 91.0%（2,502/2,750）** 直接自相矛盾。2202/4055=54.3% 的分母是旧核心 4,055（Round-13 已改为 2,750），故该百分比是陈旧派生值。
- **A4 结构化摘要属实**：摘要 L14–20 用 `**Background./Methods./Results./Conclusions.**` 四个标签分段。PLOS ONE 要求**非结构化摘要（无小标题）**，属技术检查拒修级硬要求。
- **F1 属实**：`MVP_PLOSONE_compliance_check.md` L22/L74 写 `v1.3.0`，且文件自身矛盾（L18 "37 refs" vs L20 "40/40"；L15 摘要 "256 words" 与实际 ~279–286 不符；引用不存在的 `MANIFEST.sha256`）。该自检不可信，须重建。

## 关键数独立复算（四面板 + 主编，全部与产物一致 ✓）

- 四核心基因集 set-level BH `q = 0.0022`（FE & RE 同；`_R4_geneset_setlevel_bh.csv`）
- 严格非循环 stratum `1,660/3,830 = 43.3%` vs 背景 `6,772/14,390 = 47.1%`，`perm_p = 0.0002`（耗竭；`_R4_nerveinjury_only_summary.json`）
- 中位数 `I² = 41.8%`、`τ² = 0.266`（`_R4_random_effects_meta.csv`，n=16,552）；RE core=508、FE core=2,750
- 核心 = 2,750；35 hub 中 26/35 属 meta-core、7/35 属 RE-core（`P3_hub_genes.csv`）
- SCN9A/10A/11A/8A 的 bulk meta_Z/FDR 与稿件 Table 1b 逐项吻合（`META_bulkonly_meta.csv`）
- 无虚拟 Zenodo DOI；git tag `v1.5.0` → `a5c610a` = HEAD；docx 内嵌 5×350 DPI PNG 且文本层数与 md 一致

## 逐条处置表（v1.5.0 → v1.6.0 修订清单）

| # | 来源 | 分类 | 处置（v1.6.0 动作） |
|---|---|---|---|
| B1 | A1 | **真 bug（数据完整性）** | 重建 `META_bulkonly_sensitivity_summary.json`（primary_core_size→2750，重算 overlap_pct_primary）与 `META_collapse_meta.csv`（orig_core→2750，重算 retained 比例）；稿件 L44/L50 清除陈旧的 54.3%/91.4%，统一到权威 63.2%（1,737/2,750）/91.0%（2,502/2,750） |
| A4-abs | A4 | **真 bug（合规硬 blocker）** | 摘要 L14–20 由 Background/Methods/Results/Conclusions 标签改为**非结构化连续段落**，保留全部内容且 ≤300 词 |
| F1 | A3+A4 | **真 bug（文档可信度）** | 重建 `MVP_PLOSONE_compliance_check.md`：统一版本号 `v1.5.0`、参考文献 40 条、准确摘要词数、删除不存在的 `MANIFEST.sha256` 引用 |
| F2 | A3 | **真 bug（gate 健壮性）** | 强化 `p7_consistency_gate.py` 的 `chk(label, expect, needle)`：在 `needle in txt` 之外**再断言动态 `expect in txt`**（期望值由产物派生，非写死），闭合"数值漂移"盲区（[4b] 真实单元格对账保留） |
| A2-1 | A2 | 评审过度谨慎/已正确 | 摘要 "median I² 79.1%" 已限定在 35-hub 子集语境，非全基因组；**不改**，可顺带一句澄清 |
| A2-2 | A2 | 已披露/非 blocker | GSE265957 D4/D63 同动物作独立输入（~11.4% Σw²）已在 L44 充分披露并有多敏感性分析兜底；**不改** |
| A2-3 | A2 | 已披露/非 blocker | 四核心集 q=0.0022 因同处 2000-perm 下限而相同，已披露；**不改** |
| A4-AuthorSummary | A4 | 软（合规事实更正） | PLOS ONE 的 Author Summary 是**强制**（非 compliance_check 误称的"optional"）；当前已存在（~237 词），**精简**即可 |
| A4-CCBY | A4 | 软（WARN） | CC BY 许可在投稿系统勾选；在 cover letter 补一句声明 |
| A4-STROBE | A4 | 软建议 | STROBE 对本 in-silico 元分析契合弱，建议改用 PRISMA + GEO/MIAME；**本轮不改报告指南**（STROBE 类比适用不导致退修），记入下一轮考量 |
| A1-ADRA2A | A1 | 已正确降级 | ADRA2A size-independent q=0.0025 已正确从属到失败的 0.532 原始富集；**不改** |

## 真实 gate 缺陷（非稿件 bug）与修复

- `p7_consistency_gate.py` 的 `chk()` 仅做 `needle in txt` 字符串存在性检查，从不比较动态期望值与实际值，39/49 项无法拦截数值漂移（仅 [4b] 10 项做真实单元格对账）。v1.6.0 计划改为 `expect in txt` 断言（期望由产物动态派生）。此项属流程闭环，直接呼应本沙箱既有教训"gate 期望值禁止硬编码、必须派生自权威产物"。

## 发布状态（v1.5.0）

- 已发布并经 `git ls-remote` 实测核验：`origin/main` 与 `refs/tags/v1.5.0` 均 = `a5c610a`。
- 本轮未改动任何交付物（仅评审 + 本核验报告）。

## Round 15 → v1.6.0 计划（待"继续"执行）

1. **B1**：找生成 `META_bulkonly_sensitivity_summary.json` / `META_collapse_meta.csv` 的脚本，以 2,750 核心重跑；或直接以权威数修正两文件并清理稿件 L44/L50 的 54.3%/91.4%。
2. **A4-abs**：摘要改非结构化（重写 L14–20，≤300 词）。
3. **F1**：重建 compliance_check.md（v1.5.0 / 40 refs / 准确词数 / 删 MANIFEST.sha256）。
4. **F2**：强化 p7 gate 的 `chk()` 期望值断言。
5. **A4-AuthorSummary/CCBY**：精简 Author Summary、cover letter 补 CC BY 声明。
6. 重建 docx 投稿包（Manuscript/Supporting/Cover/STROBE）→ 跑 p7 + gate_consistency + gate_word 三门 → docx 数值审计 → 提交并 SSH 发布 `v1.6.0`（ls-remote 核验）。
7. 若 A4-STROBE 建议后续采纳，下一轮再评估切换报告指南。

## 结论

Round 15 四专家一致 **minor-revision**，无科学缺陷、无 reject。真缺陷集中在三处：**B1 陈旧核心数自相矛盾（数据完整性）**、**结构化摘要（合规硬 blocker）**、**compliance_check 版本号/文献数漂移（文档可信度）**，外加 gate 健壮性（F2）。全部为可机械落地的诚实修正，落地后预期达到 accept 门槛。
