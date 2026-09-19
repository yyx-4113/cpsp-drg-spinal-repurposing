# P4 结果 · 人源层（血浆 miRNA）+ miRNA→hub 间接链

> 生成日期：2026-09-16 ｜ 脚本：`scripts/p4_mirna.py`、`p4_targets.py`、`p4_integrate.py`、`p4_figure.py`
> 数据源：GSE158825（人血浆 miRNA, n=60, 腰椎手术 + 疼痛结局）、GSE222979（人 3 体液 miRNA, n=1242）、miRDB v6.0 预测靶点
> 产物：`results/tables/P4_*.csv/json`、`results/figures/P4_human_miRNA_layer.png`

---

## 1. GSE158825（人血浆 miRNA，术后疼痛结局）

样本：**60 例**（LSS 30 / LSS+DS 30；男 32 / 女 28），表型含 **`% nprs20delta`（NRS 疼痛变化，n=56 有值，中位 59）**。
> 注：矩阵列 ID 前 30 为大写 `-SPINE`、后 30 为小写 `-spine`，须**大小写归一**才能匹配全部 60 例（易踩坑）。

| 分析 | 表达 miRNA | FDR<0.05 | 最小 p |
|---|---|---|---|
| LSS+DS vs LSS（Welch t + BH） | 999 | **0** | 1.3e-4（FDR 0.128） |
| 与 %nprs20delta 相关（Spearman + BH） | 999 | **0** | 8.5e-4（FDR 0.556） |

- **无 FDR 显著**——n=56–60 功效不足。
- 名义命中的是**免疫 miRNA 模块**：`miR-139-3p`、`miR-1260a`、**`miR-155-5p`**、**`miR-146a-3p`**、`let-7e-5p`、`miR-125a-5p`、`miR-99b-5p`。
  其中 **`miR-99b / let-7e / miR-125a` 是一个已知多顺反子簇**，其成员共同出现在前列 → 提示该簇与疼痛结局协同相关（hypothesis）。

## 2. 人源 miRNA → hub 基因 间接链（miRDB v6.0）

- 用 NCBI `gene2refseq` + `gene_info` 建人 RefSeq→symbol 映射（279308 条），把 miRDB 的 RefSeq 靶点转成基因符号。
- **35 个 hub 中 33 个有预测靶向 miRNA**；高置信（score≥80）**608 个 miRNA**。
- **603→253 个在人血浆中可检出**（GSE158825）；在 GSE222979 中三体液可检出 **308（血浆）/ 323（滑液）/ 328（尿）**。
- 名义关联最强（与疼痛结局）：`miR-146a-3p`(→TFE3, rho=0.367, p=0.0055)、`miR-199b-5p`(→FLRT3;SERPINE1, p=0.032)、`miR-204-5p`(→RUBCN)、`miR-22-3p`(→**MAPK14**)、`miR-143-3p`(→PTPN23)、`miR-9-5p`(→ITPKC)。

### 集合水平检验（关键诚实结论）
对 253 个 hub 靶向 miRNA 的 rho 做单样本检验：

| 检验 | 结果 |
|---|---|
| 单样本 t | p = **0.029** |
| Wilcoxon | p = 0.035 |
| **同尺寸随机 miRNA 集置换（5000 次）** | **p = 0.51** |
| 方向 | 144 正 / 109 负 |

→ **集合水平关联不成立**：名义 t 显著来自 miRNA 之间的强非独立性（共享靶点/共调控），置换检验校正后消失。**必须如实报告为阴性。**

## 3. GSE222979（人 3 体液 mRNA… 实为 miRNA，n=1242）

- 结构解码：**414 血浆 + 414 滑液 + 414 尿**，膝关节置换患者（LEAP 队列），含 age/sex/bmi/procedure/leap id。
- ⚠️ **无疼痛结局表型**（series_matrix 仅人口学 + 手术类型）→ **不能**做疼痛关联；仅作跨界资源：证实 hub 靶向 miRNA 在人体多体液可检出（§2），支持"这些 miRNA 在人源可测"。
- 原计划"1242 例内型分析"**不可行**，除非另获 LEAP 表型（外部申请）。

## 4. P4 总结论（写入 Limitations）

1. **人源直接验证链依然缺失**：GSE306403 非人组织（SH-SY5Y），GSE222979 无表型，GSE158825 无 FDR 显著。
2. hub 靶向 miRNA **在人体可检出**（血浆 253 / 多体液 308–328），但**与术后疼痛结局无稳健关联**（置换 p=0.51）。
3. 三类人源资源的合理定位：**GSE158825 = 名义假设来源**；**GSE222979 = 可检出性支持**；**GSE306403 = 体外阿片机制参考**。
4. **人源确证必须靠前瞻性临床 qPCR/ELISA**（Stretch），这是稿件必须明示的边界。

## 5. 产物

| 文件 | 内容 |
|---|---|
| `P4_GSE158825_miRNA_LSSDS_vs_LSS.csv` | LSS+DS vs LSS 的 log2FC/t/p/FDR |
| `P4_GSE158825_miRNA_painoutcome_spearman.csv` | 999 miRNA 与 %nprs20delta 的 Spearman + FDR |
| `P4_hub_targeting_miRNAs.csv` | 608 个 hub 靶向高置信 miRNA（3551→含全部评分） |
| `P4_hub_miRNA_human_integration.csv` | 253 个可检出 hub 靶向 miRNA + 疼痛关联 |
| `P4_setlevel_test.json` / `P4_GSE222979_detection.json` | 集合检验与三体液检出 |
| `P4_human_miRNA_layer.png` | 火山图 + 体液检出 + 置换零分布 |

## 6. 下一步（P5 → P6）

- **P5 单细胞/空间定位**：GSE328175 / GSE216039（DRG 神经元）/ GSE246288（小胶质）；细样本级 pseudobulk，验证 hub 的细胞归属（神经元 / 卫星细胞 / 小胶质 / 少突胶质）。
- **P6 虚拟筛选**：从 35 hub 选可成药蛋白（优先神经免疫/代谢 + Sigma-1 / **MAPK14** / AXL / ACVR1），按 §6 规则对接 FDA 库 + 反向阳性对照。
