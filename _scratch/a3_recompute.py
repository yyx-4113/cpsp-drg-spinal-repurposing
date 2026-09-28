import csv, json, statistics, os

ROOT = "D:/2026.9/极速交付9月会员日优惠套路/01_AI生信-虚拟多重筛药/慢性疼痛"
T = os.path.join(ROOT, "results/tables")

def f(x):
    return float(x)

print("="*70)
print("1. CORE SIGNATURE 4,055")
print("="*70)
core = list(csv.DictReader(open(os.path.join(T, "META_DRG_axis_CORE_signature.csv"))))
core_syms = set(r["symbol"] for r in core)
print("META_DRG_axis_CORE_signature.csv rows:", len(core))

st = list(csv.DictReader(open(os.path.join(T, "META_DRG_axis_stouffer.csv"))))
st_core = [r for r in st if f(r["meta_FDR"]) < 0.05 and f(r["consistency"]) >= 0.8]
st_syms = set(r["symbol"] for r in st_core)
print("stouffer meta_FDR<0.05 & consistency>=0.8:", len(st_core))
print("genes tested (stouffer rows):", len(st))
print("meta_FDR<0.05:", sum(1 for r in st if f(r["meta_FDR"]) < 0.05))
print("core(CORE_sig) == core(stouffer)?", core_syms == st_syms,
      "| only in stouffer not in sig:", len(st_syms - core_syms),
      "| only in sig not stouffer:", len(core_syms - st_syms))

print()
print("="*70)
print("2. BULK-ONLY 2,512 / 2,202 (54.3%) / 3,587 (88.5%)")
print("="*70)
bulk = list(csv.DictReader(open(os.path.join(T, "META_bulkonly_meta.csv"))))
bulk_syms = set(r["symbol"] for r in bulk)
print("META_bulkonly_meta.csv rows:", len(bulk))
bk_core = [r for r in bulk if f(r["meta_FDR"]) < 0.05 and f(r["consistency"]) >= 0.8]
bk_core_syms = set(r["symbol"] for r in bk_core)
print("bulk-only core (FDR<0.05 & cons>=0.8):", len(bk_core))

strict = core_syms & bk_core_syms
print("STRICT overlap (core ∩ bulk-only core):", len(strict),
      "->", round(100*len(strict)/len(core_syms), 4), "%")

# relaxed: primary core genes bulk-significant FDR<0.05 AND consistency>=0.75 (>=3/4 of 4)
relaxed = [r for r in bulk if f(r["meta_FDR"]) < 0.05 and f(r["consistency"]) >= 0.75]
relaxed_syms = set(r["symbol"] for r in relaxed)
rel_overlap = core_syms & relaxed_syms
print("RELAXED overlap (core ∩ bulk FDR<0.05 & cons>=0.75):", len(rel_overlap),
      "->", round(100*len(rel_overlap)/len(core_syms), 4), "%")
print("  manuscript claims 3,587/4,055 = 88.5%")

# genes not bulk-significant at all = primary core genes absent from bulk-only meta entirely
absent = core_syms - bulk_syms
print("primary core genes NOT in bulk-only meta at all (K<3):", len(absent),
      "(manuscript claims 211)")

print()
print("="*70)
print("3. 32/35 hub-core overlap")
print("="*70)
hub = list(csv.DictReader(open(os.path.join(T, "P3_hub_genes.csv"))))
print("hub rows:", len(hub))
n_in = sum(1 for r in hub if r["in_meta_core"].strip().lower() in ("true", "1", "yes"))
print("in_meta_core == True:", n_in, "/", len(hub))

print()
print("="*70)
print("4. BOOTSTRAP (from _R4_targetset_bootstrap_resamples.csv)")
print("="*70)
boot = list(csv.DictReader(open(os.path.join(T, "_R4_targetset_bootstrap_resamples.csv"))))
print("resamples:", len(boot))
sizes = [int(r["recovered_hub_set_size"]) for r in boot]
jac = [f(r["jaccard_vs_published35"]) for r in boot]
n17 = [int(r["n_dock_eligible_17_recovered"]) for r in boot]
n9 = [int(r["n_docked_9_recovered"]) for r in boot]
def med(x): return statistics.median(x)
def q(x, p):
    xs = sorted(x); k = (len(xs)-1)*p; lo = int(k); return xs[lo] + (xs[min(lo+1,len(xs)-1)]-xs[lo])*(k-lo)
print(f"hub_set_size: median={med(sizes):.1f} q25={q(sizes,0.25):.1f} q75={q(sizes,0.75):.1f} min={min(sizes)} max={max(sizes)}")
print(f"jaccard:      median={med(jac):.4f} q25={q(jac,0.25):.4f} q75={q(jac,0.75):.4f}")
print(f"dock_eligible_17 recovered: mean={sum(n17)/len(n17):.4f} median={med(n17):.1f} min={min(n17)} max={max(n17)}")
print(f"  P(>=3 of 17) = {sum(1 for x in n17 if x>=3)/len(n17):.3f}")
print(f"  P(>=5 of 17) = {sum(1 for x in n17 if x>=5)/len(n17):.3f}")
print(f"docked_9 recovered: mean={sum(n9)/len(n9):.4f} median={med(n9):.1f} min={min(n9)} max={max(n9)}")
print(f"  P(>=3 of 9) = {sum(1 for x in n9 if x>=3)/len(n9):.3f}")

print()
print("="*70)
print("4b. BOOTSTRAP JSON (active) for cross-check")
print("="*70)
bt = json.load(open(os.path.join(T, "_R4_targetset_bootstrap.json")))
print("json hub_set_size:", bt["hub_set_size"])
print("json jaccard:", bt["jaccard_vs_published35"])
print("json dock_eligible_17:", bt["dock_eligible_17"])
print("json docked_9:", bt["docked_9"])

print()
print("="*70)
print("5. LODO AUCs (leakage-controlled)")
print("="*70)
lodo = list(csv.DictReader(open(os.path.join(T, "P3_lodo_auc_ci_leakage_controlled.csv"))))
for r in lodo:
    print(f"  {r['test_dataset']:30s} AUC={f(r['auc']):.4f} CI=[{f(r['ci_lo']):.4f},{f(r['ci_hi']):.4f}] n={r['n']}")
print("Raw (non-leakage) GSE267799 for reference:")
raw = list(csv.DictReader(open(os.path.join(T, "P3_lodo_auc_ci.csv"))))
for r in raw:
    if "267799" in r["test_dataset"]:
        print(f"  {r['test_dataset']:30s} AUC={f(r['auc']):.4f} CI=[{f(r['lo']):.4f},{f(r['hi']):.4f}] n={r['n']}")

print()
print("="*70)
print("6. VIUM 33/35 + 17/33 dorsal horn")
print("="*70)
vis = list(csv.DictReader(open(os.path.join(T, "P5_GSE325938_hub_regionalization.csv"))))
present = [r for r in vis if r["present"].strip().lower() == "true"]
print("Visium rows:", len(vis), "| present=True:", len(present))
print("  absent:", [r["symbol"] for r in vis if r["present"].strip().lower() != "true"])
dh = [r for r in vis if r["top_region"].strip() == "DorsalHorn"]
print("  DorsalHorn top_region:", len(dh), "of", len(present),
      f"({100*len(dh)/len(present):.1f}%)")

print()
print("="*70)
print("7. snRNA GSE328175 hub presence (distinct dataset)")
print("="*70)
sn = list(csv.DictReader(open(os.path.join(T, "P5_GSE328175_SC_ShamSNI_hub_localisation.csv"))))
sn_syms = set(r["symbol"] for r in sn)
print("unique snRNA hub symbols:", len(sn_syms))
print("  missing from snRNA (vs 35-hub set):", sorted(set(core_syms) - sn_syms) if False else None)
# the 35-hub list is the visium list symbols
hub35 = set(r["symbol"] for r in vis)
print("  in 35-hub set but ABSENT from snRNA:", sorted(hub35 - sn_syms))
print("  in 35-hub set but ABSENT from Visium (present=False):",
      [r["symbol"] for r in vis if r["present"].strip().lower() != "true"])
