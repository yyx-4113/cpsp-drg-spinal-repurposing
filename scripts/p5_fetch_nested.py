#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""p5_fetch_nested.py -- flatten *nested* 10x archives (e.g. GSE246288 ships
   GSMxxxx_<sample>_raw_feature_bc_matrix.tar.gz) into data/raw/<GSE>/10x/<prefix>_{matrix.mtx,barcodes.tsv,features.tsv}.gz
"""
import os, sys, tarfile, gzip, shutil, glob, re

ROOT = "D:/2026.9/极速交付9月会员日优惠套路/01_AI生信-虚拟多重筛药/慢性疼痛"
SUFFIX = {"matrix.mtx.gz": "_matrix.mtx.gz", "barcodes.tsv.gz": "_barcodes.tsv.gz",
          "features.tsv.gz": "_features.tsv.gz", "genes.tsv.gz": "_features.tsv.gz"}

def flatten(gse):
    src = os.path.join(ROOT, f"data/raw/{gse}/10x")
    dst = os.path.join(ROOT, f"data/raw/{gse}/10x_flat")
    os.makedirs(dst, exist_ok=True)
    tars = sorted(glob.glob(os.path.join(src, "*.tar.gz")))
    print(f"{gse}: {len(tars)} nested archives", flush=True)
    for t in tars:
        prefix = os.path.basename(t).replace("_raw_feature_bc_matrix.tar.gz", "").replace(".tar.gz", "")
        with tarfile.open(t, "r:gz") as tf:
            for m in tf.getmembers():
                if not m.isfile():
                    continue
                base = os.path.basename(m.name)
                if base not in SUFFIX:
                    continue
                out = os.path.join(dst, prefix + SUFFIX[base])
                if os.path.exists(out) and os.path.getsize(out) > 500:
                    continue
                f = tf.extractfile(m)
                with open(out, "wb") as w:
                    shutil.copyfileobj(f, w)
        ok = all(os.path.exists(os.path.join(dst, prefix + s)) for s in
                 ["_matrix.mtx.gz", "_barcodes.tsv.gz", "_features.tsv.gz"])
        print(f"  {prefix}: {'OK' if ok else 'INCOMPLETE'}  "
              f"({', '.join(sorted(os.path.basename(p) for p in glob.glob(os.path.join(dst, prefix + '_*'))))})",
              flush=True)
    return dst

if __name__ == "__main__":
    for g in (sys.argv[1:] or ["GSE246288"]):
        d = flatten(g)
        print("->", d)
