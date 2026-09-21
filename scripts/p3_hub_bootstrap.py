#!/usr/bin/env python3
# p3_hub_bootstrap.py -- T1-12 hub-stability bootstrap.
# Resample the 72 pooled samples (with replacement) B=200 times; on each resample recompute the
# 3-method selection (LASSO lambda.min + RF MDGini top80 + XGBoost |SHAP| top80) and hub status
# (>=2/3 methods). Report, for each of the 35 published hubs, the hub-selection frequency and
# per-method frequency, plus a "borderline" flag for hubs near the 2/3 consensus threshold.
import os, json, warnings, numpy as np, pandas as pd
from scipy import stats
from sklearn.linear_model import LogisticRegression, LogisticRegressionCV
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler
import xgboost as xgb
warnings.filterwarnings("ignore")
ROOT="D:/2026.9/极速交付9月会员日优惠套路/01_AI生信-虚拟多重筛药/慢性疼痛"
OUT=os.path.join(ROOT,"data/processed"); TAB=os.path.join(ROOT,"results/tables")
SEED=42; rng=np.random.default_rng(SEED); B=200

def std_symbol(s):
    s=str(s).upper()
    if s.startswith(("ENSRNOG","ENSMUSG","ENSG","AABR","LOC","GMR","RGD","-")): return None
    if not s or s=="NAN" or len(s)>25: return None
    return s
def load_mat(fn, norm="cpm"):
    m=pd.read_csv(os.path.join(OUT,fn),index_col=0)
    m.index=[std_symbol(s) for s in m.index]
    m=m[[i is not None for i in m.index]]; m.index=[i for i in m.index if i]
    m=m.groupby(m.index).mean(numeric_only=True).apply(pd.to_numeric,errors="coerce").fillna(0)
    if norm=="cpm":
        lib=m.sum(axis=0).replace(0,np.nan); m=np.log2(m.div(lib,axis=1)*1e6+1)
    return m
def zscore_cols(m):
    mu=m.mean(axis=1); sd=m.std(axis=1).replace(0,np.nan)
    return m.sub(mu,axis=0).div(sd,axis=0)

DS=[]
m=load_mat("GSE278227_DRG_symbol_count.csv"); st=pd.read_csv(os.path.join(OUT,"GSE278227_DRG_sampletable.csv"))
s=st[st.time=="1W"]; DS.append(("GSE278227_1W_ratDRG",m,s[s.side=="ipsilateral"]["sample"].tolist(),s[s.side=="contralateral"]["sample"].tolist()))
m=load_mat("GSE267799_DRG_symbol_count.csv"); st=pd.read_csv(os.path.join(OUT,"GSE267799_DRG_sampletable.csv"))
g=st.groupby("time_group")["sample"].apply(list).to_dict(); DS.append(("GSE267799_incision_ratDRG",m,g["chronic"],g["baseline"]))
m=load_mat("GSE241361_symbol_count.csv"); st=pd.read_csv(os.path.join(OUT,"GSE241361_sampletable.csv"))
for tis,nm in [("DRG","GSE241361_mouseDRG"),("Medula","GSE241361_mouseSC")]:
    po=st[(st.treatment=="SNI")&(st.genotype=="WT")&(st.tissue==tis)]["sample"].tolist()
    ng=st[(st.treatment=="Naive")&(st.genotype=="WT")&(st.tissue==tis)]["sample"].tolist()
    DS.append((nm,m,po,ng))
m=load_mat("GSE212311_DRG_symbol_log2fpkm.csv",norm="none"); st=pd.read_csv(os.path.join(OUT,"GSE212311_DRG_sampletable.csv"))
gg=st.groupby("group")["sample"].apply(list).to_dict(); DS.append(("GSE212311_CCI_ratDRG",m,gg["CCI"],gg["Sham"]))

common=set(DS[0][1].index)
for _,m,_,_ in DS: common&=set(m.index)
common=sorted(common)
ZS={nm:zscore_cols(m.loc[common]).fillna(0) for nm,m,_,_ in DS}
def make_xy(names):
    Xs=[]; ys=[]
    for nm in names:
        po,ng=dict((n,(p,q)) for n,_,p,q in DS)[nm]
        Xs.append(ZS[nm][po].T.values); ys.append(np.ones(len(po)))
        Xs.append(ZS[nm][ng].T.values); ys.append(np.zeros(len(ng)))
    return np.vstack(Xs), np.concatenate(ys)
allnames=[nm for nm,_,_,_ in DS]
Xall,yall=make_xy(allnames)
tt=np.array([stats.ttest_ind(Xall[yall==1,j],Xall[yall==0,j],equal_var=False).pvalue for j in range(Xall.shape[1])])
tt=np.nan_to_num(tt,nan=1.0); POOL=[common[j] for j in np.argsort(tt)[:800]]
cidx={g:i for i,g in enumerate(common)}; Xp=Xall[:,[cidx[g] for g in POOL]]

# fixed C_min from full data (avoid re-running CV per resample)
cv=LogisticRegressionCV(Cs=np.logspace(-4,1.5,30),cv=5,penalty="l1",solver="liblinear",scoring="roc_auc",random_state=SEED,max_iter=5000).fit(StandardScaler().fit_transform(Xp),yall)
sc=cv.scores_[1].mean(0); se=cv.scores_[1].std(0)/np.sqrt(5); bi=int(np.argmax(sc))
Cs=np.logspace(-4,1.5,30); C_min=Cs[bi]
def lasso_nonzero(X,y,C):
    lr=LogisticRegression(penalty="l1",solver="liblinear",C=C,max_iter=5000).fit(X,y)
    return set(np.where(np.abs(lr.coef_[0])>1e-8)[0])

pub=pd.read_csv(os.path.join(TAB,"P3_hub_genes.csv"))
pubhub=pub.symbol.tolist()
hub_freq={g:0 for g in pubhub}
lasso_f={g:0 for g in pubhub}; rf_f={g:0 for g in pubhub}; xgb_f={g:0 for g in pubhub}
print(f"bootstrap B={B} over {len(Xall)} pooled samples; POOL={len(POOL)}")
for b in range(B):
    idx=rng.choice(len(yall),len(yall),replace=True)
    if len(np.unique(yall[idx]))<2: continue
    Xb=Xp[idx]; yb=yall[idx]; Xbs=StandardScaler().fit_transform(Xb)
    lnz=lasso_nonzero(Xbs,yb,C_min)
    rf=RandomForestClassifier(n_estimators=500,max_depth=5,min_samples_leaf=2,random_state=SEED+b,n_jobs=-1,class_weight="balanced").fit(Xbs,yb)
    rftop=set(pd.Series(rf.feature_importances_,index=POOL).sort_values(ascending=False).head(80).index)
    clf=xgb.XGBClassifier(n_estimators=200,max_depth=3,learning_rate=0.05,subsample=0.8,colsample_bytree=0.5,reg_lambda=2.0,eval_metric="logloss",random_state=SEED+b,n_jobs=-1).fit(Xp,yb)
    sv=clf.get_booster().predict(xgb.DMatrix(Xp),pred_contribs=True)
    sv=sv[:, :-1]  # drop the bias column (n_features+1 returned)
    shap_rank=pd.Series(np.abs(sv).mean(0),index=POOL).sort_values(ascending=False)
    xgbtop=set(shap_rank.head(80).index)
    for g in pubhub:
        gi=POOL.index(g) if g in POOL else None
        if gi is None: continue
        vot=0
        if g in lnz: lasso_f[g]+=1; vot+=1
        if g in rftop: rf_f[g]+=1; vot+=1
        if g in xgbtop: xgb_f[g]+=1; vot+=1
        if vot>=2: hub_freq[g]+=1
    if (b+1)%40==0: print(f"  resample {b+1}/{B} done")
df=pd.DataFrame({"symbol":pubhub,
                 "hub_freq":[hub_freq[g]/B for g in pubhub],
                 "lasso_freq":[lasso_f[g]/B for g in pubhub],
                 "rf_freq":[rf_f[g]/B for g in pubhub],
                 "xgb_freq":[xgb_f[g]/B for g in pubhub],
                 "n_methods_pub":pub.set_index("symbol").loc[pubhub,"n_methods"].values})
df["borderline"]=df.hub_freq.between(0.5,0.75)
df=df.sort_values("hub_freq",ascending=False)
df.to_csv(os.path.join(TAB,"P3_hub_bootstrap.csv"),index=False)
print("\n=== hub stability (B=200) ===")
print(f"stable (hub_freq>=0.9): {int((df.hub_freq>=0.9).sum())}/{len(df)}")
print(f"borderline (0.5-0.75): {int(df.borderline.sum())}")
print(df.to_string(index=False, float_format=lambda v:f"{v:.3f}"))
