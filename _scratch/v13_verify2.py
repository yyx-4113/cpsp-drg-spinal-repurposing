import pandas as pd, numpy as np, json
T="results/tables"
sto=pd.read_csv(f"{T}/META_DRG_axis_stouffer.csv")
bulk=pd.read_csv(f"{T}/META_bulkonly_meta.csv")
re_=pd.read_csv(f"{T}/_R4_random_effects_meta.csv")
hub=pd.read_csv(f"{T}/P3_hub_genes.csv")
gs=pd.read_csv(f"{T}/_R4_geneset_setlevel_bh.csv")
j=json.load(open(f"{T}/_R4_nerveinjury_only_summary.json"))

core=sto[(sto.meta_FDR<0.05)&(sto.consistency>=0.8)]
print("=== CORE / RE ===")
print("primary FE core:", len(core))
rec=re_[(re_.FDR_RE<0.05)&(re_.consistency>=0.8)]
print("RE core:", len(rec), f"= {100*len(rec)/len(core):.1f}% of primary")
print("meta_FDR<0.05 genes:", int((sto.meta_FDR<0.05).sum()), "(old 6869 ->", int((sto.meta_FDR<0.05).sum()),")")

print("\n=== BULK OVERLAP (new base 2750) ===")
bc=bulk[(bulk.meta_FDR<0.05)&(bulk.consistency>=0.8)]
cset,bset=set(core.symbol),set(bc.symbol)
strict_shared=len(cset&bset); rel=bulk[(bulk.meta_FDR<0.05)&(bulk.consistency>=0.75)]
relaxed_shared=len(cset&set(rel.symbol))
print(f"strict (>=0.8): {strict_shared}/2750 = {100*strict_shared/2750:.1f}%")
print(f"relaxed (>=0.75): {relaxed_shared}/2750 = {100*relaxed_shared/2750:.1f}%")
sk=bc[bc.symbol.isin(cset)]; rk=rel[rel.symbol.isin(cset)]
from collections import Counter
print("strict K(bulk) dist:", dict(Counter(sk.K.tolist())))
print("relaxed K(bulk) dist:", dict(Counter(rk.K.tolist())))
pure44=sum(1 for k in sk.K.tolist() if k==4)
print(f"pure 4/4 in strict overlap: {pure44} = {100*pure44/len(core):.1f}% of primary (old 1707/4055=42.1%)")
print(f"outside even relaxed: {len(core)-relaxed_shared}")
print(f"recovered at relaxed vs strict: {relaxed_shared-strict_shared}")

print("\n=== HUBS ===")
print("in_meta_core True:", int(hub.in_meta_core.sum()), "/35")
print("out:", hub[~hub.in_meta_core].symbol.tolist())

print("\n=== GENE SETS (new) ===")
for _,r in gs.iterrows():
    if r.n_present>1:
        print(f"  {r['set']:20s} {r['scale']:6s} n={int(r.n_present):2d} mean_Z={r.mean_Z:+.3f} perm_q={r.perm_q:.4g}")
    else:
        print(f"  {r['set']:20s} {r['scale']:6s} n={int(r.n_present)} (single)")

print("\n=== CACNA2D1 ===")
r=sto[sto.symbol=='CACNA2D1'].iloc[0]
print("meta_Z=%.3f meta_FDR=%.3e consistency=%.3f K=%d n_up=%d n_dn=%d"%(
    r.meta_Z,r.meta_FDR,r.consistency,int(r.K),int(r.n_up),int(r.n_dn)))
for c in ['lfc_GSE267799_SMIR_DRG','lfc_GSE212311_CCI_DRG','lfc_GSE278227_CCI_DRG','lfc_GSE241361_S1R_DRG','lfc_GSE265957_Xtail_DRG_Day4','lfc_GSE265957_Xtail_DRG_Day63']:
    print(f"   {c}: {r[c]:+.3f}")

print("\n=== TRANSLATION (from regenerated json) ===")
for k,v in j['strata'].items():
    print(f"  {k}: {v['k']}/{v['n']} = {v['rate']*100:.2f}% CI[{v['ci'][0]*100:.1f},{v['ci'][1]*100:.1f}] perm_p={v['perm_p']:.4g}")
print("risk_diff strong-weak pp:", j['risk_difference_strong_minus_weak_pp'])
print("strong vs background pp:", j['strong_vs_background_pp'])
print("NI_core_FE:", j['NI_core_FE'], "NI_core_RE:", j['NI_core_RE'])

print("\n=== core-incision (circular, descriptive) ===")
cm=core.copy()
meas=cm.incision_lfc.notna()
print("primary core genes with incision measured:", int(meas.sum()))
print("of those, incision-discordant:", int((np.sign(cm.incision_lfc)!=np.sign(np.where(cm.meta_Z.isna(),0,cm.meta_Z))).sum()))
print("primary core genes NOT measured in incision:", int((~meas).sum()))
print("core in manuscript universe: 3556 old ->", int(meas.sum()), "for new 2750")
