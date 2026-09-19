#!/usr/bin/env python3
# p2_decode_samples.py -- parse !Sample_* lines from series_matrix.txt.gz -> sample tables
import os, gzip, glob, json
import pandas as pd
ROOT="D:/2026.9/极速交付9月会员日优惠套路/01_AI生信-虚拟多重筛药/慢性疼痛"
RAW=os.path.join(ROOT,"data/raw")
OUT=os.path.join(ROOT,"data/processed"); os.makedirs(OUT,exist_ok=True)

KEYS=["!Sample_geo_accession","!Sample_title","!Sample_source_name_ch1",
      "!Sample_organism_ch1","!Sample_characteristics_ch1","!Sample_description",
      "!Sample_supplementary_file_1"]

def parse(path):
    rows={}
    order=[]
    with gzip.open(path,"rt",encoding="utf-8",errors="replace") as f:
        for ln in f:
            if not ln.startswith("!Sample_"): continue
            parts=ln.rstrip("\n").split("\t")
            key=parts[0]
            vals=[p.strip('"') for p in parts[1:]]
            if key not in rows:
                rows[key]=[]; order.append(key)
            rows[key].append(vals)   # characteristics can repeat
    # collapse: for repeated keys, join with " | "
    collapsed={}
    for k in order:
        vv=rows[k]
        n=len(vv[0])
        merged=[]
        for i in range(n):
            cell=" | ".join(v[i] for v in vv if i<len(v))
            merged.append(cell)
        collapsed[k]=merged
    return collapsed

for path in sorted(glob.glob(os.path.join(RAW,"*","*series_matrix.txt.gz"))):
    gse=os.path.basename(path).split("_series_matrix")[0].split("-")[0]
    plat=os.path.basename(path).split("_series_matrix")[0]
    d=parse(path)
    n=len(d.get("!Sample_geo_accession",[]))
    base=os.path.basename(path).replace(".series_matrix.txt.gz","")
    print("="*80)
    print(f"{base}  n_samples={n}")
    for k in ["!Sample_title","!Sample_source_name_ch1","!Sample_organism_ch1","!Sample_characteristics_ch1","!Sample_description"]:
        if k in d:
            print(f"  {k}:")
            for i in range(min(n,6)):
                print(f"     [{i}] {d[k][i]}")
            if n>6: print(f"     ... ({n} total)")
    # save tidy
    cols={}
    for k,v in d.items():
        cols[k.replace("!Sample_","")]=v
    df=pd.DataFrame(cols)
    df.to_csv(os.path.join(OUT,f"{base}_samples.csv"),index=False)
