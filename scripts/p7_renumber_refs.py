#!/usr/bin/env python3
# p7_renumber_refs.py -- Round-4 remediation T0-2.
# Nature house style requires references numbered in the order they first appear in the text.
# Hand-numbering is error-prone, so the manuscript source carries {{key}} citation markers and
# this script assigns numbers by first appearance, renders superscripts, emits the numbered
# reference list, and prints an audit of the mapping (unused keys, unknown keys, order).
import os, re, json, sys

ROOT = "D:/2026.9/极速交付9月会员日优惠套路/01_AI生信-虚拟多重筛药/慢性疼痛"
SRC  = os.path.join(ROOT, "reports/_v15_source.md")
DST  = os.path.join(ROOT, "reports/MVP_ScientificReports_submission.md")
MAPOUT = os.path.join(ROOT, "results/tables/_R4_reference_map.json")

REFS = {
 "macrae2017": "Macrae, W. A. Chronic postsurgical pain: 10 years on. *Br. J. Anaesth.* **119** (Suppl. 1), i3–i4 (2017).",
 "sapio2020": "Sapio, M. R. et al. Dynorphin and enkephalin opioid peptides and transcripts in spinal cord and dorsal root ganglion during peripheral inflammatory hyperalgesia and allodynia. *J. Pain* **21**, 783–796 (2020).",
 "xu2022": "Xu, R. et al. Genome-wide expression profiling by RNA-sequencing in spinal cord dorsal horn of a rat chronic postsurgical pain model. *J. Pain Res.* **15**, 985–1001 (2022).",
 "qu2024": "Qu, Y. et al. Neuroinflammation signatures in dorsal root ganglia following chronic constriction injury. *Heliyon* **10**, e31481 (2024).",
 "pokhilko2020": "Pokhilko, A., Nash, A. & Cader, M. Z. Common transcriptional signatures of neuropathic pain. *Pain* **161**, 1542–1554 (2020).",
 "meng2024": "Meng, X. et al. A transcriptome data set for comparing skin, muscle and dorsal root ganglion between acute and chronic postsurgical pain rats. *Sci. Data* **11**, 1229 (2024).",
 "dong2025": "Dong, F. L. et al. An atlas of neuropathic pain-associated molecular pathological characteristics in the mouse spinal cord. *Commun. Biol.* **8**, 70 (2025).",
 "gan2023": "Gan, J. H. et al. DrugRep: an automatic virtual screening server for drug repurposing. *Acta Pharmacol. Sin.* **44**, 888–896 (2023).",
 "pham2025": "Pham, P. et al. DrugPipe: generative artificial intelligence-assisted virtual screening pipeline for generalizable and efficient drug repurposing. *Biol. Methods Protoc.* **10**, bpaf038 (2025).",
 "divito2026": "Divito, A. E. et al. Suzetrigine: a novel nonopioid systemic analgesic. *Cleveland Clin. J. Med.* **93**, 94–98 (2026).",
 "haque2024": "Haque, M. M., Kuppusamy, P. & Melemedjian, O. K. Disruption of mitochondrial pyruvate oxidation in dorsal root ganglia drives persistent nociceptive sensitization and causes pervasive transcriptomic alterations. *Pain* **165**, 1531–1549 (2024).",
 "kerenshaul2017": "Keren-Shaul, H. et al. A Unique Microglia Type Associated with Restricting Development of Alzheimer's Disease. *Cell* **169**, 1276–1290.e17 (2017).",
 "yousefpour2025": "Yousefpour, N. et al. Targeting C1q prevents microglia-mediated synaptic removal in neuropathic pain. *Nat. Commun.* **16**, 4590 (2025).",
 "kong2023": "Kong, E. et al. Lyn-mediated glycolysis enhancement of microglia contributes to neuropathic pain through facilitating IRF5 nuclear translocation in spinal dorsal horn. *J. Cell. Mol. Med.* **27**, 1664–1681 (2023).",
 "tsuda2003": "Tsuda, M. et al. P2X4 receptors induced in spinal microglia gate tactile allodynia after nerve injury. *Nat. Med.* **9**, 1524–1529 (2003).",
 "mcdonnell2018": "McDonnell, A. et al. A phase II randomized, double-blind, placebo-controlled, parallel-group, multicenter study of the Nav1.7 blocker PF-05089771 in subjects with painful diabetic peripheral neuropathy. *Pain* **159**, 1465–1476 (2018).",
 "sun2021": "Sun, Y. et al. Mechanism of spinal dorsal horn SDF-1 signaling pathway involved in chronic postsurgical pain. *J. Pract. Med.* **37**, 2845–2850 (2021).",
 "luo2016": "Luo, X. et al. Crosstalk between astrocytic CXCL12 and microglial CXCR4 contributes to the development of neuropathic pain. *Mol. Pain* **12**, 1744806916636385 (2016).",
 "taves2016": "Taves, S. & Ji, R. R. Microglia and complement mediators in chronic pain and itch. *eLife* **5**, e21312 (2016).",
 "nie2025": "Nie, H. et al. Neuronal Reg3β/macrophage TNF-α–mediated positive feedback signaling contributes to pain chronicity in a rat model of CRPS-I. *Sci. Adv.* **11**, eadu4270 (2025).",
 "coull2005": "Coull, J. A. M. et al. BDNF from microglia causes the shift in neuronal anion gradient underlying neuropathic pain. *Nat. Neurosci.* **8**, 1617–1620 (2005).",
 "scholz2007": "Scholz, J. & Woolf, C. J. The neuropathic pain triad: neurons, immune cells and glia. *Nat. Neurosci.* **10**, 1361–1368 (2007).",
 "ding2019": "Ding, H. H. et al. TNF-α/STAT3 pathway epigenetically upregulates Nav1.6 expression in DRG and contributes to neuropathic pain induced by L5-VRT. *J. Neuroinflammation* **16**, 29 (2019).",
 "tansley2022": "Tansley, S. et al. Single-cell RNA sequencing reveals time- and sex-specific responses of mouse spinal cord microglia to peripheral nerve injury and links ApoE to chronic pain. *Nat. Commun.* **13**, 843 (2022).",
 "costigan2002": "Costigan, M. et al. Multiple chronic pain states are associated with a common RNA expression signature in human and rat dorsal root ganglion neurons. *Proc. Natl. Acad. Sci. U. S. A.* **99**, 13929–13934 (2002).",
 "schafer2012": "Schafer, D. P. et al. Microglia sculpt postnatal neural circuits in an activity and complement-dependent manner. *Neuron* **74**, 691–705 (2012).",
}

SUP = str.maketrans("0123456789", "⁰¹²³⁴⁵⁶⁷⁸⁹")
def sup(n): return str(n).translate(SUP)

def compress(nums):
    """[1,2,3,5] -> '1–3,5'  (runs of >=3 collapsed to an en-dash range)."""
    nums = sorted(set(nums)); out = []; i = 0
    while i < len(nums):
        j = i
        while j + 1 < len(nums) and nums[j + 1] == nums[j] + 1: j += 1
        if j - i + 1 >= 3: out.append(f"{nums[i]}–{nums[j]}")
        else: out.extend(str(x) for x in nums[i:j + 1])
        i = j + 1
    return ",".join(out)

src = open(SRC, encoding="utf-8").read()
head, _, tail = src.partition("<!--REFLIST-->")
if not tail: sys.exit("REFLIST placeholder not found")

order, unknown, firstpos = [], [], {}
def repl(m):
    keys = [k.strip() for k in m.group(1).split(";") if k.strip()]
    ns = []
    for k in keys:
        if k not in REFS: unknown.append(k); continue
        if k not in firstpos: firstpos[k] = len(order) + 1; order.append(k)
        ns.append(firstpos[k])
    return sup(compress(ns)) if ns else ""

body = re.sub(r"\{\{([^}]*)\}\}", repl, head)

lines = [f"{i}. {REFS[k]}" for i, k in enumerate(order, 1)]
reflist = "\n".join(lines)
out = body + reflist + tail
open(DST, "w", encoding="utf-8").write(out)

json.dump({"order": order, "numbered": {str(i): k for i, k in enumerate(order, 1)}},
          open(MAPOUT, "w"), indent=2)

print(f"citations rendered : {len(re.findall(r'[\u2070-\u209f\u00b9\u00b2\u00b3]', body))} superscript chars")
print(f"references emitted : {len(order)}")
print("\n#  key")
for i, k in enumerate(order, 1): print(f"{i:2d} {k}")
unused = [k for k in REFS if k not in firstpos]
print(f"\nunused keys : {unused if unused else 'none'}")
print(f"unknown keys: {unknown if unknown else 'none'}")
leftover = re.findall(r"\{\{[^}]*\}\}", out)
print(f"unrendered markers: {leftover if leftover else 'none'}")
print(f"\n[written] {DST}")
