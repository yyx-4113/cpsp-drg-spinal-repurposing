#!/usr/bin/env python3
"""Download SPARC Dataset 476 (human C2-DRG Visium) per-sample filtered_feature_bc_matrix.h5
+ phenotype xlsx, with SSL verification disabled (CERT_NONE via curl -k) and integrity checks.
"""
import json, os, subprocess, base64, hashlib, sys

ROOT = "D:/2026.9/极速交付9月会员日优惠套路/01_AI生信-虚拟多重筛药/慢性疼痛"
MANIFEST = os.path.join(ROOT, "data/raw/SPARC476/manifest.json")
BASE = "https://sparc-prod-aod-discover-publish50-use1.s3.amazonaws.com/476/"
H5_DIR = os.path.join(ROOT, "data/raw/SPARC476/h5")
META_DIR = os.path.join(ROOT, "data/raw/SPARC476/meta")
os.makedirs(H5_DIR, exist_ok=True)
os.makedirs(META_DIR, exist_ok=True)

m = json.load(open(MANIFEST))
files = m["files"]

def is_target(f):
    p = f.get("path", "")
    if not p.startswith("files/"):
        return False
    # per-sample filtered (non-spatial) feature matrix
    if p.endswith("filtered_feature_bc_matrix.h5") and "/spatial/" not in p:
        return True
    base = os.path.basename(p)
    if base in ("subjects.xlsx", "samples.xlsx"):
        return True
    return False

targets = [f for f in files if is_target(f)]
print(f"selected {len(targets)} targets", file=sys.stderr)

def sha256_of(path):
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.digest()

ok, fail = [], []
for f in targets:
    p = f["path"]
    size = f.get("size")
    want_b64 = f.get("sha256")
    url = BASE + p
    # local path
    if p.endswith(".h5"):
        # sample id from path: files/primary/sub-XXX/sam-XXX-DRGL/filtered_feature_bc_matrix.h5
        parts = p.split("/")
        sam = [x for x in parts if x.startswith("sam-")][0]
        side = "DRGL" if "DRGL" in p else ("DRGR" if "DRGR" in p else "DRG")
        local = os.path.join(H5_DIR, f"{sam}__{side}.h5")
    else:
        local = os.path.join(META_DIR, os.path.basename(p))
    # skip if already present & verified
    if os.path.exists(local) and size and os.path.getsize(local) == size:
        if want_b64:
            try:
                if sha256_of(local) == base64.b64decode(want_b64):
                    print(f"SKIP (verified) {os.path.basename(local)}", file=sys.stderr)
                    ok.append(local); continue
            except Exception:
                pass
    # short per-attempt max-time so stalls are caught fast and resumed; many retries
    cmd = ["curl", "-k", "-s", "-L", "-C", "-", "--retry", "10", "--retry-delay", "2",
           "--connect-timeout", "20", "--max-time", "120", "-o", local, url]
    for attempt in range(6):
        r = subprocess.run(cmd, capture_output=True, text=True)
        if r.returncode == 0 and os.path.exists(local):
            sz = os.path.getsize(local)
            if size and sz != size:
                print(f"  WARN size mismatch {os.path.basename(local)} got {sz} want {size}", file=sys.stderr)
                continue
            if want_b64:
                try:
                    if sha256_of(local) != base64.b64decode(want_b64):
                        print(f"  WARN sha256 mismatch {os.path.basename(local)}", file=sys.stderr)
                        continue
                except Exception as e:
                    print(f"  sha256 check skipped {os.path.basename(local)}: {e}", file=sys.stderr)
            print(f"OK {os.path.basename(local)} ({sz} bytes)", file=sys.stderr)
            ok.append(local)
            break
        else:
            print(f"  attempt {attempt+1} failed rc={r.returncode} {os.path.basename(local)}: {r.stderr[:200]}", file=sys.stderr)
    else:
        fail.append((local, url))

print(f"\nDONE ok={len(ok)} fail={len(fail)}", file=sys.stderr)
if fail:
    print("FAILED:", file=sys.stderr)
    for local, url in fail:
        print(f"  {local}  <-  {url}", file=sys.stderr)
    sys.exit(1)
