#!/usr/bin/env python3
# p5_scrna.py -- GSE216039 mouse DRG scRNA: QC -> cluster -> canonical annotation -> hub localisation
# Discipline: cell-level only descriptive; condition comparison done at SAMPLE-level pseudobulk (n=2/group -> underpowered).
import os, sys, glob, re, json
import numpy as np, pandas as pd
import scipy.io, scipy.sparse as sp
import scanpy as sc
import anndata as ad
sc.settings.verbosity=1
sc.settings.n_jobs=4

ROOT="D:/2026.9/极速交付9月会员日优惠套路/01_AI生信-虚拟多重筛药/慢性疼痛"
RAW=os.path.join(ROOT,"data/raw/GSE216039/10x")
TAB=os.path.join(ROOT,"results/tables"); os.makedirs(TAB,exist_ok=True)

def load_sample(prefix):
    mtx=os.path.join(RAW,f"{prefix}_matrix.mtx.gz")
    bcs=os.path.join(RAW,f"{prefix}_barcodes.tsv.gz")
    fts=os.path.join(RAW,f"{prefix}_features.tsv.gz")
    X=scipy.io.mmread(mtx).T.tocsr().astype(np.float32)     # cells x genes
    bc=pd.read_csv(bcs,header=None)[0].values
    ft=pd.read_csv(fts,header=None,sep="\t")
    ens=ft[0].astype(str).values
    sym=ft[1].astype(str).values if ft.shape[1]>1 else ens
    A=ad.AnnData(X=sp.csr_matrix(X))
    A.obs_names=[f"{prefix}|{b}" for b in bc]
    A.var_names=pd.Index(ens).str.split(".").str[0]      # Ensembl ID -> unique & consistent across samples
    A.var["symbol"]=sym
    A.var["mt"]=pd.Series(sym).str.upper().str.startswith("MT-").values
    A.obs["sample"]=prefix
    return A

files=sorted(set(os.path.basename(f).replace("_matrix.mtx.gz","") for f in glob.glob(os.path.join(RAW,"*_matrix.mtx.gz"))))
print("samples found:",len(files))
for f in files: print("  ",f)
ads=[load_sample(f) for f in files]
A=ad.concat(ads,join="inner",index_unique=None)   # inner: keep genes shared by all samples
A.var_names_make_unique()
# rebuild symbol map from the first sample's features (concat may drop var columns)
ft0=pd.read_csv(os.path.join(RAW,f"{files[0]}_features.tsv.gz"),header=None,sep="\t")
_e=ft0[0].astype(str).str.split(".").str[0]; _s=ft0[1].astype(str) if ft0.shape[1]>1 else _e
ens2sym=dict(zip(_e,_s))
A.var["symbol"]=[ens2sym.get(v,"") for v in A.var_names]
sym2var={}
for v,s in zip(A.var_names,A.var["symbol"]):
    sym2var.setdefault(str(s).upper(),v)   # symbol -> var name (first)
A.var["mt"]=[str(s).upper().startswith("MT-") for s in A.var["symbol"]]
def gene_view(adata,symbols):
    cols=[sym2var[s] for s in symbols if s in sym2var]
    return cols
print("combined:",A.shape)
# group label
A.obs["condition"]=["CCI" if "CCI" in s else "Sham" for s in A.obs["sample"]]
A.obs["sex"]=["Male" if "Male" in s else ("Female" if "Female" in s else "NA") for s in A.obs["sample"]]
print(A.obs.groupby(["condition","sex"],observed=True).size().to_dict())

# ---- QC ----
A.var["mt"]=A.var_names.str.upper().str.startswith("MT-")
sc.pp.calculate_qc_metrics(A,qc_vars=["mt"],percent_top=None,log1p=False,inplace=True)
n0=A.n_obs
sc.pp.filter_cells(A,min_genes=200)
sc.pp.filter_genes(A,min_cells=3)
A=A[A.obs.pct_counts_mt<15].copy()
print(f"QC: {n0} -> {A.n_obs} cells, {A.n_vars} genes")
# rebuild symbol map AFTER gene filtering so it matches A.raw / Anno
sym2var={}
for vv,ss in zip(A.var_names,A.var["symbol"]):
    sym2var.setdefault(str(ss).upper(),vv)

# ---- normalise / cluster ----
A.layers["counts"]=A.X.copy()
sc.pp.normalize_total(A,target_sum=1e4); sc.pp.log1p(A)
A.raw=A
sc.pp.highly_variable_genes(A,n_top_genes=2000)
A=A[:,A.var.highly_variable].copy()
sc.pp.scale(A,max_value=10)
sc.tl.pca(A,n_comps=30,svd_solver="arpack")
sc.pp.neighbors(A,n_neighbors=15,n_pcs=30)
sc.tl.leiden(A,resolution=1.0,key_added="leiden",flavor="igraph",n_iterations=2,directed=False)
print("clusters:",A.obs.leiden.nunique())

# ---- annotate by canonical markers ----
MARKERS={
 "Neuron":["Tubb3","Snhg11","Avil","Nefl","Nefh","Prph","Scn9a","Snap25","Elavl2"],
 "SatelliteGlia":["Fabp7","Gja1","Kcnj10","Slc1a3","Sox2","S100b","Cldn11"],
 "Schwann":["Mpz","Pmp22","Plp1","Mbp","Sox10","Mag","Egr2"],
 "Immune":["Ptprc","Cd68","Csf1r","Lyz2","Cd14","Fcgr3","Aif1"],
 "Endothelial":["Pecam1","Cldn5","Flt1","Emcn","Cd34"],
 "Fibroblast":["Dcn","Pdgfra","Col1a1","Col1a2","Lum"],
 "Erythrocyte":["Hba-a1","Hbb-bs","Hba-a2"],
}
Anno=A.raw.to_adata()   # already log-normalised (A.raw set right after normalize_total+log1p)
anno_rows=[]
for cl in sorted(A.obs.leiden.unique(),key=lambda x:int(x)):
    cells=A.obs_names[A.obs.leiden==cl]
    sub=Anno[cells]
    scores={}
    for ct,ms in MARKERS.items():
        present=gene_view(sub,[m.upper() for m in ms])
        if not present: scores[ct]=-1; continue
        scores[ct]=float(np.mean(sub[:,present].X.toarray()))
    best=max(scores,key=scores.get)
    anno_rows.append({"cluster":cl,"n_cells":len(cells),"assigned":best,
                      **{f"score_{k}":round(v,3) for k,v in scores.items()}})
    print(f"  cluster {cl} (n={len(cells)}): {best}  {[(k,round(v,2)) for k,v in sorted(scores.items(),key=lambda x:-x[1])[:3]]}")
anno=pd.DataFrame(anno_rows); anno.to_csv(os.path.join(TAB,"P5_GSE216039_cluster_annotation.csv"),index=False)
A.obs["celltype"]=A.obs.leiden.map(dict(zip(anno.cluster,anno.assigned)))
A.obs[["sample","condition","sex","leiden","celltype"]].to_csv(os.path.join(TAB,"P5_GSE216039_cellmeta.csv"))
print("celltype counts:",A.obs.celltype.value_counts().to_dict())

# ---- hub localisation (cell-level descriptive) ----
hub=pd.read_csv(os.path.join(TAB,"P3_hub_genes.csv"))["symbol"].str.upper().tolist()
hubp=[g for g in hub if g in sym2var]
print(f"hub genes present: {len(hubp)}/{len(hub)}")
rows=[]
for ct in sorted(A.obs.celltype.unique()):
    cells=A.obs_names[A.obs.celltype==ct]
    sub=Anno[cells]
    for g in hubp:
        v=sub[:,sym2var[g]].X
        v=v.toarray().ravel() if sp.issparse(v) else np.asarray(v).ravel()
        rows.append({"celltype":ct,"symbol":g,"mean_lognorm":float(v.mean()),
                     "pct_expressing":float((v>0).mean()),"n_cells":len(cells)})
loc=pd.DataFrame(rows)
loc.to_csv(os.path.join(TAB,"P5_GSE216039_hub_localisation.csv"),index=False)

# rank: which cell type expresses each hub most (and specificity)
spec=[]
for g in hubp:
    s=loc[loc.symbol==g].sort_values("mean_lognorm",ascending=False)
    top=s.iloc[0]
    spec.append({"symbol":g,"top_celltype":top.celltype,"top_mean":top.mean_lognorm,
                 "top_pct":top.pct_expressing,"n_celltypes":len(s),
                 "ratio_top2nd":float(top.mean_lognorm/(s.iloc[1].mean_lognorm+1e-9)) if len(s)>1 else np.nan})
sp_df=pd.DataFrame(spec).sort_values("top_mean",ascending=False)
sp_df.to_csv(os.path.join(TAB,"P5_GSE216039_hub_celltype_top.csv"),index=False)
print("\n=== hub top cell type ===")
print(sp_df.head(30).to_string(index=False))

# ---- sample-level pseudobulk (CCI vs Sham) per cell type ----
pbcols=[sym2var[g] for g in hubp]
def pseudobulk(A,ct):
    cells=A.obs_names[A.obs.celltype==ct]
    sub=Anno[cells][:,pbcols]
    df=pd.DataFrame(sub.X.toarray(),columns=[g for g in hubp])
    df["sample"]=A.obs.loc[cells,"sample"].values
    return df.groupby("sample").mean()
pb_rows=[]
for ct in sorted(A.obs.celltype.unique()):
    cells=A.obs_names[A.obs.celltype==ct]
    if len(cells)<20: continue
    g=pseudobulk(A,ct)
    if g.shape[0]<3: continue
    g["celltype"]=ct
    pb_rows.append(g.reset_index())
if pb_rows:
    pb=pd.concat(pb_rows,ignore_index=True)
    pb.to_csv(os.path.join(TAB,"P5_GSE216039_pseudobulk_celltype.csv"),index=False)
    print("\npseudobulk celltype x sample:",pb.shape,"(note: n=2/group -> underpowered)")
print("\n=== P5 GSE216039 done ===")
