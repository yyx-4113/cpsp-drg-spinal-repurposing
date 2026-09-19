# 项目图谱 · CPSP DRG-脊髓轴锁靶 + FDA 老药新用虚拟筛选

> **状态图例**：`[✅已完成]` `[⏳进行中]` `[⬜待办]` `[⚠️阻塞/需决策]`
> **最后更新**：2026-09-16 ｜ **负责人**：杨永新（福建中医药大学附属第二医院 麻醉科）
> **本文档定位**：项目唯一事实来源（living plan）。任何方向调整先改这里，再执行。

---

## 0. 一句话目标

用**多数据集整合 + 双机器学习**锁定慢性术后痛（CPSP）**DRG-脊髓轴**的可成药枢纽基因，再以 **FDA 已上市药物库做老药新用虚拟筛选**，产出一篇**统计严谨、可复现、数据/代码真实可获取**的高质量文章，终点直接指向可在疼痛科开展的小样本临床验证候选药。

---

## 1. 科学问题（锐化）

- **痛点**：10–50% 手术患者发展为 CPSP；现有治疗（加巴喷丁类 / NSAIDs / 阿片）疗效有限、副作用明显，且无"外周-中枢双向轴"视角的精准靶点。
- **核心假说**：CPSP 的急→慢性转化由 **DRG（外周感觉胞体）-脊髓（中枢突触）双向传导轴**上的一组协调枢纽基因驱动；其中部分枢纽蛋白是已上市药物的潜在新靶点（老药新用）。
- **可检验推论**：① DRG 与脊髓层存在共变枢纽模块；② 该模块与已知疼痛离子通道/神经炎症通路重叠；③ 模块代表基因在人源术后疼痛队列中方向一致；④ 其中可成药蛋白能被 FDA 药物库中的分子以合理亲和力对接。

---

## 2. 范围分层（保证"持续可交付"，不吊死在湿实验上）

| 层级 | 内容 | 可发表下限 | 目标期刊 |
|---|---|---|---|
| **MVP（必做）** | Phase 1–4 + 单 scRNA 定位 + Phase 6 对接（无 MD）+ Phase 7 写作 | 纯生信方法学+锁靶+重定位完整故事 | *J Transl Med* / *Front Pharmacol* / *Front Immunol* |
| **Stretch（加分）** | + 临床验证(30v30 qPCR/ELISA) + Visium 空间 + 小胶质 scRNA + 100ns MD + CMap 正交 | 机制确证+转化路径 | *Pain* / *BJA* / *Anaesthesia* |

> **原则**：MVP 即可成稿。湿实验（临床 qPCR/ELISA）是 Stretch 而非前提——这样项目**不会因临床入组/伦理卡住而停摆**，符合"持续进行"。

---

## 3. 数据资产核查表（2026-09-16 实检，全部存在且可获取）

| GSE | 角色 | 类型 | 样本数 | 物种 | 平台 | 处理矩阵 | 关键备注 / 对原方案的修正 |
|---|---|---|---|---|---|---|---|
| GSE267799 | 核心 | RNA-seq | **108** | 大鼠 | GPL32253 | ✅ FPKM+rawcount | **比原方案更丰富**：含 SMIR+LPI 双模型 × DRG/肌肉/皮肤 三组织。整合主料。 |
| GSE212311 | 外部验证 | RNA-seq | 6 | 大鼠 | GPL25947 | ✅ FPKM(带 gene_name) | CCI vs Sham（3v3），L4-6 DRG，Day11。样本极少→功效受限，作方向性外部验证。 |
| GSE265957 | **DRG+脊髓翻译组** | Ribo-seq+mRNA | **96** | 小鼠 | GPL21103(DRG)/GPL24247(SC) | ✅ xlsx(Xtail log2FC/p + TRAP TPM) | SNI/CFA 模型；含 **Xtail 翻译效率**表（mRNA_log2FC / log2FC_TE / pvalue_final）。非"纯脊髓"。 |
| GSE278227 | 性别×时间分层 | RNA-seq | **62** | 大鼠 | GPL20084/32190 | ✅ rawcount(protein_coding) | **同体对侧设计**：CCI × M/F × 24h/1W/5W × 同侧(IL)/对侧(CL)。高功效 DRG 神经损伤集。 |
| GSE241361 | 机制锚点 | RNA-seq | 36 | 小鼠 | GPL19057 | ✅ raw+TMM | **Sigma-1 受体 KO × SNI**，DRG+脊髓(Medula)，Naive/SNI × WT/KO。S1R 机制锚点。 |
| GSE158825 | 人源验证 | **miRNA-seq** | 60 | 人 | GPL21697 | ✅ mature miRNA counts | 血浆 miRNA；LSS 术后疼痛变化（%nprs20delta）。**必须 miRNA→mRNA 映射**才能接 hub。 |
| GSE222979 | 人源内型 | **miRNA-seq** | **1242** | 人 | GPL21697 | ✅ miRNA counts(3体液) | ⚠️ **原方案误判为 mRNA**：实为 miRNA；LEAP 队列膝关节置换 3 体液。改作 miRNA 内型关联。 |
| GSE306403 | ⚠️ 体外支持(**非人组织**) | RNA-seq | 18 | 人 | GPL24676 | ✅ RNAseq counts | ⚠️ **原方案误判为人源组织**：实为 **SH-SY5Y 神经母细胞瘤细胞系**，Morphine(193nM) vs Control。只能作阿片/神经细胞体外参考，**不可当患者验证**。 |
| GSE328175 | 单细胞(核) | **snRNA-seq** | 8 | 小鼠(6)+**人(2)** | GPL24247 | RAW.tar ✅已解包 | 小鼠腰椎脊髓 **Sham(3)/SNI(3)** + **SNI+Transplant(2)**。⚠️ **Transplant 两库用 hg19 注释**（人源移植细胞），**必须从小鼠臂剔除**；同研究配套空间转录组(GSE325938)。SNI=entrenched 神经病理痛，Transplant=**有效镇痛治疗组**。✅ 实跑：小鼠臂 QC 后 **54,312 核 × 25,506 基因**（Neuron 46,349 · Oligo 5,749 · Microglia 1,017 · Astrocyte 527 · OPC 415 · Fibro_Meninges 125 · Ependymal 87 · Endothelial 43）。 |
| GSE325938 | 空间 | 空间(Visium) | 8 | 小鼠(6)+**人(2)** | 待核 | suppl 待列 | ✅ **已核实为 GSE328175 的配套 Visium 数据**（同标题 "Spinal signatures of entrenched and treated neuropathic pain"、同 8 样本结构、物种含人+鼠）→ P5-Stretch：hub 在脊髓背角空间定位。 |
| GSE246288 | 单细胞 | scRNA-seq | 4 | 小鼠 | GPL28330 | RAW.tar ✅已解包 | **脊髓背角(L4-6) Cd11b+ 分选**小胶质/巨噬；**SA=PID0(sham)、3A/7A/14A=SNI PID3/7/14，每时间点仅 1 只** → 只能描述性、**不可做任何检验**。⚠️ ① 该集用**全量 10x 条形码白名单**（6,794,880 barcode/样本，名义 2,718 万"细胞"，QC 后 14,582）——载入必须剔除全零列；② 其非小胶质簇（Neuron 4,103 / Oligo 1,045 等）为 **ambient RNA 伪簇**（HVG 头部 S100A8/S100A9/RETNLG/MKI67，纯髓系+增殖），跨细胞类型定位不可用。**DAM/补体线锚点（但仅限小胶质内部表达/时程）**。 |
| GSE216039 | 单细胞 | scRNA-seq | 4 | 小鼠 | GPL24247 | RAW.tar ✅已解包 | ⚠️ **原方案误判为"紫杉醇"**：实为 **CCI 坐骨神经结扎 Day7**，双侧 L4-5 DRG，M/F 各半。**且 characteristics 明写 `cell type: neuron`**（Pirt-EGFP 神经元富集）→ **只能做神经元亚型定位，不可用于胶质/免疫定位**。 |

**核查结论**：12 个数据集全部真实存在、处理矩阵可获取（bulk 集齐全，scRNA 集走 RAW.tar）。原方案数据清单**成立**，但有五处必须修正：
1. **GSE222979 是 miRNA 不是 mRNA** → 人源 mRNA 直接验证链**实际为空**；须靠临床 qPCR 验证 + miRNA→mRNA 间接链（§4 风险）。
2. **GSE306403 是人 SH-SY5Y 细胞系（morphine vs control），不是人 DRG/患者组织** → 从"人源验证"降级为"体外/阿片机制参考"，**不得**充当人源 CPSP 证据。
3. **GSE267799 含 LPI+SMIR 双模型**，比原方案设想更丰富，整合时须按"模型×组织×状态"三维分层，避免混淆。
4. **GSE216039 是 CCI（非紫杉醇）+ 神经元富集**（series_matrix `cell type: neuron`）→ 定位层角色从"DRG 全细胞"收窄为"**DRG 神经元亚型**"；胶质/免疫定位改由 GSE328175 + GSE246288 承担。
5. **GSE328175 混种**：`Transplant1/2` 的 features 为 `hg19_ENSG...`（人源），`Sham/SNI` 为 `ENSMUSG...`（小鼠）→ 两库不可合并；本项目只取**小鼠六样本臂（Sham3 vs SNI3）**做脊髓定位与样本级统计，人源两样本单列（可选：作为人源移植细胞臂的旁证）。

**P5 定位层最终设计（据核实结果定型）**：

| 数据集 | 臂 | 覆盖细胞类型 | 样本级统计能力 |
|---|---|---|---|
| GSE328175 小鼠臂 | Sham3 vs SNI3（腰椎脊髓 snRNA） | 神经元/星形胶质/小胶质/少突/OPC/内皮/周细胞/室管膜 | **n=3 vs 3 → 可做样本级 Welch + BH（本层唯一有功效的对比）** |
| GSE246288 | PID0 vs PID3/7/14（SCDH Cd11b+） | 小胶质/巨噬（DAM/补体线） | n=1/时间点 → 仅描述性 |
| GSE216039 | Sham(M/F) vs CCI-7d(M/F) | 神经元亚型 | n=2 vs 2 → 仅描述性 |
| GSE328175 人源臂 | SNI+Transplant(2) | 人源移植细胞 | 仅描述性（可选） |

### 3.1 分组解码结果（2026-09-16 实检，逐集核对 series_matrix + 矩阵列名）

| GSE | 真实分组（已核清） | n/组 | 可用对比 |
|---|---|---|---|
| GSE267799 | LPI/SMIR × DRG/肌肉/皮肤 × 0d/6h/2d/10d/32d | 4–8 | DRG 轴 acute(6h+2d) / chronic(10d+32d) vs baseline(0d) |
| GSE212311 | CCI vs Sham（L4-6 DRG, Day11） | 3 vs 3 | CCI vs Sham |
| GSE278227 | CCI × M/F × 24h/1W/5W × IL/CL（protein_coding） | 5–7 | IL vs CL（同体对侧），按时间/性别分层 |
| GSE241361 | Naive/SNI × WT/KO × DRG/Medula | 3–5 | SNI vs Naive（WT DRG/SC）；KO vs WT（SNI DRG） |
| GSE265957 | DRG/SC × SNI vs SHM(D4/D63) × CFA vs VEH(D3)；TRAP: TAC1/GAD2 × IN/IP | 2–3 | 已提供 log2FC+ p（Xtail），直接用 |
| GSE158825 | 血浆 miRNA，LSS vs LSS+DS | 60 | 术后疼痛变化关联（P4） |
| GSE222979 | 血浆/滑液/尿 miRNA，膝关节置换（LEAP） | 1242 | miRNA 内型（P4） |
| GSE306403 | SH-SY5Y：Morphine(193nM) vs Control | 15 vs 3 | 仅体外参考 |
| GSE216039 | 小鼠双侧 L4-5 DRG，**neuron-enriched (Pirt-EGFP)**；Sham/CCI-7d × M/F | 2 vs 2 | CCI-7d vs Sham（描述性） |
| GSE328175(小鼠臂) | 腰椎脊髓 snRNA：Sham1-3 vs SNI1-3 | 3 vs 3 | **SNI vs Sham（样本级可推断）** |
| GSE328175(人源臂) | SNI+Transplant1-2（hg19 人源移植细胞） | 2 | 仅描述性 |
| GSE246288 | 脊髓背角 Cd11b+：PID 0 / 3 / 7 / 14 | 1/时间点 | 时间序列描述性 |

---

## 4. 统计纪律铁律（审稿人必问，已内化为流程红线）

1. **伪重复（pseudoreplication）**：细胞/空间点**不是独立重复单元**。单细胞与空间层一律**逐样本(动物) pseudobulk** 后做 Welch/Mann-Whitney + BH；细胞级打分只作描述，绝不用于推断。bulk 层样本=动物/患者，天然合规，但 GSE267799 须按"模型×组织×状态"正确分层，不可把组织当重复。
2. **double-dipping / 选择偏倚**：候选基因由同一批 DEG 选出再在同批上训练/评估 → 同集 AUC 必然虚高。**必须**：跨数据集 train→test（A 训 B 测）、LASSO bootstrap 稳定性（B=200，选入频率≥0.6 才算稳健核心）、RepeatedStratifiedKFold(5×20) 报 mean±sd。结论落"机制方向"而非"精确基因列表"。
3. **功效校准**：BH 全不显著时，默认它是**功效问题**（absence of evidence ≠ evidence of absence）；算 MDE 与"所需 n"，把观测效应量除以 MDE。小样本（如 3v3 scRNA）下组成/状态常均测不出，如实写"该设计两层均达不到可检边界"。
4. **复刻集真伪**：外部验证集入组前做指纹比对（GSM 归属、样本数、barcode/样本集合是否同一批二次提交），避免把同一数据当"独立复制"得出错误新颖性判断。
5. **跨物种**：动物结论为 hypothesis-generating；人源层须有独立证据；严禁把动物因果写成人因果。
6. **基因集统计（最易忽略也最出彩）**：逐集合对成员 meta_Z 做单样本 t / Wilcoxon / Stouffer；常见"集合整体 p 极小、单体 0 显著"——这正是"必须用基因集/ML"的论据。
7. **诚实评估四件套必做**：bootstrap 稳定性、重复 CV、跨数据集泛化、Limitation 章节明示选择偏倚与小样本不可复现风险。

---

## 5. 技术路线（改版）

```
[动物 bulk 层]
  GSE267799(DRG/肌肉/皮肤 × SMIR/LPI) + GSE212311(CCI-DRG) + GSE278227(DRG性别)
        ↓ 统一为 基因符号×样本 矩阵（symbol 优先；同符号取均值）
        ↓ 分数据集 DEG（Welch t + BH），核清真实分组
        ↓ Stouffer 加权 Z 元分析（w=√n_post）+ 方向一致性（要求 ≥2 集）
        ↓ ComBat 合并矩阵（设计矩阵含 group 协变量，仅作敏感性交叉验证）
[脊髓 bulk 层]
  GSE265957(脊髓翻译组 96) 单独做 DEG + 元分析，与 DRG 层取"共变枢纽交集"
        ↓
  基因集统计（GeneCards neuropathic/chronic postsurgical pain + DisGeNET C0030075
            + 离子通道家族 TRP/ASIC/KCNK/SCN/P2RX/CACNA + 神经炎症/MAPK）
        ↓ 候选池 = (基因级: 通路∩meta_p<0.05 且方向一致) ∪ (集合级: 集合显著取 |meta_Z| Top10)
[双 ML 锁靶]
  LASSO(λ.1se) + Boruta/RF(MDGini) + XGBoost gain/SHAP → 交集=hub
        ↓ 诚实评估（bootstrap/cross-dataset/重复CV）
[人源验证层]
  GSE158825(血浆 miRNA→TargetScan/miRTarBase→hub mRNA 间接链 + ROC)
  GSE306403(18例 mRNA 机制支持)  ［GSE222979 改作 miRNA 内型关联或弃用 mRNA 验证］
[单细胞/空间定位层]  (样本级统计)
  GSE328175 + GSE216039(DRG神经元) + GSE246288(小胶质) → Harmony→pseudobulk→定位
  GSE325938(Visium) → 脊髓背角空间定位 ［Stretch］
[老药新用虚拟筛选]  ← 见 §6 靶蛋白定义
  DrugBank approved + ZINC FDA-approved(~2000-3000) → Vina 对接 → ADMET(BBB/鞘内)
        → 四维评分排序 → Top 5-10 + 反向阳性对照 → 100ns MD ［Stretch］
[整合叙事 + 写作 + 复现包]
```

---

## 6. 虚拟筛选靶蛋白定义（⚠️ 原方案最致命缺口——已补）

原方案只写"分子对接"却**从未指定对接哪个蛋白**。对接必须有三维结构靶标。锁定规则：

1. **靶标来源**：Phase 3 的 hub 基因产物中，筛选满足以下全部条件的可成药蛋白：
   - 有实验解析 PDB 结构 **或** AlphaFold2 高置信度预测（pLDDT > 70）；
   - 具明确可成药口袋（非完全无序区）；
   - 与疼痛机制相关（离子通道 / GPCR / 激酶 / 趋化因子受体）；
   - 人源直系同源（用于人源验证与临床对接）。
2. **优先靶标类型**：配体门控离子通道（P2RX、SCN、CACNA2D、KCNK、TRP、ASIC）、Sigma-1（有 GSE241361 锚点且结构已知）、镇痛相关 GPCR。
3. **对接流程**：AutoDock Vina（必要时 Smina/AutoDockFR 诱导契合）→ 结合能 + 氢键/疏水接触 → ADMET（BBB 穿透、鞘内给药可行性）。
4. **四维评分排序**：结合亲和力 + 已有多靶点药理学合理性 + 临床可及性(BBB/鞘内报道) + 反向对照召回率。
5. **反向阳性对照（方法学校验必做）**：加入已知镇痛药及其靶点（如加巴喷丁→CACNA2D、米诺环素→小胶质、P2X4 拮抗剂、Sigma-1 配体），验证流程能召回已知镇痛关联；若召回失败则修正对接参数。
6. **兜底**：若对接得分普遍偏低 → 转 **CMap 签名重定位**（基于基因签名而非结构）作正交验证。

---

## 7. 分阶段路线图（持续进行 · 每阶段有出口标准）

| Phase | 目标 | 输入 | 输出 | 出口标准(DoD) | 状态 |
|---|---|---|---|---|---|
| **P0 立项与数据资产核验** | 方案定型、数据集真实验证 | 原方案二 | 本文档 + 核查表 + 骨架 | 12 集已核验、范围/MVP 已定、路线图就绪 | ✅ 本回合完成 |
| **P1 数据获取与 QC** | 下载矩阵、统一、核分组 | suppl 文件 | `data/processed/*_symbol_matrix.csv` + 样本表 | 每集统一为 symbol×样本；真实分组(模型×组织×状态)已核清；QC 报告 | ✅ 完成（7 套 suppl 矩阵全部下载；5 个 bulk 集统一为 symbol×样本：212311(27558×6)、278227(20582×62)、241361(25658×36)、306403(29655×18)、267799(25051×36)；分组逐集解码见 §3.1） |
| **P2 分数据集 DEG + 元分析** | per-dataset DEG + Stouffer Z + ComBat | P1 矩阵 | `results/tables/DEG_*.csv`、`META_DRG_axis_*.csv` | n_datasets≥2 的 meta 完成；方向一致性计算；ComBat 敏感性矩阵 | ✅ 完成核心（14 个 DEG 对比；6 数据集 DRG 轴 Stouffer 元分析；核心签名 4055 基因；切口模型方向一致性 59.9% p=2.8e-48；图 `P2_core_signature_heatmap.png`） |
| **P3 基因集统计 + 双 ML 锁靶** | 候选池 + hub | P2 | `results/tables/P3_*.csv`、`P3_hub_genes.csv`、`P3_lodo_auc_ci.csv` | 基因集统计完成；LASSO+RF+XGBoost 交集；bootstrap/LODO 评估；Limitation 草稿 | ✅ 完成（19 基因集置换检验；**神经炎症/DAM/补体↑ + 线粒体 OXPHOS↓**，p≤0.004；**Hub 35 基因**，32/35 落在元分析核心；**LODO 泛化 AUC 0.917–1.0**（切口模型 0.917[0.729,1.0]）；置换零假设 0.49；图 `P3_hub_lodo_auc.png`） |
| **P4 人源验证层** | 人源方向一致性 | GSE158825/306403 | `results/tables/P4_*.csv`、`P4_human_miRNA_layer.png` | 间接验证链建成；若 GSE222979 走内型则附 miRNA 关联 | ✅ 完成（**人源层实为阴性**：GSE158825 无 FDR 显著；253/608 hub 靶向 miRNA 在血浆可检出但集合水平置换 p=0.51；GSE222979 无疼痛表型。**人源确证须靠前瞻性临床验证**） |
| **P5 单细胞/空间定位** | hub 细胞/空间定位 | GSE328175/216039/246288(+325938) | 定位图、样本级统计 | 仅样本级统计；ambient RNA 排除；无 BH 显著则定位为"方向提示" | ✅ 完成核心（三集跑通；**DRG 侧 20/25 可检出 hub 落在损伤/再生神经元亚型**，SPRR1A 17.4×；脊髓侧 16 可定位分属 Neuron/Microglia/OPC/Astrocyte；**跨集一致定位仅 7/35**，TFE3 为唯一 Immune 一致项；pseudobulk 两集均 0 显著 → 全层标注"方向提示"；图 `P5_hub_lineage_consensus.png` 等 4 张）。**Stretch 待做**：GSE325938 Visium 空间定位 |
| **P6 老药新用虚拟筛选** | 靶蛋白对接 + 排序 + 全库广度 | P3 hub + §6 规则 | `P6_docking_scores_*.csv`、Top 候选、广度表 | 靶蛋白已定义；**全库 3,085 药 × 10 靶标 = 30,850 对接**完成；四维排序；反向对照（164 ChEMBL 实测阳性）通过；**预注册全库广度分析完成并产出诚实结论** | ✅ 全库完成（2026-09-19 `P6_FINALIZE_STATUS.json`=ready_to_finalise；审计 20/20 靶标×层一致；所有控制+广度 rc=0）。**关键诚实结论：预注册全库检验发现 ADRA2A 的 Tier-1 富集（AUC 0.618）不延续到全库（AUC 0.532, p=0.118 NS）——Tier-1 阳性是 CNS 先验子集的组成伪信号；5 个可检靶标中无一显示稳健且增量可辨的对接富集，AXL/TNIK 名义 PASS 但 ΔAUC 95%CI 含 0） |
| **P7 整合叙事 + 写作 + 复现包** | 成稿 + 可获取 | P1–P6 | 稿件 + 图 + GitHub/Zenodo 复现包 | 复现包真实可获取（实名 URL）；投稿信；目标期刊对齐 | ⬜ 待办 |

---

## 8. 风险登记册

| 风险 | 等级 | 应对（已写入流程） |
|---|---|---|
| 人源 mRNA 直接验证缺失（GSE222979 实为 miRNA） | 中 | 靠 GSE306403(18例) + 临床 qPCR 验证；miRNA→mRNA 间接链 |
| 跨物种外推被质疑 | 高 | 动物=hypothesis-generating；人源独立证据；不写人因果 |
| 小样本功效不足（double-dipping 虚高） | 高 | §4 铁律 2/3；跨数据集验证；结论落机制方向 |
| 复刻集实为同一批数据 | 中 | 入组前指纹比对（§4.4） |
| 对接得分普遍偏低 | 中 | 诱导契合 / 转 CMap 签名重定位（§6.6） |
| 临床验证(湿实验)不可行 | 中 | 降级为 MVP（纯生信仍可发表）；Stretch 择机补 |
| 单细胞伪重复 | 高 | 仅样本级统计；ambient RNA 排除（§4.1） |

---

## 9. 目标期刊与投稿策略

- **冲刺**：*Pain*(IF~6)、*BJA*/*Anaesthesia*(难，需 Stretch 临床数据)
- **稳妥(MVP 对齐)**：*J Transl Med*(6.1)、*Front Pharmacol*(5.4)、*Front Immunol*(5.9)、*CNS Neurosci Ther*(5.0)
- **保底**：*Scientific Reports*、*BMC Anesthesiology*
- **投稿前必做**：元分析型新颖性自检——用 `esummary` 拉各 GSE 的 `pubmedids`，核对核心集原文是否已占结论，避免新颖性被抢占。

---

## 10. 复现包与可获取性（用户惯例）

- 仓库名（kebab-case）：**`cpsp-drg-spinal-repurposing`**
- 标准内容：README(英文文件地图+复现命令+软件版本)、CITATION.cff、MIT LICENSE、.github/workflows/release.yml、GITHUB_DEPOSIT_SOP.md(中文)、author_verification_statement.md
- 数据可用性措辞：**实名仓库 URL** + "mirrored to Zenodo with citable DOI on acceptance"，**禁止** "available on request"
- 平铺纪律：仓库根=工作目录；中央脚本与产物必须入库；稿件侧文件排除。

---

## 11. 本次执行记录（changelog）

- **2026-09-16**：
  - 加载 `geo-bulk-multidataset-ml` + `geo-eutils-metadata` 技能，内化统计纪律（伪重复/功效/double-dipping/复刻集真伪）。
  - 用 E-utilities 实检 12 个 GSE：**全部真实存在、处理矩阵可获取**。
  - 修正两处方案错误：① GSE222979 实为 **miRNA**（非 mRNA）；② GSE267799 含 **SMIR+LPI 双模型**（比原设想更丰富）。
  - 补上原方案最致命缺口：**虚拟筛选靶蛋白定义规则**（§6）。
  - 建立项目骨架（data/scripts/figures/reports）+ 本文档 + 核查脚本 `scripts/geo_verify.py`。
  - 进入 **P1 数据获取与 QC** 并已实做：下载 GSE267799 全部 6 个处理矩阵；解码真实设计（108 例 = SMIR/LPI × DRG/肌肉/皮肤 × 0d/6h/2d/10d/32d × 4 重复）；用 NCBI `gene_info` dbXrefs 建 Ensembl→symbol 映射（覆盖 25096 大鼠基因，应用后 ~68% 获 symbol）；产出 `data/processed/GSE267799_{DRG,MUS,SKI}_symbol_count.csv` + 样本表。
  - **P1 完成**：单次读取 `gene_info.gz` 建 rat/mouse/human 三物种 Ensembl→symbol 映射（`common_map.py`；9606=38267、10116=25096）；下载 7 套 suppl 矩阵（GSE212311/265957/278227/241361/306403/158825/222979）+ 全部 series_matrix；`p2_decode_samples.py` 逐集解码真实分组（§3.1）；`p2_build_matrices.py` 统一 5 个 bulk 集为 symbol×样本（含 GSE212311 改用自带 `gene_name`、GSE278227 protein_coding 过滤、GSE241361 强制数值转换）。
  - **P2 完成核心**：`p2_deg_meta.py` 跑 14 个 DEG 对比（Welch t + BH）。发现并确证 **① GSE267799(LPI 切口)与 GSE212311(CCI 3v3) per-gene 无 FDR 显著**——非 bug，而是切口模型单基因效应弱/小样本功效不足（真实生物学+统计结论，写入论文方法学叙事）；**② 神经损伤模型(GSE278227 CCI 1W n=14/组)信号强（9103 DEG）**。6 数据集 DRG 轴 Stouffer 加权 Z（w=√(n1n2/(n1+n2))）→ 核心签名 4055 基因，Top: **ATF3/GAL/ECEL1/NPY/FLRT3/VGF/CCKBR/SOCS3/SOX11/ADCYAP1/STAC2**（全为 DRG 损伤经典基因，金标准 ATF3 排第 1）。**转化一致性**：神经损伤签名在切口模型同向率 59.9%（binomial p=2.8e-48），诚实结论"方向一致、幅度更弱"。产出 `results/tables/*.csv` + `results/figures/P2_core_signature_heatmap.png`。
  - **新增两处方案修正**（§3）：③ **GSE306403 实为人 SH-SY5Y 细胞系（morphine vs control），非人组织/患者** → 降级为体外参考，人源直接验证链实为空，须靠临床验证 + miRNA 间接链。
  - **P3 完成**：`p3_genesets.py` 对 19 个基因集做 Stouffer + 单样本 t + **2000 次同尺寸置换校准** → **神经炎症(mean_Z=+4.94)/DAM 小胶质(+3.88)/补体(+3.44) 协同上调**、**线粒体 OXPHOS(−2.37) 协同下调**（置换 p≤0.004）；**离子通道家族整体不协同**（TRP/Nav/CACNA/K 置换 p>0.17，重要阴性发现）。
  - **P3 双 ML 锁靶完成**：`p3_ml.py` 改用**留一数据集（LODO）设计**（5 个 DRG 轴数据集、逐集基因内 z-score、共同基因 13208、合并 72 样本）→ 单变量预筛 Top800 → **LASSO(λ.min)+RF(MDGini)+XGBoost(|SHAP|) 三法** → **Hub = 35 基因（≥2/3），其中 32/35（91%）落在元分析核心签名内**（ATF3/SPRR1A/TFE3/CDHR5/GALNS/NPY/MAPK14/AXL/VIP/SERPINE1…）。`p3_finalize.py` 出 **LODO 泛化 AUC：切口模型 0.917[0.729,1.0]、其余 0.95–1.0**；pooled 5×20 CV=0.999±0.004，**标签置换零假设 0.49±0.09**。诚实记录：**λ.1se 仅 1 基因**（稀疏线性信号弱）、GSE241361 DRG/SC 同批动物（LODO 非完全独立）、人源直接验证仍缺。
  - **P4 完成（人源层，结论为阴性/薄）**：`p4_mirna.py` 分析 GSE158825（人血浆 miRNA，60 例腰椎手术 + `%nprs20delta` 疼痛结局）→ **LSS+DS vs LSS 与疼痛关联均无 FDR<0.05**（最小 p 1.3e-4 / 8.5e-4）；名义命中为免疫 miRNA 簇（**miR-99b/let-7e/miR-125a** 多顺反子簇 + **miR-146a/miR-155**）。`p4_targets.py` 用 NCBI `gene2refseq`+`gene_info`（人 RefSeq→symbol 279308）把 **miRDB v6.0** 靶点转符号 → **33/35 hub 有靶向 miRNA，高置信 608 个**。`p4_integrate.py` → **253 个在血浆可检出**、GSE222979 三体液 308–328 个可检出；**集合水平置换 p=0.51（不稳健）**，故诚报阴性。GSE222979 解码为 414 血浆+414 滑液+414 尿、**无疼痛表型**（原"1242 内型分析"不可行）。
  - **结论**：人源直接验证链**依然缺失**（GSE306403 非人组织、GSE222979 无表型、GSE158825 无显著）→ **必须写入 Limitations，人源确证靠前瞻性临床 qPCR/ELISA（Stretch）**。
  - **P5 完成（单细胞层 hub 定位）**：`p5_sc.py` 通用管线（`<GSE> <DRG|SC> [样本过滤]`；纯 numpy/scipy/sklearn + KMeans/numba-free，含缓存检查点）跑通三个数据集。
    - **GSE216039（DRG，22,063 细胞 × 22,086 基因）**：`p5_subtype.py` 用**非 hub marker**（GAL/GAP43/SOX11/VGF/MMP16/CDK5R1/SCG2/NCAM1，与 hub 零重叠、逐条留痕）定义 4 个神经元亚型 → **25 个可检出 hub 中 20 个（80%）落在 CCI 诱导的损伤/再生神经元亚型**；SPRR1A 亚型内检出率 **98.1%** vs 其它亚型 17.8%（17.4×）、ATF3 99.4% vs 52.3%、ECEL1 25.7×、NPY 10.0×、FLNC 10.2×；tier = **restricted 19 / enriched 6 / broad 0**。亚型划定对留一 marker 稳健（一致率 92–100%，ρ 0.965–0.996）。
    - **GSE328175（小鼠腰段脊髓 snRNA，54,312 核 × 25,506 基因）**：33/35 hub 存在、24 可检出、**16 可定位** → Neuron 6 / **Microglia 5** / OPC 3 / Astrocyte 2（TFE3→Microglia 2.45、MEGF11→OPC 4.67、CHL1→Astrocyte 2.61、SRRM4/VASH2/GALNS→Neuron）。**ATF3（ambient_index 2.59）/AXL（3.11）/TNS3（1.77）因环境 RNA 主导被降级**；SLC2A1/AGRN→Endothelial（43 核）、FLNC/CCDC160→Ependymal（87 核）标为 rare_compartment（方向可信、功效不足）。
    - **GSE246288（脊髓背角 Cd11b+，14,582 真实细胞）**：发现该集用**全量 10x 条形码白名单**（6,794,880 barcode/样本 → 名义 2,718 万"细胞"），已在载入时剔除全零列；**其非小胶质簇（Neuron 4,103 等）确认为 ambient RNA 伪簇**（HVG 头部 S100A8/S100A9/RETNLG/MKI67，纯髓系+增殖）→ 跨细胞类型定位全部作废，仅保留小胶质时程：14/27 hub 可检出、**无时间趋势**（13 flat / 1 down）；TFE3 全程高表达（0.69–0.81）与 Immune 一致定位互证，AXL 在 PID3 达峰（0.043→0.141）。
    - **跨数据集谱系共识（仅用横跨多谱系的 DRG + 脊髓两集）**：**7/35 在两集一致定位** —— Neuronal 5（ANKRD13B/CTTN/PTPN23/SRRM4/VASH2）、**Immune 1（TFE3）**、Glial 1（CHL1）；Mixed 5；单集可定位 8；NotLocalisable 15。结论定性为"hub 是**跨 DRG-脊髓轴的多细胞程序**，非单一细胞类型签名"。
    - **判读方法学**：新增 `p5_summarize.py` 修补五个陷阱（除零假象、**文库复杂度混杂**——log-norm 均值随检出基因数系统性升高、小簇伪影 vs 稀有区室、ambient RNA、血液污染簇），判读分层（restricted/enriched/broad/undetected/rare_compartment/ambient_caution）**先验设定**，被降级明细单列 `P5_hub_localisation_dropped.csv`（49 行）可审计。
    - **样本级统计诚报阴性**：GSE216039（2v2）与 GSE328175（2–3v2–3）pseudobulk Welch+BH 均 **0/33–34 显著** → 依 §4 铁律，本层定位**一律标注为"方向提示"**。
    - 产物：`results/P5_RESULTS.md`、`results/tables/P5_*.csv`（15 张）、`results/figures/P5_*.png`（4 张）。
  - **P5 附带数据事实修正（§3）**：④ **GSE325938 = GSE328175 的 Visium 空间配套数据**（同标题、8 样本、物种含人+鼠）已确认，留作 P5-Stretch；⑤ **GSE246288 每时间点仅 1 只** → 只能描述性，不可做任何检验。
  - **待续（P6）**：虚拟筛选（§6 规则，优先神经免疫/代谢 + Sigma-1/MAPK14/AXL/ACVR1）；P5-Stretch：GSE325938 Visium 空间定位、GSE328175 人源移植臂旁证。
- **2026-09-18**：
  - **P6 Tier 1 完整交付（真实结果）**：620 已批准药(CNS/镇痛先验层) × 10 靶标 = 6201 行真实打分（`P6_docking_scores_t1_cns.csv`，09-17 07:49 rc=0）。`p6_score.py --tags t1_cns` → 四维排序 + 反向对照（`P6_ranking_drugs.csv`/`P6_ranking_pairs.csv`/`P6_reverse_control.csv`，RC=0）；`p6_figures.py` 出 6 张真实图（覆盖 `_SYNTHETIC_*` 占位）；`p6_report.py` 生成 `P6_RESULTS.md`（诚实标 2 项缺失：T2 合表、ChEMBL 阳性集）。**核心发现：ADRA2A(α2A-肾上腺素受体)为领先重定位靶标**，Top 候选麦角胺/利培酮/双氢麦角胺/鲁拉西酮/齐拉西酮/溴隐亭（composite 0.78–0.78）；已知镇痛药(麦角胺类、FLUPIRTINE 多靶)在 Top 复现=面容效度；ADRA2A 是唯一富集靶标(AUC=0.551)。机制连贯：α2A 介导下行去甲肾上腺素能痛抑制。
  - **方法学三护栏（可发表核心，不依赖 Tier 2）**：① 参数保真度前置验证(max_evals 引入系统偏倚 ρ≈−0.23~+0.11；exh1 仅标度平移 ρ≈0.78 → 选 exh1，措辞定 candidate prioritisation)；② 合成数据自检在真实长跑前挖出 3 个致命评分 bug；③ 反向阳性对照无 double-dipping(标签独立、预测来自对接)+药物级聚合避伪重复。
  - **Tier 2 阻塞根因(已定位，非代码 bug)**：后台任务被环境按 ~12h 生命周期整条连子进程清掉，单条链活不过 T2 全矩阵(~40–64h 真算)。对策：`p6_chain.py` Step1/Step2 加自愈循环(等合表真实存在，上限 10 次)+ chunk 缓存续跑；被杀后由 agent 重拉续跑。现 3/10→4/10 靶标(GALNS/SLC2A1/TNIK 83/83，ITPKC 续跑)，链 **btuVos** 后台活跃，7 vina 在跑。ChEMBL 实测阳性集仍被 EBI 5xx 阻断 → 反向对照改用本地已知镇痛药标注。
  - **产出稿件框架草稿** `reports/P6_manuscript_draft.md`（IMRaD，Tier 1 真实结果+方法，T2 段标 `[PENDING Tier 2]`；期刊对齐 A 档 Frontiers in Pharmacol/Sci Reports，C 档 Pain/BJA 需 ≥1 候选湿验证）。P6 行状态改为🟡进行中。
  - **待续**：T2 跑完→合并重评(`--tags t1_cns,t2_other`)→补 §3.5 广度→P7 复现包(GitHub+Zenodo 实名 URL)+定稿。
- **2026-09-19**：
  - **ChEMBL 独立阳性集落地**（EBI 恢复，ChEMBL_37）：`p6_reverse_control.py` → 164 条实测 drug–target 阳性（ADRA2A 115，最高 pChEMBL 9.54）。反向对照升级为**纯结合型标签**（原三层含 PAIN_PRIOR/DRH 属适应症型，会把 AUC 从 0.618 稀释到 0.592）→ ADRA2A n=88, **AUC 0.618**, `reliable` 由 False 转 **True**；Top-6 全部落 ADRA2A。
  - **MW 混淆检验**（`p6_mw_confounder.py`）：ρ(亲和力,MW)=−0.607；仅 MW 预测 AUC 0.581 vs 对接 0.618；**线性校正后 0.597、分层内 0.600** → 富集**不是尺寸伪信号**。
  - **面容效度证伪并如实改写**（`p6_face_validity.py`）：镇痛药类别不富集（AUC 0.553, p=0.081；Top-20 中 0/64）；α2 激动剂原始 AUC 0.343（MW 校正后 0.475 等同随机）。稿件新增 §3.4.1 阴性结果节，**方法效度只由 ChEMBL 结合型富集支撑**。
  - **头号排序的 MW 敏感性 + precision@k**（新增 `p6_mw_ranking_sensitivity.py`，报告 §7.3、稿件 §3.4.2）：composite Spearman 主口径 vs MW残差 **0.833**（分层 0.802）、Top-20 重叠 14/20、判定 PASS；**precision@10 = 0.800**（8/10，lift ×5.64，超几何 p=4.4e-6）、@20 = 0.700（p=9.8e-9），经 MW 校正仍 0.55–0.80。**但 Top-10 身份仅 4/10 稳定** → 只主张 **Top-20 候选集合**，不作单药首位结论。
  - **计算量归因**（新增 `p6_throughput.py` + `results/P6_throughput_note.md`）：更正先前两次错误估计（把"每块到达间隔"当"每块成本"→ ETA 高估 5 倍；用 `elapsed_total` 比较靶标→ 被续跑污染伪造出"差 4 倍"）。同受体配对阵：**T2 每单位配体成本 = T1 的 ×3.00**，由配体柔性差异解释（可扭转键 ×1.20、MW ×1.19、TPSA ×1.61、HBD ×2.00）；盒体积**不显著**（ρ=0.10, p=0.80）。
  - **Tier 2 全库合表 + 收尾编排器落地**（`p6_finalize_watch.py`，fail-fast）：等对接静默 → 审计(集合相等) → 重评(合并表**自愈重建**自逐靶标源真值) → 重算所有依赖控制(mw_confounder/face_validity/mw_ranking) → 预注册广度 → 复核 → 写 `P6_FINALIZE_STATUS.json`。全库 30,850 对；163 对(34 药)未打分（60 含硼药 Vina 不识 `B` 原子 + 103 超时大环/高柔性），已剔除并附上界证明 `P6_exclusion_bound.csv`。
  - **三处缺陷拦截（均已在跑批中修复，rc=0 收尾）**：
    1. **合并表覆盖写缺陷**：`p6_dock.py --only AXL --tag t1_cns` 用 per-invocation 的 `rows_all` 写 `P6_docking_scores_t1_cns.csv`，会把 6,200 行覆盖成 620 行 AXL-only，抹掉其余 9 靶标 t1 数据，而 `p6_score.py` 读该合并表会**静默**在残缺表上重排出图无任何报错。→ `p6_score.py` 增加 `_rebuild_tag_table()` 在读取前由逐靶标 `docking/out/<SYM>/scores_<tag>.csv` 自愈重建；`p6_dock.py` 改 merge-append。
    2. **广度脚本名遮蔽崩溃**：`p6_breadth.py` 第 259 行 `S = pd.DataFrame(stab)` 把 `import p6_stats as S` 模块别名遮蔽为 DataFrame，导致后续 `S.mw_adjust_auc/...` 抛 `AttributeError: 'DataFrame' object has no attribute 'mw_adjust_auc'`，finisher 步骤4 崩溃 → 步骤5 复核仍跑完并写 needs_review。→ 局部变量改名 `RS`，`S` 仅保留为 p6_stats 模块别名（已 `py_compile` + 重跑 rc=0）。
    3. **富集裁决统一**：`p6_mw_confounder.py` 与 `p6_breadth.py` 共用 `p6_stats.enrichment_verdict`（唯一口径），2D 理化基线 + ΔAUC 配对 bootstrap 95%CI 仅作诚实 caveat，绝不翻案。
  - **全库广度诚实结论（稿件 §3.5 已誊入）**：5 个靶标达 ≥5 独立 ChEMBL 阳性——ACVR1(FAIL_size_only_matches, 0.817≥0.797)、ADRA2A(NS, 0.532, p=0.118)、AXL(PASS_size_independent, 0.880, p=1.1e-6, 校正 0.752)、MAPK14(FAIL, 0.787≥0.779)、TNIK(PASS, 0.824, p=2.0e-4, 校正 0.803)。**AXL/TNIK 名义 PASS 但 ΔAUC(vs 尺寸基线)与(vs 2D 理化基线)的 95%CI 均含 0 → 对接相对平凡基线无增量可辨**。排序稳定性 ρ=0.988(p=9.3e-8)；口袋体积混淆 ρ=−0.018/0.042(均 p>0.9)。**结论：预注册全库检验未发现任一靶标有稳健、尺寸独立且增量可辨的对接富集；ADRA2A 的 Tier-1 阳性是组成伪信号。**
  - **Tier 2 进度**：8/10 靶标完成（GALNS/SLC2A1/TNIK/ITPKC/AXL/SERPINE1/MAPK14/VASH2 各 83/83），ACVR1 42/83 续跑、ADRA2A 待跑；剩余 126 块，ETA **5.3–7.6 h**（中位 6.5 h）。
  - **Tier 2 进度更新（11:30 实检）**：**9/10 靶标完成**，每靶标 2,443–2,455/2,465 打分成功（成功率 98.6–99.6%，失败 10–22/靶标）；仅 **ADRA2A 收尾（61/83 块 ≈73%）**，ETA ≈ 55 min。核对两件事均通过：t2 配体清单 2,465 条**无重复**；`scores_t2_other.csv` **2,465 行、chembl_id 唯一无重复**（先前"2,471 行"是我按行计数误把含换行的 err 字段算进去）。
  - **新增 `p6_breadth.py`（§3.5 广度分析，**在 T2 合表前预注册写好**并 QC 试跑通过）**：固定口径 —— 配体组成受控比较（中位亲和力 + ≤−9/≤−10 kcal/mol 深度计数）、各靶标 vs ADRA2A 配对 Wilcoxon（仅共有配体）、t1-only vs 全库的靶标排序稳定性 Spearman、ChEMBL 结合型标签富集功效（t1-only vs 全库）+ **分子量裁决**（校正后 AUC>0.5 且优于仅用 MW 的基线才判 PASS）；带 `--allow-partial`（QC 模式输出 `_QC_` 前缀）与缺产物拒跑（rc=3）双闸。
  - **QC 试跑（9/10 靶标，ADRA2A 仅 t1）三个关键发现**：
    ① **靶标排序对广度稳健**：t1-only 中位亲和力排序 vs 全库排序 **Spearman ρ = 0.988**（p=9.3e-8）→ 5 倍配体量几乎不改变靶标层秩序；
    ② **口袋体积混淆被证伪**：ρ(对接盒体积, 中位亲和力) = **−0.018**（p=0.96）、ρ(体积, 最佳亲和力)=0.042（p=0.91）→ 跨靶标原始亲和力差异**不能**归因于口袋大小（但 Vina 分数跨口袋仍不可直接比，靶标优先级继续以四维综合分为准）；
    ③ **分子量裁决下只有 ADRA2A 通过**：全库口径新增 4 个达到最少阳性数的靶标（ACVR1 n=9 AUC 0.797、AXL n=13 0.879、MAPK14 n=16 0.779、TNIK n=10 0.824），但它们的 **size-only 基线 AUC 达 0.787–0.840，等于或高于对接 AUC** → 判 `FAIL_size_only_matches`；**ADRA2A（0.618 vs size-only 0.581，校正后 0.597）是唯一 `PASS_size_not_explained`**。这坐实了"ADRA2A 是唯一经得住尺寸控制的靶标"这一主张，而非事后挑选。
  - **新增 `_wait_then_breadth.py` 收尾守望者（幂等）**：等 T2 合表 + 所有 vina 退出 → 若链已死则补齐 步骤3/4/5 → 跑正式广度分析；链活着则让链自己跑完，绝不抢写同一文件。已后台启动。
  - **⚠ 发现并修复一处真实数据完整性缺陷（配体清单变更后的陈旧 chunk 缓存）**：核对 `P6_docking_scores_t1_cns.csv` 时发现配体并集 680 ≠ 清单 620 → 定位到 **AXL 的 `t1_cns` 打分配体集合与当前 `tier1_cns.txt` 不符**：**多出 60 个（现已划入 t2_other）、缺 60 个（现属 t1）**，其余 9 靶标完全一致。根因：chunk 文件名只含 `(target, tag, chunk_index)`、**不含配体清单版本指纹**，清单被重新生成过（分层调整）后旧 chunk 仍被当有效缓存复用；后果是 AXL 的"靶标内百分位"建立在与其它靶标**不同的配体集合**上，跨靶标可比性被静默破坏且全程无报错。
    - **新增 `scripts/p6_audit_liglists.py`**（审计 + `--fix` 修复，可机读 JSON）：先验检查 `t1 ∪ t2 == pass 库`/无交集/无重复；逐 `靶标×层` 断言 `set(scores.chembl_id) == set(清单)`（缺失与多出都必须为 0）；`--fix` 把陈旧 chunk/scores **rename** 到 `_stale_<tag>_<ts>/`（不删除、保留现场）后重跑。实测：**只有 AXL/t1_cns 一处陈旧**，其余 19 个 靶标×层 全部 OK。
    - **新增 `scripts/p6_finalize_watch.py`**（收尾编排器，取代原守望者；旧的已归档到 `scripts/_deprecated/`）：① 等合表；② 若评分产物旧于合表且链已死 → 补跑 步骤3/4/5；③ 审计配体清单，不一致则隔离陈旧缓存 → 重跑该 靶标×层 → 重跑 步骤3/4/5 → 复核至 rc=0；④ 跑正式广度分析（缺产物即 rc=3 拒跑）。已后台启动。
    - 同步更新 `README.md`（新增 §6b errata 记录 + "缓存失效必须审计"约定 + 新脚本用法）与技能（新增陷阱 #27 + §12.3 收尾编排器模式）。
  - **待续**：T2 合表 → 收尾编排器自动完成（评分 + AXL t1 修复 + 广度分析）→ 补 §3.5 → 定稿 → P7 复现包。
