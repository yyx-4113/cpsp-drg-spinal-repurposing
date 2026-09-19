#!/usr/bin/env python3
# p5_fetch.py -- download GSE RAW.tar and extract 10x triplet files into data/raw/<GSE>/10x/
import os, sys, tarfile, urllib.request
ROOT="D:/2026.9/极速交付9月会员日优惠套路/01_AI生信-虚拟多重筛药/慢性疼痛"
RAW=os.path.join(ROOT,"data/raw")
def bucket(g): n=g[3:]; return "GSE"+n[:3]+"nnn"
def fetch_gse(gse):
    base=f"https://ftp.ncbi.nlm.nih.gov/geo/series/{bucket(gse)}/{gse}/suppl/"
    tar_url=base+f"{gse}_RAW.tar"
    tdir=os.path.join(RAW,gse); os.makedirs(tdir,exist_ok=True)
    tpath=os.path.join(tdir,f"{gse}_RAW.tar")
    if not (os.path.exists(tpath) and os.path.getsize(tpath)>1e6):
        print(f"[dl] {tar_url}",file=sys.stderr); urllib.request.urlretrieve(tar_url,tpath)
        print(f"[ok] tar {os.path.getsize(tpath)}",file=sys.stderr)
    dst=os.path.join(tdir,"10x"); os.makedirs(dst,exist_ok=True)
    with tarfile.open(tpath) as tf:
        members=[m for m in tf.getmembers() if m.name.endswith((".gz",".mtx",".tsv")) and m.isfile()]
        for m in members:
            out=os.path.join(dst,os.path.basename(m.name))
            if os.path.exists(out) and os.path.getsize(out)>500: continue
            f=tf.extractfile(m)
            with open(out,"wb") as w: w.write(f.read())
            print(f"[x] {os.path.basename(m.name)} {os.path.getsize(out)}",file=sys.stderr)
    print(f"[done] {gse}",file=sys.stderr)
if __name__=="__main__":
    for g in (sys.argv[1:] or ["GSE216039"]):
        fetch_gse(g)
