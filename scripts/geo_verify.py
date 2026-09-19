#!/usr/bin/env python3
# geo_verify.py -- verify GEO series existence/type via E-utilities, list suppl/ for bulk sets.
import urllib.request, urllib.parse, xml.etree.ElementTree as ET, time, json, re, sys, os

ESEARCH = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"
EFETCH  = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi"
FTP     = "https://ftp.ncbi.nlm.nih.gov/geo/series"

GSES = [
    # (gse, role)
    ("GSE267799","核心-大鼠DRG/脊髓/皮肤 SMIR"),
    ("GSE212311","外部验证-大鼠CCI DRG"),
    ("GSE265957","脊髓层-小鼠翻译组 96"),
    ("GSE278227","性别分层-大鼠DRG消退"),
    ("GSE241361","机制锚点-小鼠Sigma-1"),
    ("GSE158825","人源-血浆miRNA 1年疼痛"),
    ("GSE222979","人源-1242例关节置换内型"),
    ("GSE306403","人源-阿片副作用基因"),
    ("GSE328175","单细胞-脊髓NP 8"),
    ("GSE325938","空间-Visium"),
    ("GSE246288","单细胞-脊髓小胶质"),
    ("GSE216039","单细胞-DRG紫杉醇神经元"),
]

BULK = {"GSE267799","GSE212311","GSE265957","GSE278227","GSE241361",
        "GSE158825","GSE222979","GSE306403"}

def get(url):
    req = urllib.request.Request(url, headers={"User-Agent":"research-agent/1.0"})
    with urllib.request.urlopen(req, timeout=40) as r:
        return r.read().decode("utf-8","replace")

def local(tag):
    return tag.split('}')[-1]

def esearch(gse):
    url = f"{ESEARCH}?db=gds&term={urllib.parse.quote(gse)}%5Baccn%5D"
    try:
        txt = get(url)
        root = ET.fromstring(txt)
        ids = [i.text for i in root.findall(".//IdList/Id")]
        return ids
    except Exception as e:
        return [f"ERR:{e}"]

def efetch(uid):
    return get(f"{EFETCH}?db=gds&id={uid}&rettype=xml")

def parse_series(txt):
    # efetch?rettype=xml for a Series returns plain-text summary, not XML.
    d = {}
    lines = txt.splitlines()
    for l in lines:
        if l.startswith("1. "):
            d["Title"] = l[3:].strip()
        if l.startswith("Organism:"):
            d["Organism"] = l.split(":",1)[1].strip()
        if l.startswith("Type:"):
            d["Type"] = l.split(":",1)[1].strip()
        if l.startswith("Platform:"):
            rest = l.split(":",1)[1].strip()
            m = re.search(r"(GPL\d+)\s+(\d+)\s+Samples", rest)
            if m:
                d["Platform"] = m.group(1); d["Number-Of-Samples"] = m.group(2)
            else:
                d["PlatformRaw"] = rest
        if "(Submitter supplied)" in l:
            s = l.split(")",1)[1].strip() if ")" in l else l.strip()
            d["Summary"] = s
    # GSE-level PubMed via esummary would be extra; skip for now
    return d

def bucket(gse):
    digits = gse[3:]              # 267799
    return "GSE" + digits[:-3] + "nnn"

def list_suppl(gse):
    url = f"{FTP}/{bucket(gse)}/{gse}/suppl/"
    try:
        html = get(url)
        files = re.findall(r'href="([^"]+)"', html)
        files = [f for f in files if not f.endswith("/") and f not in ("?",)]
        return files
    except Exception as e:
        return [f"ERR:{e}"]

def main():
    results = []
    for gse, role in GSES:
        rec = {"gse": gse, "role": role}
        ids = esearch(gse)
        time.sleep(0.4)
        if not ids or str(ids[0]).startswith("ERR"):
            rec["exists"] = False
            rec["error"] = ids[0] if ids else "no id"
            results.append(rec)
            continue
        rec["uid"] = ids[0]
        rec["exists"] = True
        try:
            xml = efetch(ids[0])
            d = parse_series(xml)
            rec.update(d)
        except Exception as e:
            rec["parse_error"] = str(e)
        time.sleep(0.4)
        if gse in BULK:
            rec["suppl"] = list_suppl(gse)
            time.sleep(0.4)
        results.append(rec)
        # progress
        print(f"[OK] {gse} type={rec.get('Type','?')} nsamp={rec.get('Number-Of-Samples','?')} org={rec.get('Organism','?')}", file=sys.stderr)
    out = "D:/2026.9/极速交付9月会员日优惠套路/01_AI生信-虚拟多重筛药/慢性疼痛/data/raw/geo_meta/verify.json"
    with open(out,"w") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    # markdown table
    print("\n# GEO Verification\n")
    print("| GSE | role | exists | Type | #Samples | Organism | Platform | PubMed |")
    print("|---|---|---|---|---|---|---|---|")
    for r in results:
        if not r.get("exists"):
            print(f"| {r['gse']} | {r['role']} | NO ({r.get('error','')}) | - | - | - | - | - |")
            continue
        print(f"| {r['gse']} | {r['role']} | yes | {r.get('Type','?')} | {r.get('Number-Of-Samples','?')} | {r.get('Organism','?')} | {r.get('Platform','?')} | {r.get('PubMed','-')} |")
    print("\n## suppl/ listings (bulk sets)\n")
    for r in results:
        if "suppl" in r:
            print(f"### {r['gse']}")
            if r["suppl"] and not str(r["suppl"][0]).startswith("ERR"):
                for f in r["suppl"]:
                    print(f"- {f}")
            else:
                print(f"- {r['suppl']}")
    print(f"\nSaved -> {out}")

if __name__ == "__main__":
    main()
