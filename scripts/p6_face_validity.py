#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
P6 — 面容效度检验（face validity）：已知镇痛药 / α2 激动剂是否被筛回来？
=========================================================================
为什么单列一个脚本
------------------
"筛出的 Top 里有已知镇痛药"是虚拟筛选稿件最常见的自证话术，但它极易沦为
**挑选性举例（cherry-picking）**：从 680 个药里挑出 1–2 个讲得通的名字，
并不构成统计证据。本脚本把这句话拆成三个**可证伪**的检验：

  A. 类别层面：手工标注的镇痛药（`pain_prior`，n=64）在药物级榜单上是否整体更靠前？
     → 综合分 AUC + Top-N Fisher 精确检验
  B. 靶标层面：这些镇痛药在 ADRA2A 上的对接亲和力是否更好？
  C. 机制层面：药理学上**定义 ADRA2A** 的 α2-肾上腺素能激动剂
     （可乐定、右美托咪定、替扎尼定、溴莫尼定、阿可乐定、胍法辛、甲基多巴、洛非西定）
     在 ADRA2A 上是否被筛回？ → 并给出 **MW 校正前后**的对比

为什么 C 必须做 MW 校正
------------------------
α2 激动剂多为**小分子**（本例中位 MW 245.6，库中位 300.7），而对接打分
ρ(亲和力, MW) ≈ −0.607 —— 小分子被系统性惩罚。若不校正，会得出
"连可乐定都筛不回来"的错误悲观结论；校正后才能看清真实位置。

无 double-dipping 声明
----------------------
`pain_prior` 与 α2 激动剂名单都是**外部药理学标注**，不参与 composite 的
任何一维（composite 只由 D1 亲和力百分位 / D2 注释多靶重叠 / D3 可及性 /
D4 反向对照可信度构成），因此本检验不是循环论证。

用法
----
    python scripts/p6_face_validity.py            # 默认读 t1_cns

产出
----
    results/tables/P6_face_validity.csv
"""
import os
import sys

import numpy as np
import pandas as pd
from scipy import stats

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
try:
    from p6_paths import TAB
except Exception:  # pragma: no cover
    TAB = os.path.join("results", "tables")

# 药理学上定义 ADRA2A 的 α2-肾上腺素能激动剂（外部先验，非数据驱动）
ALPHA2_AGONISTS = [
    "CLONIDINE", "DEXMEDETOMIDINE", "TIZANIDINE", "BRIMONIDINE",
    "APRACLONIDINE", "GUANFACINE", "METHYLDOPA", "LOFEXIDINE",
]


def auc(pos, neg):
    """AUC = P(score_pos > score_neg)，同时返回单尾 p（pos 更大）。"""
    pos = np.asarray(pos, dtype=float)
    neg = np.asarray(neg, dtype=float)
    pos = pos[~np.isnan(pos)]
    neg = neg[~np.isnan(neg)]
    if len(pos) == 0 or len(neg) == 0:
        return np.nan, np.nan
    u = stats.mannwhitneyu(pos, neg, alternative="two-sided")
    p = stats.mannwhitneyu(pos, neg, alternative="greater").pvalue
    return u.statistic / (len(pos) * len(neg)), p


def main():
    import argparse
    ap = argparse.ArgumentParser()
    # 【说明】曾有一个 --tag 参数，但本脚本读的是 p6_score 已经按层合并好的
    # `P6_ranking_drugs.csv` / `P6_ranking_pairs.csv`，tag 过滤在此处无意义
    # （已按层合并，见 p6_score.py 的同靶标-配体去重逻辑），故删除以免误导。
    ap.add_argument("--target", default="ADRA2A", help="机制检验所用靶标")
    a = ap.parse_args()

    D = pd.read_csv(os.path.join(TAB, "P6_ranking_drugs.csv"))
    P = pd.read_csv(os.path.join(TAB, "P6_ranking_pairs.csv"))
    D = D.sort_values("drug_rank_score", ascending=False).reset_index(drop=True)
    D["rank"] = np.arange(1, len(D) + 1)

    rows = []
    pp = D[D.pain_prior == True]
    nn = D[D.pain_prior != True]

    # ---- A. 类别层面 ----
    for col in ("best_composite", "drug_rank_score"):
        A, p = auc(pp[col], nn[col])
        rows.append(dict(level="A. drug-level", test=f"{col}: analgesic vs rest",
                         n_pos=len(pp), n_neg=len(nn), AUC=round(A, 3), p_one_sided=round(p, 4)))
    for N in (20, 50, 100, 200):
        k = int((pp["rank"] <= N).sum())
        exp = N * len(pp) / len(D)
        odds, p = stats.fisher_exact(
            [[k, N - k], [len(pp) - k, len(nn) - (N - k)]], alternative="greater")
        rows.append(dict(level="A. drug-level", test=f"top-{N} analgesic count",
                         n_pos=k, n_neg=N - k, AUC=np.nan,
                         p_one_sided=round(p, 4)))
        rows[-1]["note"] = f"observed {k}, expected {exp:.1f}, OR={odds:.2f}"

    # ---- B. 靶标层面 ----
    g = P[P.symbol == a.target].copy()
    if len(g):
        gp = g[g.pain_prior == True]
        gn = g[g.pain_prior != True]
        A, p = auc(gp.neg_aff, gn.neg_aff)
        rows.append(dict(level=f"B. {a.target}", test="affinity: analgesic vs rest",
                         n_pos=len(gp), n_neg=len(gn), AUC=round(A, 3),
                         p_one_sided=round(p, 4)))

        # ---- C. 机制层面（α2 激动剂），含 MW 校正 ----
        ok = g.mw.notna() & g.affinity.notna()
        x = g.loc[ok, "affinity"].astype(float).values
        z = g.loc[ok, "mw"].astype(float).values
        b, a0 = np.polyfit(z, x, 1)
        pred = a0 + b * z
        # 统一「越大越好」：raw = -affinity；mw_adj = pred - affinity（优于同尺寸预期）
        g.loc[ok, "raw_score"] = -g.loc[ok, "affinity"].astype(float)
        g.loc[ok, "mw_adj_score"] = pred - g.loc[ok, "affinity"].astype(float)
        for c in ("raw_score", "mw_adj_score"):
            g.loc[ok, c + "_pct"] = g.loc[ok, c].rank(pct=True) * 100

        isA = g.pref_name.isin(ALPHA2_AGONISTS).values
        for lab, col in (("affinity (raw)", "raw_score"), ("affinity (MW-adjusted)", "mw_adj_score")):
            A, p = auc(g.loc[isA, col], g.loc[~isA, col])
            rows.append(dict(level=f"C. alpha-2 agonists on {a.target}", test=lab,
                             n_pos=int(isA.sum()), n_neg=int((~isA).sum()),
                             AUC=round(A, 3), p_one_sided=round(p, 4)))
        A, _ = auc(g.loc[isA, "mw"], g.loc[~isA, "mw"])
        rows.append(dict(level=f"C. alpha-2 agonists on {a.target}", test="MW only (size baseline)",
                         n_pos=int(isA.sum()), n_neg=int((~isA).sum()),
                         AUC=round(A, 3), p_one_sided=np.nan,
                         note=f"median MW {g.loc[isA, 'mw'].median():.1f} vs {g.loc[~isA, 'mw'].median():.1f}"))

        # 逐药百分位（原始 → MW 校正）
        sub = g[g.pref_name.isin(ALPHA2_AGONISTS)][
            ["pref_name", "mw", "affinity", "raw_score_pct", "mw_adj_score_pct"]].copy()
        sub = sub.sort_values("raw_score_pct", ascending=False)
        sub.to_csv(os.path.join(TAB, "P6_face_validity_alpha2_individual.csv"), index=False)
        print(f"\nα2 激动剂逐药位置（{a.target}，百分位越大越好）：")
        print(sub.round(1).to_string(index=False))

    R = pd.DataFrame(rows)
    out = os.path.join(TAB, "P6_face_validity.csv")
    R.to_csv(out, index=False)
    print()
    print(R.to_string(index=False))
    print(f"\n表 -> {out}")

    # ---- 判读提示（避免挑选性举例）----
    n_analgesic_top20 = int((pp["rank"] <= 20).sum())
    print(f"\n[判读] Top-20 中的镇痛药数量 = {n_analgesic_top20} / {len(pp)}"
          f"（期望 {20 * len(pp) / len(D):.1f}）。"
          "若类别层面不显著，稿件不得写「已知镇痛药在 Top 中富集」，"
          "只能把个别药物作为**假设生成性的个例**陈述。")


if __name__ == "__main__":
    main()
