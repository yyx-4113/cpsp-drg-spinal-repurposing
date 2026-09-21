# P5 Stretch · GSE325938 Visium 空间定位（35 hub 程序的空间区域化）

> 生成日期：2026-09-19 ｜ 脚本：`scripts/p5_visium325938.py`（v2，修复大小写匹配与内存）
> 数据：GEO GSE325938（`GSE325938_processed_data.tar.gz`，214 MB，spaceranger-1.3.1）。
> 产物：`results/tables/P5_GSE325938_*.csv`、`results/figures/P5_GSE325938_*.png`

## 0. 数据事实与范围（务必先读）
- GSE325938 = "Spinal signatures of entrenched and treated neuropathic pain in male mice [Visium]"，
  8 样本：**4 鼠(Sham, ENSMUS) + 4 人源移植(ENSG)**。
- **该 Visium 无鼠 SNI 臂**（样本标题 `Mouse_Sham1-4` / `Human_2/4/6/8`；
  P5 的 Sham-vs-SNI 对比来自 **snRNA GSE328175**，非本 Visium）。
- 主分析仅取鼠 4 样本臂（与 P5 排除 hg19 人源移植臂一致）；人源移植臂（ENSG）被排除。
- 因无鼠 SNI 空间臂，**无法做空间 Sham-vs-SNI DE**；改为对鼠 4 切片做 hub 程序的**空间区域化**
  （背角/腹角/白质/胶质区），并与 P5 snRNA 细胞类型定位做**跨模态互证**。

## 1. 方法（纪律）
- spot×gene 矩阵（features.tsv 第 2 列 symbol，重复 symbol 求和；**大小写不敏感匹配 hub/marker**）；
  `log1p(CPM)` 归一化；仅保留 `in_tissue` 且总计数≥中位数 5% 的 spot。
- 空间区域：HVG(top1500, 离散度) → PCA(20) → KMeans(k=7) 得 7 个转录区域；
  用 canonical marker 集（背角痛觉/运动神经元/白质/星形/小胶/室管膜/脑膜纤维）**z 标准化后 argmax** 标注区域。
- **伪重复纪律**：spot 非独立（空间自相关）→ 区域均值先按切片(样本)聚合，再跨 4 切片报 mean±sd（描述性，不报 p）。
- 排除 PAN_NUCLEAR 看家/泛核基因作 marker。

## 2. 结果
- 鼠 4 切片共 **5853** 个 in-tissue spot 进入分析；35 hub 中 **35** 个在鼠 Visium 有表达。
- 7 个空间区域标注：R0=MeningealFibro(208), R1=WhiteMatter(678), R2=WhiteMatter(2693), R3=DorsalHorn(285), R4=VentralHorn(348), R5=Ependymal(1537), R6=MeningealFibro(104)。
- hub 空间富集分层（沿用 P5 阈值 log2≥1.0=restricted，≥0.58=enriched）：
  **restricted=26，enriched=7，其余 broad/low**。
- 落在 **DorsalHorn（背角，痛觉传入第一站）** 为 top 区域的 hub 数 = **17**。
- 跨模态（vs P5 snRNA 细胞类型）：consistent=6，divergent=9
  （详见 `P5_GSE325938_crossmodal.csv`）。

## 3. 解读
- Visium 第一次给出 hub 程序的**空间坐标**：哪些 hub 富集于背角（痛觉第一站）、哪些散布于白质/胶质区——
  这是 snRNA（只给细胞类型）无法提供的维度。
- 与 P5 snRNA 的互证：snRNA 定到 Neuron 的 hub 应富集于背角神经元区；定到 Microglia 的应富集小胶区；
  一致项支持"该 hub 确属脊髓痛觉回路"，分歧项提示空间层级与细胞类型层级并非一一对应（正常）。
- 代表性 hub 空间图见 `P5_GSE325938_hub_spatial.png`（ATF3, SPRR1A, TFE3, MAPK14, NPY, CHL1）；
  区域图见 `P5_GSE325938_regions.png`；富集热图见 `P5_GSE325938_hub_region_heatmap.png`。

## 4. 局限（随结论）
1. 无鼠 SNI Visium 臂 → 空间 Sham-vs-SNI 差异不可得；区域化仅描述性。
2. n=4 鼠切片均为 Sham → 区域均值跨切片稳定性中等（mean±sd 报告，不推断）。
3. 区域标注依赖 canonical marker 集，非组织学 lamina 金标准；7 区为无监督+marker 标注，边界近似。
4. 人源移植臂被排除（物种注释不同）；若需人源 hub 定位须做鼠→人同源映射，属另一步。
5. spot 级伪重复已规避；ambient RNA：Visium 全组织切片 ambient 风险低于单核，但未做专门 ambient_index 排查
   （与 P5 §3 的 ATF3 ambient 警示对照，本层 ATF3 空间信号按"损伤/再生"预期解读，建议谨慎）。
