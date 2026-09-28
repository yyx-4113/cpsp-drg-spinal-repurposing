import pandas as pd, numpy as np, json, os
T="results/tables"
sto=pd.read_csv(f"{T}/META_DRG_axis_stouffer.csv")
bulk=pd.read_csv(f"{T}/META_bulkonly_meta.csv")
re_=pd.read_csv(f"{T}/_R4_random_effects_meta.csv")
hub=pd.read_csv(f"{T}/P3_hub_genes.csv")

# 1. primary core (FE)
core=sto[(sto.meta_FDR<0.05)&(sto.consistency>=0.8)]
print("PRIMARY FE core:", len(core))
# 2. RE core
re_core=re_[(re_.FDR_RE<0.05)&(re_.consistency>=0.8)]
print("RE core (FDR_RE<0.05 & consistency>=0.8):", len(re_core))
print("RE core %% of primary:", round(100*len(re_core)/len(core),1))
# RE core inside primary
inter=set(core.symbol)&set(re_core.symbol)
print("RE core inside primary core:", len(inter), "/", len(re_core))
# 3. bulk overlap (new base)
bc=bulk[(bulk.meta_FDR<0.05)&(bulk.consistency>=0.8)]
print("bulk-only core:", len(bc))
cset=set(core.symbol); bset=set(bc.symbol)
strict=cset&bset
# relaxed: bulk consistency>=0.75
bc_rel=bulk[(bulk.meta_FDR<0.05)&(bulk.consistency>=0.75)]
relaxed=cset&set(bc_rel.symbol)
print(f"strict overlap (>=0.8): {len(strict)} = {round(100*len(strict)/len(core),1)}% of primary")
print(f"relaxed overlap (>=0.75): {len(relaxed)} = {round(100*len(relaxed)/len(core),1)}% of primary")
# K decomposition on primary: how many datasets (of 4 bulk) agree
# use bulk consistency column: consistency = max(n_up,n_dn)/K_bulk
# strict genes K dist
sk=bc[bc.symbol.isin(cset)]
from collections import Counter
print("strict overlap K(bulk) dist:", dict(Counter(sk.K.tolist())))
rk=bc_rel[bc_rel.symbol.isin(cset)]
print("relaxed overlap K(bulk) dist:", dict(Counter(rk.K.tolist())))
# 4 hubs
print("hub in_meta_core True:", int(hub.in_meta_core.sum()), "/", len(hub))
print("hub NOT in core:", hub[~hub.in_meta_core].symbol.tolist())
# 5 CACNA2D1
row=sto[sto.symbol=="CACNA2D1"]
if len(row):
    r=row.iloc[0]
    print(f"CACNA2D1 meta_Z={r.meta_Z:.3f} meta_FDR={r.meta_FDR:.3e} consistency={r.consistency} K={int(r.K)}")
    ups=int(r.n_up); print(" n_up/n_dn:",ups,int(r.n_dn))
# 6 translation test
j=json.load(open(f"{T}/_R4_nerveinjury_only_summary.json"))
print("nerveinjury_only summary keys:", list(j.keys()))
for k in j:
    if isinstance(j[k],(int,float)):
        print(f"  {k}: {j[k]}")
    elif isinstance(j[k],dict):
        print(f"  {k}: {j[k]}")
# 7 OXPHOS RE verification
ox=re_[re_.symbol.isin(["NDUFA1","NDUFB5","NDUFS1","NDUFS3","SDHB","UQCRC1","UQCRC2","MTCO1","MTCO2","ATP5F1A","ATP5F1B","ATP5A1","ATP5O","COX4I1","COX5A","NDUFA10","NDUFA13","NDUFV1","NDUFS8"])]
print("OXPHOS members found in RE file:", len(ox))
print("OXPHOS RE mean Z_RE:", round(ox.Z_RE.mean(),4), "FE mean Z_FE:", round(ox.Z_FE.mean(),4))
print("OXPHOS RE per-gene Z_RE:", [round(v,3) for v in ox.Z_RE.tolist()])
