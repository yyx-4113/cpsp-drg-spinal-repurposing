import urllib.request, json, time
def get(u):
    return urllib.request.urlopen(urllib.request.Request(u,headers={"User-Agent":"Mozilla/5.0 research"}),timeout=60).read().decode("utf-8","replace")
j=json.loads(get("https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=gds&term=GSE325938[Accession]&retmode=json"))
uid=j["esearchresult"]["idlist"]
if not uid: print("GSE325938 not found"); raise SystemExit
s=json.loads(get(f"https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi?db=gds&id={uid[0]}&retmode=json"))
r=s["result"][uid[0]]
for k in ["accession","title","taxon","gdstype","n_samples","summary"]:
    v=r.get(k)
    print(f"{k}: {str(v)[:900] if k=='summary' else v}")
