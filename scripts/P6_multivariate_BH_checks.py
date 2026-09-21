"""
P6-bis: supplementary methodological controls requested by the Round-1 review.

T2-11  Multivariate physicochemical control
        For each of the 5 reverse-control targets, test whether docking affinity
        (neg_aff) still predicts known-binder status AFTER controlling for
        molecular weight + logP + TPSA + HBD + HBA + rotatable bonds.
        Model A: binder ~ physchem(6)
        Model B: binder ~ physchem(6) + neg_aff
        Report AUC_phys, AUC_dock(neg_aff alone), AUC_combined, and the
        likelihood-ratio test for the residual enrichment of docking.

T2-14  Benjamini-Hochberg multiple-comparison correction
        BH across the 5 targets for (i) the raw full-library enrichment p
        (p_mannwhitney) and (ii) the size-independent (MW-adjusted) p
        (deltaAUC_vs_size_only_p_le0). Show that BH does not rescue a single
        robust size-independent hit.

Outputs:
  results/tables/P6_multivariate_physchem_control.csv
  results/tables/P6_BH_correction.csv
  prints a compact summary.
"""
import json
import numpy as np
import pandas as pd
from scipy import special, stats
from sklearn.metrics import roc_auc_score

TBL = "results/tables"
TARGETS = ["ACVR1", "ADRA2A", "AXL", "MAPK14", "TNIK"]
DESC = ["mw", "logp", "tpsa", "hbd", "hba", "rotb"]


def bh(pvals):
    """Benjamini-Hochberg adjusted p (q). pvals: array, may contain NaN->treated as 1."""
    p = np.asarray(pvals, dtype=float).copy()
    mask = ~np.isnan(p)
    q = np.full_like(p, np.nan)
    pv = p[mask]
    n = len(pv)
    if n == 0:
        return q
    order = np.argsort(pv)                       # order[i] = original index of i-th smallest
    ranked = pv[order]
    adj = ranked * n / (np.arange(n) + 1)
    adj = np.minimum.accumulate(adj[::-1])[::-1]  # enforce monotonicity from largest downward
    adj = np.clip(adj, 0, 1)
    inv = np.argsort(order)                       # inverse permutation: original pos -> rank
    qmask = np.where(mask)[0]
    q[qmask] = adj[inv]                           # map back to original masked positions
    return q


def fit_logit(X, y, max_iter=200):
    """IRLS logistic regression with backtracking line search (monotone ll).
    X: (n,k) with intercept already added. Returns beta, cov, loglik."""
    X = np.asarray(X, float)
    y = np.asarray(y, float)
    n, k = X.shape
    beta = np.zeros(k)
    eta = X @ beta
    p = special.expit(eta)
    ll = np.sum(y * np.log(p + 1e-300) + (1 - y) * np.log(1 - p + 1e-300))
    for _ in range(max_iter):
        W = np.clip(p * (1 - p), 1e-12, None)
        z = eta + (y - p) / W
        XtW = X.T * W
        XtWX = XtW @ X
        XtWz = XtW @ z
        try:
            delta = np.linalg.solve(XtWX, XtWz)
        except np.linalg.LinAlgError:
            delta = np.linalg.lstsq(XtWX, XtWz, rcond=None)[0]
        step = 1.0
        improved = False
        for _b in range(50):
            bnew = beta + step * delta
            enew = np.clip(X @ bnew, -30, 30)
            pnew = special.expit(enew)
            ll_new = np.sum(y * np.log(pnew + 1e-300) + (1 - y) * np.log(1 - pnew + 1e-300))
            if np.isfinite(ll_new) and ll_new >= ll - 1e-9:
                improved = True
                break
            step *= 0.5
        if not improved:
            break
        beta, eta, p, ll = bnew, enew, pnew, ll_new
        if step * np.max(np.abs(delta)) < 1e-9:
            break
    W = np.clip(p * (1 - p), 1e-12, None)
    XtWX = (X.T * W) @ X
    cov = np.linalg.inv(XtWX)
    return beta, cov, ll


def main():
    mrg = pd.read_csv(f"{TBL}/P6_docking_scores_merged.csv")
    pos = pd.read_csv(f"{TBL}/P6_reverse_control_positives.csv")
    mw = pd.read_csv(f"{TBL}/P6_enrichment_mw_confounder_check.csv")

    known_set = set(zip(pos["symbol"], pos["chembl_id"]))

    sub = mrg[mrg["symbol"].isin(TARGETS)].copy()
    sub = sub.dropna(subset=DESC + ["neg_aff", "chembl_id"])
    sub["binder"] = [
        1 if (s, c) in known_set else 0 for s, c in zip(sub["symbol"], sub["chembl_id"])
    ]

    # ---- T2-11 multivariate physicochemical control ----
    rows = []
    print("=" * 78)
    print("T2-11  Multivariate physicochemical control (logistic binder ~ physchem + neg_aff)")
    print("=" * 78)
    print(f"{'target':8s} {'n':>5s} {'n_pos':>5s} | {'AUC_phys':>8s} {'AUC_dock':>9s} {'AUC_comb':>9s} | {'LR_dock_p':>9s}")
    for t in TARGETS:
        d = sub[sub["symbol"] == t]
        y = d["binder"].values.astype(float)
        n_pos = int(y.sum())
        if n_pos < 5 or len(d) < 50:
            print(f"{t:8s} skipped (n={len(d)}, n_pos={n_pos})")
            continue
        Z = (d[DESC].values - d[DESC].values.mean(0)) / (d[DESC].values.std(0) + 1e-9)
        za = (d["neg_aff"].values - d["neg_aff"].mean()) / (d["neg_aff"].std() + 1e-9)
        Xa = np.column_stack([np.ones(len(d)), Z])            # physchem only
        Xb = np.column_stack([np.ones(len(d)), Z, za])          # + docking
        beta_a, cov_a, ll_a = fit_logit(Xa, y)
        beta_b, cov_b, ll_b = fit_logit(Xb, y)
        auc_phys = roc_auc_score(y, Xa @ beta_a)
        auc_dock = roc_auc_score(y, za)
        auc_comb = roc_auc_score(y, Xb @ beta_b)
        # LR test: contribution of neg_aff beyond physchem
        D = 2 * (ll_b - ll_a)
        lr_p = stats.chi2.sf(D, df=1)
        # Wald p for neg_aff in model B
        se = np.sqrt(np.diag(cov_b))[-1]
        wald_z = beta_b[-1] / (se + 1e-300)
        wald_p = 2 * (1 - stats.norm.cdf(abs(wald_z)))
        rows.append(dict(symbol=t, n=len(d), n_pos=n_pos,
                         AUC_phys=round(auc_phys, 4), AUC_dock=round(auc_dock, 4),
                         AUC_combined=round(auc_comb, 4),
                         LR_dock_residual_p=lr_p, Wald_neg_aff_p=wald_p))
        print(f"{t:8s} {len(d):5d} {n_pos:5d} | {auc_phys:8.4f} {auc_dock:9.4f} {auc_comb:9.4f} | {lr_p:9.4g}")
    t211 = pd.DataFrame(rows)
    t211.to_csv(f"{TBL}/P6_multivariate_physchem_control.csv", index=False)

    # ---- T2-14 BH correction ----
    print()
    print("=" * 78)
    print("T2-14  Benjamini-Hochberg correction across the 5 reverse-control targets")
    print("=" * 78)
    mw2 = mw[mw["symbol"].isin(TARGETS)].set_index("symbol").loc[TARGETS].reset_index()
    raw_p = mw2["p_mannwhitney"].values
    size_p = mw2["deltaAUC_vs_size_only_p_le0"].values
    q_raw = bh(raw_p)
    q_size = bh(size_p)
    out = mw2[["symbol", "AUC_dock", "p_mannwhitney", "deltaAUC_vs_size_only_p_le0"]].copy()
    out["BH_q_raw_enrich"] = q_raw
    out["BH_q_size_indep"] = q_size
    out.to_csv(f"{TBL}/P6_BH_correction.csv", index=False)
    print(f"{'target':8s} {'AUC_dock':>9s} {'raw_p':>10s} {'BH_q_raw':>10s} | {'sizeIndep_p':>12s} {'BH_q_size':>10s}")
    for _, r in out.iterrows():
        print(f"{r['symbol']:8s} {r['AUC_dock']:9.3f} {r['p_mannwhitney']:10.2e} {r['BH_q_raw_enrich']:10.3e} | {r['deltaAUC_vs_size_only_p_le0']:12.4f} {r['BH_q_size_indep']:10.3f}")

    print()
    n_raw_sig = int((out["BH_q_raw_enrich"] < 0.05).sum())
    n_size_sig = int((out["BH_q_size_indep"] < 0.05).sum())
    print(f"After BH: {n_raw_sig}/5 raw enrichment p significant; {n_size_sig}/5 size-independent p significant.")


if __name__ == "__main__":
    main()
