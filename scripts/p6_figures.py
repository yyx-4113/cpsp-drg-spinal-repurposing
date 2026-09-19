#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
p6_figures.py -- P6 结果可视化

产出（results/figures/）：
  P6_ligand_funnel.png          配体库漏斗（含盐形式修复前后对比）
  P6_target_decisions.png       靶标可成药性决策分布
  P6_param_fidelity.png         **参数保真度权衡**（ρ vs 加速比，方法学核心图）
  P6_reverse_control.png        反向阳性对照逐靶标 AUC
  P6_ranking_drugs.png          Top 药物四维评分
  P6_target_drug_matrix.png     靶标 × Top 药物 结合能热图

图内标签用英文（学术图惯例，且规避中文字体缺失）。
用法：python p6_figures.py
"""
import os, json, glob
import numpy as np, pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap

ROOT = "D:/2026.9/极速交付9月会员日优惠套路/01_AI生信-虚拟多重筛药/慢性疼痛"
TAB = os.path.join(ROOT, "results/tables")
FIG = os.path.join(ROOT, "results/figures")
os.makedirs(FIG, exist_ok=True)
plt.rcParams.update({"font.size": 9, "axes.spines.top": False, "axes.spines.right": False,
                     "figure.dpi": 150, "savefig.bbox": "tight"})
# 需要红色 = 更强结合（中式惯例：数值越负越好，图上用暖色表示更强）
CMAP = LinearSegmentedColormap.from_list("aff", ["#c0392b", "#f5b041", "#f9f9f9", "#5dade2", "#2874a6"])


def save(fig, name):
    p = os.path.join(FIG, name)
    fig.savefig(p, dpi=150)
    plt.close(fig)
    print(f"  -> {name}")


def fig_funnel():
    fp = os.path.join(TAB, "P6_ligand_funnel.json")
    if not os.path.exists(fp):
        return
    f = json.load(open(fp, encoding="utf-8"))
    stages = [("ChEMBL\nmax_phase=4", f.get("chembl_max_phase4_total", 0)),
              ("with SMILES", f.get("with_smiles", 0)),
              ("small molecule", f.get("small_molecule", 0)),
              ("PDBQT ready", f.get("pdbqt_ok", 0))]
    fig, ax = plt.subplots(figsize=(6.4, 3.4))
    names = [s[0] for s in stages]
    vals = [s[1] for s in stages]
    bars = ax.bar(names, vals, color=["#5d6d7e", "#7f8c8d", "#95a5a6", "#c0392b"], width=0.62)
    for b, v in zip(bars, vals):
        ax.text(b.get_x() + b.get_width() / 2, v + max(vals) * 0.015, f"{v:,}",
                ha="center", fontsize=9, fontweight="bold")
    ax.set_ylabel("Approved drugs (n)")
    ax.set_title("P6 ligand library funnel\n(ChEMBL max_phase=4, approved-drug equivalent of DrugBank)")
    ax.set_ylim(0, max(vals) * 1.16)
    # 注解盐形式修复
    if f.get("pdbqt_ok"):
        ax.annotate("salt-form fix\n(LargestFragmentChooser)\n+1,045 ligands",
                    xy=(3, vals[-1]), xytext=(2.15, max(vals) * 0.55),
                    fontsize=8, color="#c0392b",
                    arrowprops=dict(arrowstyle="->", color="#c0392b", lw=1.2))
    save(fig, "P6_ligand_funnel.png")


def fig_decisions():
    fp = os.path.join(TAB, "P6_target_selection.csv")
    if not os.path.exists(fp):
        return
    T = pd.read_csv(fp)
    cnt = T.decision.value_counts()
    dock = T[T.decision == "DOCK"]
    rp = os.path.join(TAB, "P6_receptors.csv")
    n_ok = 0
    if os.path.exists(rp):
        R = pd.read_csv(rp)
        n_ok = int((R.status == "OK").sum()) if "status" in R.columns else 0
    fig, axes = plt.subplots(1, 2, figsize=(9.2, 3.6), gridspec_kw={"width_ratios": [1, 1.25]})
    ax = axes[0]
    order = [d for d in ["DOCK", "HOLD_AF2", "HOLD_APO", "EXCLUDE"] if d in cnt.index]
    colors = {"DOCK": "#c0392b", "HOLD_AF2": "#f5b041", "HOLD_APO": "#85c1e9", "EXCLUDE": "#aab7b8"}
    bars = ax.barh(order[::-1], [cnt[d] for d in order[::-1]],
                   color=[colors[d] for d in order[::-1]])
    for b, d in zip(bars, order[::-1]):
        ax.text(b.get_width() + 0.25, b.get_y() + b.get_height() / 2, str(cnt[d]),
                va="center", fontsize=9, fontweight="bold")
    ax.set_xlabel("candidate targets (n)")
    ax.set_title(f"Target druggability\n({len(T)} candidates = 35 hub + 8 prioritised)")
    ax.set_xlim(0, max(cnt.values) * 1.25)
    ax.text(0.98, 0.06, f"receptor-ready: {n_ok}", transform=ax.transAxes, ha="right",
            fontsize=8.5, color="#c0392b", fontweight="bold")

    ax = axes[1]
    if n_ok:
        R = pd.read_csv(rp)
        R = R[R.status == "OK"].copy()
        R["res"] = pd.to_numeric(R.get("pdb_resolution"), errors="coerce")
        y = np.arange(len(R))[::-1]
        ax.barh(y, R.receptor_atoms.astype(float) / 1000.0, color="#c0392b", alpha=0.78)
        labs = [f"{s}  {p}" for s, p in zip(R.symbol, R.pdb_id)]
        ax.set_yticks(y)
        ax.set_yticklabels(labs, fontsize=8)
        ax.set_xlabel("receptor atoms (thousand)")
        ax.set_title("Docking-ready targets\n(box defined by co-crystal ligand)")
        for yy, (_, r) in zip(y, R.iterrows()):
            ax.text(r.receptor_atoms / 1000.0 + 0.06, yy, f"{r.ligand_ref}",
                    va="center", fontsize=7.5, color="#34495e")
    save(fig, "P6_target_decisions.png")


def fig_param_fidelity():
    """方法学核心图：不同 Vina 参数设置的 保真度-速度 权衡。"""
    rows = []
    fp1 = os.path.join(TAB, "P6_stage1_param_validation.json")
    fp2 = os.path.join(TAB, "P6_exh_validation.json")
    if os.path.exists(fp1):
        j = json.load(open(fp1, encoding="utf-8"))
        for k, v in j.items():
            rows.append({"label": f"exh2 + max_evals {v['config']['me']}",
                         "spearman": v["spearman"], "speedup": v["speedup"],
                         "kind": "max_evals-limited"})
    if os.path.exists(fp2):
        j = json.load(open(fp2, encoding="utf-8"))
        for k, v in j.items():
            rows.append({"label": f"exh{k[-1]} (no max_evals)",
                         "spearman": v["spearman"],
                         "speedup": float(j.get("exh4", {}).get("mean_sec", np.nan) or np.nan),
                         "kind": "exhaustiveness-reduced"})
    if not rows:
        return
    D = pd.DataFrame(rows)
    # exh 组的 speedup 需自行算：用默认 exh4 的 32.7s / 实测
    fp3 = os.path.join(TAB, "P6_exh_validation.csv")
    if os.path.exists(fp3):
        E = pd.read_csv(fp3)
        for exh in (1, 2):
            c = f"exh{exh}_sec"
            if c in E.columns and E[c].mean() > 0:
                m = D.label == f"exh{exh} (no max_evals)"
                D.loc[m, "speedup"] = 32.73 / E[c].mean()
    D = D.dropna(subset=["spearman", "speedup"])

    fig, ax = plt.subplots(figsize=(6.6, 4.0))
    mk = {"max_evals-limited": ("o", "#c0392b"), "exhaustiveness-reduced": ("s", "#2471a3")}
    for kind, g in D.groupby("kind"):
        m, c = mk.get(kind, ("o", "#555"))
        ax.scatter(g.speedup, g.spearman, s=95, marker=m, color=c, zorder=3, label=kind)
        for _, r in g.iterrows():
            ax.annotate(r.label, (r.speedup, r.spearman), textcoords="offset points",
                        xytext=(7, 5), fontsize=8, color=c)
    ax.axhline(0, color="#7f8c8d", lw=0.9, ls="--")
    ax.axhspan(-0.3, 0.3, color="#fadbd8", alpha=0.45, zorder=0)
    ax.text(1.05, -0.24, "ranking unreliable (|ρ|<0.3)", fontsize=8, color="#c0392b")
    ax.set_xlabel("speed-up vs default setting (×)")
    ax.set_ylabel("Spearman ρ vs gold standard")
    ax.set_title("P6 parameter fidelity: why NOT to cap --max_evals\n"
                 "(gold standard = exhaustive search, ~44 s/ligand)")
    ax.set_xscale("log")
    ax.legend(frameon=False, fontsize=8, loc="lower left")
    ax.set_ylim(-0.45, 1.05)
    save(fig, "P6_param_fidelity.png")


def fig_reverse_control():
    fp = os.path.join(TAB, "P6_reverse_control.csv")
    if not os.path.exists(fp):
        return
    R = pd.read_csv(fp).dropna(subset=["auc_known_vs_rest"])
    if R.empty:
        return
    R = R.sort_values("auc_known_vs_rest", ascending=True)
    fig, ax = plt.subplots(figsize=(6.6, max(3.0, 0.34 * len(R) + 1.4)))
    cols = ["#c0392b" if a >= 0.60 else "#aab7b8" for a in R.auc_known_vs_rest]
    y = np.arange(len(R))
    ax.barh(y, R.auc_known_vs_rest, color=cols)
    ax.set_yticks(y)
    ax.set_yticklabels([f"{s} (n={int(n)})" for s, n in zip(R.symbol, R.n_known_pairs)], fontsize=8)
    ax.axvline(0.5, color="#7f8c8d", ls="--", lw=1)
    ax.axvline(0.6, color="#c0392b", ls=":", lw=1)
    ax.text(0.605, len(R) - 0.4, "reliability\nthreshold 0.60", fontsize=7.5, color="#c0392b")
    ax.set_xlabel("AUC (known analgesic ligands vs all other ligands)")
    ax.set_title("P6 reverse positive control\n(per-target discriminative power of the docking score)")
    ax.set_xlim(0, 1)
    save(fig, "P6_reverse_control.png")


def fig_ranking():
    fp = os.path.join(TAB, "P6_ranking_drugs.csv")
    if not os.path.exists(fp):
        return
    D = pd.read_csv(fp).head(20).iloc[::-1]
    if D.empty:
        return
    fig, ax = plt.subplots(figsize=(7.4, 0.34 * len(D) + 1.8))
    y = np.arange(len(D))
    dims = [("D1_affinity", "D1 affinity", "#c0392b"), ("D2_pharm_prior", "D2 pharmacology", "#e67e22"),
            ("D3_accessibility", "D3 accessibility", "#2471a3"), ("D4_reliability", "D4 reliability", "#7d3c98")]
    W = {"D1_affinity": 0.40, "D2_pharm_prior": 0.25, "D3_accessibility": 0.20, "D4_reliability": 0.15}
    left = np.zeros(len(D))
    for col, lab, c in dims:
        if col not in D.columns:
            continue
        v = pd.to_numeric(D[col], errors="coerce").fillna(0).values
        ax.barh(y, v, left=left, color=c, label=lab, height=0.66)
        left += v
    ax.set_yticks(y)
    lbl = [f"{n}" + (" ★" if p else "") for n, p in
           zip(D.pref_name.astype(str).str.slice(0, 26), D.get("pain_prior", pd.Series([False] * len(D))).fillna(False))]
    ax.set_yticklabels(lbl, fontsize=8)
    ax.set_xlabel("composite score (0.40·D1 + 0.25·D2 + 0.20·D3 + 0.15·D4)")
    ax.set_title("P6 top repurposing candidates (★ = known analgesic in library)")
    ax.legend(frameon=False, fontsize=7.5, ncol=4, loc="lower right")
    save(fig, "P6_ranking_drugs.png")


def fig_matrix():
    fp = os.path.join(TAB, "P6_ranking_pairs.csv")
    if not os.path.exists(fp):
        return
    P = pd.read_csv(fp)
    if P.empty or "pct_in_target" not in P.columns:
        return
    tops = (P.groupby("chembl_id").composite.max().sort_values(ascending=False).head(18).index
            if "composite" in P.columns else P.chembl_id.unique()[:18])
    S = P[P.chembl_id.isin(tops)]
    M = S.pivot_table(index="pref_name", columns="symbol", values="affinity", aggfunc="min")
    M = M.dropna(how="all").dropna(axis=1, how="all")
    if M.empty:
        return
    fig, ax = plt.subplots(figsize=(1.1 * M.shape[1] + 3.0, 0.32 * M.shape[0] + 2.0))
    im = ax.imshow(M.values, cmap=CMAP, aspect="auto", vmin=np.nanpercentile(M.values, 5),
                   vmax=np.nanpercentile(M.values, 95))
    ax.set_xticks(range(M.shape[1]))
    ax.set_xticklabels(M.columns, rotation=55, ha="right", fontsize=8)
    ax.set_yticks(range(M.shape[0]))
    ax.set_yticklabels([str(x)[:24] for x in M.index], fontsize=7.5)
    cb = fig.colorbar(im, ax=ax, shrink=0.7)
    cb.set_label("best Vina affinity (kcal/mol; more negative = stronger)", fontsize=8)
    ax.set_title("P6 target × top-candidate binding affinity")
    save(fig, "P6_target_drug_matrix.png")


def main():
    print("生成 P6 图件 -> results/figures/")
    for fn in (fig_funnel, fig_decisions, fig_param_fidelity, fig_reverse_control,
               fig_ranking, fig_matrix):
        try:
            fn()
        except Exception as e:
            import traceback
            print(f"  !! {fn.__name__} 失败: {type(e).__name__}: {e}")
            traceback.print_exc()


if __name__ == "__main__":
    main()
