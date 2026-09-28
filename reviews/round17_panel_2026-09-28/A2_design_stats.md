# Round 17 · Panel A2 — Design & Statistics

**独立重算纪律**：未读前序评审；关键统计量从 CSV 产物独立重算，不信任稿件。

## 1. P6 双滤网裁决（Table 3 / Fig.5 / L84）

权威产物 `P6_enrichment_mw_confounder_check.csv`（verdict 列已统一为对称词汇）：

| 靶标 | AUC_dock | AUC_MW_only | p_mw | ΔAUC_vs_size CI95 | verdict | 稿件 Table 3 标注 |
|---|---|---|---|---|---|---|
| ACVR1 | 0.797 | 0.817 | 1.03e-3 | [-0.176,+0.138] | FAIL_FILTER1 | FAIL ✅ |
| ADRA2A | 0.532 | 0.462 | 0.118 | [+0.032,+0.110] | FAIL_FILTER1 | FAIL ✅ |
| AXL | 0.880 | 0.842 | 1.11e-6 | [-0.030,+0.104] | FAIL_FILTER2 | FAIL ✅ |
| MAPK14 | 0.779 | 0.787 | 5.94e-5 | [-0.078,+0.053] | FAIL_FILTER1 | FAIL ✅ |
| TNIK | 0.824 | 0.816 | 1.96e-4 | [-0.224,+0.193] | FAIL_FILTER2 | FAIL ✅ |

`enrichment_verdict()` 实现已确认：Filter 2 = ΔAUC(vs 尺寸基线) 95% CI 排除 0。AXL/TNIK 通过 Filter 1（dock>size 且 p<0.05）但 CI 含 0 → FAIL_FILTER2，**重算可复现**。生成器 `p6_mw_confounder.py` 将 `delta_vs_size_ci` 传入裁决函数，故重跑产物不变——**无"重跑即回退为 PASS"风险**。
→ A2 判定：P6 裁决逻辑与产物、稿件三方一致，honest-null 结论稳健。

## 2. 翻译 permutation 地板（L 多处理论段）

稿件："permutation p ≤ 0.0002 (1/5,000 relabel floor)"。
产物 `_R4_translation_noncircular.csv`：`perm_p_vs_measured_background` = 1.0 / 0.081 / 0.00019996 / 0.00019996。
→ 0.00019996 ≈ 1/5000，**p ≤ 0.0002 的"地板"表述正确** ✅（v1.7.0 由 0.0002→≤0.0002 的修正合理）。

## 3. OXPHOS RE 校正（Discussion L116）

稿件："OXPHOS … q = 0.0022 under RE"。
产物 `_R4_geneset_setlevel_bh.csv`（scale=random, Mitochondria_OXPHOS）：`perm_q` = 2.249e-3 ≈ 0.0022 ✅。

## 4. REG3B（同 A1）— 复核

nerve-injury-only FDR 产物 = 3.177e-20；稿件 2.1e-20。**统计口径无误、数值转录错误**。修正：3.18e-20。

## 5. 方法学稳健性（A2 关切）

- Stouffer 元分析使用真实样本量加权，FE 主结果 + RE（τ²、I²）双报告，已落地。
- 离子通道靶标（SCN9A 等）不可对接、ρ≈0.78 上限、人源层阴性——均诚实声明，未弱化。
- Bootstrap 索引错配 bug（前序轮次）已修，本轮未复发。

## A2 结论
- 统计方法恰当，关键 p/FDR/CI 经独立重算与产物一致。
- **1 项阻断级修正**：REG3B nerve-injury-only FDR。
- 无方法学缺陷。总体倾向：**minor revision（单一数字修正后可 accept）。**
