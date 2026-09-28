# MVP PLOS ONE — Round 18 Accept-Confirmation Review (2026-09-28)

**稿件版本**：v1.8.0（commit `0f6dd30`，tag `v1.8.0`，已推送并 `git ls-remote` 核验）
**评审方法**：四专家 enforced-independence（A1–A4），未读 Round 1–17 评审正文；仅对照权威产物 CSV 复算并核验 v1.8.0 相对 v1.7.0 的修订。

## 本轮目的

Round 17 对 v1.7.0 判 **minor revision**，唯一阻断级缺陷 = REG3B nerve-injury-only FDR 稿件↔产物漂移（2.1e-20 vs 3.18e-20）。v1.8.0 已修正该缺陷并补 P2RX 措辞。本轮确认修订落地、无新引入问题。

## 复算核验（v1.8.0）

| 检查项 | 结果 |
|---|---|
| REG3B L78 nerve-injury-only FDR = 3.18×10⁻²⁰ | ✅ 与 `_R4_nerveinjury_only_meta.csv` `FDR_NI`=3.177e-20 一致 |
| REG3B 六输入 FDR = 1.38×10⁻¹³ | ✅ 与 `META_DRG_axis_stouffer.csv` 一致（未变） |
| P2RX L80 "permutation p = 0.56 in the six-input meta" | ✅ 消歧义；0.56 = 六输入 permutation p |
| 版本号（稿件/CITATION.cff/README/cover letter/compliance） | ✅ 全 v1.8.0；无 v1.7.0 残留于当前态 |
| 三门 gate | ✅ p7 0 失败/70 检查；gate_consistency 57/0；verify_sr_docx 47/0（5 图 350 DPI） |
| 全下游一致性扫描 | ✅ 旧 REG3B 2.1e-20 指纹 0 命中 |

## 委员会裁决

| 专家 | 判定 |
|---|---|
| A1 领域 | **ACCEPT** |
| A2 设计统计 | **ACCEPT** |
| A3 代码溯源 | **ACCEPT** |
| A4 期刊合规 | **ACCEPT** |

**0 reject，0 minor-revision 遗留项。全部此前发现的数值/discourse/合规问题已闭环。**

## 结论

v1.8.0 达到 **accept** 状态：科学核心健全、所有数字可溯源至产物、期刊合规全满足、gate 全绿。投稿包（Manusstit/Supporting/Cover_Letter×2/STROBE，5 图内嵌 350 DPI，CC BY，数据可用性 GitHub v1.8.0 版本化归档无伪 DOI）处于可投状态。实际期刊上传由作者在 PLOS ONE Editorial Manager 完成。

## 流程说明（对用户诚实交代）

- Round 17 的 minor-revision 源于**一处数值转录漂移**（REG3B nerve-injury-only FDR），非方法论失误、非计算 bug；该漂移由"独立重算 + 产物溯源"三件套抓出，正是您要求的审核纪律生效。
- 自 v1.0.0 至 v1.8.0 共 18 轮评审，累计修正的真实缺陷包括 bootstrap 索引错配、重复 table、结构化摘要违规、跨文件版本漂移、Unicode 引用乱序、DAM 散文陈旧数、P6 verdict 矛盾、REG3B 双 FDR 漂移等——均为"稿件↔产物↔代码三角"不一致，已全部闭环。
- "gate 全绿"不等于"评审过"：每一轮真正价值来自对散文/补充材料/产物的独立重算，gate 仅验证自洽。此纪律在 v1.8.0 末轮仍被严格执行。
