#!/usr/bin/env python3
# p1_decode3.py -- (a) fix GPL annot bucket (GPL32nnn); (b) efetch one GSM to find token naming
import urllib.request, gzip, os, sys, json
META="D:/2026.9/极速交付9月会员日优惠套路/01_AI生信-虚拟多重筛药/慢性疼痛/data/raw/geo_meta"

def dl(u,out):
    if os.path.exists(out) and os.path.getsize(out)>1000:
        print(f"[cached] {os.path.basename(out)}"); return True
    try:
        req=urllib.request.Request(u,headers={"User-Agent":"research/1.0"})
        with urllib.request.urlopen(req,timeout=120) as r: data=r.read()
        if len(data)<1000: print(f"[skip small] {u} {len(data)}"); return False
        open(out,"wb").write(data); print(f"[ok] {u} {len(data)}"); return True
    except Exception as e:
        print(f"[fail] {u}: {e}"); return False

# (a) annot
ann=os.path.join(META,"GPL32253.annot.gz")
ok=False
for u in [
 "https://ftp.ncbi.nlm.nih.gov/geo/platforms/GPL32nnn/GPL32253/annot/GPL32253.annot.gz",
 "https://ftp.ncbi.nlm.nih.gov/geo/platforms/GPL32nnn/GPL32253/soft/GPL32253.soft.gz",
]:
    if dl(u,ann): ok=True; break
if ok:
    idc=syc=None; m={}
    with gzip.open(ann,"rt",encoding="utf-8",errors="replace") as f:
        hdr=None
        for line in f:
            if line.startswith("#"): continue
            if hdr is None:
                hdr=line.rstrip("\n").split("\t")
                for j,h in enumerate(hdr):
                    hl=h.lower()
                    if h=="ID": idc=j
                    if "gene symbol" in hl or h=="Gene Symbol": syc=j
                print("[hdr]",hdr[:10],"idc",idc,"syc",syc); 
                if idc is None or syc is None: break
                continue
            p=line.rstrip("\n").split("\t")
            e=p[idc].strip(); s=p[syc].strip() if syc<len(p) else ""
            if e: m[e]=s
    print(f"[annot] mapped {len(m)}; e.g.",list(m.items())[:5])
    json.dump(m,open(os.path.join(META,"GPL32253_ens2sym.json"),"w"))

# (b) efetch GSM8278924 to find token
def get(u):
    req=urllib.request.Request(u,headers={"User-Agent":"research/1.0"})
    with urllib.request.urlopen(req,timeout=40) as r: return r.read().decode("utf-8","replace")
txt=get("https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=gds&id=8278924&rettype=xml")
print("\n===== GSM8278924 efetch (first 1500 chars) =====")
print(txt[:1500])
import re
toks=re.findall(r'[A-Za-z]+_\d+_\d+_[A-Za-z]+', txt)
print("\ntoken-like matches:", set(toks))
