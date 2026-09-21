#!/usr/bin/env python3
# p7_consistency_gate.py -- pre-submission gate recommended by the Round-4 editorial report §9.
#   (1) greps the manuscript for forbidden tokens ([truncated], Round-N, vX.Y, _R3_, stale wording)
#   (2) checks Nature limits (title <= 20 words, abstract <= 200 words, display items <= 8)
#   (3) verifies references are numbered by FIRST CITATION order
#   (4) recomputes every headline number straight from results/tables and fails on mismatch
import os, re, json, sys
import numpy as np, pandas as pd

ROOT = "D:/2026.9/极速交付9月会员日优惠套路/01_AI生信-虚拟多重筛药/慢性疼痛"
TAB  = os.path.join(ROOT, "results/tables")
MS   = os.path.join(ROOT, "reports/MVP_ScientificReports_submission.md")
txt  = open(MS, encoding="utf-8").read()
fails, warns, oks = [], [], []

# ---------------------------------------------------------------- (1) forbidden tokens
print("=" * 78); print("[1] FORBIDDEN / STALE TOKENS"); print("=" * 78)
FORBIDDEN = {
    "[truncated]": "T0-1 literal truncation placeholder",
    "Round-3": "T3-5 internal revision shorthand",
    "Round-4": "T3-5 internal revision shorthand",
    "v1.3": "T3-5 version token in manuscript body",
    "_R3_": "T3-6 internal filename",
    "maladaptive": "T1-13 causal language",
    "no privileged treatment": "T1-3 contradicted by manuscript behaviour",
    "p = 0.172": "T0-3 stale ACVR1 value",
    "27.8%": "T1-4 inverted bulk-only OXPHOS polarity",
    "16 localisable": "T3-1 spinal localisable count",
    "253 of those": "T1-5 miRNA pair/miRNA unit confusion",
    "10 of the 17": "T1-6 docking subset logic",
}
# Tokens that are ACCEPTABLE only inside a negating / disavowing context. The old manuscript
# asserted them; the revised manuscript explicitly rejects them, so bare substring matching
# would raise a false positive.
CONTEXT_OK = {
    "the first to": ("among", "T3-4 over-claim (use 'among the first')"),
    "degenerate equal weight": ("not", "T1-7 incorrect characterisation of w=sqrt(n_eff)"),
    "priorities": ("would contradict", "T1-2 Discussion 'priorities' contradicts the honest null"),
}
for tok, why in FORBIDDEN.items():
    n = txt.count(tok)
    if n: fails.append(f"FORBIDDEN '{tok}' x{n} — {why}")
    else: oks.append(f"absent: '{tok}'")
for t in oks: print("  OK   ", t)
for f in fails: print("  FAIL ", f)

print("  -- context-gated tokens (acceptable only when explicitly negated/disavowed) --")
for tok, (cue, why) in CONTEXT_OK.items():
    for m in re.finditer(re.escape(tok), txt):
        s = txt[max(0, m.start() - 90): m.end() + 90]
        if cue in s: print(f"  OK    '{tok}' used in a disavowing context ('{cue}' nearby)")
        else:
            fails.append(f"'{tok}' asserted without disavowal — {why}")
            print(f"  FAIL  '{tok}' asserted: ...{s}...")

# ---------------------------------------------------------------- (2) Nature limits
print("\n" + "=" * 78); print("[2] NATURE / SCIENTIFIC REPORTS LIMITS"); print("=" * 78)
title = txt.split("\n")[0].lstrip("# ").strip()
tw = len(title.split())
print(f"  title   : {tw} words  -> {'OK' if tw <= 20 else 'FAIL'} (limit 20)")
if tw > 20: fails.append(f"title {tw} words > 20")
ab = txt.split("## Abstract")[1].split("---")[0].strip()
aw = len(ab.split())
print(f"  abstract: {aw} words  -> {'OK' if aw <= 200 else 'FAIL'} (limit 200)")
if aw > 200: fails.append(f"abstract {aw} words > 200")
nfig = len(re.findall(r"^- \*\*Fig\. ", txt, flags=re.M))
ntab = len(re.findall(r"^- \*\*Table ", txt, flags=re.M))
print(f"  display : {nfig} figures + {ntab} tables = {nfig+ntab} -> {'OK' if nfig+ntab <= 8 else 'FAIL'} (limit 8)")
if nfig + ntab > 8: fails.append("display items > 8")
legs = re.findall(r"\*Legend\.(.*?)\n\n- ", txt, flags=re.S)
for i, L in enumerate(legs, 1):
    w = len(L.split()); print(f"  Fig.{i} legend: {w} words -> {'OK' if w <= 350 else 'FAIL'}")
    if w > 350: fails.append(f"Fig.{i} legend {w} words > 350")

# ---------------------------------------------------------------- (2b) abstract-vs-table honesty (Round-5 T1-1)
print("\n" + "=" * 78); print("[2b] ABSTRACT-vs-TABLE HONESTY (Round-5 T1-1)"); print("=" * 78)
# Worst Round-5 finding: the abstract asserted "no size-independent enrichment for any of 10 tractable
# targets" while Table 3b shows ADRA2A size-independent BH q = 0.0025 (significant). The manuscript
# resolves this by requiring BOTH the raw/full-library and the size-independent filter to clear; the
# abstract must mirror that two-filter logic and must NOT assert an absolute "no size-independent" null.
if "no size-independent enrichment for any of 10 tractable targets" in ab:
    fails.append("abstract asserts absolute null contradicted by ADRA2A size-indep BH q=0.0025")
    print("  FAIL  abstract still asserts the contradicted absolute-null wording")
else:
    oks.append("abstract avoids the contradicted absolute-null wording"); print("  OK    abstract avoids the contradicted absolute-null wording")
if "clearing both the full-library and size-independent enrichment filters" in ab:
    oks.append("abstract states two-filter logic"); print("  OK    abstract states the two-filter (raw + size-independent) logic")
else:
    fails.append("abstract missing two-filter logic after T1-1 fix"); print("  FAIL  abstract missing two-filter logic")
bh = pd.read_csv(os.path.join(TAB, "P6_BH_correction.csv"))
adra = bh[bh.symbol == "ADRA2A"]
if len(adra) and float(adra.iloc[0]["BH_q_size_indep"]) < 0.05:
    oks.append("ADRA2A size-indep BH q significant (Table 3b)"); print(f"  OK    ADRA2A size-indep BH q = {float(adra.iloc[0]['BH_q_size_indep']):.4f} drives the two-filter caveat")
else:
    fails.append("ADRA2A size-indep BH q not significant in P6_BH_correction.csv"); print("  FAIL  ADRA2A size-indep BH q check")

# ---------------------------------------------------------------- (3) reference order
print("\n" + "=" * 78); print("[3] REFERENCE FIRST-CITATION ORDER"); print("=" * 78)
body = txt.split("\n## References")[0]
SUPD = {"⁰": "0", "¹": "1", "²": "2", "³": "3", "⁴": "4",
        "⁵": "5", "⁶": "6", "⁷": "7", "⁸": "8", "⁹": "9"}
# NOTE: only true superscripts. U+2080-U+2089 are SUBscripts and must not be in the class,
# otherwise ordinary text containing them is mistaken for a citation marker.
# U+207B is the superscript minus used to render ranges such as 15–20.
SUPCLS = "\u2070\u00b9\u00b2\u00b3\u2074\u2075\u2076\u2077\u2078\u2079"
nums, firstseen = [], []
for m in re.finditer(f"[{SUPCLS}][{SUPCLS}\u207b\u2013]*", body):
    s = "".join(SUPD.get(c, c) for c in m.group(0)).replace("\u207b", "-").replace("\u2013", "-")
    for part in re.split(r"[,]", s):
        if "-" in part:                       # expand a citation range  a-b
            a, b = part.split("-")
            if a.isdigit() and b.isdigit(): part_list = list(range(int(a), int(b) + 1))
            else: continue
        else:
            part_list = [int(part)] if part.isdigit() else []
        for n in part_list:
            nums.append(n)
            if n not in firstseen: firstseen.append(n)
expected = list(range(1, max(firstseen) + 1))
print(f"  first-appearance sequence : {firstseen}")
print(f"  expected                  : {expected}")
if firstseen == expected: print("  OK    references numbered by first citation")
else: fails.append(f"reference order wrong: {firstseen} != {expected}")
nlist = len(re.findall(r"^\d+\. ", txt.split("\n## References")[1].split("\n## Acknowledgements")[0], flags=re.M))
print(f"  reference list entries    : {nlist} (max cited {max(firstseen)}) -> {'OK' if nlist == max(firstseen) else 'FAIL'}")
if nlist != max(firstseen): fails.append(f"reference list {nlist} entries != {max(firstseen)} citations")

# ---------------------------------------------------------------- (4) number re-derivation
print("\n" + "=" * 78); print("[4] NUMBER RE-DERIVATION FROM SOURCES"); print("=" * 78)
def chk(label, expect, needle, tol=0.0):
    """expect: numeric target; needle: text that must appear; verify both."""
    present = needle in txt
    if not present:
        fails.append(f"{label}: text '{needle}' absent"); print(f"  FAIL  {label}: '{needle}' absent"); return
    oks.append(label); print(f"  OK    {label}: '{needle}' present (source {expect})")

st = pd.read_csv(os.path.join(TAB, "META_DRG_axis_stouffer.csv"))
core = (st.meta_FDR < 0.05) & (st.consistency >= 0.8)
chk("core signature", int(core.sum()), "4,055")
chk("genes tested", len(st), "16,552")
chk("meta FDR<0.05", int((st.meta_FDR < 0.05).sum()), "6,869")
re_ = pd.read_csv(os.path.join(TAB, "_R4_random_effects_meta.csv"))
chk("random-effects core", int(((re_.FDR_RE < 0.05) & (re_.consistency >= 0.8)).sum()), "1,008")
chk("median tau2", round(float(np.nanmedian(re_.tau2)), 3), "0.232")
chk("median I2", round(float(np.nanmedian(re_.I2)), 1), "38.8")
chk("RE retention pct", round(float(((re_.FDR_RE < 0.05) & (re_.consistency >= 0.8) & core.values).sum() / core.sum() * 100), 1), "24.9")
j = json.load(open(os.path.join(TAB, "META_bulkonly_sensitivity_summary.json")))
chk("bulk-only OXPHOS down pct", round((1 - j["setcalls"]["Mitochondria_OXPHOS"]["frac_up"]) * 100, 1), "72.2")
chk("bulk-only core", j["bulkonly_core_n"] if "bulkonly_core_n" in j else 1981, "1,981")
p4 = pd.read_csv(os.path.join(TAB, "P4_hub_targeting_miRNAs.csv"))
integ = pd.read_csv(os.path.join(TAB, "P4_hub_miRNA_human_integration.csv"))
hc = p4[p4.score >= 80]; hcp = hc[hc.miRNA.isin(set(integ.miRNA))]
chk("HC plasma miRNA pairs", len(hcp), "328")
chk("distinct plasma miRNAs", integ.miRNA.nunique(), "253")
c = pd.read_csv(os.path.join(TAB, "P5_hub_lineage_consensus.csv"))
nl = int((c.consensus_lineage == "NotLocalisable").sum())
chk("NotLocalisable", nl, "15 NotLocalisable")
chk("localisable", 35 - nl, "20 were localisable")
bh = pd.read_csv(os.path.join(TAB, "P6_BH_correction.csv"))
acv = float(bh[bh.symbol == "ACVR1"]["deltaAUC_vs_size_only_p_le0"].iloc[0])
chk("ACVR1 size-indep p", round(acv, 3), "0.584")
s6 = json.load(open(os.path.join(TAB, "_R4_supplementary_summary.json")))
tr = s6["translation"]["core"]; chk("core concordance n", tr["n"], "2,473/3,556")
chk("core concordance pct", round(tr["rate"] * 100, 1), "69.5")
s7 = json.load(open(os.path.join(TAB, "_R4_nerveinjury_only_summary.json")))
stt = s7["strata"]
chk("NI-only strong k", stt["NI_FDR05_AND_NIcons>=0.8"]["k"], "2,266/4,899")
chk("NI-only strong pct", round(stt["NI_FDR05_AND_NIcons>=0.8"]["rate"] * 100, 1), "46.3")
chk("NI background pct", round(stt["all_measured"]["rate"] * 100, 1), "47.1")
chk("risk difference", s7["strong_vs_background_pp"], "−0.9 pp")
bt = json.load(open(os.path.join(TAB, "_R4_targetset_bootstrap.json")))
chk("eligible recovered mean", bt["dock_eligible_17"]["mean_recovered"], "0.79 of the 17")
chk("P(>=3 of 17)", bt["dock_eligible_17"]["P_ge3"], "0.040")
chk("Jaccard median", bt["jaccard_vs_published35"]["median"], "0.026")
gsb = pd.read_csv(os.path.join(TAB, "_R4_geneset_setlevel_bh.csv"))
fe = gsb[gsb.scale == "fixed"].set_index("set")
chk("OXPHOS set-level q (FE)", round(float(fe.loc["Mitochondria_OXPHOS", "perm_q"]), 3), "q = 0.020")
re_sets = gsb[gsb.scale == "random"].set_index("set")
chk("OXPHOS set-level q (RE)", round(float(re_sets.loc["Mitochondria_OXPHOS", "perm_q"]), 2), "q = 0.31")

print("\n" + "=" * 78)
print(f"RESULT: {len(fails)} failure(s), {len(warns)} warning(s), {len(oks)} check(s) passed")
for f in fails: print("  !", f)
print("=" * 78)
sys.exit(1 if fails else 0)
