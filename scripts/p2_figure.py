#!/usr/bin/env python3
# p2_figure.py -- heatmap of core DRG-axis meta signature (log2FC across datasets) + DEG counts panel
import os
import numpy as np, pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

ROOT="D:/2026.9/极速交付9月会员日优惠套路/01_AI生信-虚拟多重筛药/慢性疼痛"
TAB=os.path.join(ROOT,"results/tables")
FIG=os.path.join(ROOT,"results/figures"); os.makedirs(FIG,exist_ok=True)

meta=pd.read_csv(os.path.join(TAB,"META_DRG_axis_stouffer.csv"))
lfc_cols={
 "lfc_GSE267799_SMIR_DRG":"LPI (incision)\nrat DRG chronic",
 "lfc_GSE212311_CCI_DRG":"CCI\nrat DRG",
 "lfc_GSE278227_CCI_DRG":"CCI 1W\nrat DRG IL/CL",
 "lfc_GSE241361_S1R_DRG":"SNI\nmouse DRG WT",
 "lfc_GSE265957_Xtail_DRG_Day4":"SNI d4\nmouse DRG",
 "lfc_GSE265957_Xtail_DRG_Day63":"SNI d63\nmouse DRG",
}
core=meta[(meta["meta_FDR"]<0.05)&(meta["consistency"]>=0.8)].sort_values("meta_p")
top=core.head(35).copy()
mat=top[list(lfc_cols)].astype(float)
mat.columns=list(lfc_cols.values())
mat.index=top["symbol"].values

# ---- figure ----
fig=plt.figure(figsize=(13,12),facecolor="white")
gs=fig.add_gridspec(2,1,height_ratios=[3.2,1.0],hspace=0.28)

ax=fig.add_subplot(gs[0,0])
vmax=np.nanpercentile(np.abs(mat.values),97)
im=ax.imshow(mat.values,aspect="auto",cmap="RdBu_r",vmin=-vmax,vmax=vmax)
ax.set_xticks(range(mat.shape[1])); ax.set_xticklabels(mat.columns,fontsize=9)
ax.set_yticks(range(mat.shape[0])); ax.set_yticklabels(mat.index,fontsize=9)
ax.set_title("Core DRG-axis pain signature (Stouffer meta, FDR<0.05 & consistency>=0.8)\nlog2 fold-change per dataset",
             fontsize=13,pad=12)
cb=fig.colorbar(im,ax=ax,fraction=0.03,pad=0.02); cb.set_label("log2FC",fontsize=9)
for i in range(mat.shape[0]):
    for j in range(mat.shape[1]):
        v=mat.values[i,j]
        if np.isnan(v): ax.text(j,i,"na",ha="center",va="center",fontsize=6,color="#999")
# annotate meta stats on right
for i,sym in enumerate(mat.index):
    z=top["meta_Z"].values[i]
    ax.text(mat.shape[1]-0.35,i,f"Z={z:.1f}",va="center",ha="left",fontsize=7,color="#333")
ax.set_xlim(-0.5,mat.shape[1]-0.15)

# panel B: DEG counts per dataset
ax2=fig.add_subplot(gs[1,0])
counts={
 "LPI rat DRG\n(chronic vs base)":(0,0),
 "CCI rat DRG\n(3 vs 3)":(0,0),
 "CCI rat DRG\n1W IL vs CL":(5565,3538),
 "SNI mouse DRG\n(S1R WT)":(23,0),
 "SNI mouse SC\n(S1R WT)":(119,2),
 "Morphine SH-SY5Y\n(in vitro)":(6,4),
}
labels=list(counts.keys()); up=[counts[k][0] for k in labels]; dn=[counts[k][1] for k in labels]
x=np.arange(len(labels))
ax2.bar(x,up,color="#c0392b",label="up (FDR<0.05)")
ax2.bar(x,[-d for d in dn],color="#27ae60",label="down (FDR<0.05)")
ax2.axhline(0,color="#333",lw=0.8)
ax2.set_xticks(x); ax2.set_xticklabels(labels,fontsize=8)
ax2.set_ylabel("# DE genes",fontsize=9)
ax2.set_title("Per-dataset DE genes (Welch t + BH FDR<0.05)",fontsize=11)
ax2.legend(fontsize=8,loc="upper left")
for xi,(u,d) in enumerate(zip(up,dn)):
    ax2.text(xi,u+60,f"{u}",ha="center",fontsize=7,color="#c0392b")
    ax2.text(xi,-d-160,f"{d}",ha="center",fontsize=7,color="#27ae60")
plt.savefig(os.path.join(FIG,"P2_core_signature_heatmap.png"),dpi=160,bbox_inches="tight")
print("saved figure ->", os.path.join(FIG,"P2_core_signature_heatmap.png"))
print("core signature size:",len(core),"top35 shown")
