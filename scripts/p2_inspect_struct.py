#!/usr/bin/env python3
# p2_inspect_struct.py -- peek structure of downloaded suppl matrices (gene-id type, sample cols, head)
import os, gzip, json
ROOT="D:/2026.9/极速交付9月会员日优惠套路/01_AI生信-虚拟多重筛药/慢性疼痛"
RAW=os.path.join(ROOT,"data/raw")

def peek_gz_tsv(path, nlines=3, ncols=6):
    out={"path":os.path.relpath(path,ROOT),"size":os.path.getsize(path)}
    with gzip.open(path,"rt",encoding="utf-8",errors="replace") as f:
        lines=[]
        for i,ln in enumerate(f):
            if i>=nlines: break
            lines.append(ln.rstrip("\n"))
    if lines:
        hdr=lines[0].split("\t")
        out["n_cols"]=len(hdr)
        out["header_first"]=hdr[:ncols]
        out["first_data_row"]=lines[1].split("\t")[:ncols] if len(lines)>1 else []
        out["second_data_row"]=lines[2].split("\t")[:ncols] if len(lines)>2 else []
    return out

def peek_xlsx(path):
    import pandas as pd
    out={"path":os.path.relpath(path,ROOT),"size":os.path.getsize(path)}
    xl=pd.ExcelFile(path)
    out["sheets"]=xl.sheet_names
    for s in xl.sheet_names[:3]:
        df=xl.parse(s, nrows=3)
        out.setdefault("sheet_preview",{})[s]={"shape_head":list(df.columns[:6]),
            "row0":[str(x)[:20] for x in df.iloc[0].tolist()[:6]] if len(df)>0 else []}
    return out

files={
 "GSE212311":"GSE212311/GSE212311_genes_fpkm_expression.txt.gz",
 "GSE278227_1":"GSE278227/GSE278227_Raw_count_table_1.csv.gz",
 "GSE278227_2":"GSE278227/GSE278227_Raw_count_table_2.csv.gz",
 "GSE241361_raw":"GSE241361/GSE241361_Raw_expression.tsv.gz",
 "GSE241361_tmm":"GSE241361/GSE241361_TMM_Normalised_expression.tsv.gz",
 "GSE306403":"GSE306403/GSE306403_RNAseq_counts_matrix.txt.gz",
 "GSE158825_mi":"GSE158825/GSE158825_Lively_human_plasma_SFOA-maturemiRNAcounts.tsv.gz",
 "GSE222979_mi":"GSE222979/GSE222979_2023_Match414_3biofluids_miRNA_counts.tsv.gz",
}
report={}
for k,rel in files.items():
    p=os.path.join(RAW,rel)
    if not os.path.exists(p):
        report[k]={"missing":True}; continue
    if rel.endswith(".xlsx"):
        try: report[k]=peek_xlsx(p)
        except Exception as e: report[k]={"error":str(e)}
    else:
        report[k]=peek_gz_tsv(p)
print(json.dumps(report,indent=2,ensure_ascii=False))
json.dump(report, open(os.path.join(ROOT,"data/raw/geo_meta/p2_struct.json"),"w"), ensure_ascii=False, indent=2)
