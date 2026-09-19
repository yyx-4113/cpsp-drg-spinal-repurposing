#!/usr/bin/env python3
import gzip, os, re
import pandas as pd
ROOT="D:/2026.9/极速交付9月会员日优惠套路/01_AI生信-虚拟多重筛药/慢性疼痛"
META=os.path.join(ROOT,"data/raw/geo_meta")
ann=os.path.join(META,"GPL32253_family.soft.gz")
print("=== family.soft head ===")
with gzip.open(ann,"rt",encoding="utf-8",errors="replace") as f:
    begun=False; n=0
    for line in f:
        if line.startswith("!platform_table_begin"): begun=True; continue
        if begun:
            print(repr(line[:300]))
            n+=1
            if n>=8: break
# print actual time tokens from saved sampletable
for t in ["DRG","MUS","SKI"]:
    st=pd.read_csv(os.path.join(ROOT,"data/processed",f"GSE267799_{t}_sampletable.csv"))
    print(f"\n[{t}] time_token uniques:", sorted(st['time_token'].unique(), key=lambda x:int(x)))
    print(f"   model uniques:", st['model'].unique())
# show a few symbol-index rows of the built matrix to confirm it's ensembl
m=pd.read_csv(os.path.join(ROOT,"data/processed","GSE267799_DRG_symbol_count.csv"), index_col=0)
print("\n[matrix DRG] shape", m.shape, "index head:", list(m.index[:5]))
