#!/usr/bin/env python3
# p3_finalize.py -- recompute LODO AUC with bootstrap 95% CI (using saved hub genes) + P3 figure
import os, json
import numpy as np, pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import roc_auc_score
from sklearn.preprocessing import StandardScaler
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt

ROOT="D:/2026.9/极速交付9月会员日优惠套路/01_AI生信-虚拟多重筛药/慢性疼痛"
OUT=os.path.join(ROOT,"data/processed"); TAB=os.path.join(ROOT,"results/tables")
FIG=os.path.join(ROOT,"results/figures"); os.makedirs(FIG,exist_ok=True)
rng=np.random.default_rng(42)

def std_symbol(s):
    s=str(s).upper()
    if s.startswith(("ENSRNOG","ENSMUSG","ENSG","AABR","LOC","GMR","RGD","-")) or not s or s=="NAN" or len(s)>25: return None
    return s
def load_mat(fn,norm="cpm"):
    m=pd.read_csv(os.path.join(OUT,fn),index_col=0)
    m.index=[std_symbol(s) for s in m.index]; m=m[[i is not None for i in m.index]]; m.index=[i for i in m.index if i]
    m=m.groupby(m.index).mean(numeric_only=True).apply(pd.to_numeric,errors="coerce").fillna(0)
    if norm=="cpm":
        lib=m.sum(axis=0).replace(0,np.nan); m=np.log2(m.div(lib,axis=1)*1e6+1)
    return m
def zsc(m):
    return m.sub(m.mean(axis=1),axis=0).div(m.std(axis=1).replace(0,np.nan),axis=0)

DS=[]
m=load_mat("GSE278227_DRG_symbol_count.csv"); st=pd.read_csv(os.path.join(OUT,"GSE278227_DRG_sampletable.csv"))
s=st[st.time=="1W"]; DS.append(("GSE278227_1W_ratDRG",m,s[s.side=="ipsilateral"]["sample"].tolist(),s[s.side=="contralateral"]["sample"].tolist()))
m=load_mat("GSE267799_DRG_symbol_count.csv"); st=pd.read_csv(os.path.join(OUT,"GSE267799_DRG_sampletable.csv"))
g=st.groupby("time_group")["sample"].apply(list).to_dict(); DS.append(("GSE267799_incision_ratDRG",m,g["chronic"],g["baseline"]))
m=load_mat("GSE241361_symbol_count.csv"); st=pd.read_csv(os.path.join(OUT,"GSE241361_sampletable.csv"))
for tis,nm in [("DRG","GSE241361_mouseDRG"),("Medula","GSE241361_mouseSC")]:
    po=st[(st.treatment=="SNI")&(st.genotype=="WT")&(st.tissue==tis)]["sample"].tolist()
    ng=st[(st.treatment=="Naive")&(st.genotype=="WT")&(st.tissue==tis)]["sample"].tolist(); DS.append((nm,m,po,ng))
m=load_mat("GSE212311_DRG_symbol_log2fpkm.csv",norm="none"); st=pd.read_csv(os.path.join(OUT,"GSE212311_DRG_sampletable.csv"))
gg=st.groupby("group")["sample"].apply(list).to_dict(); DS.append(("GSE212311_CCI_ratDRG",m,gg["CCI"],gg["Sham"]))

common=set(DS[0][1].index)
for _,m,_,_ in DS: common&=set(m.index)
common=sorted(common); cidx={g:i for i,g in enumerate(common)}
ZS={nm:zsc(m.loc[common]).fillna(0) for nm,m,_,_ in DS}
hub=pd.read_csv(os.path.join(TAB,"P3_hub_genes.csv"))["symbol"].tolist()
hub=[h for h in hub if h in cidx]
print("hub genes used:",len(hub))

def xy(names):
    Xs=[];ys=[];dd={n:(p,q) for n,_,p,q in DS}
    for nm in names:
        m=ZS[nm];po,ng=dd[nm]
        Xs.append(m[po].T.values);ys.append(np.ones(len(po)))
        Xs.append(m[ng].T.values);ys.append(np.zeros(len(ng)))
    return np.vstack(Xs),np.concatenate(ys)

rows=[]
for probe in [n for n,_,_,_ in DS]:
    tr=[n for n,_,_,_ in DS if n!=probe]
    Xtr,ytr=xy(tr); cols=[cidx[g] for g in hub]
    sc=StandardScaler().fit(Xtr[:,cols]); lr=LogisticRegression(max_iter=5000).fit(sc.transform(Xtr[:,cols]),ytr)
    m=ZS[probe]; po,ng={n:(p,q) for n,_,p,q in DS}[probe]
    Xte=np.vstack([m[po].T.values,m[ng].T.values])[:,cols]; yte=np.r_[np.ones(len(po)),np.zeros(len(ng))]
    sco=lr.decision_function(sc.transform(Xte)); a=roc_auc_score(yte,sco)
    bs=[]
    for _ in range(3000):
        i=rng.choice(len(yte),len(yte),replace=True)
        if len(np.unique(yte[i]))<2: continue
        bs.append(roc_auc_score(yte[i],sco[i]))
    lo,hi=np.percentile(bs,[2.5,97.5])
    rows.append({"test_dataset":probe,"auc":a,"lo":lo,"hi":hi,"n":len(yte)})
    print(f"[LODO+CI] {probe:26s} AUC={a:.3f} [{lo:.3f},{hi:.3f}] n={len(yte)}")

met=pd.DataFrame(rows)
# add pooled CV + null from earlier run
prev=pd.read_csv(os.path.join(TAB,"P3_ml_metrics.csv"))
met.to_csv(os.path.join(TAB,"P3_lodo_auc_ci.csv"),index=False)

# ---------- figure ----------
fig,ax=plt.subplots(1,2,figsize=(14,5.5),facecolor="white",gridspec_kw={"width_ratios":[1.35,1]})
# A: LODO AUC with CI
lab=[r.test_dataset.replace("_"," ") for r in met.itertuples()]
y=np.arange(len(met))[::-1]
ax[0].barh(y,met["auc"],color="#c0392b",alpha=.85)
for i,(a,lo,hi,n) in enumerate(zip(met["auc"],met["lo"],met["hi"],met["n"])):
    ax[0].plot([lo,hi],[y[i],y[i]],color="#2c3e50",lw=1.6)
    ax[0].text(min(hi+0.01,1.0),y[i],f"{a:.2f}\n(n={n})",va="center",fontsize=8,color="#2c3e50")
ax[0].axvline(0.5,ls="--",color="#7f8c8d",lw=1); ax[0].set_xlim(0.4,1.05)
ax[0].set_yticks(y); ax[0].set_yticklabels(lab,fontsize=9)
ax[0].set_xlabel("AUC (leave-one-dataset-out)",fontsize=10)
ax[0].set_title("Cross-dataset generalization of 35-gene hub\n(train without the held-out dataset)",fontsize=12)
# B: hub gene multi-method ranks (top 20)
h=pd.read_csv(os.path.join(TAB,"P3_hub_genes.csv")).head(20)
yy=np.arange(len(h))[::-1]
ax[1].barh(yy,h["lasso_freq"],color="#2980b9",alpha=.9,label="LASSO bootstrap freq")
ax[1].barh(yy-0.28,h["rf_gini"]/h["rf_gini"].max(),color="#27ae60",alpha=.75,height=0.26,label="RF Gini (scaled)")
ax[1].barh(yy+0.28,h["shap_meanabs"]/max(h["shap_meanabs"].max(),1e-9),color="#8e44ad",alpha=.75,height=0.26,label="XGB |SHAP| (scaled)")
ax[1].set_yticks(yy); ax[1].set_yticklabels(h["symbol"],fontsize=8)
ax[1].set_xlabel("importance (normalized)",fontsize=9); ax[1].legend(fontsize=8,loc="lower right")
ax[1].set_title("Top-20 hub genes: 3-method importance",fontsize=12)
plt.tight_layout(); plt.savefig(os.path.join(FIG,"P3_hub_lodo_auc.png"),dpi=160,bbox_inches="tight")
print("saved figure ->",os.path.join(FIG,"P3_hub_lodo_auc.png"))
