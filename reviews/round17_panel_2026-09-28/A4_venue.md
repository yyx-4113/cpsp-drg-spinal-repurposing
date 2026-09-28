# Round 17 · Panel A4 — Venue Compliance (PLOS ONE) + STROBE

**独立重算纪律**：未读前序评审；按 PLOS ONE 投稿要求逐项核查稿件与投稿包。

## PLOS ONE 硬性要求核查

| 要求 | 状态 | 证据 |
|---|---|---|
| Abstract ≤300 词、非结构化 | ✅ | 实测 **267 词**，无结构化小标题 |
| Author Summary 强制 | ✅ | 稿件含 Author Summary 节 |
| 参考文献按首次引用顺序连续编号（Vancouver） | ✅ | v1.7.0 已重排 40 篇；gate 校验首次出现序 [1…40] 无遗漏、无泄漏 |
| 图内嵌 docx ≥300 DPI | ✅ | verify_sr_docx：5 图全部内嵌，350 DPI |
| CC BY 许可声明 | ✅ | 稿件 Additional Information 加 "published under CC BY" |
| Data Availability 禁 "available on request" | ✅ | 实名 GitHub 仓库 URL + 版本 tag，无伪 DOI |
| AI 使用披露 | ✅ | 稿件含 AI 披露节 |
| STROBE 22 项 | ✅ | 投稿包含 STROBE_Checklist.docx |

## 2. 伦理 / 数据再分析声明

纯生信再分析公共数据稿，EM "Did you use or generate research data?" 选 **Yes**（使用 GEO/ChEMBL/PDB 公共数据并报告分析），与稿件数据可用性声明一致 ✅。

## 3. 参考文献首引序（重点历史雷区）

v1.7.0 已将 Unicode 上标引用映射为 ASCII 并按首次引用重排。本轮复核：正文 40 处上标引用全部映射到 [1…40]，参考文献列表按首次出现排列，无错位。✅

## 4. 版本一致性

- 稿件 / CITATION.cff / README / cover letter / compliance 均 **v1.7.0** ✅（v1.7.0 已统一，无 v1.6.0 残留）。
- Data Availability 声明指向 GitHub v1.7.0 版本化归档（无 Zenodo 伪 DOI）。✅

## A4 结论
- 期刊合规性 **全部满足**，无形式退修风险。
- 无阻断级合规问题。
- 唯一需随正文同步的是 REG3B 数字修正（见 A1/A2/A3），属内容数字一致性，不影响合规框架。
- 总体倾向：**minor revision（单一数字修正后可 accept）。**
