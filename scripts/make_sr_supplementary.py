#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Generate MVP_ScientificReports_supplementary.md from authoritative CSVs.

Faithful transcription: every cell is read at run time from the CSV of record
in results/tables/. No number is hand-copied. Rounds floats to 3 decimals.
"""
import os
import pandas as pd

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TBL = os.path.join(BASE, "results", "tables")
OUT = os.path.join(BASE, "reports", "MVP_ScientificReports_supplementary.md")


def rnd(x):
    if pd.isna(x):
        return ""
    try:
        f = float(x)
        if f == int(f):
            return str(int(f))
        return f"{f:.3f}"
    except (ValueError, TypeError):
        return str(x)


def md_table(df, cols, headers):
    lines = ["| " + " | ".join(headers) + " |",
             "| " + " | ".join(["---"] * len(headers)) + " |"]
    for _, row in df.iterrows():
        cells = [str(rnd(row[c])) for c in cols]
        lines.append("| " + " | ".join(cells) + " |")
    return "\n".join(lines)


def main():
    L = []
    L.append("# Supplementary Information")
    L.append("")
    L.append("**Title.** A neuroimmune–metabolic programme defines the chronic postsurgical pain "
             "dorsal root ganglion–spinal cord axis with an honest null in FDA repurposing")
    L.append("")
    L.append("**Author.** Yang Y")
    L.append("")
    L.append("This Supplementary Information accompanies the Scientific Reports submission-ready "
             "manuscript (v1.0, 2026-09-20). It contains three supplementary tables (S1–S3) that are "
             "**not** counted toward the 8 main display-item cap (5 figures + 3 tables). Every numeric "
             "value below is reproduced programmatically from the authoritative CSV outputs in "
             "`results/tables/`; the raw CSV files are the source of record. `NA` = not applicable / "
             "blank in source.")
    L.append("")

    # ---- S1: P5 hub lineage consensus ----
    s1 = pd.read_csv(os.path.join(TBL, "P5_hub_lineage_consensus.csv"))
    L.append("## Supplementary Table S1. Cross-dataset hub lineage consensus (P5)")
    L.append("")
    L.append("Consensus across three single-cell/nucleus datasets: GSE216039 (mouse DRG neuron-enriched "
             "scRNA), GSE328175 (mouse lumbar spinal snRNA), GSE246288 (mouse spinal-cord Cd11b+ "
             "microglia scRNA). `n_methods` = number of ML routes (of 3) that flagged the gene as a hub; "
             "`n_datasets` = number of datasets in which the hub was localisable; `consensus_lineage` = "
             " Neuronal / Immune / Glial / Mixed / NotLocalisable; `confident` = True only when "
             "localisation agreed across ≥2 datasets; `mean_enrich` = mean log2 enrichment of the hub in "
             "its assigned cell type vs others; `tiers` / `lineages` list per-dataset calls.")
    L.append("")
    L.append(md_table(
        s1,
        ["symbol", "n_methods", "n_datasets", "celltypes", "consensus_lineage",
         "confident", "mean_enrich", "tiers", "lineages"],
        ["Symbol", "n_methods", "n_datasets", "Cell types", "Consensus lineage",
         "Confident", "Mean enrich", "Tiers", "Lineages"]))
    L.append("")

    # ---- S2: P5 GSE325938 Visium regionalisation (curated columns) ----
    s2 = pd.read_csv(os.path.join(TBL, "P5_GSE325938_hub_regionalization.csv"))
    L.append("## Supplementary Table S2. Visium GSE325938 spatial regionalisation of the 35 hubs (P5)")
    L.append("")
    L.append("Spatial regionalisation of the 35 hubs across seven spinal-cord regions in Visium "
             "GSE325938 (mouse spinal cord, Sham tissue). `top_region` = region of maximal mean log2 "
             "expression; `top_label_log2` = that region's label log2 value; `top_detection` = detection "
             "fraction in the top region; `tier` = restricted / enriched / broad-low; `snRNA_lineage` = "
             "lineage assigned by snRNA (blank = not localisable); `crossmodal` = consistent / divergent "
             "/ n/a between Visium top region and snRNA lineage. The full per-region breakdown "
             "(`log2_all_regions`) is retained in `results/tables/P5_GSE325938_hub_regionalization.csv`.")
    L.append("")
    L.append(md_table(
        s2,
        ["symbol", "present", "top_region", "top_label_log2", "top_detection",
         "global_mean", "detection_global", "tier", "snRNA_lineage", "crossmodal"],
        ["Symbol", "Present", "Top region", "Top log2", "Top detect",
         "Global mean", "Global detect", "Tier", "snRNA lineage", "Crossmodal"]))
    L.append("")

    # ---- S3: P6 reverse positive-control docking AUCs ----
    s3 = pd.read_csv(os.path.join(TBL, "P6_reverse_control.csv"))
    L.append("## Supplementary Table S3. Reverse positive-control docking AUCs (P6)")
    L.append("")
    L.append("Reverse positive controls for the structure-based repurposing screen. `n_known_pairs` = "
             "number of ChEMBL binding-type pairs (pChEMBL ≥ 6) for the target; `n_ligands` = number of "
             "docked FDA drugs scored; `known_median_aff` / `all_median_aff` = median Vina affinity "
             "(kcal/mol, more negative = tighter) of known binders vs the full library; "
             "`known_median_pct` = percentile of known-binder median affinity within the library; "
             "`auc_known_vs_rest` = ROC-AUC separating known binders from the rest; `reliable` = True "
             "only when ≥3 known pairs exist. Targets with 0 known pairs (GALNS, ITPKC, SERPINE1, VASH2) "
             "are undockable-to-control and shown for completeness. `known_drugs` lists the ChEMBL "
             "binding-type compounds used as positive controls.")
    L.append("")
    L.append(md_table(
        s3,
        ["symbol", "n_known_pairs", "n_ligands", "known_median_aff", "all_median_aff",
         "known_median_pct", "auc_known_vs_rest", "reliable", "known_drugs"],
        ["Target", "n_known", "n_ligands", "Known med aff", "All med aff",
         "Known pct", "AUC", "Reliable", "Known drugs (ChEMBL)"]))
    L.append("")

    with open(OUT, "w", encoding="utf-8") as fh:
        fh.write("\n".join(L) + "\n")
    print("WROTE", OUT)
    print("S1 rows:", len(s1), "S2 rows:", len(s2), "S3 rows:", len(s3))


if __name__ == "__main__":
    main()
