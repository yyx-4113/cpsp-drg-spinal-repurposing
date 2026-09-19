import urllib.request, json, os, time
OUT="data/raw/geo_meta"
os.makedirs(OUT,exist_ok=True)
def get(url):
    req=urllib.request.Request(url,headers={"User-Agent":"Mozilla/5.0 research"})
    return urllib.request.urlopen(req,timeout=60).read().decode("utf-8","replace")
for gse in ["GSE216039","GSE328175","GSE246288"]:
    try:
        j=json.loads(get(f"https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=gds&term={gse}[Accession]&retmode=json"))
        uid=j["esearchresult"]["idlist"]
        if not uid: print(gse,"no uid"); continue
        s=json.loads(get(f"https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi?db=gds&id={uid[0]}&retmode=json"))
        r=s["result"][uid[0]]
        keep={k:r.get(k) for k in ["accession","title","summary","taxon","gdsType","n_samples","gdstype","sampleTaxon","PubMedIds"]}
        open(os.path.join(OUT,f"{gse}_esummary.json"),"w",encoding="utf-8").write(json.dumps(keep,ensure_ascii=False,indent=1))
        print("="*70); print(gse, "|", r.get("taxon"), "|", r.get("gdstype"), "| n=", r.get("n_samples"))
        print("TITLE:", r.get("title"))
        print("SUMMARY:", (r.get("summary") or "")[:1200])
    except Exception as e:
        print(gse,"ERR",e)
    time.sleep(0.5)
