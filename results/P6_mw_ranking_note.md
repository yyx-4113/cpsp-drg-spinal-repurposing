# P6 头号排序的 MW 敏感性 + precision@k（实测）

脚本：`scripts/p6_mw_ranking_sensitivity.py`
产物：`results/tables/P6_mw_ranking_{pairs,drugs,summary}.csv`
报告：`results/P6_RESULTS.md` §7.3
稿件：`reports/P6_manuscript_draft.md` §3.4.2

---

## 为什么必须做

实测 ρ(对接亲和力, MW) = −0.607，对接系统性偏爱大分子。而本稿头号候选
（麦角胺类、抗精神病药）**恰好都是大分子**。此前只证明了**富集层面**
（AUC 0.618 → MW 校正 0.597）的抗尺寸性，**药物级排序本身从未做过 MW 检验**。
未检验就发表 ="结论可能只是分子量榜"。

## 做法（隔离单一变量）

保留 D2/D3/D4 与原权重（0.40 / 0.25 / 0.20 / 0.15），**只替换 D1**：

| 口径 | D1 定义 |
|---|---|
| 主口径 | 靶内亲和力百分位（= `p6_score.py` 的 `D1_affinity`）|
| 变体 A（MW 残差） | 亲和力对 MW 线性回归**残差**的靶内百分位 |
| 变体 B（MW 分层） | MW 五分位**层内**亲和力百分位（非参数，不假设线性）|

判据**事先写死**：Spearman ≥ 0.80 且 Top-20 重叠 ≥ 12 → 稳健（PASS），否则 WARN。

## 结果

### ① 排序稳健性（ADRA2A，620 配对）

| 比较 | Spearman ρ |
|---|---|
| D1 单维：主口径 vs MW 残差 | 0.784 |
| composite：主口径 vs MW 残差 | **0.833** |
| composite：主口径 vs MW 分层 | **0.802** |
| 药物级（跨 10 靶标，680 药） | 0.888 |

Top-20 名单重叠：**14/20**（MW 残差）、13/20（MW 分层）。→ **判定 PASS**

### ② precision@k（独立 ChEMBL 实测阳性，基线 14.2%）

| k | 命中 | precision | lift | 超几何 p | MW 残差 | MW 分层 |
|---|---|---|---|---|---|---|
| 10 | 8/10 | **0.800** | ×5.64 | 4.4×10⁻⁶ | 0.600 | 0.800 |
| 20 | 14/20 | **0.700** | ×4.93 | 9.8×10⁻⁹ | 0.700 | 0.550 |
| 50 | 20/50 | **0.400** | ×2.82 | 2.1×10⁻⁶ | 0.360 | 0.360 |

标签来自实测活性、预测来自对接 → **无二重蘸取**。两种 MW 校正下 precision 仍
0.55–0.80，远高于基线。

### ③ 但 Top-10 的具体身份不稳（必须披露）

三套口径的 Top-10 并列显示，**仅 4/10 重叠**：

| 主口径 | MW 残差 | MW 分层 |
|---|---|---|
| ERGOTAMINE | RISPERIDONE | DEXMEDETOMIDINE |
| RISPERIDONE | DEXMEDETOMIDINE | ERGOTAMINE |
| DIHYDROERGOTAMINE | FLUPIRTINE | NAPHAZOLINE |
| ZIPRASIDONE | ZIPRASIDONE | RISPERIDONE |
| FLUPIRTINE | MIRTAZAPINE | DIHYDROERGOTAMINE |
| LURASIDONE | NAPHAZOLINE | FLUPIRTINE |
| TRAZODONE | LOXOPROFEN | MIRTAZAPINE |
| BROMOCRIPTINE | FROVATRIPTAN | FELBINAC |
| ELETRIPTAN | FELBINAC | ZIPRASIDONE |
| ARIPIPRAZOLE | ERGOTAMINE | LURASIDONE |

MW 校正后**右美托咪定、氟吡汀挤入前五**，鲁拉西酮、阿立哌唑掉出。

## 结论（两句，必须同时引用）

1. **排序质量对 MW 稳健**：Spearman 0.80–0.83、Top-20 重叠 14/20、precision@10
   0.80（lift ×5.6, p=4.4×10⁻⁶）且经 MW 校正仍显著 → "ADRA2A 的 Top 候选集合富集
   真实 ADRA2A 结合物"**不是尺寸伪信号**。
2. **但"某个药排名第一"不稳健**（Top-10 仅 4/10 重叠）。故稿件只主张
   **Top-20 候选集合**，不作单药首位结论。

### 与 §3.4.1 的张力（有意保留）

类别层面 α2 激动剂**不富集**（MW 校正后 AUC 0.475），但**单个**选择性 α2A 激动剂
右美托咪定却是最 MW-稳健的头部候选之一。类别阴性不排除个体例外——两条都报。

## 复现

```bash
python scripts/p6_mw_ranking_sensitivity.py
```

## 附：踩到的脚本 bug（已修）

`for c in (...): bi[c] = ...` 之后在同一作用域复用 `c` 构造 rename 字典
（`{c: "score_raw"}`）—— 循环结束后 `c` 残留为**最后一个列名**，导致 rename
指向不存在的列而**静默失效**，随后 `AttributeError`。教训：**不要用循环变量
拼列名字典**，写字面量。
