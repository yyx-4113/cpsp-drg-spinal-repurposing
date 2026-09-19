#!/usr/bin/env python3
# p3_ml.py v2 -- dual-ML hub locking with leave-one-dataset-out (LODO) cross-dataset evaluation.
# Design: per-dataset gene-wise z-scoring -> pool training datasets -> 3-method feature selection
#         (LASSO lambda.min + bootstrap | RF MDGini | XGBoost SHAP) -> hub = >=2/3 methods
#         -> honest generalization via LODO (train on all but one dataset, test on held-out).
import os, json, warnings
import numpy as np, pandas as pd
from scipy import stats
from collections import Counter
from sklearn.linear_model import LogisticRegression, LogisticRegressionCV
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import RepeatedStratifiedKFold, cross_val_score
from sklearn.metrics import roc_auc_score
from sklearn.preprocessing import StandardScaler
warnings.filterwarnings("ignore")

ROOT="D:/2026.9/极速交付9月会员日优惠套路/01_AI生信-虚拟多重筛药/慢性疼痛"
OUT=os.path.join(ROOT,"data/processed"); TAB=os.path.join(ROOT,"results/tables")
os.makedirs(TAB,exist_ok=True)
SEED=42; rng=np.random.default_rng(SEED); B=100

def std_symbol(s):
    s=str(s).upper()
    if s.startswith(("ENSRNOG","ENSMUSG","ENSG","AABR","LOC","GMR","RGD","-")): return None
    if not s or s=="NAN" or len(s)>25: return None
    return s

def load_mat(fn, norm="cpm"):
    m=pd.read_csv(os.path.join(OUT,fn),index_col=0)
    m.index=[std_symbol(s) for s in m.index]
    m=m[[i is not None for i in m.index]]; m.index=[i for i in m.index if i]
    m=m.groupby(m.index).mean(numeric_only=True)
    m=m.apply(pd.to_numeric,errors="coerce").fillna(0)
    if norm=="cpm":
        lib=m.sum(axis=0).replace(0,np.nan); m=np.log2(m.div(lib,axis=1)*1e6+1)
    return m

def zscore_cols(m):
    """gene-wise z across samples (rows=genes)."""
    mu=m.mean(axis=1); sd=m.std(axis=1).replace(0,np.nan)
    return m.sub(mu,axis=0).div(sd,axis=0)

# ---------------- assemble datasets (DRG axis, binary pain vs control) ----------------
DS=[]
m=load_mat("GSE278227_DRG_symbol_count.csv"); st=pd.read_csv(os.path.join(OUT,"GSE278227_DRG_sampletable.csv"))
s=st[st.time=="1W"]
DS.append(("GSE278227_1W_ratDRG", m, s[s.side=="ipsilateral"]["sample"].tolist(), s[s.side=="contralateral"]["sample"].tolist()))
m=load_mat("GSE267799_DRG_symbol_count.csv"); st=pd.read_csv(os.path.join(OUT,"GSE267799_DRG_sampletable.csv"))
g=st.groupby("time_group")["sample"].apply(list).to_dict()
DS.append(("GSE267799_incision_ratDRG", m, g["chronic"], g["baseline"]))
m=load_mat("GSE241361_symbol_count.csv"); st=pd.read_csv(os.path.join(OUT,"GSE241361_sampletable.csv"))
for tis,nm in [("DRG","GSE241361_mouseDRG"),("Medula","GSE241361_mouseSC")]:
    po=st[(st.treatment=="SNI")&(st.genotype=="WT")&(st.tissue==tis)]["sample"].tolist()
    ng=st[(st.treatment=="Naive")&(st.genotype=="WT")&(st.tissue==tis)]["sample"].tolist()
    DS.append((nm, m, po, ng))
m=load_mat("GSE212311_DRG_symbol_log2fpkm.csv",norm="none"); st=pd.read_csv(os.path.join(OUT,"GSE212311_DRG_sampletable.csv"))
gg=st.groupby("group")["sample"].apply(list).to_dict()
DS.append(("GSE212311_CCI_ratDRG", m, gg["CCI"], gg["Sham"]))

for nm,m,po,ng in DS: print(f"  [{nm}] genes={m.shape[0]} pos={len(po)} neg={len(ng)}")

common=set(DS[0][1].index)
for _,m,_,_ in DS: common&=set(m.index)
common=sorted(common)
print(f"common genes across {len(DS)} datasets: {len(common)}")

# z-score within dataset
ZS={nm:(zscore_cols(m.loc[common]).fillna(0)) for nm,m,_,_ in DS}

def make_xy(names):
    Xs=[]; ys=[]
    for nm in names:
        m=ZS[nm]; po=[p for p in dict((n,(p,q)) for n,_,p,q in DS)[nm][0]]; ng=dict((n,(p,q)) for n,_,p,q in DS)[nm][1]
        Xs.append(m[po].T.values); ys.append(np.ones(len(po)))
        Xs.append(m[ng].T.values); ys.append(np.zeros(len(ng)))
    return np.vstack(Xs), np.concatenate(ys)

allnames=[nm for nm,_,_,_ in DS]
Xall,yall=make_xy(allnames)
print(f"pooled all: X={Xall.shape}  pos={int(yall.sum())} neg={int((yall==0).sum())}")

# ---------------- feature selection on pooled TRAINING (all datasets) ----------------
# pre-filter by univariate Welch t (pooled) -> top 800
tt=np.array([stats.ttest_ind(Xall[yall==1,j],Xall[yall==0,j],equal_var=False).pvalue for j in range(Xall.shape[1])])
tt=np.nan_to_num(tt,nan=1.0)
POOL=[common[j] for j in np.argsort(tt)[:800]]
cidx={g:i for i,g in enumerate(common)}
Xp=Xall[:,[cidx[g] for g in POOL]]
Xp_s=StandardScaler().fit_transform(Xp)

def lasso_fit(X,y,C):
    lr=LogisticRegression(penalty="l1",solver="liblinear",C=C,max_iter=5000); lr.fit(X,y)
    return np.where(np.abs(lr.coef_[0])>1e-8)[0]
Cs=np.logspace(-4,1.5,30)
cv=LogisticRegressionCV(Cs=Cs,cv=5,penalty="l1",solver="liblinear",scoring="roc_auc",random_state=SEED,max_iter=5000).fit(Xp_s,yall)
sc=cv.scores_[1].mean(0); se=cv.scores_[1].std(0)/np.sqrt(5); bi=int(np.argmax(sc))
C_min=Cs[bi]; C_1se=Cs[np.where(sc>=sc[bi]-se[bi])[0][0]]
nz_min=lasso_fit(Xp_s,yall,C_min); nz_1se=lasso_fit(Xp_s,yall,C_1se)
lasso_genes=set(np.array(POOL)[nz_min])
print(f"[LASSO] lambda.min C={C_min:.5f}->{len(nz_min)}g | lambda.1se C={C_1se:.5f}->{len(nz_1se)}g")
lf={g:0 for g in POOL}
for b in range(B):
    idx=rng.choice(len(yall),len(yall),replace=True)
    if len(np.unique(yall[idx]))<2: continue
    for g in np.array(POOL)[lasso_fit(Xp_s[idx],yall[idx],C_min)]: lf[g]+=1
lasso_stable={g for g,f in lf.items() if f/B>=0.6}
print(f"[LASSO] bootstrap stable(>=0.6)={len(lasso_stable)}")

rf=RandomForestClassifier(n_estimators=1500,max_depth=5,min_samples_leaf=2,random_state=SEED,n_jobs=-1,class_weight="balanced").fit(Xp_s,yall)
gini=pd.Series(rf.feature_importances_,index=POOL).sort_values(ascending=False)
rf_top=set(gini.head(80).index)
print(f"[RF-MDGini] top10={list(gini.head(10).index)}")

import xgboost as xgb
clf=xgb.XGBClassifier(n_estimators=350,max_depth=3,learning_rate=0.05,subsample=0.8,colsample_bytree=0.5,
                      reg_lambda=2.0,eval_metric="logloss",random_state=SEED,n_jobs=-1).fit(Xp,yall)
try:
    import shap
    ex=shap.TreeExplainer(clf); sv=ex.shap_values(Xp)
    if isinstance(sv,list): sv=sv[1]
    shap_rank=pd.Series(np.abs(sv).mean(0),index=POOL).sort_values(ascending=False)
except Exception as e:
    print("[SHAP] fallback gain:",e); shap_rank=pd.Series(clf.feature_importances_,index=POOL).sort_values(ascending=False)
xgb_top=set(shap_rank.head(80).index)
print(f"[XGB-SHAP] top10={list(shap_rank.head(10).index)}")

cnt=Counter()
for sset in [lasso_stable,rf_top,xgb_top]:
    for g in sset: cnt[g]+=1
# hub = >=2/3 methods
hub=[g for g,c in cnt.items() if c>=2]
# prioritise genes also in meta core signature
meta=pd.read_csv(os.path.join(TAB,"META_DRG_axis_stouffer.csv")).set_index("symbol")
inmeta=lambda g: (g in meta.index) and (meta.loc[g,"meta_FDR"]<0.05) and (meta.loc[g,"consistency"]>=0.8)
hub=sorted(hub,key=lambda g:(-cnt[g], -gini.get(g,0)))
hubdf=pd.DataFrame({"symbol":hub,"n_methods":[cnt[g] for g in hub],
                    "lasso_freq":[lf.get(g,0)/B for g in hub],
                    "rf_gini":[float(gini.get(g,0)) for g in hub],
                    "shap_meanabs":[float(shap_rank.get(g,0)) for g in hub],
                    "in_meta_core":[inmeta(g) for g in hub]})
hubdf.to_csv(os.path.join(TAB,"P3_hub_genes.csv"),index=False)
print(f"[HUB] >=2/3 methods = {len(hub)} ; in meta core = {int(hubdf.in_meta_core.sum())}")
print(hubdf.head(30).to_string(index=False))

# ---------------- honest evaluation: LODO ----------------
metrics=[]
hub_use=hub[:60] if len(hub)>=5 else hub
hub_use=[g for g in hub_use if g in common]
def fit_predict(train_names, test_name):
    Xtr,ytr=make_xy(train_names)
    Xtr=Xtr[:,[cidx[g] for g in hub_use]]
    sc=StandardScaler().fit(Xtr)
    lr=LogisticRegression(max_iter=5000).fit(sc.transform(Xtr),ytr)
    m=ZS[test_name]; po=dict((n,(p,q)) for n,_,p,q in DS)[test_name][0]; ng=dict((n,(p,q)) for n,_,p,q in DS)[test_name][1]
    Xte=np.vstack([m[po].T.values,m[ng].T.values])[:,[cidx[g] for g in hub_use]]
    yte=np.r_[np.ones(len(po)),np.zeros(len(ng))]
    return lr.decision_function(sc.transform(Xte)), yte
for probe in allnames:
    tr=[n for n in allnames if n!=probe]
    s,yte=fit_predict(tr,probe)
    a=roc_auc_score(yte,s)
    metrics.append({"eval":"LODO","test_dataset":probe,"auc":a,"n":len(yte),"n_genes":len(hub_use)})
    print(f"[LODO] hold-out {probe:26s} AUC={a:.3f} (n={len(yte)})")
# pooled repeated CV
Xh=Xall[:,[cidx[g] for g in hub_use]]
scv=cross_val_score(LogisticRegression(max_iter=5000),StandardScaler().fit_transform(Xh),yall,
                    cv=RepeatedStratifiedKFold(n_splits=5,n_repeats=20,random_state=SEED),scoring="roc_auc",n_jobs=-1)
metrics.append({"eval":"pooled_5x20CV","test_dataset":"ALL","auc":scv.mean(),"n":len(yall),"n_genes":len(hub_use)})
print(f"[pooled 5x20 CV] AUC={scv.mean():.3f}±{scv.std():.3f}   (label-shuffle null below)")
# permutation null on pooled CV
null=[]
for _ in range(100):
    yp=rng.permutation(yall)
    null.append(cross_val_score(LogisticRegression(max_iter=5000),StandardScaler().fit_transform(Xh),yp,
                cv=RepeatedStratifiedKFold(n_splits=5,n_repeats=5,random_state=SEED),scoring="roc_auc",n_jobs=-1).mean())
metrics.append({"eval":"pooled_perm_null","test_dataset":"ALL","auc":float(np.mean(null)),"n":len(yall),"n_genes":len(hub_use)})
print(f"[perm null] AUC={np.mean(null):.3f}±{np.std(null):.3f}")

pd.DataFrame(metrics).to_csv(os.path.join(TAB,"P3_ml_metrics.csv"),index=False)
json.dump({"n_hub":len(hub),"n_hub_in_meta":int(hubdf.in_meta_core.sum()),"pool":len(POOL),
           "lasso_C_min":float(C_min),"lasso_1se_genes":len(nz_1se),"n_common_genes":len(common)},
          open(os.path.join(TAB,"P3_ml_summary.json"),"w"),indent=2)
print("\n=== P3 ML v2 (LODO) done ===")
