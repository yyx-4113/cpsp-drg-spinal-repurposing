#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
p6_fetch_assets.py -- P6 资源下载：AutoDock Vina 二进制 + 药物重定位库

为什么需要：
  ① 本机 Python 3.13 无 vina 的 Windows 轮子（PyPI 上 vina 1.2.7 只有 Linux/macOS wheel），
     必须下载官方 Windows 可执行文件当作 CLI 引擎；
  ② 老药新用需要一个**已批准药物**配体库。DrugBank 需授权，改用
     **Broad Institute Drug Repurposing Hub**（CC0，含 canonical SMILES，覆盖 FDA 已批准 + 临床期药物），
     这是文献中广泛使用的开放替代品。脚本会同时记下来源 URL 与下载时间以便审稿追溯。

用法: python p6_fetch_assets.py
"""
import os, sys, hashlib, json, time, urllib.request

ROOT = "D:/2026.9/极速交付9月会员日优惠套路/01_AI生信-虚拟多重筛药/慢性疼痛"
TOOLS = os.path.join(ROOT, "tools")
DRUGLIB = os.path.join(ROOT, "data/raw/druglib")
os.makedirs(TOOLS, exist_ok=True)
os.makedirs(DRUGLIB, exist_ok=True)

ASSETS = [
    ("vina.exe",
     "https://github.com/ccsb-scripps/AutoDock-Vina/releases/download/v1.2.5/vina_1.2.5_win.exe",
     TOOLS),
    ("repurposing_drugs.txt",
     "https://s3.amazonaws.com/data.clue.io/repurposing/downloads/repurposing_drugs_20200324.txt",
     DRUGLIB),
    ("repurposing_targets.txt",
     "https://s3.amazonaws.com/data.clue.io/repurposing/downloads/repurposing_targets_20200324.txt",
     DRUGLIB),
]


def fetch(url, dest, retries=3):
    for i in range(retries):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 research"})
            with urllib.request.urlopen(req, timeout=600) as r, open(dest, "wb") as f:
                n = 0
                while True:
                    chunk = r.read(1 << 20)
                    if not chunk:
                        break
                    f.write(chunk)
                    n += len(chunk)
            return n
        except Exception as e:
            print(f"  retry {i+1}/{retries} {type(e).__name__}: {str(e)[:100]}", flush=True)
            time.sleep(3)
    return None


manifest = {}
for name, url, d in ASSETS:
    dest = os.path.join(d, name)
    if os.path.exists(dest) and os.path.getsize(dest) > 10000:
        print(f"[skip] {name} already present ({os.path.getsize(dest)} B)", flush=True)
    else:
        print(f"[get ] {name}", flush=True)
        n = fetch(url, dest)
        if n is None:
            print(f"  FAILED {name}", flush=True)
            continue
        print(f"  ok {n} bytes -> {dest}", flush=True)
    if os.path.exists(dest):
        h = hashlib.sha256(open(dest, "rb").read()).hexdigest()[:16]
        manifest[name] = {"url": url, "bytes": os.path.getsize(dest), "sha256_16": h}

# 验证 vina.exe 是可执行的 PE 文件，且能打印版本
vina = os.path.join(TOOLS, "vina.exe")
if os.path.exists(vina):
    with open(vina, "rb") as f:
        magic = f.read(2)
    print(f"\nvina.exe magic = {magic!r} (expect b'MZ')", flush=True)
    import subprocess
    try:
        p = subprocess.run([vina, "--version"], capture_output=True, text=True, timeout=60)
        print("vina --version:", (p.stdout or p.stderr).strip()[:200], flush=True)
        manifest["vina_version_output"] = (p.stdout or p.stderr).strip()[:200]
    except Exception as e:
        print("vina exec FAILED:", e, flush=True)

with open(os.path.join(DRUGLIB, "MANIFEST.json"), "w", encoding="utf-8") as f:
    json.dump({"retrieved_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
               "assets": manifest}, f, ensure_ascii=False, indent=1)
print("\nmanifest ->", os.path.join(DRUGLIB, "MANIFEST.json"))
print("assets:", list(manifest.keys()))
