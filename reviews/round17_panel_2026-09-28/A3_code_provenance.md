# Round 17 · Panel A3 — Code & Provenance Audit

**独立重算纪律**：未读前序评审；逐行核对关键分析脚本实现是否与稿件描述一致，并独立重算 ≥1 处关键统计量。

## 1. gate ≠ 正确性 复盘

- `p7_consistency_gate.py` 旧版硬编码 `if "v1.6.0" not in txt` → v1.7.0 升档时该 gate 会**误判 FAIL**。v1.7.0 已改为从 `CITATION.cff` 动态读取版本（行分割解析，免 BOM/正则陷阱）。✅ 已核实：解析返回 `v1.7.0`。
- 本轮实测：p7（70 检查 0 失败）、gate_consistency（57 通过 0 失败）、verify_sr_docx（47 通过 0 失败，5 图内嵌 ≥350 DPI）。

## 2. P6 verdict 生成器 ↔ 产物 ↔ 稿件 三角一致

- 旧 `enrichment_verdict()` 在 AXL/TNIK（dock>size、p<0.05、adj>0.5）会输出 `PASS_size_independent`，但稿件 Table 3 标 FAIL——**代码↔稿件矛盾**。
- v1.7.0 已重定义为对称双滤网：Filter 2 = ΔAUC(vs 尺寸基线) CI 排除 0；AXL/TNIK CI 含 0 → FAIL_FILTER2。
- 已核实 `p6_mw_confounder.py` 将 `delta_vs_size_ci=(dlo_s,dhi_s)` 传入裁决函数 → 重跑产物 = 当前 CSV，**不会回退为 PASS**。✅

## 3. 关键数字溯源（A3 强制：稿件每数须可追产物）

| 稿件数字 | 产物文件 | 一致? |
|---|---|---|
| DAM TYROBP/TREM2/APOE | META_DRG_axis_stouffer / META_bulkonly_meta | ✅ |
| Table 3 十靶标 meta_Z/FDR/cons/FDR_RE | 同上 + _R4_random_effects_meta | ✅ |
| P2RX perm p 0.56 | P3_geneset_stats / _R4 | ✅ |
| REG3B 六输入 FDR 1.38e-13 | META_DRG_axis_stouffer | ✅ |
| **REG3B nerve-injury-only 2.1e-20** | **_R4_nerveinjury_only_meta = 3.18e-20** | ❌ **漂移** |
| OXPHOS RE q 0.0022 | _R4_geneset_setlevel_bh | ✅ |
| 翻译 perm ≤0.0002 | _R4_translation_noncircular | ✅ |

## 4. 全下游一致性扫描（修上游后必做）

REG3B nerve-injury-only 2.1e-20 仅在稿件 L78 出现一处（grep 确认）。修正为 3.18e-20 后无遗留旧指纹。

## A3 结论
- 代码↔稿件↔产物三角一致已实质建立；gate 不再硬编码。
- **1 项阻断级修正**：REG3B nerve-injury-only FDR 产物溯源为 3.18e-20，稿件须对齐。
- 其余数字全部可溯源、可复现。总体倾向：**minor revision（单一溯源修正后可 accept）。**
