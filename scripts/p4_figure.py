#!/usr/bin/env python3
# p4_figure.py -- P4 human miRNA layer figure
import os, json
import numpy as np, pandas as pd
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt

ROOT="D:/2026.9/极速交付9月会员日优惠套路/01_AI生信-虚拟多重筛药/慢性疼痛"
TAB=os.path.join(ROOT,"results/tables"); FIG=os.path.join(ROOT,"results/figures")

intab=pd.read_csv(os.path.join(TAB,"P4_hub_miRNA_human_integration.csv"))
det=json.load(open(os.path.join(TAB,"P4_GSE222979_detection.json")))
sl=json.load(open(os.path.join(TAB,"P4_setlevel_test.json")))
assoc=pd.read_csv(os.path.join(TAB,"P4_GSE158825_miRNA_painoutcome_spearman.csv"))

fig=plt.figure(figsize=(14,5.6),facecolor="white")
gs=fig.add_gridspec(1,3,width_ratios=[1.5,1,1],wspace=0.32)

# A: volcano of hub-targeting miRNAs vs pain outcome
ax=fig.add_subplot(gs[0,0])
x=intab["rho_pain"]; y=-np.log10(intab["p_pain"].clip(1e-6,1))
ax.scatter(x,y,s=14,color="#2980b9",alpha=.55)
top=intab.nsmallest(8,"p_pain")
ax.scatter(top["rho_pain"],-np.log10(top["p_pain"].clip(1e-6,1)),s=30,color="#c0392b")
for r in top.itertuples():
    ax.annotate(r.miRNA,(r.rho_pain,-np.log10(max(r.p_pain,1e-6))),fontsize=6,xytext=(3,2),textcoords="offset points")
ax.axhline(-np.log10(0.05),ls="--",color="#7f8c8d",lw=1)
ax.set_xlabel("Spearman rho with %NPRS pain change",fontsize=9)
ax.set_ylabel("-log10 p",fontsize=9)
ax.set_title(f"Hub-targeting miRNAs vs pain outcome\n(n={len(intab)} detected in plasma; nominal p, none FDR<0.05)",fontsize=11)

# B: detection across biofluids
ax2=fig.add_subplot(gs[0,1])
labels=["plasma\n(GSE158825)","plasma\n(GSE222979)","synovial\nfluid","urine"]
vals=[253]+[det.get(k,0) for k in ["plasma","synovial","urine"]]
b=ax2.bar(range(len(vals)),vals,color=["#c0392b","#2980b9","#27ae60","#8e44ad"])
ax2.bar_label(b,fontsize=8)
ax2.set_xticks(range(len(labels))); ax2.set_xticklabels(labels,fontsize=8)
ax2.set_ylabel("# hub-targeting miRNAs detected",fontsize=9)
ax2.set_title("Detection of 608 hub-targeting miRNAs\nacross human biofluids",fontsize=11)

# C: set-level test (REAL permutation null)
ax3=fig.add_subplot(gs[0,2])
rng=np.random.default_rng(42)
allrho=assoc["rho"].dropna().values
n=sl["n"]; null=np.array([np.mean(rng.choice(allrho,n,replace=False)) for _ in range(5000)])
ax3.hist(null,bins=40,color="#95a5a6",alpha=.7)
ax3.axvline(sl["mean_rho"],color="#c0392b",lw=2.5)
ax3.text(sl["mean_rho"],ax3.get_ylim()[1]*0.9,f" obs={sl['mean_rho']:.3f}\n nominal t-p={sl['t_p']:.3f}\n permutation p={sl['perm_p']:.2f}",
         fontsize=8,color="#c0392b",ha="left")
ax3.set_xlabel("mean rho (null distribution)",fontsize=9); ax3.set_yticks([])
ax3.set_title("Set-level test: NOT robust\n(permutation p≈0.5)",fontsize=11)
plt.savefig(os.path.join(FIG,"P4_human_miRNA_layer.png"),dpi=160,bbox_inches="tight")
print("saved ->",os.path.join(FIG,"P4_human_miRNA_layer.png"))
