#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Apply Round-16 (v1.6.0 -> v1.7.0) manuscript edits to
reports/MVP_PLOSONE_submission.md.

Edits:
  T1-1  DAM hallmark numbers (TYROBP/TREM2/APOE) + clause  [Round16 A1 Check2]
  T1-2  P2RX/P2RY six-input perm_p 0.440 -> 0.56          [A1 Check5]
  T2-1  REG3B six-input Stouffer FDR 7.1e-14 -> 1.38e-13   [A1 Check6]
  T2-3  translation perm_p = 0.0002 -> <= 0.0002 (floor)   [A2 Check4]
  T3-3  Nav1.8/axotomy mis-citation softened               [A1 Check3]
  T3-2  Author Summary tightened to "both-filters"         [A4 P3]
  T3-1  CC BY statement added to manuscript body          [A4 P2]
  VER   v1.6.0 -> v1.7.0 in body
  T0-1  References renumbered to first-citation order      [A4 P1]
"""
import io, sys, re, unicodedata

SRC = "reports/MVP_PLOSONE_submission.md"

# Superscript-digit <-> int helpers (Unicode superscripts)
SUP_DIGITS = {
    "\u2070":"0","\u00b9":"1","\u00b2":"2","\u00b3":"3","\u2074":"4",
    "\u2075":"5","\u2076":"6","\u2077":"7","\u2078":"8","\u2079":"9",
}
DIG_TO_SUP = {v:k for k,v in SUP_DIGITS.items()}

def sup_to_int(s):
    return int("".join(SUP_DIGITS[c] for c in s))

def int_to_sup(n):
    return "".join(DIG_TO_SUP[c] for c in str(n))

# T0-1: old reference number -> new (first-citation order) [A4 P1 mapping]
REFMAP = {}
for i in range(1,22): REFMAP[i]=i
REFMAP.update({38:22,40:23,22:24,23:25,26:26,24:27,25:28,27:29,28:30,
               29:31,30:32,31:33,32:34,33:35,34:36,35:37,36:38,37:39,39:40})
assert sorted(REFMAP.values())==list(range(1,41)), "REFMAP not a clean permutation"

def renumber_citations(body):
    out=[]; i=0; n=len(body)
    while i<n:
        c=body[i]
        if c in SUP_DIGITS:
            j=i
            while j<n and body[j] in SUP_DIGITS: j+=1
            run=body[i:j]; old=sup_to_int(run)
            if old not in REFMAP:
                sys.exit(f"citation number {old} not in REFMAP; abort")
            out.append(int_to_sup(REFMAP[old]))
            i=j
        else:
            out.append(c); i+=1
    return "".join(out)

# ---- main ----
with io.open(SRC, encoding="utf-8") as f:
    text=f.read()

orig=text
edits=[]

def apply_once(old, new, count=1, label=""):
    global text
    nfound=text.count(old)
    if nfound!=count:
        sys.exit(f"[{label}] expected {count} occurrence(s) of old string, found {nfound}.\n---OLD---\n{old}\n---")
    text=text.replace(old,new,1 if count==1 else nfound)
    edits.append((label,count))

def apply_all(old, new, label=""):
    global text
    nfound=text.count(old)
    if nfound==0:
        sys.exit(f"[{label}] expected >=1 occurrence(s) of old string, found 0.\n---OLD---\n{old}")
    text=text.replace(old,new)
    edits.append((label,nfound))

# T1-1a : DAM hallmark fragment (keeps the lead-in "K = 5-6" sentence intact)
old_dam=("TYROBP (meta FDR 8.8 \u00d7 10\u207b\u2079; consistency 5/5 datasets) and "
         "TREM2 (meta FDR 1.3 \u00d7 10\u207b\u00b3; consistency 5/6) are both within the FDR < 0.05 core, "
         "whereas APOE, although directionally consistent (consistency 6/6, up-regulated), does not reach "
         "the FDR < 0.05 threshold (meta FDR 0.070)")
new_dam=("TYROBP is in the core (meta_FDR = 1.2 \u00d7 10\u207b\u2077; consistency 4/5 = 0.80, up in four of five datasets), "
         "whereas TREM2, although highly significant (meta_FDR = 3.0 \u00d7 10\u207b\u00b3 six-input, 1.3 \u00d7 10\u207b\u00b3 four-bulk), "
         "fails the core consistency gate (4/6 = 0.67; 3/4 = 0.75 in the bulk-only meta), and "
         "APOE does not reach meta-significance (meta_FDR = 0.84 six-input, 0.30 four-bulk; consistency 4/6 = 0.67)")
apply_once(old_dam, new_dam, 1, "T1-1a DAM numbers")

# T1-1b : DAM clause
old_clause=("the partial, time- and sex-dependent recruitment of the DAM programme is therefore a "
            "data-supported, not merely metaphorical, descriptor.")
new_clause=("the partial, time- and sex-dependent recruitment of the DAM programme \u2014 TYROBP in-core, "
            "TREM2 significant but consistency-failing, APOE absent \u2014 is therefore a data-supported, "
            "not merely metaphorical, descriptor.")
apply_once(old_clause, new_clause, 1, "T1-1b DAM clause")

# T1-2 : P2RX six-input perm_p
apply_once("p = 0.440 in the six-input meta", "p = 0.56 in the six-input meta", 1, "T1-2 P2RX")

# T2-1 : REG3B six-input FDR
apply_once("six-input Stouffer FDR 7.1\u00d710\u207b\u00b9\u2074",
           "1.38\u00d710\u207b\u00b9\u00b3", 1, "T2-1 REG3B FDR")

# T2-3 : translation floor (all occurrences)
apply_all("permutation p = 0.0002", "permutation p \u2264 0.0002", "T2-3 translation <=")
# T2-3b : add relabel-floor note where the (significant) callout sits
apply_once("permutation p \u2264 0.0002 (significant)",
           "permutation p \u2264 0.0002 (significant; 1/5,000 relabel floor)", 1, "T2-3b floor note")

# T3-3 : Nav1.8 / axotomy mis-citation softening
old_nav=("SCN10A/Nav1.8 mRNA is down-regulated after axotomy, and bulk DRG signal is confounded by "
         "injury-induced neuronal atrophy/loss\u00b9\u00b2 and by the dilution of neuronal transcripts by "
         "infiltrating immune and glial cells.")
new_nav=("bulk DRG signal is confounded by injury-induced neuronal atrophy/loss\u00b9\u00b2 and by the "
         "dilution of neuronal transcripts by infiltrating immune and glial cells; consistent with this, "
         "Nav1.8 (SCN10A) transcript is known to fall after axotomy (e.g., in spared-nerve/axotomised DRG "
         "neuron studies), and the present bulk down-regulation is most parsimoniously read as a "
         "neuronal-loss/dilution signal rather than a neuronal up-regulation.")
apply_once(old_nav, new_nav, 1, "T3-3 Nav1.8 citation")

# T3-2 : Author Summary tightening
apply_once("found no drug target that held up reliably, a deliberately honest negative result, reported as a methodological boundary rather than a false lead.",
           "found that no target cleared both enrichment filters we applied \u2014 an honestly negative result reported as a methodological boundary rather than a false lead.",
           1, "T3-2 Author Summary")

# T3-1 : CC BY statement appended to Additional Information
apply_once("The STROBE checklist for this observational reanalysis is provided as Supporting Information (`MVP_STROBE_checklist.md`).",
           "The STROBE checklist for this observational reanalysis is provided as Supporting Information (`MVP_STROBE_checklist.md`).\n\nThis article will be published under the Creative Commons Attribution (CC BY) license.",
           1, "T3-1 CC BY")

# VER : version in body
apply_all("v1.6.0", "v1.7.0", "VER version")

# ---------- T0-1 : reference reorder ----------
if "\n## References" not in text:
    sys.exit("Cannot locate '## References' marker for reorder.")
refs_idx=text.index("\n## References")
ack_idx=text.index("\n## Acknowledgements")
body=text[:refs_idx]
refs_block=text[refs_idx:ack_idx]
tail=text[ack_idx:]

# renumber citations in BODY only (refs use ASCII numbers, handled separately)
body=renumber_citations(body)

# parse + renumber + reorder reference list
ref_lines=re.findall(r'(?m)^(\d+\.\s.*)$', refs_block)
print(f"[reorder] parsed {len(ref_lines)} reference entries")
if len(ref_lines)!=40:
    sys.exit(f"[reorder] expected 40 entries, parsed {len(ref_lines)}")
new_entries=[]
for ln in ref_lines:
    m=re.match(r'^(\d+)\.\s', ln)
    oldn=int(m.group(1))
    if oldn not in REFMAP:
        sys.exit(f"[reorder] ref {oldn} not in REFMAP")
    newn=REFMAP[oldn]
    newln=re.sub(r'^\d+\.', f"{newn}.", ln, count=1)
    new_entries.append((newn,newln))
new_entries.sort(key=lambda x:x[0])
new_refs_block="\n## References\n\n"+"\n\n".join(ln for _,ln in new_entries)+"\n"
text=body+new_refs_block+tail

# sanity: every new number 1..40 present exactly once in the list
present=sorted(e[0] for e in new_entries)
assert present==list(range(1,41)), f"ref list numbers off: {present}"

# verify no old citation leaked: count how many superscript citation runs remain out of map
leaked=[]
i=0; n=len(body)
while i<n:
    c=body[i]
    if c in SUP_DIGITS:
        j=i
        while j<n and body[j] in SUP_DIGITS: j+=1
        v=sup_to_int(body[i:j])
        if v not in REFMAP: leaked.append(v)
        i=j
    else: i+=1
assert not leaked, f"unmapped citation numbers in body: {sorted(set(leaked))}"

with io.open(SRC,"w",encoding="utf-8") as f:
    f.write(text)

print("Edits applied:")
for label,c in edits: print(f"  {label}: {c}")
print(f"Body citation renumber: OK (no leaks).")
print(f"Reference list renumbered 1..40 and reordered to first-citation order.")
print(f"Characters changed: {len(orig)} -> {len(text)}")
