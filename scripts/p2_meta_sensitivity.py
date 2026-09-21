#!/usr/bin/env python3
# p2_meta_sensitivity.py -- T1-1 sensitivity analysis.
# Reproduce the DRG-axis Stouffer meta two ways and compare the core signature:
#   (A) ORIGINAL (6 inputs: 4 primary datasets + GSE265957 Day4 + GSE265957 Day63, as published)
#   (B) COLLAPSED (5 inputs: 4 primary + GSE265957 merged into ONE study, w=1.0)
# Goal: show the 4,055-gene core is NOT an artefact of counting one study twice.
import os, numpy as np, pandas as pd
from scipy import stats
ROOT="D:/2026.9/极速交付9月会员日优惠套路/01_AI生信-虚拟多重筛药/慢性疼痛"
TAB=os.path.join(ROOT,"results/tables"); OUT=os.path.join(ROOT,"data/processed")

def bh(p):
    p=np.asarray(p,float); ok=~np.isnan(p); idx=np.where(ok)[0]
    q=np.full_like(p,np.nan); pv=p[idx]; m=len(pv)
    order=np.argsort(pv); ranked=pv[order]
    adj=ranked*m/np.arange(1,m+1)
    adj=np.minimum.accumulate(adj[::-1])[::-1]
    q[idx[order]]=np.clip(adj,0,1); return q

def z_from_tp(t,p):
    return np.sign(t)*stats.norm.isf(np.clip(p,1e-300,1)/2)

def load_deg(fn):
    d=pd.read_csv(os.path.join(ROOT,fn), index_col=0).dropna(subset=["t","p"])
    d["Z"]=z_from_tp(d["t"],d["p"])
    d["w"]=np.sqrt(d["n_case"]*d["n_ctrl"]/(d["n_case"]+d["n_ctrl"]))
    return d[["log2FC","Z","w"]]

# primary contrasts (same as p2_deg_meta.py `primary`)
primaries={
 "GSE267799_SMIR_DRG__chronic_vs_baseline":"results/tables/DEG_GSE267799_SMIR_DRG__chronic_vs_baseline.csv",
 "GSE212311_CCI_DRG__CCI_vs_Sham":"results/tables/DEG_GSE212311_CCI_DRG__CCI_vs_Sham.csv",
 "GSE278227_CCI_DRG__1W_IL_vs_CL_pooled":"results/tables/DEG_GSE278227_CCI_DRG__1W_IL_vs_CL_pooled.csv",
 "GSE241361_S1R_DRG__SNI_vs_Naive_WT":"results/tables/DEG_GSE241361_S1R_DRG__SNI_vs_Naive_WT.csv",
}
def xt_tab(fn):
    xt=pd.read_csv(os.path.join(OUT,fn)).dropna(subset=["gene","mRNA_log2FC","pvalue_final"])
    z=np.sign(xt["mRNA_log2FC"])*stats.norm.isf(xt["pvalue_final"].clip(1e-300,1)/2)
    t=pd.DataFrame({"log2FC":xt["mRNA_log2FC"].values,"Z":z.values},index=xt["gene"].astype(str).str.upper().values)
    return t.groupby(t.index).mean()
xt_d4=xt_tab("GSE265957_Xtail_DRG_Day4_SNI_vs_SHM.csv")
xt_d63=xt_tab("GSE265957_Xtail_DRG_Day63_SNI_vs_SHM.csv")

def run_meta(datasets, label):
    allg=set()
    for d in datasets.values(): allg|=set(d.index)
    rows=[]
    for gene in allg:
        zs=[]; ws=[]; lf={}
        for k,d in datasets.items():
            if gene in d.index and not np.isnan(d.loc[gene,"Z"]):
                zs.append(float(d.loc[gene,"Z"])); ws.append(float(d.loc[gene,"w"])); lf[k]=float(d.loc[gene,"log2FC"])
        k_=len(zs)
        if k_<3: continue
        zs=np.array(zs); ws=np.array(ws)
        Zc=(zs*ws).sum()/np.sqrt((ws**2).sum())
        p=2*stats.norm.sf(abs(Zc))
        up=sum(1 for x in zs if x>0); cons=max(up,k_-up)/k_
        rows.append({"symbol":gene,"K":k_,"meta_Z":Zc,"meta_p":p,"consistency":cons,
                     "n_up":up,"n_dn":k_-up})
    meta=pd.DataFrame(rows); meta["meta_FDR"]=bh(meta["meta_p"].values)
    core=meta[(meta["meta_FDR"]<0.05)&(meta["consistency"]>=0.8)]
    print(f"[{label}] inputs={len(datasets)} genes_tested={len(meta)} FDR<0.05={int((meta['meta_FDR']<0.05).sum())} core={len(core)}")
    return meta,core

# (A) ORIGINAL 6-input
A=dict((k,load_deg(v)) for k,v in primaries.items())
A["GSE265957_Xtail_DRG_Day4"]=pd.DataFrame({"log2FC":xt_d4["log2FC"],"Z":xt_d4["Z"],"w":np.full(len(xt_d4),1.0)})
A["GSE265957_Xtail_DRG_Day63"]=pd.DataFrame({"log2FC":xt_d63["log2FC"],"Z":xt_d63["Z"],"w":np.full(len(xt_d63),1.0)})
metaA,coreA=run_meta(A,"A_ORIGINAL_6input")

# (B) COLLAPSED 5-input: merge Day4 + Day63 into one study (mean Z, mean log2FC, w=1.0)
merged_Z=(xt_d4["Z"].add(xt_d63["Z"],fill_value=0))/2.0
merged_lfc=(xt_d4["log2FC"].add(xt_d63["log2FC"],fill_value=0))/2.0
B=dict((k,load_deg(v)) for k,v in primaries.items())
B["GSE265957_Xtail_DRG_merged"]=pd.DataFrame({"log2FC":merged_lfc,"Z":merged_Z,"w":np.full(len(merged_Z),1.0)})
metaB,coreB=run_meta(B,"B_COLLAPSED_5input")

# overlap
sa=set(coreA.symbol); sb=set(coreB.symbol)
print(f"\nSensitivity: original core={len(sa)}  collapsed core={len(sb)}  shared={len(sa&sb)}  "
      f"only_in_original={len(sa-sb)}  only_in_collapsed={len(sb-sa)}")
print(f"Collapsed core retained {len(sa&sb)/max(len(sa),1):.1%} of the original core.")
out=os.path.join(TAB,"P2_meta_sensitivity.csv")
pd.DataFrame({"metric":["orig_inputs","orig_core","collapsed_inputs","collapsed_core","shared_core",
                        "only_in_original","only_in_collapsed","retained_fraction"],
              "value":[len(A),len(sa),len(B),len(sb),len(sa&sb),len(sa-sb),len(sb-sa),
                       round(len(sa&sb)/max(len(sa),1),4)]}).to_csv(out,index=False)
print("wrote",out)
