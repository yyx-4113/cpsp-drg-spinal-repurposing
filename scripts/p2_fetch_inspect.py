#!/usr/bin/env python3
# p2_fetch_inspect.py -- download + inspect remaining bulk/miRNA matrices
import urllib.request, os, sys, gzip
import pandas as pd

ROOT="D:/2026.9/极速交付9月会员日优惠套路/01_AI生信-虚拟多重筛药/慢性疼痛"
RAW=os.path.join(ROOT,"data/raw"); 

FILES=[
 # (gse, bucket_nnn, filename, kind)
 ("GSE212311","GSE212nnn","GSE212311_genes_fpkm_expression.txt.gz","txt"),
 ("GSE265957","GSE265nnn","GSE265957_processed_files_tpms_and_degs_SNI_TRAP_and_RF.xlsx","xlsx"),
 ("GSE278227","GSE278nnn","GSE278227_Raw_count_table_1.csv.gz","csv"),
 ("GSE278227","GSE278nnn","GSE278227_Raw_count_table_2.csv.gz","csv"),
 ("GSE241361","GSE241nnn","GSE241361_Raw_expression.tsv.gz","tsv"),
 ("GSE241361","GSE241nnn","GSE241361_TMM_Normalised_expression.tsv.gz","tsv"),
 ("GSE306403","GSE306nnn","GSE306403_RNAseq_counts_matrix.txt.gz","txt"),
 ("GSE158825","GSE158nnn","GSE158825_Lively_human_plasma_SFOA-maturemiRNAcounts.tsv.gz","tsv"),
 ("GSE222979","GSE222nnn","GSE222979_2023_Match414_3biofluids_miRNA_counts.tsv.gz","tsv"),
]

def dl(gse,bucket,fn):
    d=os.path.join(RAW,gse); os.makedirs(d,exist_ok=True)
    out=os.path.join(d,fn)
    url=f"https://ftp.ncbi.nlm.nih.gov/geo/series/{bucket}/{gse}/suppl/{fn}"
    if os.path.exists(out) and os.path.getsize(out)>1000:
        print(f"[cached] {gse}/{fn}",file=sys.stderr); return out
    print(f"[dl] {url}",file=sys.stderr)
    urllib.request.urlretrieve(url,out)
    return out

def inspect(gse,fn,kind,path):
    print(f"\n===== {gse}/{fn} ({kind}) =====")
    if kind=="xlsx":
        xl=pd.ExcelFile(path)
        print("sheets:",xl.sheet_names)
        df=xl.parse(xl.sheet_names[0], nrows=5)
        print("shape(first sheet head):", df.shape)
        print("cols[:6]:", list(df.columns[:6]))
        print(df.head(3).to_string())
        return
    # text gz
    if fn.endswith(".txt.gz"):
        df=pd.read_csv(path, sep="\t", compression="gzip", nrows=5)
    elif fn.endswith(".tsv.gz"):
        df=pd.read_csv(path, sep="\t", compression="gzip", nrows=5)
    elif fn.endswith(".csv.gz"):
        df=pd.read_csv(path, compression="gzip", nrows=5)
    else:
        df=pd.read_csv(path, nrows=5)
    # full shape via quick count of lines
    print("cols[:6]:", list(df.columns[:6]))
    print("first col name:", repr(df.columns[0]), "dtype:", df.dtypes.iloc[0])
    print("first-col head:", df[df.columns[0]].head(6).tolist())
    print("head(3):")
    print(df.iloc[:3,:5].to_string())
    # approximate full row count
    if fn.endswith(".gz"):
        with gzip.open(path,"rt",encoding="utf-8",errors="replace") as f:
            n=sum(1 for _ in f)
        print("approx rows (incl header):", n)

if __name__=="__main__":
    for gse,bucket,fn,kind in FILES:
        p=dl(gse,bucket,fn)
        inspect(gse,fn,kind,p)
