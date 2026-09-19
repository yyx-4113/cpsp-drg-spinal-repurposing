# P2 结果 · 分数据集 DEG + DRG 轴 Stouffer 元分析

> 生成日期：2026-09-16 ｜ 脚本：`scripts/p2_deg_meta.py`、`scripts/p2_figure.py`
> 产物：`results/tables/DEG_*.csv`（14 个对比）、`results/tables/META_DRG_axis_stouffer.csv`、
> `results/tables/META_DRG_axis_CORE_signature.csv`、`results/figures/P2_core_signature_heatmap.png`

---

## 1. 方法与纪律

- **标准化**：原始计数 → `log2(CPM+1)`；GSE212311 用其自带 `log2(FPKM+1)`；同 symbol 取均值。
- **DEG**：Welch t 检验（不等方差）+ Benjamini–Hochberg FDR。
- **元分析**：对每个基因，取各数据集 Welch-t 导出的 Z（`sign(t)·Φ⁻¹(1-p/2)`），
  权重 `w = √(n_case·n_ctrl/(n_case+n_ctrl))`（反 SE 尺度），
  `Z_meta = Σ(w·Z)/√Σw²`，双侧 p + BH FDR；要求基因出现于 **K≥3** 个数据集。
- **方向一致性** = `max(n_up, n_dn)/K`。
- **跨物种**：symbol 统一大写（Atf3/ATF3 → ATF3）；已知局限（部分基因跨物种异名会丢失，属保守偏倚）。

## 2. per-dataset DEG 结果（FDR<0.05）

| 数据集 / 对比 | 轴 | n_case vs n_ctrl | DE 数 | up | down |
|---|---|---|---|---|---|
| GSE267799 SMIR DRG · chronic(10d+32d) vs baseline(0d) | DRG | 12 vs 8 | **0** | 0 | 0 |
| GSE267799 SMIR DRG · acute(6h+2d) vs baseline | DRG | 16 vs 8 | **0** | 0 | 0 |
| GSE267799 SMIR DRG · chronic vs acute | DRG | 12 vs 16 | 1 | 1 | 0 |
| GSE212311 CCI vs Sham | DRG | 3 vs 3 | **0** | 0 | 0 |
| GSE278227 CCI M_24h IL vs CL | DRG | 6 vs 6 | 882 | 571 | 311 |
| GSE278227 CCI M_1W IL vs CL | DRG | 7 vs 7 | 7613 | 4620 | 2993 |
| GSE278227 CCI F_1W IL vs CL | DRG | 7 vs 7 | 6996 | 4348 | 2648 |
| GSE278227 CCI M_5W IL vs CL | DRG | 5 vs 5 | 3976 | 2426 | 1550 |
| GSE278227 CCI F_5W IL vs CL | DRG | 6 vs 6 | 6222 | 3506 | 2716 |
| GSE278227 CCI 1W IL vs CL（合并性别） | DRG | 14 vs 14 | **9103** | 5565 | 3538 |
| GSE241361 S1R SNI vs Naive（WT DRG） | DRG | 4 vs 5 | 23 | 23 | 0 |
| GSE241361 S1R SNI vs Naive（WT 脊髓） | SC | 4 vs 5 | 121 | 119 | 2 |
| GSE241361 S1R KO vs WT（SNI DRG） | DRG | 4 vs 4 | 4 | 1 | 3 |
| GSE306403 SH-SY5Y Morphine vs Control（体外） | in vitro | 15 vs 3 | 10 | 6 | 4 |

### 两个关键「阴性/弱信号」结论（非 bug，是发现）

1. **GSE267799（LPI 切口模型，CPSP 最贴近）单基因层面无 FDR 显著**：最小 p=2.2×10⁻⁵，但 16016 个基因 BH 校正后无一通过。
   说明**切口模型 DRG 的转录反应幅度小、组内方差大**——单基因不足以定罪，必须靠**跨模型元分析 / 基因集 / ML** 聚合。
2. **GSE212311（CCI 3v3）**同样 0 显著——**小样本功效不足**（absence of evidence ≠ evidence of absence）。ATE3/Gal 等仍有明确定向效应（见元分析）。

> 这两点是论文「为什么必须做多集整合 + 基因集/ML」的直接论据，须写入方法学/讨论。

## 3. DRG 轴 Stouffer 元分析核心签名

- 参与：GSE267799(chronic vs base)、GSE212311、GSE278227(1W IL/CL)、GSE241361(SNI WT)、GSE265957 DRG D4、GSE265957 DRG D63 → **6 个对比，跨大鼠+小鼠，含切口+神经损伤**。
- 检验基因 **16552**；`meta_FDR<0.05` = **6869**；**核心签名（FDR<0.05 & 一致性≥0.8）= 4055**。
- Top 30（按 meta_p）：

| 排名 | 基因 | K | meta_Z | meta_FDR | 一致性 |
|---|---|---|---|---|---|
| 1 | **ATF3** | 6 | 10.53 | 1.0e-21 | 1.00 |
| 2 | **GAL** | 6 | 10.34 | 3.9e-21 | 1.00 |
| 3 | SMAGP | 3 | 9.66 | 2.5e-18 | 1.00 |
| 4 | **ECEL1** | 6 | 9.54 | 5.7e-18 | 1.00 |
| 5 | CDHR5 | 4 | 9.39 | 2.0e-17 | 1.00 |
| 6 | **NPY** | 6 | 9.27 | 4.9e-17 | 1.00 |
| 7 | FLRT3 | 6 | 9.25 | 5.2e-17 | 1.00 |
| 8 | ITGA7 | 6 | 9.20 | 7.3e-17 | 0.83 |
| 9 | STAC2 | 6 | 9.14 | 1.1e-16 | 0.83 |
| 10 | **ADCYAP1 (PACAP)** | 6 | 8.95 | 5.7e-16 | 1.00 |
| 11 | IL13RA1 | 5 | 8.88 | 9.7e-16 | 1.00 |
| 12 | TGM1 | 4 | 8.86 | 1.1e-15 | 1.00 |
| 13 | SDC1 | 6 | 8.85 | 1.1e-15 | 1.00 |
| 14 | **SOCS3** | 5 | 8.78 | 1.9e-15 | 1.00 |
| 15 | ZDHHC18 | 6 | 8.72 | 3.0e-15 | 1.00 |
| 16 | CCKBR | 6 | 8.71 | 3.2e-15 | 1.00 |
| 17 | COL16A1 | 6 | 8.59 | 8.5e-15 | 1.00 |
| 18 | **VGF** | 6 | 8.56 | 9.5e-15 | 1.00 |
| 19 | SBNO2 | 6 | 8.56 | 9.5e-15 | 1.00 |
| 20 | **SOX11** | 5 | 8.56 | 9.6e-15 | 1.00 |
| 21–30 | NKAIN1, DRAXIN, CHL1, FADS3, AZIN2, ABCA1, TUBB6, MAP7D1, PLAUR, JUN | | 8.2–8.5 | | |

**解读**：Top 签名几乎全是 DRG 损伤/疼痛的经典分子——**ATF3**（神经损伤金标准转录因子，排第 1，强阳性对照通过）、
**GAL / NPY / VGF / ADCYAP1(PACAP) / CCKBR**（痛觉神经肽及其受体）、**SOCS3 / SOX11 / JUN**（损伤应答转录调控）、
**STAC2 / FLRT3 / ECEL1 / CHL1 / DCC 通路**（神经重塑）。**流程有效性已被生物学阳性对照证实**。

## 4. 转化一致性：神经损伤签名 → 切口模型（CPSP 最贴近）

对「FDR<0.05 & 一致性≥0.6」且有切口模型数据的 5447 个基因：

- **在 LPI 切口 DRG 中同向 = 3261/5447 = 59.9%**（binomial vs 50%，**p = 2.8×10⁻⁴⁸**）。

**诚实结论**：切口模型与神经损伤模型**方向高度显著一致**，但**幅度更弱**（故单基因 FDR 不显著）。
即：CPSP 的分子签名与神经损伤部分共享，这既是"可外推"的证据，也提示切口模型需要更大 n 或基因集/ML 方法。

## 5. 产物清单

| 文件 | 内容 |
|---|---|
| `results/tables/DEG_*.csv` | 14 个对比的 log2FC / t / p / FDR（含 mean_case/ctrl、n） |
| `results/tables/META_DRG_axis_stouffer.csv` | 16552 基因元分析全表（含各集 log2FC、一致性、切口一致性） |
| `results/tables/META_DRG_axis_CORE_signature.csv` | 4055 核心签名 |
| `results/figures/P2_core_signature_heatmap.png` | 核心签名跨 6 集热图 + DEG 计数面板 |

## 6. 下一步（P2 尾 → P3）

1. **ComBat 敏感性矩阵**（仅作交叉验证，不做主要推断）。
2. **基因集统计**：对 GeneCards（neuropathic/chronic postsurgical pain）、DisGeNET、离子通道家族（TRP/ASIC/KCNH/SCN/P2RX/CACNA）、神经炎症/MAPK 各集合做成员 meta_Z 的 Stouffer/单样本检验。
3. **候选池** 构建：基因级（通路∩meta_p<0.05 且方向一致）∪ 集合级（集合显著取 |meta_Z| Top10）。
4. **双 ML 锁靶**：LASSO(λ.1se) + Boruta/RF(MDGini) + XGBoost gain/SHAP → 交集 hub；bootstrap(B=200,≥0.6) + 跨数据集 train→test 诚实评估。
5. **单细胞/空间定位**（P5）与 **虚拟筛选靶蛋白定义**（P6，见 `PROJECT_PLAN.md` §6）。
