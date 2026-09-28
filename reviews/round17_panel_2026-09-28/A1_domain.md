# Round 17 · Panel A1 — Domain (DRG–脊髓轴 / 神经免疫 / 药物重定位)

**独立重算纪律**：本评审**未读取** Round 1–16 任何评审文件或作者 rebuttal；所有数字从产物文件独立重算。

## 1. DAM 核心闸（Discussion L116）

| 基因 | 稿件声称 | 权威产物 `META_DRG_axis_stouffer.csv` (六输入) | 一致? |
|---|---|---|---|
| TYROBP | meta_FDR 1.2×10⁻⁷, cons 4/5=0.80 | 1.185e-7, 0.80 | ✅ |
| TREM2 | meta_FDR 3.0×10⁻³, cons 4/6=0.67 | 3.036e-3, 0.667 | ✅ |
| APOE | meta_FDR 0.84, cons 4/6=0.67 | 0.845, 0.667 | ✅ |

四-bulk（`META_bulkonly_meta.csv`）：TREM2 FDR 1.32e-3（稿件 1.3×10⁻³ ✅）、APOE 0.295（稿件 0.30 ✅）。
→ A1 判定：DAM 描述与产物**逐字一致**，无领域事实错误。

## 2. P2RX 转录本家族（L80）

稿件："P2RX/P2RY … p = 0.56 in the six-input meta"。
产物 `P3_geneset_stats.csv`：`P2RX_P2RY` 六输入 Stouffer p = 4.07e-2（显著），**permutation p = 5.797e-1**；`_R4` fixed permutation p = 5.607e-1。
→ 稿件 "0.56" = 六输入 **permutation** p，与产物一致 ✅。
⚠️ 轻微提示：该句并列结构为 "permutation p = 0.339 in the bulk-only meta; p = 0.56 in the six-input meta"，第二分句省略了 "permutation"，可能被误读为 Stouffer p（实为 0.04）。建议补 "permutation" 以消除歧义（非阻断级）。

## 3. REG3B（L78）— **阻断级发现**

稿件："REG3B … meta-significant (1.38×10⁻¹³; nerve-injury-only FDR 2.1×10⁻²⁰)"。
- 六输入 FDR：`META_DRG_axis_stouffer.csv` REG3B meta_FDR = 1.379e-13 ✅ 与稿件 1.38×10⁻¹³ 一致。
- **nerve-injury-only FDR**：权威产物 `_R4_nerveinjury_only_meta.csv` REG3B `FDR_NI` = **3.177e-20**。
- 稿件写 **2.1×10⁻²⁰**，与产物 **3.18×10⁻²⁰ 不符**；全仓检索无任何产物含 2.1e-20 的 REG3B nerve-injury 值。
→ **A1 判定：REG3B nerve-injury-only FDR 为稿件↔产物漂移，须改为 3.18×10⁻²⁰（或 3.2×10⁻²⁰）。** 这是本轮唯一阻断级数字错误。

## 4. Table 3 十个靶标（Panel A/B）

ADRA2A / MAPK14 / AXL / TNIK / ACVR1 / SERPINE1 / SLC2A1 / GALNS / VASH2 / ITPKC 的 meta_Z、meta_FDR、consistency、FDR_RE 全部与 `META_DRG_axis_stouffer.csv` + `_R4_random_effects_meta.csv` 逐项核对，**10/10 一致**（GALNS FDR_RE=0.0001 对应产物 1.18e-4，属四舍五入，可接受）。

## A1 结论
- 领域叙事准确，DAM 三基因与 Table 3 数字经独立重算无误。
- **1 项阻断级修正**：REG3B nerve-injury-only FDR 2.1e-20 → 3.18e-20。
- **1 项非阻断建议**：P2RX 句补 "permutation" 消除 Stouffer/permutation 歧义。
- **总体倾向：minor revision（单一精确数字修正后即可 accept）。**
