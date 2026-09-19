#!/usr/bin/env python3
# p1_map_ncbi.py -- Ensembl->symbol via NCBI gene_info dbXrefs (single file, no gene2ensembl)
import urllib.request, gzip, os, sys, re, json
import pandas as pd

ROOT="D:/2026.9/极速交付9月会员日优惠套路/01_AI生信-虚拟多重筛药/慢性疼痛"
REF=os.path.join(ROOT,"data/raw/ref"); os.makedirs(REF,exist_ok=True)
PROC=os.path.join(ROOT,"data/processed")
META=os.path.join(ROOT,"data/raw/geo_meta")
TISSUES={"DRG":"DRG","MUS":"muscle","SKI":"skin"}
TOKEN2TIME={"0":("0d","baseline"),"1":("6h","acute"),"2":("2d","acute"),
            "10":("10d","chronic"),"32":("32d","chronic")}
CACHED=os.path.join(META,"GSE267799_ens2sym.json")

def dl(u,out):
    if os.path.exists(out) and os.path.getsize(out)>1000:
        print(f"[cached] {os.path.basename(out)}",file=sys.stderr); return
    print(f"[dl] {u}",file=sys.stderr)
    urllib.request.urlretrieve(u,out)

if os.path.exists(CACHED) and os.path.getsize(CACHED)>10:
    ens2sym=json.load(open(CACHED))
    print(f"[loaded cached ens2sym] {len(ens2sym)}",file=sys.stderr)
else:
    gi=os.path.join(REF,"gene_info.gz")
    dl("https://ftp.ncbi.nlm.nih.gov/gene/DATA/gene_info.gz", gi)
    ens2sym={}; entrez2sym={}
    header=None
    with gzip.open(gi,"rt",encoding="utf-8",errors="replace") as f:
        for line in f:
            if line.startswith("#"):
                header=line[1:].rstrip("\n").split("\t"); continue
            if header is None: continue
            p=line.rstrip("\n").split("\t")
            if len(p)<6 or p[0]!="10116": continue
            d=dict(zip(header,p))
            gid=d.get("GeneID"); sym=d.get("Symbol",""); dbx=d.get("dbXrefs","")
            if gid and sym:
                entrez2sym[gid]=sym
                for ref in dbx.split("|"):
                    if ref.startswith("Ensembl:"):
                        ens=ref.split(":",1)[1]
                        if ens.startswith("ENSRNOG"):
                            ens2sym[ens]=sym
    print(f"[gene_info rat] entrez={len(entrez2sym)} ensembl_mapped={len(ens2sym)}",file=sys.stderr)
    json.dump(ens2sym, open(CACHED,"w"))

# apply to cached matrices
all_samples=[]
for tiss in TISSUES:
    m=pd.read_csv(os.path.join(PROC,f"GSE267799_{tiss}_symbol_count.csv"), index_col=0)
    m.index=m.index.astype(str); m.index.name=None
    m["symbol"]=m.index.map(lambda e: ens2sym.get(e,"") or e)
    num=m.drop(columns=["symbol"]).apply(pd.to_numeric, errors="coerce")
    num["symbol"]=m["symbol"]
    agg=num.groupby("symbol").mean()
    agg=agg.loc[~(agg.sum(axis=1)==0)]
    agg.to_csv(os.path.join(PROC,f"GSE267799_{tiss}_symbol_count.csv"))
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
    mapped=int((~agg.index.str.startswith("ENSRNO")).sum())
    print(f"[done] {tiss}: {agg.shape}  symbol_mapped={mapped}/{agg.shape[0]} ({mapped/agg.shape[0]*100:.1f}%)")

big=pd.concat(all_samples, ignore_index=True)
big.to_csv(os.path.join(PROC,"GSE267799_all_sampletable.csv"), index=False)
print("\n[ALL] time_group:", big['time_group'].value_counts().to_dict())
print("      time_label:", big['time_label'].value_counts().to_dict())
print("      model:", big['model'].value_counts().to_dict())
