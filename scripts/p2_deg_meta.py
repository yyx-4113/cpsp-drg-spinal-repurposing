#!/usr/bin/env python3
# p2_deg_meta.py -- per-dataset DEG (Welch t + BH) on DRG/spinal axis, then Stouffer weighted-Z meta.
# Discipline: log-space, per-dataset effect, cross-species symbol harmonisation (uppercase),
# meta weights = sqrt(n1*n2/(n1+n2)) (inverse-SE scale), direction-consistency reported.
import os, sys, json
import numpy as np, pandas as pd
from scipy import stats

ROOT="D:/2026.9/极速交付9月会员日优惠套路/01_AI生信-虚拟多重筛药/慢性疼痛"
OUT=os.path.join(ROOT,"data/processed")
DEG=os.path.join(ROOT,"results/tables"); os.makedirs(DEG,exist_ok=True)

def bh(p):
    p=np.asarray(p,float); ok=~np.isnan(p); idx=np.where(ok)[0]
    q=np.full_like(p,np.nan); pv=p[idx]; m=len(pv)
    order=np.argsort(pv); ranked=pv[order]
    adj=ranked*m/np.arange(1,m+1)
    adj=np.minimum.accumulate(adj[::-1])[::-1]
    q[idx[order]]=np.clip(adj,0,1); return q

def std_symbol(s):
    s=str(s).upper()
    if s.startswith(("ENSRNOG","ENSMUSG","ENSG","AABR","LOC","GMR","RGD","-")): return None
    if not s or s=="NAN": return None
    if len(s)>25: return None
    return s

def logcpm(m):
    m=m.apply(pd.to_numeric,errors="coerce").fillna(0)
    lib=m.sum(axis=0); lib=lib.replace(0,np.nan)
    return np.log2(m.div(lib,axis=1)*1e6+1)

def load_mat(fn, norm="cpm"):
    m=pd.read_csv(os.path.join(OUT,fn),index_col=0)
    m.index=[x for x in (std_symbol(s) for s in m.index)]
    m=m[[i is not None for i in m.index]]
    m.index=[i for i in m.index if i is not None]
    m=m.groupby(m.index).mean(numeric_only=True)
    if norm=="cpm": m=logcpm(m)
    return m

def welch(mat, case_cols, ctrl_cols):
    A=mat[case_cols]; B=mat[ctrl_cols]
    m1=A.mean(axis=1); m2=B.mean(axis=1); v1=A.var(axis=1,ddof=1); v2=B.var(axis=1,ddof=1)
    n1=len(case_cols); n2=len(ctrl_cols)
    se=np.sqrt(v1/n1+v2/n2)
    t=(m1-m2)/se.replace(0,np.nan)
    dfw=(v1/n1+v2/n2)**2/(((v1/n1)**2)/(n1-1)+((v2/n2)**2)/(n2-1))
    p=2*stats.t.sf(np.abs(t),dfw)
    res=pd.DataFrame({"log2FC":m1-m2,"t":t,"p":p,"mean_case":m1,"mean_ctrl":m2})
    res["FDR"]=bh(res["p"].values)
    res["n_case"]=n1; res["n_ctrl"]=n2
    return res

def st_group(st, col):
    return st.groupby(col)["sample"].apply(list).to_dict()

# ---------------- build DEG contrasts ----------------
contrasts=[]

# 1) GSE267799 SMIR DRG  (incision -> CPSP-relevant)
m=load_mat("GSE267799_DRG_symbol_count.csv")
st=pd.read_csv(os.path.join(OUT,"GSE267799_DRG_sampletable.csv"))
g=st.groupby("time_group")["sample"].apply(list).to_dict()
for tag,(case,ctrl) in {"chronic_vs_baseline":("chronic","baseline"),
                        "acute_vs_baseline":("acute","baseline"),
                        "chronic_vs_acute":("chronic","acute")}.items():
    r=welch(m,g[case],g[ctrl]); r["dataset"]="GSE267799_SMIR_DRG"; r["contrast"]=tag; r["axis"]="DRG"
    contrasts.append(r)

# 2) GSE212311 CCI vs Sham (rat DRG)
m=load_mat("GSE212311_DRG_symbol_log2fpkm.csv",norm="none")
st=pd.read_csv(os.path.join(OUT,"GSE212311_DRG_sampletable.csv"))
g=st_group(st,"group")
r=welch(m,g["CCI"],g["Sham"]); r["dataset"]="GSE212311_CCI_DRG"; r["contrast"]="CCI_vs_Sham"; r["axis"]="DRG"
contrasts.append(r)

# 3) GSE278227 CCI rat DRG: IL vs CL by time & sex
m=load_mat("GSE278227_DRG_symbol_count.csv")
st=pd.read_csv(os.path.join(OUT,"GSE278227_DRG_sampletable.csv"))
for t in ["24h","1W","5W"]:
    for sx in ["M","F"]:
        sub=st[(st.time==t)&(st.sex=={"M":"male","F":"female"}[sx])]
        il=sub[sub.side=="ipsilateral"]["sample"].tolist()
        cl=sub[sub.side=="contralateral"]["sample"].tolist()
        if len(il)>=3 and len(cl)>=3:
            r=welch(m,il,cl); r["dataset"]="GSE278227_CCI_DRG"; r["contrast"]=f"{sx}_{t}_IL_vs_CL"; r["axis"]="DRG"
            contrasts.append(r)
# pooled 1W (both sexes)
sub=st[(st.time=="1W")]
r=welch(m,sub[sub.side=="ipsilateral"]["sample"].tolist(),sub[sub.side=="contralateral"]["sample"].tolist())
r["dataset"]="GSE278227_CCI_DRG"; r["contrast"]="1W_IL_vs_CL_pooled"; r["axis"]="DRG"; contrasts.append(r)

# 4) GSE241361 mouse Sigma-1: SNI vs Naive (WT DRG), and KO vs WT (SNI DRG)
m=load_mat("GSE241361_symbol_count.csv")
st=pd.read_csv(os.path.join(OUT,"GSE241361_sampletable.csv"))
wt_drg_sni=st[(st.treatment=="SNI")&(st.genotype=="WT")&(st.tissue=="DRG")]["sample"].tolist()
wt_drg_nai=st[(st.treatment=="Naive")&(st.genotype=="WT")&(st.tissue=="DRG")]["sample"].tolist()
r=welch(m,wt_drg_sni,wt_drg_nai); r["dataset"]="GSE241361_S1R_DRG"; r["contrast"]="SNI_vs_Naive_WT"; r["axis"]="DRG"; contrasts.append(r)
ko_sni=st[(st.treatment=="SNI")&(st.genotype=="KO")&(st.tissue=="DRG")]["sample"].tolist()
r=welch(m,ko_sni,wt_drg_sni); r["dataset"]="GSE241361_S1R_DRG"; r["contrast"]="KO_vs_WT_SNI"; r["axis"]="DRG"; contrasts.append(r)

# 5) GSE241361 spinal cord (Medula) axis
wt_sc_sni=st[(st.treatment=="SNI")&(st.genotype=="WT")&(st.tissue=="Medula")]["sample"].tolist()
wt_sc_nai=st[(st.treatment=="Naive")&(st.genotype=="WT")&(st.tissue=="Medula")]["sample"].tolist()
r=welch(m,wt_sc_sni,wt_sc_nai); r["dataset"]="GSE241361_S1R_SC"; r["contrast"]="SNI_vs_Naive_WT_SC"; r["axis"]="SC"; contrasts.append(r)

# 6) GSE306403 human SH-SY5Y morphine vs control (in-vitro; NOT patient)
m=load_mat("GSE306403_SH-SY5Y_symbol_count.csv")
st=pd.read_csv(os.path.join(OUT,"GSE306403_sampletable.csv"))
g=st_group(st,"group")
r=welch(m,g["Morphine"],g["Control"]); r["dataset"]="GSE306403_SHSY5Y"; r["contrast"]="Morphine_vs_Control"; r["axis"]="in_vitro"
contrasts.append(r)

# save per-contrast DEG tables
for r in contrasts:
    tag=f"{r['dataset'].iloc[0]}__{r['contrast'].iloc[0]}"
    r.sort_values("p").to_csv(os.path.join(DEG,f"DEG_{tag}.csv"))
    sig=(r["FDR"]<0.05).sum()
    print(f"[DEG] {tag:44s} n={len(r):6d}  FDR<0.05={sig:5d}  up={( (r['FDR']<0.05)&(r['log2FC']>0)).sum():5d} dn={((r['FDR']<0.05)&(r['log2FC']<0)).sum():5d}")

# ---------------- meta-analysis (DRG-axis injury contrasts) ----------------
META_SETS={
 "GSE267799_SMIR_DRG__chronic_vs_baseline":"incision(LPI) rat DRG chronic",
 # GSE212311
 # GSE278227
 # GSE241361
}
# pick primary contrasts for meta
primary={
 "GSE267799_SMIR_DRG__chronic_vs_baseline":"LPI_chronic",
 "GSE212311_CCI_DRG__CCI_vs_Sham":"CCI_rat",
 "GSE278227_CCI_DRG__1W_IL_vs_CL_pooled":"CCI_rat_1W",
 "GSE241361_S1R_DRG__SNI_vs_Naive_WT":"SNI_mouse_WT",
 "GSE265957_Xtail_DRG_Day4":"SNI_mouse_d4",
}
# add GSE265957 DRG from provided Xtail log2FC/p (derive Z), Day4 (acute) + Day63 (chronic)
def xt_tab_from(fn):
    xt=pd.read_csv(os.path.join(OUT,fn)).dropna(subset=["gene","mRNA_log2FC","pvalue_final"])
    xt["symbol"]=[std_symbol(g) for g in xt["gene"]]
    xt=xt[xt["symbol"].notna()]
    z=np.sign(xt["mRNA_log2FC"])*stats.norm.isf(xt["pvalue_final"].clip(1e-300,1)/2)
    t=pd.DataFrame({"log2FC":xt["mRNA_log2FC"].values,"Z":z.values},index=xt["symbol"].values)
    return t.groupby(t.index).mean()
xt_d4=xt_tab_from("GSE265957_Xtail_DRG_Day4_SNI_vs_SHM.csv")
xt_d63=xt_tab_from("GSE265957_Xtail_DRG_Day63_SNI_vs_SHM.csv")

# assemble per-dataset (log2FC, Z, w)
datasets={}
for r in contrasts:
    key=f"{r['dataset'].iloc[0]}__{r['contrast'].iloc[0]}"
    if key in primary:
        # Z from t (Welch) with normal approx on df-corrected t -> use t dist
        zz=np.sign(r["t"])*stats.norm.isf(r["p"].clip(1e-300,1)/2)
        w=np.sqrt(r["n_case"]*r["n_ctrl"]/(r["n_case"]+r["n_ctrl"]))*np.ones(len(r))
        datasets[key]=pd.DataFrame({"log2FC":r["log2FC"],"Z":zz,"w":w})
datasets["GSE265957_Xtail_DRG_Day4"]=pd.DataFrame({"log2FC":xt_d4["log2FC"],"Z":xt_d4["Z"],"w":np.full(len(xt_d4),np.sqrt(2*2/4))})
datasets["GSE265957_Xtail_DRG_Day63"]=pd.DataFrame({"log2FC":xt_d63["log2FC"],"Z":xt_d63["Z"],"w":np.full(len(xt_d63),np.sqrt(2*2/4))})

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
    # direction consistency = max(up,dn)/k
    up=sum(1 for x in zs if x>0); cons=max(up,k_-up)/k_
    row={"symbol":gene,"K":k_,"meta_Z":Zc,"meta_p":p,"consistency":cons,
         "n_up":up,"n_dn":k_-up}
    for k,d in datasets.items(): row[f"lfc_{k.split('__')[0] if '__' in k else k}"]=lf.get(k,np.nan)
    rows.append(row)
meta=pd.DataFrame(rows)
meta["meta_FDR"]=bh(meta["meta_p"].values)
meta=meta.sort_values("meta_p")

# translational concordance: does the nerve-injury meta signature hold direction in the INCISION model?
inc_col="lfc_GSE267799_SMIR_DRG"
meta["incision_lfc"]=meta.get(inc_col, np.nan)
meta["concordant_incision"]=np.sign(meta["meta_Z"])==np.sign(meta["incision_lfc"])
sig=(meta["meta_FDR"]<0.05)&(meta["consistency"]>=0.6)
sub=meta[sig].dropna(subset=["incision_lfc"])
print("\n=== translational concordance (nerve-injury signature -> incision model) ===")
if len(sub):
    print(f"FDR<0.05 & consistency>=0.6 genes with incision measured: {len(sub)}")
    print(f"  same direction in incision(LPI) DRG: {sub['concordant_incision'].sum()}/{len(sub)} = {sub['concordant_incision'].mean():.1%}")
    from scipy.stats import binomtest
    print(f"  binomial vs 50%: p={binomtest(int(sub['concordant_incision'].sum()), len(sub), 0.5).pvalue:.2e}")

meta.to_csv(os.path.join(DEG,"META_DRG_axis_stouffer.csv"),index=False)
core=meta[(meta["meta_FDR"]<0.05)&(meta["consistency"]>=0.8)].copy()
core.to_csv(os.path.join(DEG,"META_DRG_axis_CORE_signature.csv"),index=False)

print("\n=== META (DRG axis, K>=3) ===")
print(f"genes tested={len(meta)}  FDR<0.05={(meta['meta_FDR']<0.05).sum()}  "
      f"core(FDR<0.05 & consistency>=0.8)={len(core)}")
print(meta.head(30).to_string(index=False))
