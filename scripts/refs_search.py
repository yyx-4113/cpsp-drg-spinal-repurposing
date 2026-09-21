#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
P6 FJNSF 申请书参考文献检索：PubMed E-utilities (esearch + esummary)
输出真实 DOI/PMID，限定 2023:2026，按相关性取前 N。
用法：python refs_search.py [--proxy http://127.0.0.1:49501]
"""
import json
import os
import ssl
import sys
import time
import urllib.parse
import urllib.request

EUTILS = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/"
UA = "Mozilla/5.0 (compatible; refsearch/1.0; mailto:960856791@qq.com)"
OUT_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "results", "tables")
RETMAX = 8

# 主题 -> PubMed 检索式（英文，无 dp 后缀，脚本统一加 2023:2026[dp]）
QUERIES = {
    "A_CPSP_epi": '(("chronic postsurgical pain"[tiab] OR "chronic post-surgical pain"[tiab] OR "persistent postsurgical pain"[tiab] OR "persistent post-surgical pain"[tiab]) AND (epidemiolog*[tiab] OR incidence[tiab] OR risk factor*[tiab] OR mechanism*[tiab]))',
    "A_CPSP_mech": '("chronic postsurgical pain"[tiab] OR "persistent postsurgical pain"[tiab]) AND (neuroinflammation[tiab] OR "central sensitization"[tiab] OR "neuropathic"[tiab] OR prevention[tiab])',
    "B_DRG_transcript": '("dorsal root ganglion"[tiab] AND (transcriptom*[tiab] OR "single-cell RNA"[tiab] OR "single-cell transcriptom*"[tiab] OR "snRNA"[tiab]) AND (neuropathic pain[tiab] OR pain[tiab]))',
    "B_SpinalCord_sc": '("spinal cord"[tiab] AND ("single-cell"[tiab] OR "single cell"[tiab] OR "single-nucleus"[tiab]) AND (pain[tiab] OR nociception[tiab] OR "neuropathic"[tiab]))',
    "B_DRG_atlas": '("dorsal root ganglion"[tiab] AND (atlas[tiab] OR "cell type*"[tiab] OR "human"[tiab]) AND (pain[tiab] OR somatosensory[tiab]))',
    "C_meta_omics": '(("meta-analysis"[tiab] OR "integrative analysis"[tiab] OR "cross-species"[tiab] OR "multi-omics"[tiab]) AND (transcriptom*[tiab]) AND (pain[tiab] OR neuropathic[tiab]))',
    "C_ML_hub": '(("machine learning"[tiab] OR "random forest"[tiab] OR "LASSO"[tiab] OR "bioinformatics"[tiab]) AND ("hub gene*"[tiab] OR "biomarker*"[tiab] OR "key gene*"[tiab]) AND (neuropathic pain[tiab] OR "chronic pain"[tiab]))',
    "D_alpha2": '(("alpha2 adrenergic"[tiab] OR "alpha-2 adrenergic"[tiab] OR "α2 adrenergic"[tiab] OR "alpha2-adrenoceptor"[tiab] OR "α2A"[tiab]) AND (analgesi*[tiab] OR "pain"[tiab] OR antinocicept*[tiab]))',
    "D_dexmed": '((dexmedetomidine[tiab] OR clonidine[tiab]) AND ("intrathecal"[tiab] OR "spinal"[tiab] OR "perineural"[tiab]) AND (pain[tiab] OR analgesi*[tiab]))',
    "D_ADRA2A": '("ADRA2A"[tiab] OR "alpha-2A adrenergic receptor"[tiab] OR "alpha2A-adrenoceptor"[tiab]) AND (pain[tiab] OR analgesi*[tiab] OR "dorsal root ganglion"[tiab])',
    "E_repurposing": '(("drug repurposing"[tiab] OR "drug repositioning"[tiab]) AND ("machine learning"[tiab] OR "virtual screening"[tiab] OR "molecular docking"[tiab] OR "transcriptom*"[tiab]))',
    "F_pseudo": '(("pseudoreplication"[tiab] OR "pseudo-replication"[tiab] OR "double dipping"[tiab] OR "double-dipping"[tiab]) AND ("single-cell"[tiab] OR "single cell"[tiab] OR scRNA[tiab]))',
}


def build_opener(proxy):
    handlers = []
    if proxy:
        handlers.append(urllib.request.ProxyHandler({"http": proxy, "https": proxy}))
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE
    handlers.append(urllib.request.HTTPSHandler(context=ctx))
    return urllib.request.build_opener(*handlers)


def fetch(opener, url, retries=3):
    last = None
    for i in range(retries):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": UA})
            with opener.open(req, timeout=60) as r:
                return r.read().decode("utf-8", "replace")
        except Exception as e:  # noqa
            last = e
            time.sleep(1.0 + i)
    raise RuntimeError(f"fetch failed: {last}")


def parse_summary(summ_json):
    res = []
    result = summ_json.get("result", {})
    for uid in result.get("uids", []):
        rec = result.get(uid, {})
        if not rec:
            continue
        doi = ""
        for aid in rec.get("articleids", []):
            if aid.get("idtype") == "doi":
                doi = aid.get("value", "")
                break
        authors = [a.get("name", "") for a in rec.get("authors", [])][:3]
        res.append({
            "pmid": uid,
            "title": rec.get("title", "").strip(),
            "journal": rec.get("source", ""),
            "year": (rec.get("pubdate", "") or "")[:4],
            "authors": authors,
            "doi": doi,
        })
    return res


def main():
    proxy = None
    if "--proxy" in sys.argv:
        proxy = sys.argv[sys.argv.index("--proxy") + 1]
    opener = build_opener(proxy)
    os.makedirs(OUT_DIR, exist_ok=True)
    all_out = {}
    for name, term in QUERIES.items():
        q = f"({term}) AND 2023:2026[dp]"
        try:
            u = (EUTILS + "esearch.fcgi?db=pubmed&retmode=json&sort=relevance&retmax="
                 + str(RETMAX) + "&term=" + urllib.parse.quote(q))
            ids = json.loads(fetch(opener, u))["esearchresult"]["idlist"]
            time.sleep(0.5)
            if not ids:
                all_out[name] = []
                print(f"[{name}] 0 hits")
                continue
            u2 = EUTILS + "esummary.fcgi?db=pubmed&retmode=json&id=" + ",".join(ids)
            summ = json.loads(fetch(opener, u2))
            recs = parse_summary(summ)
            all_out[name] = recs
            print(f"[{name}] {len(recs)} hits")
            for r in recs:
                print(f"   {r['year']} | {r['journal']} | PMID {r['pmid']} | {r['title'][:90]}")
            time.sleep(0.5)
        except Exception as e:  # noqa
            all_out[name] = {"error": str(e)}
            print(f"[{name}] ERROR: {e}")
    path = os.path.join(OUT_DIR, "P6_refs_candidates.json")
    with open(path, "w", encoding="utf-8") as f:
        json.dump(all_out, f, ensure_ascii=False, indent=2)
    print("\nSaved ->", path)


if __name__ == "__main__":
    main()
