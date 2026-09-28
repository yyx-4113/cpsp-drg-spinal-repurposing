# MVP PLOS ONE — Round 17 Enforced-Independence Review (2026-09-28)

**稿件版本**：v1.7.0（commit `cad9dfc`，tag `v1.7.0`，已推送并 `git ls-remote` 核验）
**评审方法**：四专家 enforced-independence（A1 领域 / A2 设计统计 / A3 代码溯源 / A4 期刊合规+STROBE）。专家**未读取** Round 1–16 任何文件或作者 rebuttal；关键统计量**从产物 CSV 独立重算**，不信任稿件。

## 综合判定

| 专家 | 判定 | 阻断级发现 |
|---|---|---|
| A1 领域 | minor revision | REG3B nerve-injury-only FDR 2.1e-20 → 3.18e-20 |
| A2 设计统计 | minor revision | 同上（统计口径无误、数值转录错） |
| A3 代码溯源 | minor revision | 同上（产物溯源 3.18e-20） |
| A4 期刊合规 | minor revision | 无合规阻断；唯一随正文同步 REG3B 修正 |

**0 reject，0 科学缺陷。唯一阻断级问题 = REG3B nerve-injury-only FDR 稿件↔产物漂移。**

## 独立重算要点（全部从产物文件，非稿件）

- **DAM 三基因**（六输入 + 四-bulk）：TYROBP/TREM2/APOE 的 meta_FDR 与 consistency 与 `META_DRG_axis_stouffer.csv` / `META_bulkonly_meta.csv` **逐项一致**。
- **Table 3 十靶标**（ADRA2A…ITPKC）：meta_Z / meta_FDR / consistency / FDR_RE 与 `META_DRG_axis_stouffer.csv` + `_R4_random_effects_meta.csv` **10/10 一致**（GALNS FDR_RE 0.0001≈1.18e-4，四舍五入可接受）。
- **P2RX perm p 0.56**（六输入）= 产物 `P3_geneset_stats.csv` / `_R4` permutation p ✅。
- **REG3B 六输入 FDR 1.38e-13** = `META_DRG_axis_stouffer.csv` meta_FDR 1.379e-13 ✅。
- **REG3B nerve-injury-only FDR**：产物 `_R4_nerveinjury_only_meta.csv` `FDR_NI` = **3.177e-20**；稿件写 **2.1e-20**，全仓无此值来源 → **漂移**。
- **P6 双滤网裁决**：ACVR1/MAPK14/ADRA2A → FAIL_FILTER1；AXL/TNIK → FAIL_FILTER2（ΔAUC CI 含 0）；`enrichment_verdict()` 实现与生成器传参已确认重跑可复现，无"重跑回退 PASS"风险。
- **OXPHOS RE q 0.0022** = `_R4_geneset_setlevel_bh.csv` random perm_q 2.249e-3 ✅。
- **翻译 perm ≤0.0002** = `_R4_translation_noncircular.csv` 0.00019996 (1/5000 地板) ✅。

## gate 终态（v1.7.0）

- p7_consistency_gate：70 检查 / 0 失败（版本已从 CITATION.cff 动态读取，去硬编码）
- gate_consistency：57 通过 / 0 失败
- verify_sr_docx：47 通过 / 0 失败（5 图内嵌 350 DPI）

## 实施决定

仅 1 处阻断级修正：稿件 L78 REG3B nerve-injury-only FDR **2.1×10⁻²⁰ → 3.18×10⁻²⁰**（溯源权威产物）。
另 1 处非阻断建议（A1/A2）：P2RX 句补 "permutation" 以消除 Stouffer/permutation 歧义。
→ 落 v1.8.0：改稿件 + 版本号 + 重建 docx + 跑 gate + commit/tag/push/ls-remote 核验，随后复评为 **accept**。

## 历史教训（不重复前错）

- 前序轮次"gate 全绿"曾掩盖 bootstrap 索引错配与重复 table 等真 bug；本轮坚持"审代码+独立重算+产物溯源"三件套，确证除 REG3B 单点数字漂移外，稿件↔产物↔代码三角一致。
- REG3B 漂移属"与产物不一致"类（真 bug），非循环验证；修正后须全下游扫描确认无旧指纹残留。
