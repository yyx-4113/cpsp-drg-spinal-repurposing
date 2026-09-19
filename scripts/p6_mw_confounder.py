#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
P6 — 富集信号的分子量混淆检验（MW-confounder check）
=====================================================
为什么必须有这一步
------------------
分子对接打分天然偏袒**大分子**：配体越大、可接触的重原子越多，
打分函数给出的亲和力数值越负（Vina 的 gauss/repulsion/ hydrophobic
项都随原子数单调累加）。因此"已知活性药在对接榜单上富集"很可能是
**分子量（MW）伪信号**，而不是方法真的有效。

若不排除这一混淆，回顾性富集 AUC 就是一个不可解释的数字，
审稿人有充分理由据此拒稿。本脚本给出三重防线：

  1. AUC_MW_only      —— 仅用 MW 预测"是否为已知活性药"的 AUC
                         （尺寸偏倚的**上界基线**）
  2. AUC_MW_adjusted  —— 把对接打分对 MW 做线性回归取残差后的 AUC
                         （去除 MW 线性贡献）
  3. AUC_MW_stratified—— 按 MW 五分位分层、层内计算 AUC 再平均
                         （非参数、不假设线性，最稳健）

判读规则（写死在报告里，避免事后解释）：
  · 只有 docking AUC 显著 > 0.5 **且** MW 校正/分层后仍 > 0.5，
    才可声称"富集不是尺寸伪信号"；
  · 若 AUC_MW_only ≥ AUC_dock，则富集**完全可由尺寸解释**，不得声称为方法效度证据。

无 double-dipping 声明
----------------------
标签（是否为该靶标的已知活性分子）来自 **ChEMBL 实测活性**（pChEMBL ≥ 6，
由 scripts/p6_reverse_control.py 抓取），预测来自 **AutoDock Vina 对接打分**。
两者数据源独立，标签不参与任何打分或阈值设定，因此不存在二重蘸取。

用法
----
    python scripts/p6_mw_confounder.py                 # 默认读 t1_cns
    python scripts/p6_mw_confounder.py --tags t1_cns,t2_other

产出
----
    results/tables/P6_enrichment_mw_confounder_check.csv
"""
import os
import sys

import numpy as np
import pandas as pd
from scipy import stats

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
try:
    from p6_paths import TAB  # 若存在统一路径模块则复用
except Exception:  # pragma: no cover
    TAB = os.path.join("results", "tables")
# 唯一统计口径模块（裁决函数、AUC、尺寸控制三件套、2D 基线全在它里面）
import p6_stats as S  # noqa: E402

MIN_KNOWN = 5          # 少于 5 个已知阳性不做检验（统计上无意义）
N_MW_STRATA = 5        # MW 分层数


def auc(y, score):
    """AUC via Mann-Whitney U；score 越大代表预测越"像阳性"。"""
    y = np.asarray(y)
    score = np.asarray(score, dtype=float)
    m = ~np.isnan(score)
    y, score = y[m], score[m]
    if len(set(y)) < 2:
        return np.nan
    a, b = score[y == 1], score[y == 0]
    if len(a) == 0 or len(b) == 0:
        return np.nan
    return float(stats.mannwhitneyu(a, b, alternative="two-sided").statistic) / (len(a) * len(b))


def _residualise(x, z):
    """x 对 z 做线性拟合后取残差（去掉 z 的线性贡献）。"""
    x = np.asarray(x, dtype=float)
    z = np.asarray(z, dtype=float)
    return x - np.polyval(np.polyfit(z, x, 1), z)


def load(tags):
    import glob
    frames = []
    for t in tags:
        f = os.path.join(TAB, f"P6_docking_scores_{t}.csv")
        if not os.path.exists(f):
            print(f"[warn] 缺对接产物，跳过：{f}")
            continue
        frames.append(pd.read_csv(f))
    if not frames:
        raise SystemExit("没有任何对接打分文件，退出")
    sc = pd.concat(frames, ignore_index=True)

    lig = pd.read_csv(os.path.join(TAB, "P6_ligand_library.csv"))
    posp = os.path.join(TAB, "P6_reverse_control_positives.csv")
    if not os.path.exists(posp):
        raise SystemExit("缺 P6_reverse_control_positives.csv —— 先跑 scripts/p6_reverse_control.py")
    pos = pd.read_csv(posp)

    for d in (sc, lig, pos):
        d["chembl_id"] = d["chembl_id"].astype(str)

    M = sc.merge(lig[["chembl_id", "mw", "logp", "tpsa", "hbd", "hba", "rotb"]],
                 on="chembl_id", how="left")
    return M, pos


def main():
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument("--tags", default="t1_cns", help="逗号分隔的对接层 tag")
    ap.add_argument("--min-known", type=int, default=MIN_KNOWN)
    a = ap.parse_args()
    tags = [t.strip() for t in a.tags.split(",") if t.strip()]

    M, pos = load(tags)
    print(f"对接打分 {len(M)} 行 | 靶标 {M.symbol.nunique()} 个 | "
          f"配体 {M.chembl_id.nunique()} 个 | ChEMBL 阳性 {len(pos)} 条")
    if M["mw"].isna().any():
        print(f"[warn] {int(M['mw'].isna().sum())} 行缺 MW，将被逐靶标剔除")

    rows = []
    for sym, g in M.groupby("symbol"):
        known_ids = set(pos.loc[pos.symbol == sym, "chembl_id"])
        g = g.copy()
        g["known"] = g.chembl_id.isin(known_ids).astype(int)
        if g.known.sum() < a.min_known:
            continue

        aff = g.affinity.astype(float)      # 越负越好
        mw = g.mw.astype(float)
        ok = (~np.isnan(mw)).values & (~np.isnan(aff)).values

        # 1)–3) 尺寸控制三件套：走**共享统计模块**（p6_stats），确保与 p6_breadth 同一套数学。
        # 【踩过的坑 · 已修 2026-09-19】此前本脚本与 p6_breadth.py **各写了一套裁决规则**，
        # 对 AXL 给出**相反结论**（本脚本 PASS、breadth FAIL）——同一份稿件里两个互斥裁决。
        # 现在唯一的裁决函数是 p6_stats.enrichment_verdict()。
        auc_adj, auc_mw, auc_dock, slope = S.mw_adjust_auc(aff, mw, g.known.values)
        # 4) 显著性：阳性配体的亲和力是否显著更优（**单侧**，方向与 AUC 一致）
        neg = (-aff).values
        p = S.auc_p(neg[(g.known.values == 1) & ok], neg[(g.known.values == 0) & ok])
        # 5) 打分-MW 相关（尺寸偏倚强度）
        rho = stats.spearmanr(aff[ok], mw[ok]).statistic
        # 6) MW 分层内 AUC 均值
        strat = []
        try:
            q = pd.qcut(mw[ok], N_MW_STRATA, labels=False, duplicates="drop")
            qv = pd.Series(q).values
            for k in pd.Series(qv).dropna().unique():
                sel = ok & (qv == k)
                v = S.auc(g.known.values[sel], (-aff).values[sel])
                if not np.isnan(v):
                    strat.append(v)
        except Exception:
            pass
        # 7) 【第二道平凡基线】2D 理化性质 logistic 回归的交叉验证 AUC。
        #    仅 MW 是最弱的平凡基线；审稿人更可能问"5 个常见描述符能不能打平对接"。
        #    小样本必须交叉验证，否则基线被过拟合高估。
        auc_phys, n_feat = S.physchem_baseline_auc(
            g[["mw", "logp", "tpsa", "hbd", "hba", "rotb"]], g.known.values)
        # 8) Bootstrap 95% CI：小样本（n_pos 9–16）下必须报不确定度，否则
        #    "0.879 vs 0.839"这种差距会被读成"显著优于基线"，而实际 CI 大幅重叠。
        ci_lo, ci_hi = S.auc_boot_ci(neg[(g.known.values == 1) & ok],
                                     neg[(g.known.values == 0) & ok])
        cs_lo, cs_hi = S.auc_boot_ci(mw[(g.known.values == 1) & ok],
                                     mw[(g.known.values == 0) & ok])
        # 10) 【决定性统计量】同一批配体上 ΔAUC = AUC(对接) − AUC(基线) 的配对 bootstrap CI。
        #     单看"对接 0.879 > 基线 0.841"不足以声称增量：两个 AUC 各自有不确定度，
        #     小样本下其**差值**的 CI 往往跨 0。CI 含 0 ⇒ 不能说对接提供增量信息。
        d0_s, dlo_s, dhi_s = S.delta_auc_paired_ci(neg, mw, g.known.values)
        p_d_s = S.delta_auc_p_le0(neg, mw, g.known.values)
        phys_score = S.physchem_in_sample_score(
            g[["mw", "logp", "tpsa", "hbd", "hba", "rotb"]], g.known.values)
        if phys_score is not None:
            d0_p, dlo_p, dhi_p = S.delta_auc_paired_ci(neg, phys_score, g.known.values)
            p_d_p = S.delta_auc_p_le0(neg, phys_score, g.known.values)
        else:
            d0_p = dlo_p = dhi_p = p_d_p = np.nan
        # 11) 唯一裁决（把两个 ΔAUC 的 CI 一起交给它，让"增量不显著"写进理由里）
        verdict, reason = S.enrichment_verdict(
            int(g.known.sum()), auc_dock, auc_mw, auc_adj, p,
            auc_physchem=auc_phys,
            delta_vs_size_ci=(dlo_s, dhi_s), delta_vs_physchem_ci=(dlo_p, dhi_p))

        rows.append(dict(
            symbol=sym, n_known=int(g.known.sum()), n_total=len(g),
            AUC_dock=round(auc_dock, 3) if np.isfinite(auc_dock) else np.nan,
            AUC_dock_CI95=f"[{ci_lo:.3f}, {ci_hi:.3f}]" if np.isfinite(ci_lo) else "n/a",
            AUC_MW_only=round(auc_mw, 3) if np.isfinite(auc_mw) else np.nan,
            AUC_MW_only_CI95=f"[{cs_lo:.3f}, {cs_hi:.3f}]" if np.isfinite(cs_lo) else "n/a",
            AUC_MW_adjusted=round(auc_adj, 3) if np.isfinite(auc_adj) else np.nan,
            AUC_MW_stratified=round(float(np.mean(strat)), 3) if strat else np.nan,
            AUC_physchem_2D_CV=round(auc_phys, 3) if np.isfinite(auc_phys) else np.nan,
            n_physchem_feat=n_feat,
            deltaAUC_vs_size_only=round(d0_s, 3) if np.isfinite(d0_s) else np.nan,
            deltaAUC_vs_size_only_CI95=(f"[{dlo_s:+.3f}, {dhi_s:+.3f}]"
                                        if np.isfinite(dlo_s) else "n/a"),
            deltaAUC_vs_size_only_p_le0=round(p_d_s, 4) if np.isfinite(p_d_s) else np.nan,
            deltaAUC_vs_physchem=round(d0_p, 3) if np.isfinite(d0_p) else np.nan,
            deltaAUC_vs_physchem_CI95=(f"[{dlo_p:+.3f}, {dhi_p:+.3f}]"
                                       if np.isfinite(dlo_p) else "n/a"),
            deltaAUC_vs_physchem_p_le0=round(p_d_p, 4) if np.isfinite(p_d_p) else np.nan,
            rho_affinity_MW=round(float(rho), 3),
            mw_slope_on_neg_affinity=round(float(slope), 5) if np.isfinite(slope) else np.nan,
            p_mannwhitney=p, verdict=verdict, verdict_reason=reason))

    R = pd.DataFrame(rows)
    if R.empty:
        print("没有任何靶标达到 min-known 门槛，未产出表")
        return
    out = os.path.join(TAB, "P6_enrichment_mw_confounder_check.csv")
    R.to_csv(out, index=False)
    cols = ["symbol", "n_known", "n_total", "AUC_dock", "AUC_dock_CI95", "AUC_MW_only",
            "AUC_MW_adjusted", "AUC_physchem_2D_CV", "rho_affinity_MW", "p_mannwhitney", "verdict"]
    print()
    print(R[[c for c in cols if c in R.columns]].to_string(index=False))
    n_pass = int((R.verdict == "PASS_size_independent").sum())
    print(f"\n裁决汇总：PASS_size_independent {n_pass} / {len(R)}（唯一判据见 p6_stats.enrichment_verdict）")
    for _, r in R.iterrows():
        print(f"  · {r.symbol:8s} {r.verdict:32s} {r.verdict_reason}")
    print(f"\n表 -> {out}")


if __name__ == "__main__":
    main()
