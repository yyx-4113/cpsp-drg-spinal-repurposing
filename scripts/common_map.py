#!/usr/bin/env python3
# common_map.py -- single-pass per-species Ensembl->symbol from NCBI gene_info dbXrefs
# Reads gene_info.gz ONCE, dumps rat/mouse/human Ensembl->symbol maps to data/raw/geo_meta/ens2sym_tax{TAX}.json
import os, sys, json, gzip
ROOT="D:/2026.9/极速交付9月会员日优惠套路/01_AI生信-虚拟多重筛药/慢性疼痛"
REF=os.path.join(ROOT,"data/raw/ref")
META=os.path.join(ROOT,"data/raw/geo_meta")
GI=os.path.join(REF,"gene_info.gz")

TAX={10116:"rat",10090:"mouse",9606:"human"}
PREFIX=("ENSRNOG","ENSMUSG","ENSG")

def main():
    if not os.path.exists(GI):
        print(f"MISSING gene_info.gz at {GI}",file=sys.stderr); sys.exit(1)
    maps={t:{} for t in TAX}
    print(f"[single-pass] reading {GI} ...",file=sys.stderr)
    n=0
    with gzip.open(GI,"rt",encoding="utf-8",errors="replace") as f:
        for line in f:
            if line.startswith("#"): continue
            p=line.rstrip("\n").split("\t")
            if len(p)<6: continue
            try: tid=int(p[0])
            except ValueError: continue
            if tid not in TAX: continue
            sym=p[2] if len(p)>2 else ""
            if not sym: continue
            dbx=p[5] if len(p)>5 else ""
            for ref in dbx.split("|"):
                if ref.startswith("Ensembl:"):
                    ens=ref.split(":",1)[1]
                    if ens.startswith(PREFIX):
                        maps[tid].setdefault(ens,sym)
            n+=1
    for t,name in TAX.items():
        cache=os.path.join(META,f"ens2sym_tax{t}.json")
        json.dump(maps[t], open(cache,"w"))
        print(f"[done {name} tax={t}] ensembl_mapped={len(maps[t])}",file=sys.stderr)

if __name__=="__main__":
    main()
