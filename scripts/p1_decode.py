#!/usr/bin/env python3
# p1_decode.py -- decode GSE267799 sample design + build Ensembl->symbol map (P1)
import urllib.request, gzip, io, os, sys, csv, re
import pandas as pd

RAW = "D:/2026.9/极速交付9月会员日优惠套路/01_AI生信-虚拟多重筛药/慢性疼痛/data/raw"
META = os.path.join(RAW, "geo_meta")
os.makedirs(META, exist_ok=True)

def download(url, out):
    if os.path.exists(out) and os.path.getsize(out) > 0:
        print(f"[cached] {os.path.basename(out)}", file=sys.stderr)
        return out
    print(f"[dl] {url}", file=sys.stderr)
    req = urllib.request.Request(url, headers={"User-Agent":"research/1.0"})
    with urllib.request.urlopen(req, timeout=180) as r:
        data = r.read()
    with open(out, "wb") as f:
        f.write(data)
    print(f"[dl] {len(data)} bytes -> {out}", file=sys.stderr)
    return out

# ---- 1) series matrix: decode sample characteristics ----
mat_url = "https://ftp.ncbi.nlm.nih.gov/geo/series/GSE267nnn/GSE267799/matrix/GSE267799_series_matrix.txt.gz"
mat_path = os.path.join(META, "GSE267799_series_matrix.txt.gz")
download(mat_url, mat_path)

chars_rows = []   # each: list across samples
titles = None
gsm = None
with gzip.open(mat_path, "rt", encoding="utf-8", errors="replace") as f:
    for line in f:
        if line.startswith("!Sample_title"):
            titles = line.rstrip("\n").split("\t")[1:]
        elif line.startswith("!Sample_geo_accession"):
            gsm = line.rstrip("\n").split("\t")[1:]
        elif line.startswith("!Sample_characteristics_ch1"):
            chars_rows.append(line.rstrip("\n").split("\t")[1:])
        if line.startswith("!series_matrix_table_begin"):
            break

n = len(titles)
print(f"\n[n samples] {n}")
print(f"[title head] {titles[:6]}")
print(f"[gsm head]  {gsm[:6]}")

# transpose characteristics: per sample list of "k: v"
per_sample = [[] for _ in range(n)]
for row in chars_rows:
    for i in range(min(n, len(row))):
        if row[i].strip():
            per_sample[i].append(row[i].strip())

# build dataframe
recs = []
for i in range(n):
    d = {"geo_accession": gsm[i] if gsm else "", "title": titles[i] if titles else ""}
    for c in per_sample[i]:
        if ":" in c:
            k, v = c.split(":", 1)
            d[k.strip()] = v.strip()
        else:
            d.setdefault("note", "")
            d["note"] += c + "; "
    recs.append(d)

sdf = pd.DataFrame(recs)
out_csv = os.path.join(META, "GSE267799_samples.csv")
sdf.to_csv(out_csv, index=False)
print(f"\n[saved sample table] {out_csv}")
# show unique characteristic keys + value counts
for col in sdf.columns:
    if col in ("geo_accession","title","note"):
        continue
    vc = sdf[col].value_counts(dropna=False)
    print(f"\n-- {col} ({sdf[col].nunique()} unique) --")
    print(vc.to_string())

# ---- 2) GPL32253 annotation: Ensembl -> symbol ----
ann_url = "https://ftp.ncbi.nlm.nih.gov/geo/platforms/GPL3nnn/GPL32253/annot/GPL32253.annot.gz"
ann_path = os.path.join(META, "GPL32253.annot.gz")
download(ann_url, ann_path)
# parse annot: find ID and Gene Symbol columns
idcol = symcol = None
ens2sym = {}
with gzip.open(ann_path, "rt", encoding="utf-8", errors="replace") as f:
    header = None
    for line in f:
        if line.startswith("#"):
            continue
        if header is None:
            header = line.rstrip("\n").split("\t")
            print("\n[annot header]", header[:12])
            for j,h in enumerate(header):
                hl = h.lower()
                if h == "ID":
                    idcol = j
                if "gene symbol" in hl or h == "Gene Symbol" or "symbol" == hl:
                    symcol = j
            print(f"[annot] idcol={idcol} symcol={symcol}")
            continue
        parts = line.rstrip("\n").split("\t")
        if idcol is None or symcol is None:
            break
        eid = parts[idcol].strip()
        sym = parts[symcol].strip() if symcol < len(parts) else ""
        if eid:
            ens2sym[eid] = sym
print(f"\n[annot] mapped {len(ens2sym)} IDs; sample:", list(ens2sym.items())[:5])
import json
with open(os.path.join(META, "GPL32253_ens2sym.json"), "w") as f:
    json.dump(ens2sym, f)
print("[saved] GPL32253_ens2sym.json")
