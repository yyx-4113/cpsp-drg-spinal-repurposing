import re, urllib.request, json, sys, ssl

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

md = open("reports/MVP_PLOSONE_submission.md", encoding="utf-8").read()
dois = re.findall(r"10\.\d{4,9}/[^\s)\]]+", md)
# de-dup preserve order
seen, uniq = set(), []
for d in dois:
    if d not in seen:
        seen.add(d); uniq.append(d)
print(f"Found {len(uniq)} unique DOI(s) in manuscript")

ok, bad = 0, []
for d in uniq:
    try:
        url = "https://api.crossref.org/works/" + d
        req = urllib.request.Request(url, headers={"User-Agent": "mailto:960856791@qq.com"})
        with urllib.request.urlopen(req, timeout=30, context=ctx) as r:
            data = json.load(r)
        msg = data.get("message", {})
        title = (msg.get("title") or ["<no title>"])[0]
        ok += 1
        print(f"[PASS] {d}  -> {title[:70]}")
    except Exception as e:
        bad.append(d)
        print(f"[FAIL] {d}  -> {e}")

print(f"\n==== DOI verification: {ok} PASS / {len(bad)} FAIL (of {len(uniq)}) ====")
for b in bad:
    print("  FAIL:", b)
sys.exit(1 if bad else 0)
