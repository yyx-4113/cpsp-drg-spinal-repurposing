#!/usr/bin/env python3
# p3_ml_leakage_controlled.py
# T0-1 fix: the original p3_ml.py selected features on the POOLED 72-sample matrix and then
# reused that global feature set for every LODO fold -> feature-selection leakage. Here feature
# selection is performed INSIDE each training fold (Top-800 Welch on the 4 training datasets only,
# + LASSO / RF / XGBoost selectors on training), then tested on the held-out 5th dataset.
# These AUCs are the leakage-controlled generalisation metric. The global 35-hub candidate list
# (P3_hub_genes.csv) is left untouched as a descriptive product.
import os, json, warnings
import numpy as np, pandas as pd
from scipy import stats
from sklearn.linear_model import LogisticRegression, LogisticRegressionCV
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import RepeatedStratifiedKFold, cross_val_predict
from sklearn.metrics import roc_auc_score
from sklearn.preprocessing import StandardScaler
warnings.filterwarnings("ignore")

ROOT="D:/2026.9/极速交付9月会员日优惠套路/01_AI生信-虚拟多重筛药/慢性疼痛"
OUT=os.path.join(ROOT,"data/processed"); TAB=os.path.join(ROOT,"results/tables")
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
    mu=m.mean(axis=1); sd=m.std(axis=1).replace(0,np.nan)
    return m.sub(mu,axis=0).div(sd,axis=0)

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

common=set(DS[0][1].index)
for _,m,_,_ in DS: common&=set(m.index)
common=sorted(common)
ZS={nm:(zscore_cols(m.loc[common]).fillna(0)) for nm,m,_,_ in DS}
cidx={g:i for i,g in enumerate(common)}

def make_xy(names):
    Xs=[]; ys=[]
    D=dict((n,(p,q)) for n,_,p,q in DS)
    for nm in names:
        m=ZS[nm]; po=D[nm][0]; ng=D[nm][1]
        Xs.append(m[po].T.values); ys.append(np.ones(len(po)))
        Xs.append(m[ng].T.values); ys.append(np.zeros(len(ng)))
    return np.vstack(Xs), np.concatenate(ys)

allnames=[nm for nm,_,_,_ in DS]

def delong_bootstrap_ci(yte, score, n_boot=2000):
    """Bootstrap CI for AUC (robust at small n)."""
    yte=np.asarray(yte); score=np.asarray(score)
    auc=roc_auc_score(yte,score)
    rng_loc=np.random.default_rng(SEED)
    aucs=[]
    idx=np.arange(len(yte))
    for _ in range(n_boot):
        b=rng_loc.choice(idx,len(idx),replace=True)
        if len(np.unique(yte[b]))<2: continue
        aucs.append(roc_auc_score(yte[b],score[b]))
    if len(aucs)<10: return auc, (float("nan"),float("nan"))
    lo,hi=np.percentile(aucs,[2.5,97.5])
    return auc,(float(lo),float(hi))

def select_features(Xtr,ytr,POOL_LOCAL,POOL_IDX,top=800,rf_top=80,xgb_top=80):
    """Within-fold selection: Welch pre-filter + LASSO + RF + XGBoost, all on training only."""
    # Welch univariate pre-filter
    tt=np.array([stats.ttest_ind(Xtr[ytr==1,j],Xtr[ytr==0,j],equal_var=False).pvalue for j in range(Xtr.shape[1])])
    tt=np.nan_to_num(tt,nan=1.0)
    POOL_ARR=np.array(POOL_LOCAL)
    pre=POOL_ARR[np.argsort(tt)[:top]]
    pi={g:i for i,g in enumerate(POOL_LOCAL)}
    Xpre=Xtr[:,[pi[g] for g in pre]]
    Xs=StandardScaler().fit_transform(Xpre)
    # LASSO
    Cs=np.logspace(-4,1.5,30)
    cv=LogisticRegressionCV(Cs=Cs,cv=5,penalty="l1",solver="liblinear",scoring="roc_auc",random_state=SEED,max_iter=5000).fit(Xs,ytr)
    sc=cv.scores_[1].mean(0); se=cv.scores_[1].std(0)/np.sqrt(5); bi=int(np.argmax(sc))
    C_min=Cs[bi]
    lr=LogisticRegression(penalty="l1",solver="liblinear",C=C_min,max_iter=5000).fit(Xs,ytr)
    lasso_set=set(np.array(pre)[np.where(np.abs(lr.coef_[0])>1e-8)[0]])
    # RF
    rf=RandomForestClassifier(n_estimators=800,max_depth=5,min_samples_leaf=2,random_state=SEED,n_jobs=-1,class_weight="balanced").fit(Xs,ytr)
    rf_set=set(pd.Series(rf.feature_importances_,index=pre).sort_values(ascending=False).head(rf_top).index)
    # XGBoost (gain importance, no SHAP to keep it fast)
    import xgboost as xgb
    clf=xgb.XGBClassifier(n_estimators=300,max_depth=3,learning_rate=0.05,subsample=0.8,colsample_bytree=0.5,
                          reg_lambda=2.0,eval_metric="logloss",random_state=SEED,n_jobs=-1).fit(Xtr,ytr)
    xgb_set=set(pd.Series(clf.feature_importances_,index=POOL_LOCAL).sort_values(ascending=False).head(xgb_top).index)
    sel=lasso_set|rf_set|xgb_set
    return sel

metrics=[]
for probe in allnames:
    tr=[n for n in allnames if n!=probe]
    Xtr,ytr=make_xy(tr)
    # restrict to common genes present in both train and test
    Xte,yte=make_xy([probe])
    # use only genes in common for both
    Xtr=Xtr[:,[cidx[g] for g in common]]
    Xte=Xte[:,[cidx[g] for g in common]]
    sel=select_features(Xtr,ytr,common,{})
    if len(sel)<5:
        print(f"[LC-LODO] {probe}: too few selected ({len(sel)}), skip"); continue
    si={g:i for i,g in enumerate(common)}
    Xtr_s=StandardScaler().fit_transform(Xtr[:,[si[g] for g in sel]])
    Xte_s=StandardScaler().fit_transform(Xte[:,[si[g] for g in sel]])
    lr=LogisticRegression(max_iter=5000).fit(Xtr_s,ytr)
    s=lr.decision_function(Xte_s)
    auc,(lo,hi)=delong_bootstrap_ci(yte,s)
    metrics.append({"eval":"LC-LODO","test_dataset":probe,"auc":auc,"ci_lo":lo,"ci_hi":hi,
                    "n":len(yte),"n_selected":len(sel)})
    print(f"[LC-LODO] hold-out {probe:26s} AUC={auc:.3f} [{lo:.3f},{hi:.3f}] (n={len(yte)}, sel={len(sel)})")

pd.DataFrame(metrics).to_csv(os.path.join(TAB,"P3_lodo_auc_ci_leakage_controlled.csv"),index=False)
print("\n=== Leakage-controlled LODO done ===")
print(pd.DataFrame(metrics).to_string(index=False))
