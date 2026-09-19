#!/usr/bin/env python3
# p1_build.py -- GSE267799 unified symbol x sample count matrices (v2: mygene mapping)
import os, sys, re
import pandas as pd
import numpy as np

ROOT="D:/2026.9/极速交付9月会员日优惠套路/01_AI生信-虚拟多重筛药/慢性疼痛"
RAW=os.path.join(ROOT,"data/raw/GSE267799")
PROC=os.path.join(ROOT,"data/processed")
os.makedirs(PROC,exist_ok=True)

# token -> (time_label, group)
TOKEN2TIME={"0":("0d","baseline"),"1":("6h","acute"),"2":("2d","acute"),
            "10":("10d","chronic"),"32":("32d","chronic")}
TISSUES={"DRG":"DRG","MUS":"muscle","SKI":"skin"}

# 1) gather all ensembl ids from cached matrices
ids=set()
for tiss in TISSUES:
    m=pd.read_csv(os.path.join(PROC,f"GSE267799_{tiss}_symbol_count.csv"), index_col=0)
    ids.update(m.index.astype(str))
ids=list(ids)
print(f"[ids] {len(ids)}", file=sys.stderr)

# 2) map ensembl -> symbol via mygene (rat)
import mygene
mg=mygene.MyGeneInfo()
res=mg.querymany(ids, scopes="ensembl.gene", fields="symbol", species="rat",
                as_dataframe=True, df_index=True, verbose=False)
symcol = "symbol" if "symbol" in res.columns else res.columns[0]
ens2sym={i:res.loc[i,symcol] for i in res.index if isinstance(res.loc[i,symcol],str) and res.loc[i,symcol]}
print(f"[mapped] {len(ens2sym)} / {len(ids)}", file=sys.stderr)
import json
json.dump(ens2sym, open(os.path.join(ROOT,"data/raw/geo_meta","GSE267799_ens2sym.json"),"w"))

# 3) rebuild symbol matrices
all_samples=[]
for tiss,tn in TISSUES.items():
    m=pd.read_csv(os.path.join(PROC,f"GSE267799_{tiss}_symbol_count.csv"), index_col=0)
    m.index=m.index.astype(str)
    m["symbol"]=m.index.map(lambda e: ens2sym.get(e,"") or e)
    num=m.drop(columns=["symbol"]).apply(pd.to_numeric, errors="coerce")
    num["symbol"]=m["symbol"]
    agg=num.groupby("symbol").mean()
    agg=agg.loc[~(agg.drop(columns=["symbol"]).sum(axis=1)==0)]
    # drop rows whose symbol is still an ensembl id (unmapped) -> keep but flag? keep for completeness
    agg.to_csv(os.path.join(PROC,f"GSE267799_{tiss}_symbol_count.csv"))
    # sample table (rebuild from filename tokens)
    recs=[]
    for c in m.columns:
        if c=="symbol": continue
        mm=re.match(r"(\w+)_(\w+)_(\d+)d_rep(\d+)", c)
        if not mm: continue
        model,tissc,tok,rep=mm.groups()
        tl,grp=TOKEN2TIME.get(tok,("?","?"))
        recs.append({"sample":c,"model":model,"tissue":tissc,"time_token":int(tok),
                     "time_label":tl,"time_group":grp,"rep":int(rep)})
    st=pd.DataFrame(recs)
    st.to_csv(os.path.join(PROC,f"GSE267799_{tiss}_sampletable.csv"), index=False)
    all_samples.append(st)
    print(f"[done] {tiss}: {agg.shape}  mapped_genes={int((~agg.index.str.startswith('ENSRNO')).sum())}/{agg.shape[0]}")

big=pd.concat(all_samples, ignore_index=True)
big.to_csv(os.path.join(PROC,"GSE267799_all_sampletable.csv"), index=False)
print("\n[ALL] time_group:", big['time_group'].value_counts().to_dict())
print("      time_label:", big['time_label'].value_counts().to_dict())
print("      model:", big['model'].value_counts().to_dict())
