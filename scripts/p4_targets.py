#!/usr/bin/env python3
# p4_targets.py -- miRDB predicted targets (v6.0) -> hub-gene targeting miRNAs.
# Maps miRDB RefSeq targets to symbols via NCBI gene2refseq + gene_info (human, tax 9606).
import os, gzip, json
import numpy as np, pandas as pd

ROOT="D:/2026.9/极速交付9月会员日优惠套路/01_AI生信-虚拟多重筛药/慢性疼痛"
REF=os.path.join(ROOT,"data/raw/ref"); TAB=os.path.join(ROOT,"results/tables")
META=os.path.join(ROOT,"data/raw/geo_meta")

def build_refseq2sym():
    cache=os.path.join(META,"refseq2sym_human.json")
    if os.path.exists(cache) and os.path.getsize(cache)>1000:
        return json.load(open(cache))
    # 1) GeneID -> Symbol (human)
    g2s={}
    with gzip.open(os.path.join(REF,"gene_info.gz"),"rt",encoding="utf-8",errors="replace") as f:
        for ln in f:
            if ln.startswith("#"): continue
            p=ln.rstrip("\n").split("\t")
            if len(p)<3 or p[0]!="9606": continue
            g2s[p[1]]=p[2]
    print("human GeneID->Symbol:",len(g2s))
    # 2) RefSeq RNA -> GeneID -> Symbol
    r2s={}
    with gzip.open(os.path.join(REF,"gene2refseq.gz"),"rt",encoding="utf-8",errors="replace") as f:
        for ln in f:
            if ln.startswith("#"): continue
            p=ln.rstrip("\n").split("\t")
            if len(p)<4 or p[0]!="9606": continue
            acc=p[3].split(".")[0]
            if acc.startswith(("NM_","XM_","NR_","XR_")):
                sym=g2s.get(p[1])
                if sym: r2s[acc]=sym
    print("human RefSeq->Symbol:",len(r2s))
    json.dump(r2s,open(cache,"w")); return r2s

r2s=build_refseq2sym()
hub=pd.read_csv(os.path.join(TAB,"P3_hub_genes.csv"))["symbol"].tolist()
hubs=set(hub)
print("hub genes:",len(hub))

rows=[]
with gzip.open(os.path.join(REF,"miRDB_v6.0_prediction_result.txt.gz"),"rt",encoding="utf-8",errors="replace") as f:
    for ln in f:
        p=ln.rstrip("\n").split("\t")
        if len(p)<3: continue
        mir,tgt,score=p[0],p[1],p[2]
        if not mir.startswith("hsa-"): continue
        sym=r2s.get(tgt.split(".")[0])
        if sym and sym.upper() in hubs:
            rows.append({"miRNA":mir,"symbol":sym.upper(),"score":float(score)})
t=pd.DataFrame(rows).drop_duplicates(subset=["miRNA","symbol"])
t=t.sort_values(["symbol","score"],ascending=[True,False])
t.to_csv(os.path.join(TAB,"P4_hub_targeting_miRNAs.csv"),index=False)
print("hub-targeting hsa-miRNAs (score>=0):",len(t))
hi=t[t.score>=80]
print("high-confidence (score>=80):",len(hi))
print("hub genes covered:",t["symbol"].nunique(),"/",len(hub))
print(t.head(40).to_string(index=False))
