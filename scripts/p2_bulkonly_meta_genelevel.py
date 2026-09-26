#!/usr/bin/env python3
# p2_bulkonly_meta_genelevel.py
# Bulk-only (4 bulk-transcriptome contrasts, GSE265957 translatome EXCLUDED) Stouffer
# weighted-Z meta-analysis, per gene. Writes results/tables/META_bulkonly_meta.csv.
import os, json
import numpy as np, pandas as pd
from scipy import stats

ROOT = "D:/2026.9/极速交付9月会员日优惠套路/01_AI生信-虚拟多重筛药/慢性疼痛"
DEG = os.path.join(ROOT, "results/tables")
OUT = os.path.join(DEG, "META_bulkonly_meta.csv")

bulk = [
    ("DEG_GSE267799_SMIR_DRG__chronic_vs_baseline.csv", "GSE267799"),
    ("DEG_GSE212311_CCI_DRG__CCI_vs_Sham.csv",         "GSE212311"),
    ("DEG_GSE278227_CCI_DRG__1W_IL_vs_CL_pooled.csv",  "GSE278227"),
    ("DEG_GSE241361_S1R_DRG__SNI_vs_Naive_WT.csv",     "GSE241361_DRG"),
]

def bh(p):
    p = np.asarray(p, float); ok = ~np.isnan(p); idx = np.where(ok)[0]
    q = np.full_like(p, np.nan); pv = p[idx]; m = len(pv)
    order = np.argsort(pv); ranked = pv[order]
    adj = ranked * m / np.arange(1, m + 1)
    adj = np.minimum.accumulate(adj[::-1])[::-1]
    q[idx[order]] = np.clip(adj, 0, 1)
    return q

datasets = {}
for fn, key in bulk:
    d = pd.read_csv(os.path.join(DEG, fn), index_col=0)
    d.index = d.index.astype(str)
    d = d[~d.index.isin(["nan", "None", "", "NaN"])]
    d = d.dropna(subset=["p", "t"])
    n_case = float(d["n_case"].iloc[0]); n_ctrl = float(d["n_ctrl"].iloc[0])
    w = np.sqrt(n_case * n_ctrl / (n_case + n_ctrl))
    z = np.sign(d["t"]) * stats.norm.isf(np.clip(d["p"].values, 1e-300, 1) / 2.0)
    df = pd.DataFrame({"log2FC": d["log2FC"].values, "Z": z, "w": w}, index=d.index)
    df = df[~df.index.isin([None, "nan", "None", ""])]
    df = df.groupby(df.index).mean(numeric_only=True)
    datasets[key] = df
    print(f"[bulk] {key:14s} w={w:.6f} n_genes={len(df)}")

allg = set()
for d in datasets.values():
    allg |= set(d.index)

rec = []
for gene in allg:
    zs, ws, lf = [], [], {}
    for key, d in datasets.items():
        if gene in d.index and not np.isnan(d.loc[gene, "Z"]):
            zs.append(float(d.loc[gene, "Z"])); ws.append(float(d.loc[gene, "w"]))
            lf[key] = float(d.loc[gene, "log2FC"])
    K = len(zs)
    if K < 3:
        continue
    zs = np.array(zs); ws = np.array(ws)
    Zc = float((zs * ws).sum() / np.sqrt((ws ** 2).sum()))
    p = float(2 * stats.norm.sf(np.abs(Zc)))
    up = int((zs > 0).sum()); cons = max(up, K - up) / K
    rec.append({"symbol": gene, "K": K, "meta_Z": Zc, "meta_p": p,
                "consistency": cons, "n_up": up, "n_dn": K - up,
                **{f"lfc_{k}": lf.get(k, np.nan) for k in datasets}})

meta = pd.DataFrame(rec)
print("meta columns:", list(meta.columns)[:8], "... rows:", len(meta))
meta["meta_FDR"] = bh(meta["meta_p"].values)
meta = meta.sort_values("meta_p").reset_index(drop=True)
meta.to_csv(OUT, index=False)

with open(os.path.join(DEG, "META_bulkonly_sensitivity_summary.json")) as f:
    js = json.load(f)
scn = js["scn_tab"]
print("\n=== validation vs JSON scn_tab ===")
for g in ["SCN9A", "SCN10A", "SCN11A", "SCN8A"]:
    r = meta[meta.symbol == g].iloc[0]
    exp = scn[g]
    okz = abs(r.meta_Z - exp["bulk_meta_Z"]) < 1e-4
    print(f"{g:7s} Z {r.meta_Z:.6f} vs {exp['bulk_meta_Z']:.6f} {'OK' if okz else 'MISMATCH'} | "
          f"FDR {r.meta_FDR:.3e} vs {exp['bulk_meta_FDR']:.3e}")

print(f"\n[bulk-only] genes tested K>=3 = {len(meta)}")
print(f"meta_FDR<0.05 = {(meta.meta_FDR<0.05).sum()}")
print(f"core (FDR<0.05 & consistency>=0.8) = {((meta.meta_FDR<0.05)&(meta.consistency>=0.8)).sum()}")
print(f"wrote {OUT}")
