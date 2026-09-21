#!/usr/bin/env python3
"""Download Pennsieve Dataset 480 (human DRG snRNA-seq atlas, CC-BY-4.0) filtered_feature_bc_matrix.h5
+ phenotype xlsx, with sha256 verification. Reuses SPARC S3 open bucket pattern.
Naming uses the DEEPEST sam-UTD-* folder (unique per sample) to avoid L/R or T6L/T8L collisions.
Parallel curl via ThreadPoolExecutor (6 workers) to beat S3 anonymous throttling.
"""
import json, os, subprocess, hashlib, base64, sys
from concurrent.futures import ThreadPoolExecutor

ROOT = "D:/2026.9/极速交付9月会员日优惠套路/01_AI生信-虚拟多重筛药/慢性疼痛"
MANIFEST = os.path.join(ROOT, "data/raw/Pennsieve480/manifest.json")
BASE = "https://sparc-prod-aod-discover-publish50-use1.s3.amazonaws.com/480/"
H5_DIR = os.path.join(ROOT, "data/raw/Pennsieve480/h5")
META_DIR = os.path.join(ROOT, "data/raw/Pennsieve480/meta")
os.makedirs(H5_DIR, exist_ok=True)
os.makedirs(META_DIR, exist_ok=True)

m = json.load(open(MANIFEST))
files = m["files"]

def deepest_sam(p):
    # return the deepest folder starting with sam-UTD- (unique sample id)
    parts = p.split("/")
    cand = [x for x in parts if x.startswith("sam-UTD-")]
    return cand[-1] if cand else os.path.basename(p).replace("sample_", "").replace("_feature_bc_matrix.h5", "")

def sub_of(p):
    for x in p.split("/"):
        if x.startswith("sub-UTD-"):
            return x
    return None

def is_target(f):
    p = f.get("path", "")
    if not p.startswith("files/"):
        return False
    if p.endswith("sample_filtered_feature_bc_matrix.h5"):
        return True
    if os.path.basename(p).endswith(".xlsx"):
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

# build job list with correct local names + donor map
jobs = []
donor_map = {}   # local_h5_name -> sub-UTD-XXX
for f in targets:
    p = f["path"]
    if p.endswith(".h5"):
        stem = deepest_sam(p)
        local = os.path.join(H5_DIR, stem + ".h5")
        donor_map[stem + ".h5"] = sub_of(p)
    else:
        local = os.path.join(META_DIR, os.path.basename(p))
    jobs.append((p, local, f.get("size"), f.get("sha256")))

# clear stale mis-named h5 (parent-only stem without -DRG* suffix) from prior run
for fn in os.listdir(H5_DIR):
    if fn.endswith(".h5") and fn not in {os.path.basename(j[1]) for j in jobs}:
        try:
            os.remove(os.path.join(H5_DIR, fn))
            print(f"removed stale {fn}", file=sys.stderr)
        except Exception as e:
            print(f"warn cannot remove {fn}: {e}", file=sys.stderr)

# write donor map for analysis
with open(os.path.join(ROOT, "data/raw/Pennsieve480/donor_map.json"), "w") as fh:
    json.dump(donor_map, fh, indent=2)

def verify(local, size, b64):
    if not (size and os.path.exists(local) and os.path.getsize(local) == size):
        return False
    if not b64:
        return True
    try:
        return sha256_of(local) == base64.b64decode(b64)
    except Exception:
        return False

def dl(job):
    p, local, size, b64 = job
    url = BASE + p
    if verify(local, size, b64):
        return ("SKIP", os.path.basename(local))
    for attempt in range(12):
        r = subprocess.run(["curl", "-k", "-s", "-L", "-C", "-", "--retry", "6", "--retry-delay", "2",
                            "--connect-timeout", "20", "--max-time", "180", "-o", local, url],
                           capture_output=True, text=True)
        if r.returncode == 0 and os.path.exists(local):
            if verify(local, size, b64):
                return ("OK", os.path.basename(local))
            # size mismatch -> truncate and retry
            try:
                if os.path.getsize(local) != size:
                    os.truncate(local, 0)
            except Exception:
                pass
    return ("FAIL", os.path.basename(local) + "  <-  " + url)

ok = 0; skip = 0; fail = []
with ThreadPoolExecutor(max_workers=6) as ex:
    for status, name in ex.map(dl, jobs):
        if status == "SKIP":
            skip += 1; print(f"SKIP(verified) {name}", file=sys.stderr)
        elif status == "OK":
            ok += 1; print(f"OK {name}", file=sys.stderr)
        else:
            fail.append(name); print(f"FAIL {name}", file=sys.stderr)

print(f"\nDONE ok={ok} skip={skip} fail={len(fail)}", file=sys.stderr)
if fail:
    sys.exit(1)
