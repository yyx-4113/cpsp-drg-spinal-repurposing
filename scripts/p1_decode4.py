#!/usr/bin/env python3
# p1_decode4.py -- locate GPL32253 annot dir + resolve one GSM token via esearch->efetch
import urllib.request, re, os, sys, json
META="D:/2026.9/极速交付9月会员日优惠套路/01_AI生信-虚拟多重筛药/慢性疼痛/data/raw/geo_meta"
def get(u):
    req=urllib.request.Request(u,headers={"User-Agent":"research/1.0"})
    with urllib.request.urlopen(req,timeout=60) as r: return r.read().decode("utf-8","replace")

# 1) find correct platform bucket
found=None
for bucket in ["GPL3nnn","GPL32nnn","GPL322nn","GPL3225nn"]:
    url=f"https://ftp.ncbi.nlm.nih.gov/geo/platforms/{bucket}/"
    try:
        html=get(url)
        if "GPL32253" in html:
            print(f"[bucket FOUND] {bucket}"); found=bucket
            # list files for GPL32253
            sub=f"https://ftp.ncbi.nlm.nih.gov/geo/platforms/{bucket}/GPL32253/"
            try:
                h2=get(sub)
                files=re.findall(r'href="([^"]+)"',h2)
                files=[f for f in files if not f.endswith("/")]
                print("[GPL32253 dir files]:", files[:20])
            except Exception as e: print("[subdir err]",e)
            break
        else:
            print(f"[bucket empty] {bucket}")
    except Exception as e:
        print(f"[bucket 404] {bucket}: {e}")

# 2) GSM8278924 -> UID -> efetch, find token
es=json.loads(get(f"https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=gds&term=GSM8278924%5Baccn%5D"))
uid=es.get("esearchresult",{}).get("idlist",[None])[0]
print("\n[GSM8278924 uid]",uid)
if uid:
    txt=get(f"https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=gds&id={uid}&rettype=xml")
    print("[efetch head 1200]\n",txt[:1200])
    toks=set(re.findall(r'[A-Za-z]+_\d+_\d+_[A-Za-z]+',txt))
    print("\ntoken-like:",toks)
