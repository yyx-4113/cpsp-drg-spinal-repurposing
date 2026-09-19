#!/usr/bin/env python3
# p5_generic.py -- generic scRNA pipeline: QC -> cluster -> canonical marker annotation -> hub localisation.
# usage: p5_generic.py <GSE> <tissue:DRG|SC>
import os, sys, glob, json
import numpy as np, pandas as pd
import scipy.io, scipy.sparse as sp
import scanpy as sc, anndata as ad
sc.settings.verbosity=1; sc.settings.n_jobs=4

ROOT="D:/2026.9/极速交付9月会员日优惠套路/01_AI生信-虚拟多重筛药/慢性疼痛"
GSE=sys.argv[1] if len(sys.argv)>1 else "GSE328175"
TISSUE=sys.argv[2] if len(sys.argv)>2 else "SC"
RAW=os.path.join(ROOT,f"data/raw/{GSE}/10x")
TAB=os.path.join(ROOT,"results/tables")

MARKERS_DRG={
 "Neuron":["Tubb3","Snhg11","Avil","Nefl","Nefh","Prph","Scn9a","Snap25","Elavl2"],
 "SatelliteGlia":["Fabp7","Gja1","Kcnj10","Slc1a3","Sox2","Cldn11"],
 "Schwann":["Mpz","Pmp22","Plp1","Mbp","Sox10","Mag","Egr2"],
 "Immune":["Ptprc","Cd68","Csf1r","Lyz2","Cd14","Fcgr3","Aif1"],
 "Endothelial":["Pecam1","Cldn5","Flt1","Emcn"],
 "Fibroblast":["Dcn","Pdgfra","Col1a1","Col1a2","Lum"],
}
MARKERS_SC={
 "Neuron":["Snap25","Rbfox3","Syt1","Tubb3","Elavl2","Meg3","Snhg11"],
 "Astrocyte":["Aqp4","Gja1","Slc1a3","Gfap","Aldh1l1","Sox9"],
 "Microglia":["Cx3cr1","P2ry12","Tmem119","Csf1r","C1qa","C1qb","C1qc","Hexb"],
 "Oligodendrocyte":["Mbp","Plp1","Mog","Mag","Cnp","Sox10","Mobp"],
 "OPC":["Pdgfra","Cspg4","Olig1","Olig2","Sox10"],
 "Endothelial":["Pecam1","Cldn5","Flt1","Emcn"],
 "Pericyte":["Pdgfrb","Rgs5","Kcnj8","Des","Vtn"],
 "Ependymal":["Foxj1","Ccdc153","Hdc","Rarres2"],
}
MARKERS=MARKERS_DRG if TISSUE=="DRG" else MARKERS_SC

def load_sample(prefix):
    X=scipy.io.mmread(os.path.join(RAW,f"{prefix}_matrix.mtx.gz")).T.tocsr().astype(np.float32)
    bc=pd.read_csv(os.path.join(RAW,f"{prefix}_barcodes.tsv.gz"),header=None)[0].values
    ft=pd.read_csv(os.path.join(RAW,f"{prefix}_features.tsv.gz"),header=None,sep="\t")
    A=ad.AnnData(X=sp.csr_matrix(X))
    A.obs_names=[f"{prefix}|{b}" for b in bc]
    A.var_names=pd.Index(ft[0].astype(str)).str.split(".").str[0]
    A.var["symbol"]=(ft[1].astype(str).values if ft.shape[1]>1 else ft[0].astype(str).values)
    A.obs["sample"]=prefix
    return A

files=sorted(set(os.path.basename(f).replace("_matrix.mtx.gz","") for f in glob.glob(os.path.join(RAW,"*_matrix.mtx.gz"))))
print(f"[{GSE}] samples: {len(files)}"); [print("   ",f) for f in files]
A=ad.concat([load_sample(f) for f in files],join="inner",index_unique=None)
A.var_names_make_unique()
ft0=pd.read_csv(os.path.join(RAW,f"{files[0]}_features.tsv.gz"),header=None,sep="\t")
ens2sym=dict(zip(ft0[0].astype(str).str.split(".").str[0], ft0[1].astype(str) if ft0.shape[1]>1 else ft0[0].astype(str)))
A.var["symbol"]=[ens2sym.get(v,"") for v in A.var_names]
A.var["mt"]=[str(s).upper().startswith("MT-") for s in A.var["symbol"]]
# condition parse
import re
def cond(s):
    s=str(s)
    for k in ["Sham","SNI","CCI","Transplant","Naive","VEH"]:
        if k.lower() in s.lower(): return k
    return "NA"
A.obs["condition"]=[cond(s) for s in A.obs["sample"]]
print("conditions:",A.obs.condition.value_counts().to_dict())

n0=A.n_obs
sc.pp.calculate_qc_metrics(A,qc_vars=["mt"],percent_top=None,log1p=False,inplace=True)
sc.pp.filter_cells(A,min_genes=200); sc.pp.filter_genes(A,min_cells=3)
A=A[A.obs.pct_counts_mt<15].copy()
print(f"QC: {n0} -> {A.n_obs} cells, {A.n_vars} genes")
sym2var={}
for vv,ss in zip(A.var_names,A.var["symbol"]): sym2var.setdefault(str(ss).upper(),vv)

A.layers["counts"]=A.X.copy()
sc.pp.normalize_total(A,target_sum=1e4); sc.pp.log1p(A); A.raw=A
sc.pp.highly_variable_genes(A,n_top_genes=2000)
A=A[:,A.var.highly_variable].copy()
sc.pp.scale(A,max_value=10)
sc.tl.pca(A,n_comps=30,svd_solver="arpack")
sc.pp.neighbors(A,n_neighbors=15,n_pcs=30)
sc.tl.leiden(A,resolution=1.0,key_added="leiden",flavor="igraph",n_iterations=2,directed=False)
print("clusters:",A.obs.leiden.nunique())
Anno=A.raw.to_adata()
# cluster mean expression via sparse matmul
leiden_codes=A.obs.leiden.astype(str)
cats=sorted(leiden_codes.unique(),key=lambda x:int(x))
present={ct:[sym2var[m.upper()] for m in ms if m.upper() in sym2var] for ct,ms in MARKERS.items()}
rows=[]
for cl in cats:
    mask=(leiden_codes==cl).values
    n=int(mask.sum())
    scores={}
    for ct,cols in present.items():
        if not cols: scores[ct]=-1; continue
        M=Anno[mask][:,cols].X
        scores[ct]=float(M.mean()) if M.nnz else 0.0
    best=max(scores,key=scores.get)
    rows.append({"cluster":cl,"n_cells":n,"assigned":best,**{f"s_{k}":round(v,3) for k,v in scores.items()}})
    print(f"  cl{cl} n={n}: {best}  {[(k,round(v,2)) for k,v in sorted(scores.items(),key=lambda x:-x[1])[:3]]}")
anno=pd.DataFrame(rows); anno.to_csv(os.path.join(TAB,f"P5_{GSE}_cluster_annotation.csv"),index=False)
A.obs["celltype"]=A.obs.leiden.map(dict(zip(anno.cluster,anno.assigned)))
A.obs[["sample","condition","leiden","celltype"]].to_csv(os.path.join(TAB,f"P5_{GSE}_cellmeta.csv"))

hub=pd.read_csv(os.path.join(TAB,"P3_hub_genes.csv"))["symbol"].str.upper().tolist()
hubp=[g for g in hub if g in sym2var]
print(f"hub present {len(hubp)}/{len(hub)}")
rows=[]
for ct in sorted(A.obs.celltype.unique()):
    cells=A.obs_names[A.obs.celltype==ct]; sub=Anno[cells]
    for g in hubp:
        v=sub[:,sym2var[g]].X; v=v.toarray().ravel() if sp.issparse(v) else np.asarray(v).ravel()
        rows.append({"celltype":ct,"symbol":g,"mean_lognorm":float(v.mean()),
                     "pct_expressing":float((v>0).mean()),"n_cells":len(cells)})
loc=pd.DataFrame(rows); loc.to_csv(os.path.join(TAB,f"P5_{GSE}_hub_localisation.csv"),index=False)
spec=[]
for g in hubp:
    s=loc[loc.symbol==g].sort_values("mean_lognorm",ascending=False); t=s.iloc[0]
    spec.append({"symbol":g,"top_celltype":t.celltype,"top_mean":t.mean_lognorm,"top_pct":t.pct_expressing})
pd.DataFrame(spec).sort_values("top_mean",ascending=False).to_csv(os.path.join(TAB,f"P5_{GSE}_hub_celltype_top.csv"),index=False)
print(f"=== P5 {GSE} done ===")
