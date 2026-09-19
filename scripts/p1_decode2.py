#!/usr/bin/env python3
# p1_decode2.py -- (a) map suppl token <-> time via source_name; (b) fetch GPL32253 annot (correct bucket)
import urllib.request, gzip, os, sys, json
import pandas as pd

META = "D:/2026.9/极速交付9月会员日优惠套路/01_AI生信-虚拟多重筛药/慢性疼痛/data/raw/geo_meta"
mat_path = os.path.join(META, "GSE267799_series_matrix.txt.gz")

title=src=gsm=None
chars=[]
with gzip.open(mat_path, "rt", encoding="utf-8", errors="replace") as f:
    for line in f:
        if line.startswith("!Sample_title"): title=line.rstrip("\n").split("\t")[1:]
        elif line.startswith("!Sample_source_name_ch1"): src=line.rstrip("\n").split("\t")[1:]
        elif line.startswith("!Sample_geo_accession"): gsm=line.rstrip("\n").split("\t")[1:]
        elif line.startswith("!Sample_characteristics_ch1"): chars.append(line.rstrip("\n").split("\t")[1:])
        if line.startswith("!series_matrix_table_begin"): break

n=len(title)
print(f"[n] {n}; src_head={src[:4] if src else None}")
# decode token -> time by pairing source_name (token) with characteristics(time)
per=[[] for _ in range(n)]
for r in chars:
    for i in range(min(n,len(r))):
        if r[i].strip(): per[i].append(r[i].strip())
recs=[]
for i in range(n):
    d={"geo":gsm[i] if gsm else "","source":src[i] if src else "","title":title[i] if title else ""}
    for c in per[i]:
        if ":" in c:
            k,v=c.split(":",1); d[k.strip()]=v.strip()
    recs.append(d)
sdf=pd.DataFrame(recs)
out=os.path.join(META,"GSE267799_samples_full.csv")
sdf.to_csv(out,index=False)
print(f"[saved] {out}")
print("\nsample (source | tissue | treatment | time | rep):")
for _,r in sdf.iterrows():
    print(f"  {r.get('source',''):22} | {r.get('tissue','')} | {r.get('treatment','')} | {r.get('time','')} | {r.get('replicated animal_number','')}")
# token -> time mapping summary
print("\n== token(time-digit) -> time label ==")
import re
m={}
for _,r in sdf.iterrows():
    s=r.get('source','')
    t=r.get('time','')
    mm=re.search(r'_(\d+)_', str(s))
    if mm and t:
        m[mm.group(1)]=t
for k in sorted(m): print(f"  token {k} -> {m[k]}")

# ---- (b) GPL32253 annot ----
def try_dl(urls, outp):
    for u in urls:
        try:
            print(f"\n[try] {u}", file=sys.stderr)
            req=urllib.request.Request(u, headers={"User-Agent":"research/1.0"})
            with urllib.request.urlopen(req, timeout=120) as r:
                data=r.read()
            if len(data)<1000:
                print(f"  too small ({len(data)}), skip", file=sys.stderr); continue
            with open(outp,"wb") as f: f.write(data)
            print(f"  OK {len(data)} bytes", file=sys.stderr)
            return u
        except Exception as e:
            print(f"  fail: {e}", file=sys.stderr)
    return None

ann_out=os.path.join(META,"GPL32253.annot.gz")
urls=[
 "https://ftp.ncbi.nlm.nih.gov/geo/platforms/GPL322nn/GPL32253/annot/GPL32253.annot.gz",
 "https://ftp.ncbi.nlm.nih.gov/geo/platforms/GPL3nnn/GPL32253/annot/GPL32253.annot.gz",
 "https://ftp.ncbi.nlm.nih.gov/geo/platforms/GPL322nn/GPL32253/soft/GPL32253.soft.gz",
]
got=try_dl(urls, ann_out)
print(f"\n[annot] got={got}")
if got:
    idcol=symcol=None; ens2sym={}
    with gzip.open(ann_out,"rt",encoding="utf-8",errors="replace") as f:
        header=None
        for line in f:
            if line.startswith("#"): continue
            if header is None:
                header=line.rstrip("\n").split("\t")
                for j,h in enumerate(header):
                    hl=h.lower()
                    if h=="ID": idcol=j
                    if "gene symbol" in hl or h=="Gene Symbol": symcol=j
                print("[annot header]",header[:10],"idcol",idcol,"symcol",symcol)
                if idcol is None or symcol is None: break
                continue
            parts=line.rstrip("\n").split("\t")
            eid=parts[idcol].strip(); sym=parts[symcol].strip() if symcol<len(parts) else ""
            if eid: ens2sym[eid]=sym
    print(f"[annot] mapped {len(ens2sym)}; sample {list(ens2sym.items())[:5]}")
    json.dump(ens2sym, open(os.path.join(META,"GPL32253_ens2sym.json"),"w"))
    print("[saved] GPL32253_ens2sym.json")
