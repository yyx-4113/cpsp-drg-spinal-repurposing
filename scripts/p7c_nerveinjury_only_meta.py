#!/usr/bin/env python3
# p7c_nerveinjury_only_meta.py -- Round-4 remediation: the definitive non-circular test.
#
# Building the selection set on a meta-analysis that INCLUDES the incision contrast leaves a
# residual circularity even after splitting consistency (p7b). Here the selection is done on a
# NERVE-INJURY-ONLY meta (the 5 nerve-injury contrasts; incision contrast removed entirely from
# both the Z and the consistency filter). The incision contrast is then used once, as the
# held-out test of direction agreement.
#
# Also reports the same meta under random effects (DL).
import os, json, numpy as np, pandas as pd
from scipy import stats

ROOT = "D:/2026.9/极速交付9月会员日优惠套路/01_AI生信-虚拟多重筛药/慢性疼痛"
TAB  = os.path.join(ROOT, "results/tables")

f = pd.read_csv(os.path.join(TAB, "_R4_random_effects_meta.csv")).set_index("symbol")
# per-contrast Z were not persisted; recompute the NI-only meta from the R4 FE table is not
# possible directly, so rebuild from sources exactly as in p7_round4_supplementary.py
import importlib.util
spec = importlib.util.spec_from_file_location("s7", os.path.join(ROOT, "scripts/p7_round4_supplementary.py"))

BULK = [("GSE267799_SMIR_DRG","DEG_GSE267799_SMIR_DRG__chronic_vs_baseline.csv",12,8,"incision"),
        ("GSE212311_CCI_DRG","DEG_GSE212311_CCI_DRG__CCI_vs_Sham.csv",3,3,"nerve_injury"),
        ("GSE278227_CCI_DRG","DEG_GSE278227_CCI_DRG__1W_IL_vs_CL_pooled.csv",14,14,"nerve_injury"),
        ("GSE241361_S1R_DRG","DEG_GSE241361_S1R_DRG__SNI_vs_Naive_WT.csv",4,5,"nerve_injury")]
XTAIL= [("GSE265957_Xtail_DRG_Day4","GSE265957_Xtail_DRG_Day4_SNI_vs_SHM.csv",2,2,"nerve_injury"),
        ("GSE265957_Xtail_DRG_Day63","GSE265957_Xtail_DRG_Day63_SNI_vs_SHM.csv",2,2,"nerve_injury")]
PROC = os.path.join(ROOT, "data/processed")
def bh(p):
    p=np.asarray(p,float); n=len(p); o=np.argsort(p); q=np.empty(n); prev=1.0
    for i in range(n-1,-1,-1):
        prev=min(prev,p[o[i]]*n/(i+1)); q[o[i]]=prev
    return np.minimum(q,1.0)
def wilson(k,n,z=1.959963985):
    if n==0: return (np.nan,np.nan)
    ph=k/n; d=1+z*z/n; c=(ph+z*z/(2*n))/d
    h=z*np.sqrt(ph*(1-ph)/n+z*z/(4*n*n))/d
    return (max(0.,c-h),min(1.,c+h))

Zt={}; W={}
for key,fn,n1,n2,kind in BULK:
    d=pd.read_csv(os.path.join(TAB,fn)); d=d.rename(columns={d.columns[0]:"symbol"})
    d["symbol"]=d["symbol"].astype(str).str.upper(); d=d.groupby("symbol").mean(numeric_only=True)
    Zt[key]=np.sign(d["t"])*stats.norm.isf(np.clip(d["p"],1e-300,1)/2); W[key]=np.sqrt(n1*n2/(n1+n2))
for key,fn,n1,n2,kind in XTAIL:
    d=pd.read_csv(os.path.join(PROC,fn)).dropna(subset=["gene","mRNA_log2FC","pvalue_final"])
    d["symbol"]=d["gene"].astype(str).str.upper(); d=d.groupby("symbol").mean(numeric_only=True)
    Zt[key]=np.sign(d["mRNA_log2FC"])*stats.norm.isf(np.clip(d["pvalue_final"],1e-300,1)/2); W[key]=np.sqrt(n1*n2/(n1+n2))

NI=[k for k,*_ in BULK+XTAIL if k!="GSE267799_SMIR_DRG"]
INC="GSE267799_SMIR_DRG"
Z=pd.DataFrame(Zt).dropna(how="all"); Z=Z.reindex(f.index)
w=np.array([W[k] for k in NI]); w2=w**2
Zm=Z[NI].values; mask=~np.isnan(Zm); Kp=mask.sum(1)
Zni=np.nansum(Zm*w,1)/np.sqrt(np.nansum(np.where(mask,w2,0),1))
pni=2*stats.norm.sf(np.abs(Zni)); fdni=bh(pni)
cons_ni=(np.nansum(Zm>0,1))/np.maximum(Kp,1)
cons_ni=np.maximum(cons_ni,1-cons_ni)
# random effects on the NI-only set
D=Zm/w; iv=np.where(mask,w2,0.); s_iv=iv.sum(1)
dFE=np.nansum(np.where(mask,D*iv,0),1)/s_iv
Q=np.nansum(np.where(mask,iv*(D-dFE[:,None])**2,0),1)
C=s_iv-(iv**2).sum(1)/s_iv
tau2=np.maximum(0.,(Q-(Kp-1))/np.where(C>0,C,np.nan))
wst=np.where(mask,1./(1./w2+tau2[:,None]),0.)
dRE=np.nansum(np.where(mask,D*wst,0),1)/wst.sum(1); Zre=dRE*np.sqrt(wst.sum(1))
pre=2*stats.norm.sf(np.abs(Zre)); fdre=bh(pre)

inc=Z[INC].values
meas=~np.isnan(inc)
agr=(np.sign(inc)==np.sign(Zni)).astype(float)

out=pd.DataFrame({"symbol":Z.index,"K_ni":Kp,"Z_NI":Zni,"p_NI":pni,"FDR_NI":fdni,
                  "ni_consistency":cons_ni,"Z_NI_RE":Zre,"p_NI_RE":pre,"FDR_NI_RE":fdre,
                  "incision_Z":inc,"incision_agreement":np.where(meas,agr,np.nan)})
out.to_csv(os.path.join(TAB,"_R4_nerveinjury_only_meta.csv"))

res={}
rng=np.random.default_rng(42); NP=5000
pool=np.where(meas)[0]; agrp=agr[pool]
def stratum(name,m):
    m=m&meas; n=int(m.sum()); k=int(np.nansum(agr[m])); r=k/n if n else np.nan
    lo,hi=wilson(k,n)
    null=np.array([np.nanmean(agrp[rng.choice(len(pool),n,replace=False)]) for _ in range(NP)])
    pv=(np.sum(np.abs(null-null.mean())>=abs(r-null.mean()))+1)/(NP+1)
    print(f"[{name}] {k}/{n} = {r:.1%}  Wilson [{lo:.1%},{hi:.1%}]  perm p={pv:.4g}")
    res[name]={"k":k,"n":n,"rate":round(r,4),"ci":[round(lo,4),round(hi,4)],"perm_p":float(pv)}
    return r

print("=== DEFINITIVE NON-CIRCULAR TEST (selection built on nerve-injury contrasts ONLY) ===")
r_all   = stratum("all_measured", np.ones(len(out),bool))
sig     = (fdni<0.05)
r_sig   = stratum("NI_FDR05_any_consistency", sig)
strong  = sig & (cons_ni>=0.8) & (Kp>=3)
r_strong= stratum("NI_FDR05_AND_NIcons>=0.8", strong)
weak    = sig & (cons_ni<0.8)
r_weak  = stratum("NI_FDR05_AND_NIcons<0.8", weak)
r_strongRE = stratum("NI_FDRRE05_AND_NIcons>=0.8", (fdre<0.05)&(cons_ni>=0.8)&(Kp>=3))
print(f"\nrisk difference (NI-strong minus NI-weak): {(r_strong-r_weak)*100:+.1f} pp")
print(f"NI-strong vs background(all measured):      {(r_strong-r_all)*100:+.1f} pp")
print(f"\nNI-only core (FDR_NI<0.05 & NI-consistency>=0.8): {int(strong.sum())} genes")
print(f"NI-only core under random effects (FDR_NI_RE<0.05 & cons>=0.8): {int(((fdre<0.05)&(cons_ni>=0.8)&(Kp>=3)).sum())} genes")

json.dump({"strata":res,
           "risk_difference_strong_minus_weak_pp":round((r_strong-r_weak)*100,1),
           "strong_vs_background_pp":round((r_strong-r_all)*100,1),
           "NI_core_FE":int(strong.sum()),
           "NI_core_RE":int(((fdre<0.05)&(cons_ni>=0.8)&(Kp>=3)).sum())},
          open(os.path.join(TAB,"_R4_nerveinjury_only_summary.json"),"w"),indent=2)
print("\n[written] _R4_nerveinjury_only_meta.csv, _R4_nerveinjury_only_summary.json")
