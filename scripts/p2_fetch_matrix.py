#!/usr/bin/env python3
# p2_fetch_matrix.py -- download ALL series_matrix.txt.gz for target GSEs (handles multi-platform)
import os, sys, re, urllib.request
ROOT="D:/2026.9/极速交付9月会员日优惠套路/01_AI生信-虚拟多重筛药/慢性疼痛"
RAW=os.path.join(ROOT,"data/raw")
GSES=["GSE212311","GSE265957","GSE278227","GSE241361","GSE306403","GSE158825","GSE222979"]
def bucket(gse):
    n=gse[3:]; return "GSE"+n[:3]+"nnn"
def fetch(gse):
    b=bucket(gse)
    base=f"https://ftp.ncbi.nlm.nih.gov/geo/series/{b}/{gse}/matrix/"
    try:
        h=urllib.request.urlopen(base,timeout=40).read().decode("utf-8","replace")
    except Exception as e:
        print(f"[FAIL list] {gse}: {e}",file=sys.stderr); return
    names=[n for n in re.findall(r'href="([^"]+)"',h) if "series_matrix" in n]
    dst_dir=os.path.join(RAW,gse); os.makedirs(dst_dir,exist_ok=True)
    for fn in names:
        dst=os.path.join(dst_dir,fn)
        if os.path.exists(dst) and os.path.getsize(dst)>500:
            print(f"[skip] {fn}",file=sys.stderr); continue
        try:
            urllib.request.urlretrieve(base+fn,dst)
            print(f"[ok] {gse}/{fn} {os.path.getsize(dst)}",file=sys.stderr)
        except Exception as e:
            print(f"[FAIL dl] {gse}/{fn}: {e}",file=sys.stderr)
for g in GSES:
    fetch(g)
print("[done]",file=sys.stderr)
