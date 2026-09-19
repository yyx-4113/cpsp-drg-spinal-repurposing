#!/usr/bin/env python3
# p2_build_matrices.py -- build unified symbol x sample matrices for P2 bulk sets.
# Outputs to data/processed/. All sample grouping derived from series_matrix / self-describing colnames.
import os, sys, json, gzip, re
import pandas as pd
import numpy as np

ROOT="D:/2026.9/极速交付9月会员日优惠套路/01_AI生信-虚拟多重筛药/慢性疼痛"
RAW=os.path.join(ROOT,"data/raw")
META=os.path.join(ROOT,"data/raw/geo_meta")
OUT=os.path.join(ROOT,"data/processed"); os.makedirs(OUT,exist_ok=True)

def load_map(tax):
    p=os.path.join(META,f"ens2sym_tax{tax}.json")
    return json.load(open(p))

def agg_symbol(df, idcol, symcol=None, mapper=None):
    """df: rows=genes, columns=samples (numeric). Return symbol-indexed mean-aggregated frame."""
    d=df.copy()
    if symcol is not None and symcol in d.columns:
        d["__sym"]=d[symcol]
    elif mapper is not None:
        d["__sym"]=d[idcol].map(mapper)
    else:
        d["__sym"]=d[idcol]
    d=d[d["__sym"].notna() & (d["__sym"].astype(str)!="") & (~d["__sym"].astype(str).str.startswith("ENSRNOG"))]
    num=d.drop(columns=[c for c in d.columns if c in (idcol,symcol) or c.startswith("__")],
               errors="ignore")
    num=num.apply(pd.to_numeric, errors="coerce")
    num=num.drop(columns=[c for c in num.columns if num[c].notna().sum()==0])
    num["__sym"]=d["__sym"].values
    g=num.groupby("__sym").mean(numeric_only=True)
    g=g.loc[~(g.sum(axis=1)==0)]
    g.index.name="symbol"
    return g

# ---------------- GSE212311 : rat DRG, CCI vs Sham (FPKM) ----------------
def build_212311():
    p=os.path.join(RAW,"GSE212311/GSE212311_genes_fpkm_expression.txt.gz")
    df=pd.read_csv(p,sep="\t",compression="gzip")
    samp=[c for c in df.columns if c.startswith("FPKM.")]
    # gene_name column carries the rat gene symbol (authoritative; native to file)
    sub=df[["gene_id","gene_name"]+samp].copy()
    sub=sub.rename(columns={c:c.replace("FPKM.","") for c in samp})
    sub["gene_name"]=sub["gene_name"].astype(str)
    num=sub.drop(columns=["gene_id"]).set_index("gene_name")
    num=num.apply(pd.to_numeric, errors="coerce")
    num=num.loc[~((num.sum(axis=1)==0)|(num.index=="nan"))]
    g=num.groupby(num.index).mean(numeric_only=True)
    g.index.name="symbol"
    g=np.log2(g+1)
    grp={c:("CCI" if c.startswith("CCI") else "Sham") for c in g.columns}
    st=pd.DataFrame({"sample":g.columns,"group":[grp[c] for c in g.columns]})
    g.to_csv(os.path.join(OUT,"GSE212311_DRG_symbol_log2fpkm.csv"))
    st.to_csv(os.path.join(OUT,"GSE212311_DRG_sampletable.csv"),index=False)
    print(f"[212311] DRG log2FPKM {g.shape}  groups={st.group.value_counts().to_dict()}")

# ---------------- GSE278227 : rat DRG, CCI time-course (counts) ----------------
def build_278227():
    frames=[]
    for tbl in ["GSE278227_Raw_count_table_1.csv.gz","GSE278227_Raw_count_table_2.csv.gz"]:
        df=pd.read_csv(os.path.join(RAW,"GSE278227",tbl),sep="\t",compression="gzip")
        samples=[c for c in df.columns if c.startswith("DRG_")]
        f=df[["gene","gene_biotype"]+samples].copy()
        frames.append(f)
    allc=pd.concat(frames,axis=1)
    # drop duplicate columns if any
    allc=allc.loc[:,~allc.columns.duplicated()]
    # filter to protein_coding for DEG robustness
    pc=allc[allc["gene_biotype"]=="protein_coding"].copy()
    samples=[c for c in pc.columns if c.startswith("DRG_")]
    mat=pc.set_index("gene")[samples]
    mat=mat.groupby(mat.index).mean(numeric_only=True)
    mat=mat.loc[~(mat.sum(axis=1)==0)]
    mat.index.name="symbol"
    rows=[]
    for c in mat.columns:
        m=re.match(r"DRG_([MF])_(24h|1W|5W)_(CL|IL)_R(\d+)",c)
        if m:
            rows.append({"sample":c,"sex":{"M":"male","F":"female"}[m.group(1)],
                         "time":m.group(2),"side":{"CL":"contralateral","IL":"ipsilateral"}[m.group(3)],
                         "rep":int(m.group(4)),"group":f"{m.group(1)}_{m.group(2)}_{m.group(3)}"})
    st=pd.DataFrame(rows)
    mat.to_csv(os.path.join(OUT,"GSE278227_DRG_symbol_count.csv"))
    st.to_csv(os.path.join(OUT,"GSE278227_DRG_sampletable.csv"),index=False)
    print(f"[278227] DRG counts {mat.shape}  groups={sorted(st.group.unique())}")

# ---------------- GSE241361 : mouse Sigma-1 KO x SNI (counts + TMM) ----------------
def build_241361():
    m=load_map(10090)  # mouse
    for tag,fn in [("count","GSE241361_Raw_expression.tsv.gz"),("tmm","GSE241361_TMM_Normalised_expression.tsv.gz")]:
        df=pd.read_csv(os.path.join(RAW,"GSE241361",fn),sep="\t",compression="gzip")
        samp=[c for c in df.columns if c!="ENSMBL_GENE"]
        d=df.rename(columns={"ENSMBL_GENE":"ens"}).copy()
        d["ens"]=d["ens"].str.split(".").str[0]
        g=agg_symbol(d, "ens", mapper=m)
        g.to_csv(os.path.join(OUT,f"GSE241361_symbol_{tag}.csv"))
        if tag=="count":
            rows=[]
            for c in g.columns:
                mm=re.match(r"[A-F]\d+_(Naive|SNI)\d+(WT|KO)(DRG|Medula)",c)
                if mm:
                    rows.append({"sample":c,"treatment":mm.group(1),
                                 "genotype":mm.group(2),"tissue":mm.group(3)})
            pd.DataFrame(rows).to_csv(os.path.join(OUT,"GSE241361_sampletable.csv"),index=False)
            print(f"[241361] {tag} {g.shape}")
            print("         groups:", pd.DataFrame(rows).groupby(['treatment','genotype','tissue']).size().to_dict())

# ---------------- GSE306403 : human SH-SY5Y morphine vs control (counts) ----------------
def build_306403():
    m=load_map(9606)  # human
    df=pd.read_csv(os.path.join(RAW,"GSE306403/GSE306403_RNAseq_counts_matrix.txt.gz"),
                   sep="\t",compression="gzip")
    samp=[c for c in df.columns if c!="Geneid"]
    d=df.rename(columns={"Geneid":"ens"}).copy()
    d["ens"]=d["ens"].str.split(".").str[0]
    g=agg_symbol(d,"ens",mapper=m)
    g.to_csv(os.path.join(OUT,"GSE306403_SH-SY5Y_symbol_count.csv"))
    rows=[]
    for c in g.columns:
        grp="Control" if c.lower().startswith("control") else "Morphine"
        rows.append({"sample":c,"group":grp})
    pd.DataFrame(rows).to_csv(os.path.join(OUT,"GSE306403_sampletable.csv"),index=False)
    print(f"[306403] SH-SY5Y {g.shape}  groups={pd.DataFrame(rows).group.value_counts().to_dict()}")

# ---------------- GSE265957 : mouse DRG+SC Ribo-seq (Xtail tables) ----------------
def build_265957():
    p=os.path.join(RAW,"GSE265957/GSE265957_processed_files_tpms_and_degs_SNI_TRAP_and_RF.xlsx")
    xl=pd.ExcelFile(p)
    xt=[s for s in xl.sheet_names if s.startswith("Xtail")]
    for s in xt:
        df=xl.parse(s)
        tag=re.sub(r"[^A-Za-z0-9]+","_",s).strip("_")
        keep=[c for c in ["ensmusg","gene","mRNA_log2FC","RPF_log2FC","log2FC_TE_v1","pvalue_v1",
                          "log2FC_TE_v2","pvalue_v2","log2FC_TE_final","pvalue_final","pvalue.adjust","category"] if c in df.columns]
        out=df[keep].copy()
        out.to_csv(os.path.join(OUT,f"GSE265957_{tag}.csv"),index=False)
        print(f"[265957] sheet '{s}' -> {tag} shape={out.shape}")
    # TRAP TPM sheets (cell-type specific spinal cord)
    for s in [x for x in xl.sheet_names if "DEGs" in x]:
        df=xl.parse(s)
        tag=re.sub(r"[^A-Za-z0-9]+","_",s).strip("_")
        df.to_csv(os.path.join(OUT,f"GSE265957_TRAP_{tag}.csv"),index=False)
        print(f"[265957] TRAP sheet '{s}' -> shape={df.shape}")

if __name__=="__main__":
    print("== building P2 matrices ==")
    for fn in [build_212311, build_278227, build_241361, build_306403, build_265957]:
        try: fn()
        except Exception as e:
            import traceback; print(f"[ERR] {fn.__name__}: {e}",file=sys.stderr); traceback.print_exc()
    print("== done ==")
