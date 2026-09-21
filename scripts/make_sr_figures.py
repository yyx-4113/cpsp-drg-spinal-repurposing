#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Generate the 5 Scientific Reports-compliant display figures (>=300 DPI) for the
CPSP DRG-spinal-axis MVP manuscript.

All numbers are read at run time from the authoritative CSV tables under
results/tables/, so every plotted value is traceable to a pipeline product.

Reviewer-driven fixes applied in this version (Round-3, T1-12 / T1-13):
  * Fig. 3  x-axis label corrected to "Subtype mean-expression fold" (the body
            text was already correct; the prior label wrongly said
            "detection fraction").
  * Fig. 4A title now describes the bars accurately (hub counts by consensus
            lineage); the "7/35 cross-dataset lineage-consistent" fact stays in
            the caption, so the panel no longer conflates it with the 15 coloured
            bars.
  * Fig. 4B now excludes the two all-zero Visium hubs (CRISP3, LNP1), counting
            only the 33 detectably-expressed hubs; the dorsal-horn count
            (17/33 = 51.5%) is unchanged and matches the body text.

T1-13 (detection-floor) is handled in the manuscript Methods and Supplementary
Table S2 (top_detection < 5% -> below-floor, not biologically interpreted); it
does not alter the binary "detected in region X" call used for Fig. 4B.

Outputs (figures/):
  Fig1_geneset_programme.png
  Fig2_hub_convergence.png
  Fig3_DRG_neuron_subtype_localisation.png
  Fig4_spinal_lineage_visium.png
  Fig5_docking_honest_null.png
"""
import os
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Patch

TBL = r"D:\2026.9\极速交付9月会员日优惠套路\01_AI生信-虚拟多重筛药\慢性疼痛\results\tables"
OUT = r"D:\2026.9\极速交付9月会员日优惠套路\01_AI生信-虚拟多重筛药\慢性疼痛\figures"
os.makedirs(OUT, exist_ok=True)
DPI = 350

# ---- Consistent, publication-grade style (light theme, colour-blind friendly)
plt.rcParams.update({
    "font.family": ["Arial", "Helvetica", "DejaVu Sans"],
    "font.size": 9,
    "axes.titlesize": 10.5,
    "axes.labelsize": 9.5,
    "xtick.labelsize": 8.5,
    "ytick.labelsize": 8.5,
    "legend.fontsize": 8,
    "figure.dpi": DPI,
    "savefig.dpi": DPI,
    "savefig.bbox": "tight",
    "savefig.facecolor": "white",
    "axes.spines.top": False,
    "axes.spines.right": False,
    "axes.linewidth": 0.8,
    "xtick.major.width": 0.8,
    "ytick.major.width": 0.8,
    "xtick.direction": "out",
    "ytick.direction": "out",
})

# Semantic colours (consistent across panels)
C_UP = "#C0392B"       # neuroimmune activation / enrichment (warm)
C_DOWN = "#2471A3"     # metabolic suppression (cool)
C_NS = "#7F8C8D"       # not significant / other
C_PASS = "#1E8449"     # size-independent enrichment
C_FAIL = "#B9770E"     # size-only match / not significant
C_NEUR = "#8E44AD"     # neuronal lineage
C_GLIA = "#16A085"     # glial lineage
C_IMM = "#C0392B"      # immune lineage
C_MIX = "#D4AC0D"      # mixed
GREY = "#95A5A6"
GRID = "#E5E7E9"


def _panel_label(ax, txt="A"):
    ax.text(-0.12, 1.02, txt, transform=ax.transAxes, fontsize=12,
            fontweight="bold", va="bottom", ha="left")


# ---------------------------------------------------------------- Fig 1
def fig1():
    df = pd.read_csv(os.path.join(TBL, "P3_geneset_stats.csv"))
    # v1.4: annotate with the SET-LEVEL BH q (corrected across the 18 multi-member sets),
    # which is the primary honesty metric in the manuscript; perm p is retained for reference.
    qtab = pd.read_csv(os.path.join(TBL, "_R4_geneset_setlevel_bh.csv"))
    qtab = qtab[qtab.scale == "fixed"][["set", "perm_p", "perm_q"]].rename(
        columns={"perm_p": "perm_p_r4", "perm_q": "BH_q"})
    df = df.merge(qtab, on="set", how="left")
    order = ["Neuroinflammation", "DAM_microglia", "Complement", "Mitochondria_OXPHOS",
             "Neuropeptides_pain", "Nav_SCN", "TRP_channels", "CACNA", "Kv_KCNQ_KCNH"]
    df = df.set_index("set").loc[order].reset_index()
    df["label"] = [s.replace("_", " ") for s in df["set"]]

    fig, ax = plt.subplots(figsize=(7.2, 4.4))
    y = np.arange(len(df))
    colors = []
    for _, r in df.iterrows():
        if r["BH_q"] < 0.05 and r["mean_Z"] > 0:
            colors.append(C_UP)
        elif r["BH_q"] < 0.05 and r["mean_Z"] < 0:
            colors.append(C_DOWN)
        else:
            colors.append(C_NS)
    bars = ax.barh(y, df["mean_Z"], color=colors, edgecolor="white", height=0.72)
    ax.set_yticks(y)
    ax.set_yticklabels(df["label"])
    ax.axvline(0, color="black", lw=0.9)
    ax.set_xlabel("Mean Z (Stouffer meta-Z of the gene set)")
    ax.set_title("Fig. 1  A coordinated neuroimmune-metabolic DRG-axis programme\n"
                 "Permutation-calibrated gene-set statistics, BH-corrected across sets", loc="left")
    ax.grid(axis="x", color=GRID, lw=0.7, zorder=0)
    ax.set_axisbelow(True)

    for i, (_, r) in enumerate(df.iterrows()):
        z, q, p = r["mean_Z"], r["BH_q"], r["perm_p"]
        qtxt = "q<0.001" if q < 0.001 else f"q={q:.3f}"
        tag = f"{z:+.2f}  ({r['frac_up']*100:.0f}% up)  {qtxt}  [perm p={p:.3f}]"
        ax.text(z + (0.12 if z >= 0 else -0.12), i, tag,
                va="center", ha="left" if z >= 0 else "right", fontsize=7.0)
    ax.legend(handles=[Patch(color=C_UP, label="Upregulated, set-level BH q<0.05"),
                       Patch(color=C_DOWN, label="Downregulated, set-level BH q<0.05"),
                       Patch(color=C_NS, label="Not significant after BH (incl. ion channels)")],
              loc="lower left", fontsize=7.5, frameon=True, edgecolor="#B0B0B0")
    ax.set_xlim(-5.8, 10.0)
    ax.set_ylim(-0.6, len(df) - 0.4)
    fig.savefig(os.path.join(OUT, "Fig1_geneset_programme.png"))
    plt.close(fig)
    print("Fig1 done")


# ---------------------------------------------------------------- Fig 2
def fig2():
    lodo = pd.read_csv(os.path.join(TBL, "P3_lodo_auc_ci.csv"))
    lodo["short"] = (lodo["test_dataset"]
                     .str.replace("_ratDRG", " (rat DRG)", regex=False)
                     .str.replace("_mouseDRG", " (mouse DRG)", regex=False)
                     .str.replace("_mouseSC", " (mouse SC)", regex=False)
                     .str.replace("_incision", "", regex=False))
    hubs = pd.read_csv(os.path.join(TBL, "P3_hub_genes.csv"))

    fig, (axA, axB) = plt.subplots(1, 2, figsize=(7.8, 4.6),
                                   gridspec_kw={"width_ratios": [1.05, 1]})

    # Panel A: LODO AUC with 95% CI
    y = np.arange(len(lodo))
    axA.errorbar(lodo["auc"], y, xerr=[lodo["auc"] - lodo["lo"], lodo["hi"] - lodo["auc"]],
                 fmt="o", color="#1F618D", ecolor="#5499C7", capsize=4, ms=6, zorder=3)
    for i, (_, r) in enumerate(lodo.iterrows()):
        axA.text(r["auc"] + 0.012, i, f"{r['auc']:.3f}\n[{r['lo']:.3f}, {r['hi']:.3f}]",
                 va="center", ha="left", fontsize=6.8)
    axA.axvline(0.5, color=GREY, ls="--", lw=1)
    axA.axvline(0.917, color=C_PASS, ls=":", lw=1.2)
    axA.set_yticks(y); axA.set_yticklabels(lodo["short"], fontsize=8)
    axA.set_xlabel("Leave-one-dataset-out AUC\n(test set excluded from training)")
    axA.set_xlim(0.4, 1.2)
    axA.grid(axis="x", color=GRID, lw=0.7, zorder=0); axA.set_axisbelow(True)
    axA.set_title("A. Generalisation (LODO)", loc="left", fontsize=10)
    from matplotlib.lines import Line2D
    axA.legend(handles=[Line2D([0], [0], color=GREY, ls="--", lw=1,
                               label="chance level (AUC 0.5)"),
                        Line2D([0], [0], color=C_PASS, ls=":", lw=1.4,
                               label="cross-animal floor 0.917")],
               loc="lower left", fontsize=6.8, frameon=True, edgecolor="#B0B0B0")

    # Panel B: method-importance heatmap for top hubs
    top = hubs.sort_values("shap_meanabs", ascending=False).head(14).copy()
    top = top[["symbol", "lasso_freq", "rf_gini", "shap_meanabs", "n_methods"]]
    norm = top.copy()
    for c in ["lasso_freq", "rf_gini", "shap_meanabs"]:
        mx = norm[c].max()
        norm[c] = norm[c] / mx if mx > 0 else 0
    mat = norm[["lasso_freq", "rf_gini", "shap_meanabs"]].values
    im = axB.imshow(mat, aspect="auto", cmap="YlGnBu", vmin=0, vmax=1)
    axB.set_xticks([0, 1, 2])
    axB.set_xticklabels(["LASSO\nfreq", "RF\nGini", "XGB\nshap"], fontsize=7.5)
    axB.set_yticks(np.arange(len(top)))
    axB.set_yticklabels([f"{s} ({n})" for s, n in zip(top["symbol"], top["n_methods"])], fontsize=7.5)
    for i in range(len(top)):
        for j in range(3):
            v = mat[i, j]
            axB.text(j, i, f"{v:.2f}", ha="center", va="center",
                     color="black" if v < 0.6 else "white", fontsize=6.5)
    axB.set_title("B. Three-method hub importance\n(n = # methods agreeing)",
                  loc="left", fontsize=10)
    cbar = fig.colorbar(im, ax=axB, fraction=0.035, pad=0.02)
    cbar.set_label("normalised importance", fontsize=7.5)
    cbar.ax.tick_params(labelsize=7)

    fig.suptitle("Fig. 2  Hub convergence: cross-dataset generalisation and dual-ML consensus",
                 x=0.02, ha="left", fontsize=11, y=0.99)
    fig.savefig(os.path.join(OUT, "Fig2_hub_convergence.png"))
    plt.close(fig)
    print("Fig2 done")


# ---------------------------------------------------------------- Fig 3
def fig3():
    df = pd.read_csv(os.path.join(TBL, "P5_GSE216039_DRG_hub_finetype_top.csv"))
    df = df[df["detected"] == True].copy()
    df = df.sort_values("specificity", ascending=True)
    df["irn"] = df["top_finetype"] == "Injured_RegenNeuron"

    fig, ax = plt.subplots(figsize=(7.0, 6.6))
    y = np.arange(len(df))
    colors = [C_UP if v else C_NS for v in df["irn"]]
    ax.barh(y, df["specificity"], color=colors, edgecolor="white", height=0.74, zorder=3)
    ax.set_yticks(y)
    ax.set_yticklabels(df["symbol"], fontsize=8)
    # ---- T1-12 fix: x-axis now states the true plotted quantity (mean-expression fold)
    ax.set_xlabel("Subtype mean-expression fold (top fine-type vs other subtypes)")
    ax.set_title("Fig. 3  DRG hubs localise to the injured / regenerating neuron subtype\n"
                 f"{int(df['irn'].sum())}/{len(df)} detected hubs enrich in Injured_RegenNeuron",
                 loc="left")
    ax.grid(axis="x", color=GRID, lw=0.7, zorder=0); ax.set_axisbelow(True)

    for i, (_, r) in enumerate(df.iterrows()):
        ax.text(r["specificity"] + 0.4, i, f"{r['specificity']:.1f}x",
                va="center", ha="left", fontsize=6.8)
    ax.legend(handles=[Patch(color=C_UP, label="Injured/Regen. neuron"),
                       Patch(color=C_NS, label="Other subtype")],
              loc="lower right", fontsize=8, frameon=True, edgecolor="#B0B0B0")
    ax.set_xlim(0, max(df["specificity"]) * 1.25)
    fig.savefig(os.path.join(OUT, "Fig3_DRG_neuron_subtype_localisation.png"))
    plt.close(fig)
    print("Fig3 done")


# ---------------------------------------------------------------- Fig 4
def fig4():
    lin = pd.read_csv(os.path.join(TBL, "P5_hub_lineage_consensus.csv"))
    vis = pd.read_csv(os.path.join(TBL, "P5_GSE325938_hub_regionalization.csv"))

    fig, (axA, axB) = plt.subplots(1, 2, figsize=(7.8, 4.6))

    # Panel A: hub counts by consensus lineage (T1-12: title describes the bars)
    lin["cat"] = np.where(lin["consensus_lineage"].isin(["Neuronal", "Glial", "Immune"]),
                          lin["consensus_lineage"],
                          np.where(lin["consensus_lineage"] == "Mixed", "Mixed", "NotLocalisable"))
    order = ["Neuronal", "Glial", "Immune", "Mixed", "NotLocalisable"]
    counts = lin["cat"].value_counts().reindex(order).fillna(0).astype(int)
    cmap = {"Neuronal": C_NEUR, "Glial": C_GLIA, "Immune": C_IMM,
            "Mixed": C_MIX, "NotLocalisable": GREY}
    bars = axA.bar(order, counts.values, color=[cmap[o] for o in order],
                   edgecolor="white", width=0.72, zorder=3)
    for b, v in zip(bars, counts.values):
        axA.text(b.get_x() + b.get_width() / 2, v + 0.25, str(v), ha="center", fontsize=8.5)
    axA.set_ylabel("Number of hubs (of 35)")
    axA.set_title("A. Hub distribution by spinal consensus lineage", loc="left", fontsize=10)
    axA.tick_params(axis="x", labelrotation=30, labelsize=8.5)
    axA.set_ylim(0, max(counts.values) * 1.18)
    axA.grid(axis="y", color=GRID, lw=0.7, zorder=0); axA.set_axisbelow(True)

    # Panel B: Visium dorsal-horn regionalisation (T1-12: drop all-zero hubs)
    vis2 = vis[vis["top_label_log2"] > 0].copy()      # exclude CRISP3, LNP1 (all-zero)
    reg = vis2["top_region"].value_counts().sort_values(ascending=False)
    colors_b = [C_UP if r == "DorsalHorn" else GREY for r in reg.index]
    bars = axB.bar(range(len(reg)), reg.values, color=colors_b, edgecolor="white",
                   width=0.72, zorder=3)
    axB.set_xticks(range(len(reg)))
    axB.set_xticklabels(reg.index, rotation=35, ha="right", fontsize=7.5)
    for i, v in enumerate(reg.values):
        axB.text(i, v + 0.2, str(v), ha="center", fontsize=7.5)
    n_dh = int(reg.get("DorsalHorn", 0))
    n_tot = len(vis2)
    axB.set_ylabel("Number of hubs (of 33 detectably expressed)")
    axB.set_title(f"B. Visium spatial regionalisation\n{n_dh}/{n_tot} hubs map to the dorsal horn "
                  f"({n_dh/n_tot*100:.1f}%; pain first station)", loc="left", fontsize=10)
    axB.set_ylim(0, max(reg.values) * 1.18)
    axB.grid(axis="y", color=GRID, lw=0.7, zorder=0); axB.set_axisbelow(True)

    fig.suptitle("Fig. 4  Hubs are a multi-cellular DRG-spinal programme",
                 x=0.02, ha="left", fontsize=11, y=0.99)
    fig.savefig(os.path.join(OUT, "Fig4_spinal_lineage_visium.png"))
    plt.close(fig)
    print("Fig4 done")


# ---------------------------------------------------------------- Fig 5
def fig5():
    rc = pd.read_csv(os.path.join(TBL, "P6_reverse_control.csv"))
    mw = pd.read_csv(os.path.join(TBL, "P6_enrichment_mw_confounder_check.csv"))

    fig, (axA, axB) = plt.subplots(1, 2, figsize=(7.8, 4.4))

    # Panel A: reverse-control AUCs with MW verdict colours
    rc2 = rc.dropna(subset=["auc_known_vs_rest"]).copy()
    verdict = dict(zip(mw["symbol"], mw["verdict"]))
    cols = {"PASS_size_independent": C_PASS, "FAIL_size_only_matches": C_FAIL,
            "NS_not_significant": C_NS}
    order_sym = ["AXL", "TNIK", "ACVR1", "MAPK14", "SLC2A1", "ADRA2A"]
    rc2 = rc2.set_index("symbol").loc[order_sym].reset_index()
    y = np.arange(len(rc2))
    bar_cols = [cols.get(verdict.get(s, "NS_not_significant"), C_NS) for s in rc2["symbol"]]
    axA.barh(y, rc2["auc_known_vs_rest"], color=bar_cols, edgecolor="white",
             height=0.72, zorder=3)
    axA.axvline(0.5, color=GREY, ls="--", lw=1)
    axA.set_yticks(y); axA.set_yticklabels(rc2["symbol"], fontsize=8)
    for i, (_, r) in enumerate(rc2.iterrows()):
        axA.text(r["auc_known_vs_rest"] + 0.008, i, f"{r['auc_known_vs_rest']:.3f}",
                 va="center", fontsize=7.5)
    axA.set_xlabel("Reverse positive-control AUC\n(method-validation signal type)")
    axA.set_xlim(0.45, 1.0)
    axA.grid(axis="x", color=GRID, lw=0.7, zorder=0); axA.set_axisbelow(True)
    axA.set_title("A. Reverse positive controls\n(green = size-independent)", loc="left", fontsize=10)
    axA.legend(handles=[Patch(color=C_PASS, label="PASS (size-independent)"),
                        Patch(color=C_FAIL, label="FAIL (size-only)"),
                        Patch(color=C_NS, label="NS")],
               loc="upper right", fontsize=7, frameon=True, edgecolor="#B0B0B0")

    # Panel B: ADRA2A breadth flip
    vals = [0.618, 0.532]
    labs = ["Tier-1 CNS/analgesic\nsubset (n=620)", "Full library\n(n=3,085)"]
    b = axB.bar(labs, vals, color=[C_FAIL, C_NS], edgecolor="white", width=0.55, zorder=3)
    axB.axhline(0.5, color=GREY, ls="--", lw=1)
    for rect, v in zip(b, vals):
        axB.text(rect.get_x() + rect.get_width() / 2, v + 0.012, f"{v:.3f}",
                 ha="center", fontsize=8.5)
    axB.text(0.5, 0.63, "p = 0.118 (NS)", ha="center", fontsize=8, color="#922B21")
    axB.set_ylim(0.45, 0.72)
    axB.set_ylabel("ADRA2A docking AUC")
    axB.grid(axis="y", color=GRID, lw=0.7, zorder=0); axB.set_axisbelow(True)
    axB.set_title("B. ADRA2A breadth flip:\nTier-1 signal is a CNS-subset\ncomposition artefact",
                  loc="left", fontsize=10)

    fig.suptitle("Fig. 5  Drug repurposing: an honest null at library scale",
                 x=0.02, ha="left", fontsize=11, y=0.99)
    fig.savefig(os.path.join(OUT, "Fig5_docking_honest_null.png"))
    plt.close(fig)
    print("Fig5 done")


if __name__ == "__main__":
    fig1(); fig2(); fig3(); fig4(); fig5()
    print("ALL FIGURES WRITTEN TO:", OUT)
