import urllib.request, gzip, io, os, re
ROOT="D:/2026.9/极速交付9月会员日优惠套路/01_AI生信-虚拟多重筛药/慢性疼痛"
OUT=os.path.join(ROOT,"data/raw/geo_meta"); os.makedirs(OUT,exist_ok=True)
def bucket(g): n=g[3:]; return "GSE"+n[:3]+"nnn"
for gse in ["GSE216039","GSE328175","GSE246288"]:
    url=f"https://ftp.ncbi.nlm.nih.gov/geo/series/{bucket(gse)}/{gse}/matrix/{gse}_series_matrix.txt.gz"
    try:
        req=urllib.request.Request(url,headers={"User-Agent":"Mozilla/5.0 research"})
        raw=urllib.request.urlopen(req,timeout=120).read()
        p=os.path.join(OUT,f"{gse}_series_matrix.txt.gz")
        open(p,"wb").write(raw)
        txt=gzip.decompress(raw).decode("utf-8","replace")
        lines=txt.splitlines()
        print("="*78); print(gse, len(raw),"bytes")
        for key in ["!Series_title","!Series_summary","!Series_overall_design","!Series_platform_id"]:
            for L in lines:
                if L.startswith(key+"\t"):
                    print(L[:400]); break
        for key in ["!Sample_title","!Sample_source_name_ch1","!Sample_characteristics_ch1","!Sample_organism_ch1"]:
            for L in lines:
                if L.startswith(key):
                    vals=[v.strip('"') for v in L.split("\t")[1:]]
                    print(f"{key}: {vals}")
                    break
    except Exception as e:
        print(gse,"ERR",e)
