#!/usr/bin/env python3
# p7_targetset_bootstrap.py -- Round-4 review remediation T1-11.
#
# The published bootstrap (scripts/p3_hub_bootstrap.py) reported PER-GENE hub-recovery
# frequency only, so it could not answer "is the docking TARGET SET itself stable?".
# This script re-runs the identical 3-method bootstrap (B=200, SEED=42) and additionally
# records, for every resample, the full recovered hub set. It then asks, for the 17
# dock-eligible hubs (n_holo_PDB >= 1) and the 9 docked hubs:
#   - per-gene recovery frequency
#   - how many of the set are recovered per resample (distribution + P(>=k))
#   - Jaccard overlap of each resample hub set with the published 35-gene set
#
# It does NOT overwrite results/tables/P3_hub_bootstrap.csv (the published artifact).
# Outputs: _R4_targetset_bootstrap.csv, _R4_targetset_bootstrap.json
import os, json, warnings, numpy as np, pandas as pd
from scipy import stats
from sklearn.linear_model import LogisticRegression, LogisticRegressionCV
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler
import xgboost as xgb
warnings.filterwarnings("ignore")

ROOT = "D:/2026.9/极速交付9月会员日优惠套路/01_AI生信-虚拟多重筛药/慢性疼痛"
OUT = os.path.join(ROOT, "data/processed"); TAB = os.path.join(ROOT, "results/tables")
SEED = 42; rng = np.random.default_rng(SEED); B = 200

# 17 dock-eligible hubs (n_holo_PDB >= 1) as stated in the manuscript Results
DOCK_ELIGIBLE = ["ACVR1","AXL","CDHR5","CTTN","FLNC","FLRT3","GALNS","ITPKC","MAPK14",
                 "NPY","PTPN23","RUBCN","SERPINE1","SLC2A1","TFE3","TNIK","VASH2"]
# 9 of the 17 that were actually docked (ADRA2A is the 10th target and is NOT a hub)
DOCKED_HUBS   = ["ACVR1","AXL","GALNS","ITPKC","MAPK14","SERPINE1","SLC2A1","TNIK","VASH2"]

def std_symbol(s):
    s = str(s).upper()
    if s.startswith(("ENSRNOG","ENSMUSG","ENSG","AABR","LOC","GMR","RGD","-")): return None
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
for tis, nm in [("DRG","GSE241361_mouseDRG"),("Medula","GSE241361_mouseSC")]:
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

cv = LogisticRegressionCV(Cs=np.logspace(-4, 1.5, 30), cv=5, penalty="l1", solver="liblinear",
                          scoring="roc_auc", random_state=SEED, max_iter=5000).fit(StandardScaler().fit_transform(Xp), yall)
Cs = np.logspace(-4, 1.5, 30); C_min = Cs[int(np.argmax(cv.scores_[1].mean(0)))]

def lasso_nonzero(X, y, C):
    lr = LogisticRegression(penalty="l1", solver="liblinear", C=C, max_iter=5000).fit(X, y)
    return set(np.where(np.abs(lr.coef_[0]) > 1e-8)[0])

pub = pd.read_csv(os.path.join(TAB, "P3_hub_genes.csv")); pubhub = pub.symbol.tolist()
POOLSET = set(POOL)
elig_in_pool = [g for g in DOCK_ELIGIBLE if g in POOLSET]
dock_in_pool = [g for g in DOCKED_HUBS if g in POOLSET]
print(f"POOL={len(POOL)}  published hubs={len(pubhub)}  dock-eligible in POOL={len(elig_in_pool)}/17  docked in POOL={len(dock_in_pool)}/9")

elig_freq = {g: 0 for g in DOCK_ELIGIBLE}; dock_freq = {g: 0 for g in DOCKED_HUBS}
elig_cnt = []; dock_cnt = []; jac = []; sizes = []
done = 0
for b in range(B):
    idx = rng.choice(len(yall), len(yall), replace=True)
    if len(np.unique(yall[idx])) < 2: continue
    done += 1
    Xb = Xp[idx]; yb = yall[idx]; Xbs = StandardScaler().fit_transform(Xb)
    lnz = lasso_nonzero(Xbs, yb, C_min)
    rf = RandomForestClassifier(n_estimators=500, max_depth=5, min_samples_leaf=2,
                                random_state=SEED + b, n_jobs=-1, class_weight="balanced").fit(Xbs, yb)
    rftop = set(pd.Series(rf.feature_importances_, index=POOL).sort_values(ascending=False).head(80).index)
    clf = xgb.XGBClassifier(n_estimators=200, max_depth=3, learning_rate=0.05, subsample=0.8,
                            colsample_bytree=0.5, reg_lambda=2.0, eval_metric="logloss",
                            random_state=SEED + b, n_jobs=-1).fit(Xp, yb)
    sv = clf.get_booster().predict(xgb.DMatrix(Xp), pred_contribs=True)[:, :-1]
    xgbtop = set(pd.Series(np.abs(sv).mean(0), index=POOL).sort_values(ascending=False).head(80).index)

    votes = {}
    for s_ in (lnz, rftop, xgbtop):
        for g in s_: votes[g] = votes.get(g, 0) + 1
    hubs_b = {g for g, v in votes.items() if v >= 2}
    sizes.append(len(hubs_b))
    jac.append(len(hubs_b & set(pubhub)) / len(hubs_b | set(pubhub)) if hubs_b else 0.0)
    ne = sum(1 for g in elig_in_pool if g in hubs_b)
    nd = sum(1 for g in dock_in_pool if g in hubs_b)
    elig_cnt.append(ne); dock_cnt.append(nd)
    for g in elig_in_pool:
        if g in hubs_b: elig_freq[g] += 1
    for g in dock_in_pool:
        if g in hubs_b: dock_freq[g] += 1
    if (b + 1) % 25 == 0: print(f"  resample {b+1}/{B} done", flush=True)

sizes = np.array(sizes); jac = np.array(jac); ec = np.array(elig_cnt); dc = np.array(dock_cnt)
print(f"\nresamples completed: {done}")
print(f"resample hub-set size: median {np.median(sizes):.0f}, IQR [{np.percentile(sizes,25):.0f}-{np.percentile(sizes,75):.0f}]")
print(f"Jaccard vs published 35: median {np.median(jac):.3f}, IQR [{np.percentile(jac,25):.3f}-{np.percentile(jac,75):.3f}]")
print(f"\ndock-ELIGIBLE (n={len(elig_in_pool)} in POOL) recovered per resample: mean {ec.mean():.2f}, median {np.median(ec):.0f}, min {ec.min()}, max {ec.max()}")
for k in (1, 3, 5, 9, 13, 17):
    print(f"  P(>= {k:2d} of {len(elig_in_pool)} recovered) = {np.mean(ec >= k):.3f}")
print(f"\nDOCKED hubs (n={len(dock_in_pool)} in POOL) recovered per resample: mean {dc.mean():.2f}, median {np.median(dc):.0f}, min {dc.min()}, max {dc.max()}")
for k in (1, 3, 5, 9):
    print(f"  P(>= {k} of {len(dock_in_pool)} recovered) = {np.mean(dc >= k):.3f}")

rows = []
for g in DOCK_ELIGIBLE:
    rows.append({"symbol": g, "set": "dock_eligible_17", "in_ML_pool": g in POOLSET,
                 "recovery_freq": elig_freq.get(g, 0) / max(done, 1)})
for g in DOCKED_HUBS:
    rows.append({"symbol": g, "set": "docked_9", "in_ML_pool": g in POOLSET,
                 "recovery_freq": dock_freq.get(g, 0) / max(done, 1)})
df = pd.DataFrame(rows).sort_values(["set", "recovery_freq"], ascending=[True, False])
df.to_csv(os.path.join(TAB, "_R4_targetset_bootstrap.csv"), index=False)
print("\n" + df.to_string(index=False, float_format=lambda v: f"{v:.3f}"))

json.dump({
    "B": B, "resamples_completed": done, "POOL_size": len(POOL),
    "hub_set_size": {"median": float(np.median(sizes)),
                     "q25": float(np.percentile(sizes, 25)), "q75": float(np.percentile(sizes, 75))},
    "jaccard_vs_published35": {"median": round(float(np.median(jac)), 3),
                               "q25": round(float(np.percentile(jac, 25)), 3),
                               "q75": round(float(np.percentile(jac, 75)), 3)},
    "dock_eligible_17": {"n_in_pool": len(elig_in_pool),
                         "mean_recovered": round(float(ec.mean()), 2),
                         "median_recovered": float(np.median(ec)),
                         "min": int(ec.min()), "max": int(ec.max()),
                         "P_ge1": round(float(np.mean(ec >= 1)), 3),
                         "P_ge2": round(float(np.mean(ec >= 2)), 3),
                         "P_ge3": round(float(np.mean(ec >= 3)), 3),
                         "P_ge4": round(float(np.mean(ec >= 4)), 3),
                         "P_ge5": round(float(np.mean(ec >= 5)), 3),
                         "P_ge9": round(float(np.mean(ec >= 9)), 3),
                         "P_all17": round(float(np.mean(ec >= len(elig_in_pool))), 3)},
    "docked_9": {"n_in_pool": len(dock_in_pool),
                 "mean_recovered": round(float(dc.mean()), 2),
                 "median_recovered": float(np.median(dc)),
                 "min": int(dc.min()), "max": int(dc.max()),
                 "P_ge1": round(float(np.mean(dc >= 1)), 3),
                 "P_ge2": round(float(np.mean(dc >= 2)), 3),
                 "P_ge3": round(float(np.mean(dc >= 3)), 3),
                 "P_ge5": round(float(np.mean(dc >= 5)), 3),
                 "P_all9": round(float(np.mean(dc >= len(dock_in_pool))), 3)},
}, open(os.path.join(TAB, "_R4_targetset_bootstrap.json"), "w"), indent=2)
print("\n[written] _R4_targetset_bootstrap.csv / .json")
