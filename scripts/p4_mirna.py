#!/usr/bin/env python3
# p4_mirna.py -- human plasma miRNA layer (GSE158825): pain-outcome association + LSS+DS vs LSS DEG.
import os, re, gzip
import numpy as np, pandas as pd
from scipy import stats

ROOT="D:/2026.9/极速交付9月会员日优惠套路/01_AI生信-虚拟多重筛药/慢性疼痛"
RAW=os.path.join(ROOT,"data/raw"); OUT=os.path.join(ROOT,"data/processed")
TAB=os.path.join(ROOT,"results/tables"); os.makedirs(TAB,exist_ok=True)

def bh(p):
    p=np.asarray(p,float); ok=~np.isnan(p); q=np.full_like(p,np.nan)
    idx=np.where(ok)[0]; pv=p[idx]; m=len(pv)
    o=np.argsort(pv); a=pv[o]*m/np.arange(1,m+1)
    a=np.minimum.accumulate(a[::-1])[::-1]
    q[idx[o]]=np.clip(a,0,1); return q

# ---- load matrix ----
mat=pd.read_csv(os.path.join(RAW,"GSE158825/GSE158825_Lively_human_plasma_SFOA-maturemiRNAcounts.tsv.gz"),
                sep="\t",compression="gzip")
mat=mat.rename(columns={mat.columns[0]:"miRNA"}).set_index("miRNA")
mat.columns=[c.split("-miRNAcount")[0].upper() for c in mat.columns]   # "86-SPINE" (case-normalised)
print("matrix:",mat.shape)

# ---- phenotypes ----
ph=pd.read_csv(os.path.join(OUT,"GSE158825_series_matrix.txt.gz_samples.csv"))
def g(ch,key):
    m=re.search(rf"{key}:\s*([^|]+)",str(ch)); return m.group(1).strip() if m else None
ph["diagnosis"]=ph["characteristics_ch1"].apply(lambda c:g(c,"diagnosis"))
ph["sex"]=ph["characteristics_ch1"].apply(lambda c:g(c,"Sex"))
ph["nprs20delta"]=ph["characteristics_ch1"].apply(lambda c:g(c,"% ?nprs20delta"))
ph["nprs20delta"]=pd.to_numeric(ph["nprs20delta"],errors="coerce")
ph["title"]=ph["title"].astype(str).str.upper()
print("groups:",ph["diagnosis"].value_counts().to_dict()," sex:",ph["sex"].value_counts().to_dict())
print("nprs20delta: n=",ph["nprs20delta"].notna().sum()," median=",ph["nprs20delta"].median())

id2gsm=dict(zip(ph["title"],ph["geo_accession"]))
id2diag=dict(zip(ph["title"],ph["diagnosis"]))
id2npr=dict(zip(ph["title"],ph["nprs20delta"]))
id2sex=dict(zip(ph["title"],ph["sex"]))
# align matrix columns to phenotype (keep those matching)
cols=[c for c in mat.columns if c in id2gsm]
mat=mat[cols]
samples=pd.DataFrame({"lib":cols,"title":cols,"gsm":[id2gsm[c] for c in cols],
                      "diagnosis":[id2diag[c] for c in cols],
                      "sex":[id2sex[c] for c in cols],
                      "nprs20delta":[id2npr[c] for c in cols]})
samples.to_csv(os.path.join(OUT,"GSE158825_sampletable.csv"),index=False)
print("aligned samples:",mat.shape[1])

# ---- filter + normalise ----
mat=mat.apply(pd.to_numeric,errors="coerce").fillna(0)
keep=mat.sum(axis=1)>=10          # drop near-empty miRNAs
mat=mat.loc[keep]
cpm=np.log2(mat.div(mat.sum(axis=0),axis=1)*1e6+1)
print("expressed miRNAs:",mat.shape[0])

# ---- A) DEG: LSS+DS vs LSS ----
diag=samples.set_index("lib")["diagnosis"]
gA=diag[diag=="LSS+DS"].index.tolist(); gB=diag[diag=="LSS"].index.tolist()
A=cpm[gA]; B=cpm[gB]
m1=A.mean(axis=1); m2=B.mean(axis=1); v1=A.var(axis=1,ddof=1); v2=B.var(axis=1,ddof=1)
n1,n2=len(gA),len(gB)
se=np.sqrt(v1/n1+v2/n2); t=(m1-m2)/se.replace(0,np.nan)
dfw=(v1/n1+v2/n2)**2/(((v1/n1)**2)/(n1-1)+((v2/n2)**2)/(n2-1))
p=2*stats.t.sf(np.abs(t),dfw)
deg=pd.DataFrame({"log2FC":m1-m2,"t":t,"p":p}); deg["FDR"]=bh(deg["p"].values)
deg=deg.sort_values("p"); deg.to_csv(os.path.join(TAB,"P4_GSE158825_miRNA_LSSDS_vs_LSS.csv"))
print(f"[DEG LSS+DS vs LSS] n={len(deg)} FDR<0.05={(deg['FDR']<0.05).sum()}")

# ---- B) association with pain outcome (%nprs20delta) ----
y=samples.set_index("lib")["nprs20delta"]
ok=y.notna()
res=[]
for mir in cpm.index:
    x=cpm.loc[mir, ok.values]
    if x.std()==0: res.append((mir,np.nan,np.nan)); continue
    r,pv=stats.spearmanr(x.values, y[ok].values)
    res.append((mir,r,pv))
assoc=pd.DataFrame(res,columns=["miRNA","rho","p"]).set_index("miRNA")
assoc["FDR"]=bh(assoc["p"].values)
assoc=assoc.sort_values("p")
assoc.to_csv(os.path.join(TAB,"P4_GSE158825_miRNA_painoutcome_spearman.csv"))
print(f"[ASSOC with %nprs20delta] n={len(assoc)} FDR<0.05={(assoc['FDR']<0.05).sum()} (n_samples={int(ok.sum())})")
print("\nTop 15 by association:")
print(assoc.head(15).to_string())
print("\nTop 10 DEG:")
print(deg.head(10).to_string())
