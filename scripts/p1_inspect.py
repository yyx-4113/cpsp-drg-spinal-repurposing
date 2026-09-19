#!/usr/bin/env python3
# p1_inspect.py -- download + inspect GSE267799 SMIR_DRG matrix structure (P1 start)
import urllib.request, gzip, io, os, sys
import pandas as pd

FTP = "https://ftp.ncbi.nlm.nih.gov/geo/series/GSE267nnn/GSE267799/suppl"
RAW = "D:/2026.9/极速交付9月会员日优惠套路/01_AI生信-虚拟多重筛药/慢性疼痛/data/raw/GSE267799"
os.makedirs(RAW, exist_ok=True)

FILES = [
    "GSE267799_SMIR_DRG_gene_sample_count.xls.gz",
    "GSE267799_SMIR_DRG_gene_sample_FPKM.xls.gz",
]

def download(fname):
    url = f"{FTP}/{fname}"
    out = os.path.join(RAW, fname)
    if not os.path.exists(out):
        print(f"[dl] {fname} ...", file=sys.stderr)
        req = urllib.request.Request(url, headers={"User-Agent":"research/1.0"})
        with urllib.request.urlopen(req, timeout=120) as r:
            data = r.read()
        with open(out, "wb") as f:
            f.write(data)
        print(f"[dl] saved {len(data)} bytes", file=sys.stderr)
    else:
        print(f"[dl] cached {fname}", file=sys.stderr)
    return out

def inspect(fname):
    gz = os.path.join(RAW, fname)
    # despite .xls.gz extension, these are gzipped TAB-separated text
    df = pd.read_csv(gz, sep="\t", compression="gzip")
    print(f"\n===== {fname} =====")
    print("shape:", df.shape)
    print("columns[:6]:", list(df.columns[:6]))
    print("n columns:", len(df.columns))
    first = df.columns[0]
    print("first col name:", repr(first), "| dtype:", df.dtypes.iloc[0])
    print("first-col sample (head 8):", df[first].head(8).tolist())
    print("first col numeric?:", pd.api.types.is_numeric_dtype(df[first]))
    print("head(3) transposed (first 4 cols):")
    print(df.iloc[:3, :4].to_string())
    # sample-column name pattern
    print("sample-column examples:", list(df.columns[1:6]))

if __name__ == "__main__":
    for fn in FILES:
        p = download(fn)
        inspect(fn)
