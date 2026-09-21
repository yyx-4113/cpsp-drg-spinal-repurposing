#!/bin/bash
# Parallel resilient download for SPARC 476 (throttled anonymous S3).
# Short per-attempt max-time + resume (-C -) + many retries; 3 concurrent.
set -u
ROOT="D:/2026.9/极速交付9月会员日优惠套路/01_AI生信-虚拟多重筛药/慢性疼痛"
cd "$ROOT"
BASE="https://sparc-prod-aod-discover-publish50-use1.s3.amazonaws.com/476/"
PY="C:/Users/Administrator/.workbuddy/binaries/python/envs/default/Scripts/python.exe"
URLS="data/raw/SPARC476/_urls.txt"
mkdir -p data/raw/SPARC476/h5 data/raw/SPARC476/meta

"$PY" - "$BASE" <<'PY' > "$URLS"
import json,sys,os
base=sys.argv[1]
m=json.load(open("data/raw/SPARC476/manifest.json"))
for f in m["files"]:
    p=f.get("path","")
    if not p.startswith("files/"): continue
    if p.endswith("filtered_feature_bc_matrix.h5") and "/spatial/" not in p:
        sam=[x for x in p.split("/") if x.startswith("sam-")][0]
        side="DRGL" if "DRGL" in p else ("DRGR" if "DRGR" in p else "DRG")
        print(base+p, f"data/raw/SPARC476/h5/{sam}__{side}.h5")
    if os.path.basename(p) in ("subjects.xlsx","samples.xlsx"):
        print(base+p, f"data/raw/SPARC476/meta/{os.path.basename(p)}")
PY

echo "== url list ($(wc -l < "$URLS") targets) =="
cat "$URLS"

# pass 1: parallel download with resume
echo "== parallel pass =="
cat "$URLS" | xargs -P 3 -n 2 bash -c 'curl -k -s -L -C - --retry 40 --retry-delay 2 --connect-timeout 20 --max-time 120 -o "$2" "$1" && echo "OK $(basename $2)" || echo "FAIL $(basename $2)"' sh

echo "== verifying =="
"$PY" - <<'PY'
import json,os,base64,hashlib
m=json.load(open("data/raw/SPARC476/manifest.json"))
files=m["files"]
def need():
    out=[]
    for f in files:
        p=f.get("path","")
        if p.endswith("filtered_feature_bc_matrix.h5") and "/spatial/" not in p:
            sam=[x for x in p.split("/") if x.startswith("sam-")][0]
            side="DRGL" if "DRGL" in p else ("DRGR" if "DRGR" in p else "DRG")
            out.append(("data/raw/SPARC476/h5/%s__%s.h5"%(sam,side), f.get("size"), f.get("sha256")))
        if os.path.basename(p) in ("subjects.xlsx","samples.xlsx"):
            out.append(("data/raw/SPARC476/meta/"+os.path.basename(p), f.get("size"), f.get("sha256")))
    return out
ok=0;bad=0
for path,size,sha in need():
    if not os.path.exists(path):
        print("MISSING", path); bad+=1; continue
    sz=os.path.getsize(path)
    if size and sz!=size:
        print("SIZE_MISMATCH want=%s got=%s %s"%(size,sz,path)); bad+=1; continue
    if sha:
        h=hashlib.sha256()
        with open(path,"rb") as fh:
            for c in iter(lambda: fh.read(1<<20), b""): h.update(c)
        if h.digest()!=base64.b64decode(sha):
            print("SHA_MISMATCH", path); bad+=1; continue
    ok+=1
print("VERIFY ok=%d bad=%d"%(ok,bad))
PY
