#!/usr/bin/env python3
# A3 SCRATCH probe (audit only; writes NOTHING into results/tables).
# Question: in scripts/p3_hub_bootstrap.py / scripts/p7_targetset_bootstrap.py the XGBoost
# selector is fit on (Xp, yb) instead of (Xp[idx], yb) == (Xbs, yb). Is the resampled label
# vector paired with the resampled feature rows? Compare the published (buggy) variant with
# an index-aligned (fixed) variant on identical resamples.
import os, json, warnings, numpy as np, pandas as pd
from scipy import stats
from sklearn.linear_model import LogisticRegression, LogisticRegressionCV
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler
import xgboost as xgb
warnings.filterwarnings("ignore")

ROOT = "D:/2026.9/极速交付9月会员日优惠套路/01_AI生信-虚拟多重筛药/慢性疼痛"
OUT = os.path.join(ROOT, "data/processed"); TAB = os.path.join(ROOT, "results/tables")
SEED = 42; B = 100

def std_symbol(s):
    s = str(s).upper()
    if s.startswith(("ENSRNOG", "ENSMUSG", "ENSG", "AABR", "LOC", "GMR", "RGD", "-")): return None
    if not s or s == "NAN" or len(s) > 25: return None
    return s

def load_mat(fn, norm="cpm"):
    m = pd.read_csv(os.path.join(OUT, fn), index_col=0)
    m.index = [std_symbol(s) for s in m.index]
    m = m[[i is not None for i in m.index]]; m.index = [i for i in m.index if i]
    m = m.groupby(m.index).mean(numeric_only=True).apply(pd.to_numeric, errors="coerce").fillna(0)
    if norm == "cpm":
        lib = m.sum(axis=0).replace(0, np.nan); m = np.log2(m.div(lib, axis=1) * 1e6 + 1)
    return m

def zscore_cols(m):
    mu = m.mean(axis=1); sd = m.std(axis=1).replace(0, np.nan)
    return m.sub(mu, axis=0).div(sd, axis=0)

DS = []
m = load_mat("GSE278227_DRG_symbol_count.csv"); st = pd.read_csv(os.path.join(OUT, "GSE278227_DRG_sampletable.csv"))
s = st[st.time == "1W"]; DS.append(("GSE278227_1W_ratDRG", m, s[s.side == "ipsilateral"]["sample"].tolist(), s[s.side == "contralateral"]["sample"].tolist()))
m = load_mat("GSE267799_DRG_symbol_count.csv"); st = pd.read_csv(os.path.join(OUT, "GSE267799_DRG_sampletable.csv"))
g = st.groupby("time_group")["sample"].apply(list).to_dict(); DS.append(("GSE267799_incision_ratDRG", m, g["chronic"], g["baseline"]))
m = load_mat("GSE241361_symbol_count.csv"); st = pd.read_csv(os.path.join(OUT, "GSE241361_sampletable.csv"))
for tis, nm in [("DRG", "GSE241361_mouseDRG"), ("Medula", "GSE241361_mouseSC")]:
    po = st[(st.treatment == "SNI") & (st.genotype == "WT") & (st.tissue == tis)]["sample"].tolist()
    ng = st[(st.treatment == "Naive") & (st.genotype == "WT") & (st.tissue == tis)]["sample"].tolist()
    DS.append((nm, m, po, ng))
m = load_mat("GSE212311_DRG_symbol_log2fpkm.csv", norm="none"); st = pd.read_csv(os.path.join(OUT, "GSE212311_DRG_sampletable.csv"))
gg = st.groupby("group")["sample"].apply(list).to_dict(); DS.append(("GSE212311_CCI_ratDRG", m, gg["CCI"], gg["Sham"]))

common = set(DS[0][1].index)
for _, mm, _, _ in DS: common &= set(mm.index)
common = sorted(common)
ZS = {nm: zscore_cols(mm.loc[common]).fillna(0) for nm, mm, _, _ in DS}

def make_xy(names):
    Xs = []; ys = []
    for nm in names:
        po, ng = dict((n, (p, q)) for n, _, p, q in DS)[nm]
        Xs.append(ZS[nm][po].T.values); ys.append(np.ones(len(po)))
        Xs.append(ZS[nm][ng].T.values); ys.append(np.zeros(len(ng)))
    return np.vstack(Xs), np.concatenate(ys)

Xall, yall = make_xy([nm for nm, _, _, _ in DS])
tt = np.array([stats.ttest_ind(Xall[yall == 1, j], Xall[yall == 0, j], equal_var=False).pvalue for j in range(Xall.shape[1])])
tt = np.nan_to_num(tt, nan=1.0); POOL = [common[j] for j in np.argsort(tt)[:800]]
cidx = {g: i for i, g in enumerate(common)}; Xp = Xall[:, [cidx[g] for g in POOL]]
print(f"POOL={len(POOL)}  n_samples={len(yall)}")

cv = LogisticRegressionCV(Cs=np.logspace(-4, 1.5, 30), cv=5, penalty="l1", solver="liblinear",
                          scoring="roc_auc", random_state=SEED, max_iter=5000).fit(StandardScaler().fit_transform(Xp), yall)
Cs = np.logspace(-4, 1.5, 30); C_min = Cs[int(np.argmax(cv.scores_[1].mean(0)))]
print("C_min =", C_min)

def lasso_nonzero(X, y, C):
    lr = LogisticRegression(penalty="l1", solver="liblinear", C=C, max_iter=5000).fit(X, y)
    return set(np.where(np.abs(lr.coef_[0]) > 1e-8)[0])

pub = pd.read_csv(os.path.join(TAB, "P3_hub_genes.csv")); pubhub = pub.symbol.tolist()
DOCK_ELIGIBLE = ["ACVR1","AXL","CDHR5","CTTN","FLNC","FLRT3","GALNS","ITPKC","MAPK14",
                 "NPY","PTPN23","RUBCN","SERPINE1","SLC2A1","TFE3","TNIK","VASH2"]
DOCKED_HUBS = ["ACVR1","AXL","GALNS","ITPKC","MAPK14","SERPINE1","SLC2A1","TNIK","VASH2"]
POOLSET = set(POOL)
elig_in_pool = [g for g in DOCK_ELIGIBLE if g in POOLSET]
dock_in_pool = [g for g in DOCKED_HUBS if g in POOLSET]

res = {k: dict(hub={g:0 for g in pubhub}, las={g:0 for g in pubhub},
               rf={g:0 for g in pubhub}, xgb={g:0 for g in pubhub},
               sizes=[], jac=[], ec=[], dc=[], lasso_nz=[])
       for k in ("published_bug", "index_aligned_fix")}
POOL_IDX = {g: i for i, g in enumerate(POOL)}
for variant in res:
    rng = np.random.default_rng(SEED); done = 0
    for b in range(B):
        idx = rng.choice(len(yall), len(yall), replace=True)
        if len(np.unique(yall[idx])) < 2: continue
        done += 1
        Xb = Xp[idx]; yb = yall[idx]; Xbs = StandardScaler().fit_transform(Xb)
        lnz = lasso_nonzero(Xbs, yb, C_min)
        res[variant]["lasso_nz"].append(len(lnz))
        rf = RandomForestClassifier(n_estimators=500, max_depth=5, min_samples_leaf=2,
                                    random_state=SEED + b, n_jobs=-1, class_weight="balanced").fit(Xbs, yb)
        rftop = set(pd.Series(rf.feature_importances_, index=POOL).sort_values(ascending=False).head(80).index)
        if variant == "published_bug":
            X_fit, X_shap = Xp, Xp
        else:
            X_fit, X_shap = Xbs, Xbs
        clf = xgb.XGBClassifier(n_estimators=200, max_depth=3, learning_rate=0.05, subsample=0.8,
                                colsample_bytree=0.5, reg_lambda=2.0, eval_metric="logloss",
                                random_state=SEED + b, n_jobs=-1).fit(X_fit, yb)
        sv = clf.get_booster().predict(xgb.DMatrix(X_shap), pred_contribs=True)[:, :-1]
        xgbtop = set(pd.Series(np.abs(sv).mean(0), index=POOL).sort_values(ascending=False).head(80).index)
        votes = {}
        for sset in (lnz, rftop, xgbtop):
            for gg in sset: votes[gg] = votes.get(gg, 0) + 1
        hubs_b = {gg for gg, v in votes.items() if v >= 2}
        for gg in pubhub:
            if gg in lnz: res[variant]["las"][gg] += 1
            if gg in rftop: res[variant]["rf"][gg] += 1
            if gg in xgbtop: res[variant]["xgb"][gg] += 1
            if votes.get(gg, 0) >= 2: res[variant]["hub"][gg] += 1
        res[variant]["sizes"].append(len(hubs_b))
        res[variant]["jac"].append(len(hubs_b & set(pubhub)) / len(hubs_b | set(pubhub)) if hubs_b else 0.0)
        res[variant]["ec"].append(sum(1 for gg in elig_in_pool if gg in hubs_b))
        res[variant]["dc"].append(sum(1 for gg in dock_in_pool if gg in hubs_b))
    print(f"[{variant}] done={done}")

print("\n" + "=" * 78)
for variant in res:
    r = res[variant]; n = len(r["sizes"])
    hf = np.array([r["hub"][g] / n for g in pubhub])
    rf = np.array([r["rf"][g] / n for g in pubhub])
    xg = np.array([r["xgb"][g] / n for g in pubhub])
    ec = np.array(r["ec"]); dc = np.array(r["dc"]); sz = np.array(r["sizes"]); jc = np.array(r["jac"])
    print(f"\n--- {variant} (B={n}) ---")
    print(f"  hub_freq      min {hf.min():.3f}  median {np.median(hf):.3f}  max {hf.max():.3f}   >=0.9: {int((hf>=0.9).sum())}/35")
    print(f"  rf_freq       mean {rf.mean():.3f}")
    print(f"  xgb_freq      mean {xg.mean():.3f}   (random-chance expectation = 80/800 = 0.100)")
    print(f"  lasso total selections per resample: mean {np.mean(r['lasso_nz']):.1f}  max {max(r['lasso_nz'])}")
    print(f"  resample hub-set size median {np.median(sz):.0f} IQR [{np.percentile(sz,25):.0f}-{np.percentile(sz,75):.0f}]")
    print(f"  Jaccard vs 35 median {np.median(jc):.3f}")
    print(f"  dock-eligible 17 recovered: mean {ec.mean():.2f} median {np.median(ec):.0f}  P(>=3)={np.mean(ec>=3):.3f}  P(>=5)={np.mean(ec>=5):.3f}")
    print(f"  docked 9 recovered:         mean {dc.mean():.2f} median {np.median(dc):.0f}  P(>=3)={np.mean(dc>=3):.3f}")
json.dump({k: {"hub_freq": {g: v / len(res[k]['sizes']) for g, v in res[k]["hub"].items()},
               "xgb_freq": {g: v / len(res[k]['sizes']) for g, v in res[k]["xgb"].items()},
               "rf_freq": {g: v / len(res[k]['sizes']) for g, v in res[k]["rf"].items()},
               "mean_elig": float(np.mean(res[k]["ec"])), "mean_dock": float(np.mean(res[k]["dc"])),
               "median_size": float(np.median(res[k]["sizes"])),
               "median_jaccard": float(np.median(res[k]["jac"])),
               "P_ge3_17": float(np.mean(np.array(res[k]["ec"]) >= 3)),
               "lasso_mean_nz": float(np.mean(res[k]["lasso_nz"])),
               "xgb_freq_mean": float(np.mean([v / len(res[k]['sizes']) for v in res[k]["xgb"].values()]))}
          for k in res}, open(os.path.join(ROOT, "_scratch", "a3_bootstrap_probe.json"), "w"), indent=2)
print("\n[written] _scratch/a3_bootstrap_probe.json")
