#!/usr/bin/env python3
# p4_integrate.py -- integrate miRDB hub-targeting miRNAs with human plasma cohorts (GSE158825, GSE222979).
import os, re
import numpy as np, pandas as pd
from scipy import stats

ROOT="D:/2026.9/极速交付9月会员日优惠套路/01_AI生信-虚拟多重筛药/慢性疼痛"
RAW=os.path.join(ROOT,"data/raw"); OUT=os.path.join(ROOT,"data/processed"); TAB=os.path.join(ROOT,"results/tables")
rng=np.random.default_rng(42)

tgt=pd.read_csv(os.path.join(TAB,"P4_hub_targeting_miRNAs.csv"))
assoc=pd.read_csv(os.path.join(TAB,"P4_GSE158825_miRNA_painoutcome_spearman.csv")).set_index("miRNA")
deg=pd.read_csv(os.path.join(TAB,"P4_GSE158825_miRNA_LSSDS_vs_LSS.csv")).set_index("miRNA")

# detected miRNAs in GSE158825 plasma
mat=pd.read_csv(os.path.join(RAW,"GSE158825/GSE158825_Lively_human_plasma_SFOA-maturemiRNAcounts.tsv.gz"),sep="\t",compression="gzip")
mat=mat.rename(columns={mat.columns[0]:"miRNA"}).set_index("miRNA")
mat=mat.apply(pd.to_numeric,errors="coerce").fillna(0)
detected=set(mat.index[mat.sum(axis=1)>=10])

def norm(m): return str(m).strip()
tgt["miRNA"]=tgt["miRNA"].map(norm)
hi=tgt[tgt.score>=80].copy()
hi_det=hi[hi.miRNA.isin(detected)].copy()
print(f"hub-targeting miRNAs (score>=80): {hi.miRNA.nunique()}")
print(f"  detected in human plasma (GSE158825): {hi_det.miRNA.nunique()}")

# annotate with pain-outcome association
rows=[]
for mir in sorted(hi_det.miRNA.unique()):
    if mir in assoc.index:
        rows.append({"miRNA":mir,"targets":";".join(sorted(hi_det[hi_det.miRNA==mir]["symbol"].unique())),
                     "max_score":hi_det[hi_det.miRNA==mir]["score"].max(),
                     "rho_pain":assoc.loc[mir,"rho"],"p_pain":assoc.loc[mir,"p"],"FDR_pain":assoc.loc[mir,"FDR"],
                     "LSSDS_log2FC":deg.loc[mir,"log2FC"] if mir in deg.index else np.nan,
                     "LSSDS_FDR":deg.loc[mir,"FDR"] if mir in deg.index else np.nan})
intab=pd.DataFrame(rows).sort_values("p_pain")
intab.to_csv(os.path.join(TAB,"P4_hub_miRNA_human_integration.csv"),index=False)
print(f"annotated: {len(intab)}")
print(intab.head(20).to_string(index=False))

# ---- set-level test: are hub-targeting miRNAs associated with pain outcome (direction) more than random? ----
rho_hub=intab["rho_pain"].dropna().values
allrho=assoc["rho"].dropna().values
if len(rho_hub)>=5:
    t1=stats.ttest_1samp(rho_hub,0)
    w=stats.wilcoxon(rho_hub)
    # permutation: random same-size miRNA sets
    null=[]
    for _ in range(5000):
        s=rng.choice(allrho,len(rho_hub),replace=False); null.append(np.mean(s))
    null=np.array(null); obs=np.mean(rho_hub)
    pperm=(np.sum(np.abs(null)>=abs(obs))+1)/(len(null)+1)
    print(f"\n[SET TEST] hub-targeting miRNAs n={len(rho_hub)}  mean_rho={obs:.3f}  "
          f"t-p={t1.pvalue:.3g}  wilcoxon-p={w.pvalue:.3g}  permutation-p={pperm:.4g}")
    print(f"  sign: {(rho_hub>0).sum()} positive / {(rho_hub<0).sum()} negative")
    json_out={"n":len(rho_hub),"mean_rho":float(obs),"t_p":float(t1.pvalue),
              "wilcoxon_p":float(w.pvalue),"perm_p":float(pperm),
              "n_pos":int((rho_hub>0).sum()),"n_neg":int((rho_hub<0).sum())}
    import json; json.dump(json_out,open(os.path.join(TAB,"P4_setlevel_test.json"),"w"),indent=2)

# ---- GSE222979: detection across 3 biofluids ----
try:
    m2=pd.read_csv(os.path.join(RAW,"GSE222979/GSE222979_2023_Match414_3biofluids_miRNA_counts.tsv.gz"),sep="\t",compression="gzip")
    m2=m2.rename(columns={m2.columns[0]:"miRNA"}).set_index("miRNA")
    cols=list(m2.columns)
    fluid=["plasma" if c.split("_")[1].startswith("PL") else ("synovial" if c.split("_")[1].startswith("SF") else "urine") for c in cols]
    m2=m2.apply(pd.to_numeric,errors="coerce").fillna(0)
    det2={f:set(m2.index[m2[[c for c,fl in zip(cols,fluid) if fl==f]].sum(axis=1)>=10]) for f in ["plasma","synovial","urine"]}
    for f,s in det2.items(): print(f"[GSE222979 {f}] detected={len(s)}  hub-targeting detected={len(set(hi.miRNA)&s)}")
    import json; json.dump({f:len(set(hi.miRNA)&s) for f,s in det2.items()},open(os.path.join(TAB,"P4_GSE222979_detection.json"),"w"),indent=2)
except Exception as e:
    print("[GSE222979] skip:",e)
