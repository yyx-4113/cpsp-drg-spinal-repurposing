# -*- coding: utf-8 -*-
"""
p6_breadth.py —— P6 全库广度分析（稿件 §3.5「Full-library breadth」的预注册分析）

【为什么单独写这个脚本】
Tier 1 只对 620 个「CNS/镇痛先验」配体做了对接。它带来一个**结构性的比较偏倚**：
10 个靶标面对的配体集合不是同一批（每靶标 t1 集合相同，但 t1 本身是筛选过的子集），
而且 ADRA2A 的富集检验只有 n=88 个 ChEMBL 阳性可用、统计功效偏低。
Tier 2 把**同一批 2,465 个其余已批准药**对 10 个靶标全部对接后：
  (1) 靶标层面比较变成**配体组成受控**——10 个靶标面对的是**完全相同的 3,085 配体**，
      因此靶标间差异不再能被"某靶标的配体更小/更亲脂"这类组成效应解释；
  (2) ADRA2A 的 ChEMBL 阳性数从 88 上升到全库可用数，**功效提高**；
  (3) 可以定量回答"广度会不会改变靶标排序"（t1-only 排序 vs 全库排序的 Spearman ρ）。
这三点正是稿件 §3.5 需要回答的问题。

【预注册纪律】
本脚本在 Tier 2 合表**之前**写好，分析口径在此固定：
  · 配体组成受控比较：用每靶标的 affinity **分布中位数**（主）+ ≤−9.0 / ≤−10.0 kcal/mol
    的**深度计数**（辅），两者都对极端值不敏感；
  · ADRA2A 与各靶标的配对检验：只在**两靶标共有的配体**上做 Wilcoxon 符号秩检验（配对）；
  · 富集检验标签：**只用 ChEMBL 结合型标签**（pChEMBL≥6，与 p6_score.py 口径一致），
    绝不掺入 PAIN_PRIOR / DRH 注释型标签；
  · MW 混淆：与已发表的 MW 控制同口径 —— 对所有配体把 (-affinity) 对 MW 做线性回归，
    取残差再算 AUC；并给出"仅用 MW 当打分"的 size-only 基线。
不做事后挑选（no cherry-picking）：所有靶标、所有通过阈值的富集检验都进表。

用法：
  python p6_breadth.py                      # 默认要求 10 靶标 × 两 tag 全齐，否则拒跑
  python p6_breadth.py --allow-partial      # QC 用：允许缺靶标，输出加 _QC_ 前缀（不覆盖正式产物）
产出：
  results/tables/{prefix}_target_summary.csv        每靶标分布统计（组成受控）
  results/tables/{prefix}_paired_vs_adra2a.csv      各靶标 vs ADRA2A 的配对 Wilcoxon
  results/tables/{prefix}_target_rank_stability.csv t1-only 排序 vs 全库排序
  results/tables/{prefix}_chembl_power.csv          各靶标富集 AUC：t1-only vs 全库（含 MW 控制）
  results/figures/{prefix}_breadth.png
  results/{prefix}_note.md                          人读摘要（含 caveats）
"""
import os, sys, json, glob, argparse
import numpy as np
import pandas as pd
from scipy import stats

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
# 唯一统计口径模块 —— 裁决函数只用它里面的那一个（见 p6_stats 模块 docstring：
# 此前本脚本与 p6_mw_confounder.py 各写一套规则，对 AXL 给出**相反**结论）
import p6_stats as S  # noqa: E402

ROOT = "D:/2026.9/极速交付9月会员日优惠套路/01_AI生信-虚拟多重筛药/慢性疼痛"
TAB = os.path.join(ROOT, "results/tables")
DOCK = os.path.join(ROOT, "docking/out")
FIG = os.path.join(ROOT, "results/figures")
RES = os.path.join(ROOT, "results")

TAGS = ["t1_cns", "t2_other"]
TARGETS = ["ACVR1", "ADRA2A", "AXL", "GALNS", "ITPKC",
           "MAPK14", "SERPINE1", "SLC2A1", "TNIK", "VASH2"]

DEEP = -9.0     # 「深度」阈值 1（kcal/mol）
DEEP2 = -10.0   # 「深度」阈值 2
MIN_ACT = 5     # 富集检验的最少阳性数（不足则只报 n 不报 AUC，避免功效不足的伪结论）


def auc(pos, neg):
    """AUC = P(pos>neg)+0.5P(tie)，秩公式（结平处理与 p6_score.py 一致）"""
    pos, neg = np.asarray(pos, float), np.asarray(neg, float)
    if len(pos) == 0 or len(neg) == 0:
        return np.nan
    allv = np.concatenate([pos, neg])
    r = pd.Series(allv).rank().to_numpy()
    Rp = r[:len(pos)].sum()
    U = Rp - len(pos) * (len(pos) + 1) / 2.0
    return float(U / (len(pos) * len(neg)))


def auc_p(pos, neg):
    """Hanley–McNeil 正态近似 p 值（双侧），与 p6_face_validity / mw_confounder 同口径"""
    a = auc(pos, neg)
    n1, n2 = len(pos), len(neg)
    if not np.isfinite(a) or n1 < 2 or n2 < 2:
        return np.nan
    q1 = a / (2 - a) if a != 2 else 0.0
    q2 = 2 * a * a / (1 + a) if a != -1 else 0.0
    var = (a * (1 - a) + (n1 - 1) * (q1 - a * a) + (n2 - 1) * (q2 - a * a)) / (n1 * n2)
    if var <= 0:
        return np.nan
    z = (a - 0.5) / np.sqrt(var)
    return float(2 * (1 - stats.norm.cdf(abs(z))))


# 【已删除本地的 mw_adjust_auc 实现 · 2026-09-19】它与 p6_mw_confounder.py 里的同名函数
# 是两份独立实现，正是"同一批数字、两套算法"的隐患来源。现统一走 p6_stats.mw_adjust_auc()。
# 教训：**同一种统计量只允许有一份实现**；一旦出现第二份，两份迟早会在某个边界条件上分叉，
# 而且分叉时不会有任何报错——只会让稿件里出现两个互相矛盾的数。
def load_table(sym, tag):
    p = os.path.join(DOCK, sym, f"scores_{tag}.csv")
    if not os.path.exists(p):
        return None
    d = pd.read_csv(p)
    d["symbol"] = sym
    d["tag"] = tag
    d["chembl_id"] = d.chembl_id.astype(str)
    d["affinity"] = pd.to_numeric(d.affinity, errors="coerce")
    if "rc" in d.columns:
        d = d[pd.to_numeric(d.rc, errors="coerce").fillna(1).eq(0)]
    d = d[np.isfinite(d.affinity)]
    return d[["symbol", "chembl_id", "affinity", "tag"]]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--allow-partial", action="store_true",
                    help="QC 模式：允许靶标/tag 缺失，输出自动加 _QC_ 前缀，不覆盖正式产物")
    ap.add_argument("--out-prefix", default=None)
    a = ap.parse_args()

    prefix = a.out_prefix or ("_QC_breadth" if a.allow_partial else "P6_breadth")

    # ---------- 载入 ----------
    frames, missing = [], []
    for sym in TARGETS:
        for tg in TAGS:
            t = load_table(sym, tg)
            if t is None:
                missing.append(f"{sym}/{tg}")
            else:
                frames.append(t)
    if missing:
        msg = ("缺产物: " + ", ".join(missing))
        if not a.allow_partial:
            print(f"[STOP] {msg}")
            print("       Tier 2 尚未全齐，拒绝产出正式广度分析（避免用残缺数据得出'最终'结论）。")
            print("       如仅做 QC，请加 --allow-partial。")
            sys.exit(3)
        print(f"[QC] {msg}  —— 允许缺项，结果仅供参考，产物带 {prefix} 前缀")

    sc = pd.concat(frames, ignore_index=True)
    sc = sc.drop_duplicates(["symbol", "chembl_id"], keep="first")

    lig = pd.read_csv(os.path.join(TAB, "P6_ligand_library.csv"))
    lig = lig[lig["pass"] == True].copy()
    lig["chembl_id"] = lig.chembl_id.astype(str)
    sc = sc.merge(lig[["chembl_id", "pref_name", "mw", "logp", "rotb", "pain_prior"]],
                  on="chembl_id", how="left")
    n_all = len(lig)
    print(f"配体库(可用)={n_all}  已对接打分={len(sc)}  靶标={sc.symbol.nunique()}")
    print(f"覆盖组合: {len(sc)}/{n_all * len(TARGETS)} = {100*len(sc)/(n_all*len(TARGETS)):.1f}%")

    have = sorted(sc.symbol.unique())
    t1 = sc[sc.tag == "t1_cns"]
    t2 = sc[sc.tag == "t2_other"]

    # ---------- (1) 配体组成受控的靶标层比较 ----------
    # 【重要 caveat · 2026-09-19 QC 发现】即使配体集合完全相同，**跨靶标的原始亲和力依然
    # 不可直接比较**：Vina 打分随结合口袋体积/埋藏程度单调更负，大口袋天然占便宜。
    # 因此本表用于「组成受控」的稳健性描述 + 排序稳定性检验，**不用来重排靶标**；
    # 体积混淆由下面 target_summary 里的 box_volume / receptor_atoms 两列 + 相关性检验量化。
    rec = pd.read_csv(os.path.join(TAB, "P6_receptors.csv"))
    rec = rec[rec.symbol.isin(TARGETS)].copy()

    def _bv(s):
        try:
            v = [float(x) for x in str(s).strip("[]").split(",")]
            return float(np.prod(v)) if len(v) == 3 else np.nan
        except Exception:
            return np.nan

    rec["box_volume"] = rec.box_size.map(_bv)

    rows = []
    for sym in have:
        s = sc[sc.symbol == sym]
        s_all = s.affinity
        r = rec[rec.symbol == sym]
        def _g(col, _r=r):
            if len(_r) == 0:
                return np.nan
            v = _r[col].iloc[0]
            try:
                return float(v)
            except Exception:
                return np.nan
        rows.append(dict(
            symbol=sym,
            n_scored=len(s),
            n_t1=len(s[s.tag == "t1_cns"]),
            n_t2=len(s[s.tag == "t2_other"]),
            best_affinity=float(s_all.min()),
            p1=float(np.percentile(s_all, 1)),
            median_affinity=float(s_all.median()),
            q1=float(s_all.quantile(.25)),
            q3=float(s_all.quantile(.75)),
            n_le_9=int((s_all <= DEEP).sum()),
            n_le_10=int((s_all <= DEEP2).sum()),
            pdb_id=(r.pdb_id.iloc[0] if len(r) else None),
            box_volume=_g("box_volume"),
            receptor_atoms=_g("receptor_atoms"),
            ref_lig_heavy=_g("ligand_n_heavy"),
        ))
    T = pd.DataFrame(rows).sort_values("median_affinity")
    T["rank_by_median"] = T.median_affinity.rank().astype(int)
    T["rank_by_depth9"] = T["n_le_9"].rank(ascending=False).astype(int)
    T.to_csv(os.path.join(TAB, f"{prefix}_target_summary.csv"), index=False)

    # 体积/尺寸混淆检验：跨靶标原始亲和力到底有多少是"口袋大小"带来的
    vol_conf = {}
    if T.box_volume.notna().sum() >= 4:
        r1, p1v = stats.spearmanr(T.box_volume, T.median_affinity, nan_policy="omit")
        r2, p2v = stats.spearmanr(T.box_volume, T.best_affinity, nan_policy="omit")
        r3, p3v = stats.spearmanr(T.receptor_atoms, T.median_affinity, nan_policy="omit")
        vol_conf = dict(rho_box_vol_vs_median=float(r1), p_box_vol_vs_median=float(p1v),
                        rho_box_vol_vs_best=float(r2), p_box_vol_vs_best=float(p2v),
                        rho_receptor_atoms_vs_median=float(r3), p_receptor_atoms_vs_median=float(p3v),
                        n_targets=int(T.box_volume.notna().sum()))
        json.dump(vol_conf, open(os.path.join(TAB, f"{prefix}_pocket_volume_confound.json"), "w"),
                  indent=2)
        print(f"口袋体积混淆: ρ(box体积, 中位亲和力)={r1:.3f} (p={p1v:.3g}); "
              f"ρ(box体积, 最佳亲和力)={r2:.3f} (p={p2v:.3g})")

    # 配对检验：各靶标 vs ADRA2A（只在共有配体上）
    paired = []
    if "ADRA2A" in have:
        a2 = sc[sc.symbol == "ADRA2A"].set_index("chembl_id").affinity
        for sym in have:
            if sym == "ADRA2A":
                continue
            o = sc[sc.symbol == sym].set_index("chembl_id").affinity
            common = a2.index.intersection(o.index)
            if len(common) < 20:
                paired.append(dict(symbol=sym, n_paired=len(common), median_diff=np.nan, p_wilcoxon=np.nan))
                continue
            da, dO = a2.loc[common].to_numpy(), o.loc[common].to_numpy()
            # 越负越好 → diff = 靶标 − ADRA2A；diff>0 表示 ADRA2A 更强
            diff = dO - da
            try:
                w = stats.wilcoxon(da, dO, zero_method="wilcox", alternative="two-sided")
                p = float(w.pvalue)
            except Exception:
                p = np.nan
            paired.append(dict(symbol=sym, n_paired=len(common),
                               median_affinity_this=float(np.median(dO)),
                               median_affinity_adra2a=float(np.median(da)),
                               median_diff_this_minus_adra2a=float(np.median(diff)),
                               p_wilcoxon=p))
    P = pd.DataFrame(paired)
    if len(P):
        P.to_csv(os.path.join(TAB, f"{prefix}_paired_vs_adra2a.csv"), index=False)

    # ---------- (2) 靶标排序稳定性：t1-only vs 全库 ----------
    stab = []
    for sym in have:
        s = sc[sc.symbol == sym]
        s1 = s[s.tag == "t1_cns"].affinity
        if len(s1) < 20:
            continue
        stab.append(dict(symbol=sym,
                         median_t1=float(s1.median()),
                         median_full=float(s.affinity.median()),
                         delta=float(s.affinity.median() - s1.median())))
    RS = pd.DataFrame(stab)
    rho = pval = np.nan
    if len(RS) >= 4:
        rho, pval = stats.spearmanr(RS.median_t1, RS.median_full)
        rho, pval = float(rho), float(pval)
        RS["rank_t1"] = RS.median_t1.rank().astype(int)
        RS["rank_full"] = RS.median_full.rank().astype(int)
        RS["rank_shift"] = RS.rank_t1 - RS.rank_full
    RS.to_csv(os.path.join(TAB, f"{prefix}_target_rank_stability.csv"), index=False)

    # ---------- (3) ChEMBL 富集功效：t1-only vs 全库 ----------
    rcp_fp = os.path.join(TAB, "P6_reverse_control_positives.csv")
    power_rows = []
    if os.path.exists(rcp_fp):
        RCP = pd.read_csv(rcp_fp)
        RCP["chembl_id"] = RCP.chembl_id.astype(str)
        for sym in have:
            for label, sub in (("t1_only", sc[(sc.symbol == sym) & (sc.tag == "t1_cns")]),
                               ("full_library", sc[sc.symbol == sym])):
                pos_ids = set(RCP[RCP.symbol.str.upper() == sym].chembl_id)
                is_pos = sub.chembl_id.isin(pos_ids).to_numpy()
                npos = int(is_pos.sum())
                neg_all = -sub.affinity
                pos_v, neg_v = neg_all[is_pos], neg_all[~is_pos]
                a_ = S.auc_from_pos_neg(pos_v, neg_v) if npos >= MIN_ACT else np.nan
                # 显著性：用与 mw_confounder **同一个** 单侧 Mann-Whitney p（裁决函数的输入口径）；
                # Hanley–McNeil 双侧 p 另存一列备查（两者量纲不同，不可混用于裁决）。
                p_mwu = S.auc_p(pos_v, neg_v) if npos >= MIN_ACT else np.nan
                p_hn = auc_p(pos_v, neg_v) if npos >= MIN_ACT else np.nan
                aa, amw, a_dock, slope = S.mw_adjust_auc(sub.affinity, sub.mw, is_pos)
                # 【判据修正 2026-09-19】旧写法要求 `aa > amw`（校正后 AUC > 仅 MW 基线）——
                # 口径错配：校正后 AUC 是"残差"的判别力，仅 MW 基线是"原始尺寸"的判别力，
                # 二者不可直接比大小。扣掉尺寸必然带走尺寸贡献的判别力，故该条件会**系统性
                # 冤枉**所有阳性天然偏大的靶标。正确比对是同口径的"对接原始 AUC vs 仅 MW 原始 AUC"，
                # 并补上显著性要求 —— 见 p6_stats.enrichment_verdict()。
                verdict, reason = S.enrichment_verdict(npos, a_dock, amw, aa, p_mwu)
                power_rows.append(dict(symbol=sym, set=label, n_ligands=len(sub), n_actives=npos,
                                       auc=a_, p_auc_mwu_onesided=p_mwu, p_auc_hn_twosided=p_hn,
                                       auc_dock_recomputed=a_dock,
                                       auc_mw_adjusted=aa, auc_size_only=amw,
                                       mw_slope_on_neg_affinity=slope,
                                       mw_control_verdict=verdict, verdict_reason=reason))
    PW = pd.DataFrame(power_rows)
    if len(PW):
        PW.to_csv(os.path.join(TAB, f"{prefix}_chembl_power.csv"), index=False)

    # ---------- (4) 图 ----------
    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
        os.makedirs(FIG, exist_ok=True)
        order = list(T.sort_values("median_affinity").symbol)
        fig, ax = plt.subplots(1, 2, figsize=(13.5, 5.4))
        data = [sc[sc.symbol == s].affinity.to_numpy() for s in order]
        bp = ax[0].boxplot(data, orientation="horizontal", tick_labels=order,
                           showfliers=False, patch_artist=True, widths=.62)
        for b in bp["boxes"]:
            b.set_facecolor("#cfe0f5"); b.set_edgecolor("#33608f")
        for i, s in enumerate(order, start=1):
            v = sc[sc.symbol == s].affinity.min()
            ax[0].plot(v, i, "o", color="#c0392b", ms=4, zorder=5)
        ax[0].axvline(DEEP, ls="--", lw=1, color="#7f8c8d")
        ax[0].axvline(DEEP2, ls=":", lw=1, color="#7f8c8d")
        ax[0].set_xlabel("Vina affinity (kcal/mol, more negative = better)")
        ax[0].set_title("Per-target affinity distribution\n(identical 3,085-ligand set → composition-controlled)")
        ax[0].grid(alpha=.25, axis="x")
        if len(RS) >= 4:
            ax[1].scatter(RS.median_t1, RS.median_full, s=46, color="#2c7fb8", zorder=3)
            for _, r in RS.iterrows():
                ax[1].annotate(r.symbol, (r.median_t1, r.median_full),
                               textcoords="offset points", xytext=(4, 3), fontsize=8)
            lo = min(RS.median_t1.min(), RS.median_full.min()) - .2
            hi = max(RS.median_t1.max(), RS.median_full.max()) + .2
            ax[1].plot([lo, hi], [lo, hi], ls="--", lw=1, color="#95a5a6")
            ax[1].set_xlabel("median affinity — Tier 1 only (620 CNS-prioritised)")
            ax[1].set_ylabel("median affinity — full library (3,085)")
            ax[1].set_title(f"Target ranking stability\nSpearman ρ = {rho:.3f} (p = {pval:.3g})")
            ax[1].grid(alpha=.25)
        fig.suptitle("P6 breadth analysis — full approved-drug library (3,085 ligands × 10 targets)",
                     fontsize=12)
        fig.tight_layout(rect=[0, 0, 1, .95])
        fig.savefig(os.path.join(FIG, f"{prefix}_breadth.png"), dpi=190)
        plt.close(fig)
        print(f"图已出: results/figures/{prefix}_breadth.png")
    except Exception as e:
        print(f"[warn] 出图失败: {e}")

    # ---------- (5) 人读摘要 ----------
    top = T.iloc[0]
    L = []
    L.append(f"# P6 全库广度分析（{prefix}）\n")
    L.append(f"配体库 = {n_all}（Tier1 620 + Tier2 {n_all-620}）；已打分 {len(sc)} 行；"
             f"覆盖 {100*len(sc)/(n_all*len(TARGETS)):.1f}% 的 靶标×配体 组合。\n")
    L.append("## 1. 靶标层（配体组成受控）")
    L.append("10 个靶标面对的是**完全相同的配体集合**，因此下列差异不含配体组成效应。\n")
    L.append(T.to_markdown(index=False, floatfmt=".2f"))
    L.append(f"\n- 最佳中位数亲和力靶标：**{top.symbol}**（{top.median_affinity:.2f} kcal/mol）")
    L.append(f"- ≤ −9 kcal/mol 深度计数最高：**{T.sort_values('n_le_9', ascending=False).iloc[0].symbol}**")
    if vol_conf:
        L.append("\n### 1b. 口袋体积混淆（**决定能否跨靶标比较原始亲和力**）")
        L.append(f"- ρ(对接盒体积, 中位亲和力) = **{vol_conf['rho_box_vol_vs_median']:.3f}** "
                 f"(p = {vol_conf['p_box_vol_vs_median']:.3g})")
        L.append(f"- ρ(对接盒体积, 最佳亲和力) = **{vol_conf['rho_box_vol_vs_best']:.3f}** "
                 f"(p = {vol_conf['p_box_vol_vs_best']:.3g})")
        L.append(f"- ρ(受体原子数, 中位亲和力) = {vol_conf['rho_receptor_atoms_vs_median']:.3f} "
                 f"(p = {vol_conf['p_receptor_atoms_vs_median']:.3g})")
        if vol_conf["rho_box_vol_vs_median"] < -0.4:
            L.append("\n→ 体积越大的口袋亲和力系统性更负：**跨靶标的原始亲和力不可直接比较**，"
                     "靶标优先级仍以「靶标内百分位 + 成药性先验」的四维综合分为准（§3.3）。")
        else:
            L.append("\n→ 未发现强体积-亲和力关联，但跨靶标原始亲和力仍不宜单独作为靶标排序依据。")
    if len(P):
        sig = P[(P.p_wilcoxon < 0.05)]
        L.append(f"\n## 2. 各靶标 vs ADRA2A 配对 Wilcoxon（仅共有配体）")
        L.append(P.to_markdown(index=False, floatfmt=".3g"))
        L.append(f"\n- 与 ADRA2A 达到 p<0.05 的靶标数：{len(sig)}/{len(P)}"
                 "（配对检验消除了配体组成效应，但**未**消除口袋体积效应，只作描述）")
    L.append(f"\n## 3. 靶标排序稳定性（Tier1-only vs 全库）")
    L.append(f"Spearman ρ = **{rho:.3f}**（p = {pval:.3g}，n={len(RS)} 靶标）")
    if len(RS):
        L.append(RS.to_markdown(index=False, floatfmt=".3f"))
    if len(PW):
        L.append("\n## 4. ChEMBL 结合型标签的富集功效（t1-only vs 全库）")
        L.append("判据 `mw_control_verdict`（**唯一规范判据**，实现在 `p6_stats.enrichment_verdict`，"
                 "与 §7.1 MW 混淆检验共用同一函数）：1) 仅分子量基线的**原始** AUC ≥ 对接**原始** AUC "
                 "→ `FAIL_size_only_matches`（一行式尺寸启发式就够好）；2) 对接 AUC 的单侧 "
                 "Mann-Whitney p ≥ 0.05 → `NS_not_significant`（只能说趋势）；3) 扣掉尺寸趋势后的"
                 "残差 AUC > 0.5 → `PASS_size_independent`，否则 `WEAK_residual_below_chance`。\n")
        L.append(PW.to_markdown(index=False, floatfmt=".4f"))
        fw = PW[PW.set == "full_library"]
        n_ok = int((fw.mw_control_verdict == "PASS_size_independent").sum())
        L.append(f"\n- 全库口径下达到最少阳性数（≥{MIN_ACT}）的靶标："
                 f"{int((fw.n_actives >= MIN_ACT).sum())} 个；其中**通过尺寸控制且显著**：{n_ok} 个"
                 f"（{', '.join(fw[fw.mw_control_verdict == 'PASS_size_independent'].symbol) or '无'}）")
        L.append("- 每个靶标未通过的具体理由见 `verdict_reason` 列（逐条给出，不吞掉失败原因）。")
    L.append("\n## Caveats（随结论一并携带）")
    L.append("- 广度提升的是**配体组成受控性**与**富集检验功效**，不解决对接本身的分辨率上限"
             "（exh1 的 ρ≈0.78 保真度天花板仍适用，结论限定为候选优先级而非精确排序）。")
    L.append("- 跨靶标原始亲和力仍受**口袋体积**混淆，故靶标优先级以四维综合分为准，不以原始打分排名。")
    L.append("- 单一晶体构象、无诱导契合与膜环境；所有候选仍为假说，需湿实验验证。")
    L.append("- 富集标签一律为 ChEMBL 结合型（pChEMBL≥6），未掺入注释/适应症型标签。")
    L.append(f"- 若产出于 QC 模式（前缀 {prefix}），缺项已在表内体现，不得作为最终数字引用。")
    open(os.path.join(RES, f"{prefix}_note.md"), "w", encoding="utf-8").write("\n".join(L))
    print(f"摘要已写: results/{prefix}_note.md")
    print(f"\n靶标中位数排序（越负越好）:\n{T[['symbol','median_affinity','best_affinity','n_le_9']].to_string(index=False)}")
    print(f"排序稳定性 Spearman ρ = {rho:.3f} (p={pval:.3g})")
    if len(PW):
        sub = PW[PW.set == "full_library"][["symbol", "n_actives", "auc", "p_auc_mwu_onesided",
                                           "auc_mw_adjusted", "auc_size_only", "mw_control_verdict"]]
        print(f"\n全库富集（达到最少阳性数者）:\n{sub.dropna(subset=['n_actives']).to_string(index=False)}")


if __name__ == "__main__":
    main()
