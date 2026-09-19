#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""P6 头号排序的分子量（MW）敏感性检验

背景（为什么必须做）
------------------
实测 ρ(对接亲和力, MW) = −0.607：大分子在对接里系统性拿到更好的分。而 P6 的
头号结论"ADRA2A 领先、Top 候选为麦角胺类/抗精神病药"里，这些候选恰好**都是
大分子**。此前已证明**富集层面**的抗 MW 性（AUC 0.618 -> MW 校正后 0.597），
但**药物级排序本身**从未做 MW 敏感性检验 —— 这是"结论是否只是分子量榜"的
最后一道闸门。

做法（三套打分并存、互相比较，不覆盖主口径）
--------------------------------------------
主口径   D1_raw     = 靶内亲和力百分位（= p6_score.py 的 D1_affinity）
变体 A   D1_mwres   = 靶内 (亲和力对 MW 线性回归残差) 的百分位
变体 B   D1_mwstrat = 靶内 MW 五分位**各层内部**的亲和力百分位（非参数，不假设线性）

三套均保留 D2_pharm_prior / D3_accessibility / D4_reliability 与原权重
(0.40 / 0.25 / 0.20 / 0.15)，只替换 D1，从而**隔离 MW 这一个变量**。

判据（写死在脚本里，不做事后解释）
----------------------------------
- Spearman(主口径 composite, 变体 composite) ≥ 0.80 且 Top-20 重叠 ≥ 12
  -> "排序对 MW 稳健"（PASS）
- 否则 -> "排序部分由分子量驱动，必须作为局限披露"（WARN）
二者结论均需写入稿件；不得只保留好看的一套。

输出
----
results/tables/P6_mw_ranking_pairs.csv       逐配对：三套 D1 / composite / 排名
results/tables/P6_mw_ranking_drugs.csv       逐药物：三套药物级排名
results/tables/P6_mw_ranking_summary.csv     汇总判据（含 precision@k）
"""
import os
import re
import sys

import numpy as np
import pandas as pd
from scipy import stats

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TAB = os.path.join(ROOT, "results", "tables")
W = {"D1": 0.40, "D2": 0.25, "D3": 0.20, "D4": 0.15}
MAIN_TARGET = "ADRA2A"
TOPK = [10, 20, 50]


def _mw_variants(g):
    """在单个靶标内构造三套 D1（均为 0–1，越大越好）。"""
    g = g.copy()
    aff = g.affinity.astype(float)
    mw = g.mw.astype(float)
    ok = aff.notna() & mw.notna()

    # 主口径：原始亲和力百分位（越负越好 -> 用 -affinity 排名）
    g["D1_raw"] = (-aff).rank(pct=True)

    # 变体 A：对 MW 线性回归取残差，再排名
    d1a = pd.Series(np.nan, index=g.index, dtype=float)
    if ok.sum() >= 10:
        z = mw[ok].values
        y = aff[ok].values
        b, a = np.polyfit(z, y, 1)
        resid = y - (a + b * z)            # 残差 >0 = 比同尺寸分子更弱
        d1a.loc[ok] = pd.Series(-resid, index=g.index[ok]).rank(pct=True)
    g["D1_mwres"] = d1a

    # 变体 B：MW 五分位分层内排名（非参数）
    d1b = pd.Series(np.nan, index=g.index, dtype=float)
    if ok.sum() >= 25:
        bins = pd.qcut(mw[ok], 5, labels=False, duplicates="drop")
        s = pd.Series(-aff[ok].values, index=g.index[ok])
        d1b.loc[ok] = s.groupby(bins).rank(pct=True)
    g["D1_mwstrat"] = d1b

    for k in ("D1_raw", "D1_mwres", "D1_mwstrat"):
        g["comp_" + k] = (W["D1"] * g[k].fillna(g["D1_raw"]) +
                          W["D2"] * g.D2_pharm_prior.fillna(0.5) +
                          W["D3"] * g.D3_accessibility.fillna(0.5) +
                          W["D4"] * g.D4_reliability.fillna(0.5))
    return g


def _spearman(a, b):
    m = a.notna() & b.notna()
    if m.sum() < 5:
        return np.nan
    return float(stats.spearmanr(a[m], b[m]).statistic)


def main():
    fp = os.path.join(TAB, "P6_ranking_pairs.csv")
    if not os.path.exists(fp):
        print("[FAIL] 缺 %s" % fp)
        return 1
    P = pd.read_csv(fp)
    P["chembl_id"] = P.chembl_id.astype(str)

    # 逐靶标构造三套打分，再合并回全表
    parts = [_mw_variants(g) for _, g in P.groupby("symbol", sort=False)]
    P = pd.concat(parts, ignore_index=True)

    keep = ["symbol", "chembl_id", "pref_name", "mw", "affinity", "n_torsions",
            "pct_in_target", "D1_affinity", "D2_pharm_prior", "D3_accessibility",
            "D4_reliability", "composite",
            "D1_raw", "D1_mwres", "D1_mwstrat",
            "comp_D1_raw", "comp_D1_mwres", "comp_D1_mwstrat"]
    keep = [c for c in keep if c in P.columns]
    R = P[keep].copy()
    for c in ("comp_D1_raw", "comp_D1_mwres", "comp_D1_mwstrat"):
        R["rank_" + c] = R.groupby("symbol")[c].rank(ascending=False, method="min")
    R.sort_values(["symbol", "rank_comp_D1_raw"]).round(4).to_csv(
        os.path.join(TAB, "P6_mw_ranking_pairs.csv"), index=False)

    # ---------- 主靶标（ADRA2A）配对级 ----------
    G = R[R.symbol == MAIN_TARGET].copy()
    if len(G) < 20:
        print("[FAIL] %s 配对数不足（%d）" % (MAIN_TARGET, len(G)))
        return 1
    G = G.sort_values("comp_D1_raw", ascending=False).reset_index(drop=True)
    G["rank_raw"] = np.arange(1, len(G) + 1)
    G["rank_mwres"] = G.comp_D1_mwres.rank(ascending=False, method="min")
    G["rank_mwstrat"] = G.comp_D1_mwstrat.rank(ascending=False, method="min")

    # ---------- 判据 ----------
    rho_res = _spearman(G.comp_D1_raw, G.comp_D1_mwres)
    rho_str = _spearman(G.comp_D1_raw, G.comp_D1_mwstrat)
    rho_d1 = _spearman(G.D1_raw, G.D1_mwres)      # 仅亲和力维度的稳健性
    ov = {}
    for k in TOPK:
        A = set(G.nsmallest(k, "rank_raw").chembl_id)
        for tag, col in (("mwres", "rank_mwres"), ("mwstrat", "rank_mwstrat")):
            B = set(G.nsmallest(k, col).chembl_id)
            ov[(k, tag)] = len(A & B)

    # ---------- precision@k（独立 ChEMBL 阳性） ----------
    prec = {}
    rcp = os.path.join(TAB, "P6_reverse_control_positives.csv")
    if os.path.exists(rcp):
        CP = pd.read_csv(rcp)
        CP["chembl_id"] = CP.chembl_id.astype(str)
        pos = set(CP.loc[CP.symbol == MAIN_TARGET, "chembl_id"])
        n_in = len(pos & set(G.chembl_id))
        base = n_in / len(G)
        prec["baseline"] = round(base, 4)
        prec["n_positives"] = n_in
        N = len(G)
        for k in TOPK:
            for tag, col in (("raw", "rank_raw"), ("mwres", "rank_mwres"),
                             ("mwstrat", "rank_mwstrat")):
                hit = len(set(G.nsmallest(k, col).chembl_id) & pos)
                prec["prec@%d_%s" % (k, tag)] = round(hit / k, 3)
                prec["hit@%d_%s" % (k, tag)] = hit
                # 超几何检验：从 N 个里取 k 个，命中 >= hit 的概率（越小越不可能偶然）
                prec["hyper_p@%d_%s" % (k, tag)] = float(
                    stats.hypergeom.sf(hit - 1, N, n_in, k))
            prec["lift@%d_raw" % k] = round(prec["prec@%d_raw" % k] / base, 2)

    # ---------- 药物级（跨 10 靶标）----------
    bi = {}
    for c in ("comp_D1_raw", "comp_D1_mwres", "comp_D1_mwstrat"):
        idx = R.groupby("chembl_id")[c].idxmax()
        bi[c] = R.loc[idx, ["chembl_id", "pref_name", "symbol", "mw", "affinity", c]]
    # 注意：不要在这里复用循环变量 c —— 循环结束后它残留为最后一个列名，
    # 会让 rename 字典指向不存在的列而静默失效（本脚本曾因此 KeyError）。
    DR = (bi["comp_D1_raw"]
          .rename(columns={"symbol": "best_target_raw",
                           "comp_D1_raw": "score_raw"}))
    for c, tag in (("comp_D1_mwres", "mwres"), ("comp_D1_mwstrat", "mwstrat")):
        other = bi[c].rename(columns={"symbol": "best_target_" + tag, c: "score_" + tag})
        DR = DR.merge(other[["chembl_id", "best_target_" + tag, "score_" + tag]],
                      on="chembl_id", how="outer")
    DR["rank_raw"] = DR.score_raw.rank(ascending=False, method="min")
    DR["rank_mwres"] = DR.score_mwres.rank(ascending=False, method="min")
    DR["rank_mwstrat"] = DR.score_mwstrat.rank(ascending=False, method="min")
    DR.sort_values("rank_raw").round(4).to_csv(
        os.path.join(TAB, "P6_mw_ranking_drugs.csv"), index=False)
    drug_rho = _spearman(DR.score_raw, DR.score_mwres)
    drug_ov = {k: len(set(DR.nsmallest(k, "rank_raw").chembl_id) &
                      set(DR.nsmallest(k, "rank_mwres").chembl_id)) for k in TOPK}

    # ---------- 打印 ----------
    print("=" * 90)
    print("P6 头号排序的 MW 敏感性检验")
    print("=" * 90)
    print("主靶标 %s：n 配对=%d，其中 ChEMBL 实测阳性 %d（基线 %.1f%%）"
          % (MAIN_TARGET, len(G), prec.get("n_positives", 0),
             100 * prec.get("baseline", float("nan"))))
    print()
    print("排序稳健性（Spearman）：")
    print("  D1 单维      主口径 vs MW残差   rho=%.3f" % rho_d1)
    print("  composite    主口径 vs MW残差   rho=%.3f" % rho_res)
    print("  composite    主口径 vs MW分层   rho=%.3f" % rho_str)
    print()
    print("Top-k 重叠（主口径 ∩ 变体）/ k：")
    for k in TOPK:
        print("  Top%-3d  MW残差 %2d/%d    MW分层 %2d/%d"
              % (k, ov[(k, "mwres")], k, ov[(k, "mwstrat")], k))
    print()
    if prec:
        print("precision@k（ChEMBL 实测阳性占比；基线 %.1f%%）：" % (100 * prec["baseline"]))
        for k in TOPK:
            print("  Top%-3d  主口径 %.3f (lift x%.2f, p=%.2g)   MW残差 %.3f   MW分层 %.3f"
                  % (k, prec["prec@%d_raw" % k], prec["lift@%d_raw" % k],
                     prec["hyper_p@%d_raw" % k],
                     prec["prec@%d_mwres" % k], prec["prec@%d_mwstrat" % k]))
    print()
    print("ADRA2A Top-10 名单（三套口径并列，看具体身份是否稳定）：")
    t10 = pd.DataFrame({
        "raw": G.nsmallest(10, "rank_raw").pref_name.values,
        "mwres": G.nsmallest(10, "rank_mwres").pref_name.values,
        "mwstrat": G.nsmallest(10, "rank_mwstrat").pref_name.values})
    print(t10.to_string(index=False))
    print()
    print("药物级（跨 10 靶标，n=%d）：Spearman 主口径 vs MW残差 = %.3f"
          % (len(DR), drug_rho))
    print("  Top-k 重叠：%s" % ", ".join("Top%d %d/%d" % (k, drug_ov[k], k) for k in TOPK))

    # ---------- 判据输出 ----------
    verdict = "PASS" if (rho_res >= 0.80 and ov[(20, "mwres")] >= 12) else "WARN"
    print()
    print("=" * 90)
    print("判据：Spearman>=0.80 且 Top-20 重叠>=12  ->  %s" % verdict)
    if verdict == "PASS":
        print("  头号排序对分子量稳健；MW 不构成排序的主要驱动。")
    else:
        print("  排序部分由分子量驱动 —— 必须在稿件中作为局限显式披露，"
              "并同时报告 MW 校正后的榜单。")
    print("=" * 90)

    S = pd.DataFrame([{
        "target": MAIN_TARGET, "n_pairs": len(G),
        "rho_D1_raw_vs_mwres": round(rho_d1, 4),
        "rho_composite_raw_vs_mwres": round(rho_res, 4),
        "rho_composite_raw_vs_mwstrat": round(rho_str, 4),
        "top20_overlap_mwres": ov[(20, "mwres")],
        "top20_overlap_mwstrat": ov[(20, "mwstrat")],
        "drug_rho_raw_vs_mwres": round(drug_rho, 4),
        "drug_top20_overlap_mwres": drug_ov[20],
        "verdict": verdict, **prec}])
    S.to_csv(os.path.join(TAB, "P6_mw_ranking_summary.csv"), index=False)
    print()
    print("-> results/tables/P6_mw_ranking_pairs.csv")
    print("-> results/tables/P6_mw_ranking_drugs.csv")
    print("-> results/tables/P6_mw_ranking_summary.csv")
    return 0


if __name__ == "__main__":
    sys.exit(main())
