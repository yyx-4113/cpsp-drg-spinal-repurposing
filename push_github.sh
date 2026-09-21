#!/usr/bin/env bash
# push_github.sh — safe, CURATED push of the CPSP science deposit to GitHub.
# Run from Git Bash in the project root:  bash push_github.sh
# Account discipline: pushes to yyx-4113/cpsp-drg-spinal-repurposing (NEVER yongxinyang).
#
# SCOPE DISCIPLINE (CRITICAL):
#   This repo is the *public science deposit*. The following are deliberately EXCLUDED
#   because they contain pending-grant strategy or internal review material and must NOT
#   be public:
#     - results/P6_FJNSF_*            (Fujian NSFC application drafts)
#     - results/MVP_FJNSF_*           (grant consistency checklist)
#     - results/MVP_journal_recommendation.md / MVP_novelty_check.md  (publication strategy)
#     - results/P4_ACCESS_DOSSIER.md / P4_HUMAN_REANALYSIS_*.md / P4_SPARC476_results.md /
#       P4b_Pennsieve480_results.md  (P4 human-reanalysis dossiers — peripheral, not in MVP manuscript)
#     - reports/REVIEW_PANEL*/  reports/REVIEW_round*/  reports/RESPONSE_round*  (internal review)
#     - reports/_v14_source.md / _v15_source.md / MVP_manuscript_draft_v1.md / MVP_manuscript_skeleton.md
#     - any 标书 / 提交版 / _QC_ files
#   => we NEVER do `git add results/` or `git add reports/` wholesale. Every path is listed.
set -euo pipefail

REPO_ROOT="D:/2026.9/极速交付9月会员日优惠套路/01_AI生信-虚拟多重筛药/慢性疼痛"
cd "$REPO_ROOT"

echo "== 0. clear any stale git index lock =="
rm -f .git/index.lock || true

echo "== 1. WORKING-TREE big/forbidden scan (data/ docking/ .workbuddy/) =="
LEAK=$(git status --short | grep -iE "data/|docking/|\.workbuddy/" || true)
if [ -n "$LEAK" ]; then echo "WORKING-TREE LEAK — aborting:"; echo "$LEAK"; exit 1; fi
echo "   clean (submission_pack/ untracked is OK; it is never added)"

echo "== 2. results/ .gz size guard (<100 MB each, GitHub hard limit) =="
BAD=0
while IFS= read -r f; do
  sz=$(stat -c%s "$f" 2>/dev/null || echo 0)
  if [ "$sz" -gt 104857600 ]; then echo "TOO BIG: $f ($sz bytes)"; BAD=1; fi
done < <(find results -name '*.gz' 2>/dev/null)
if [ "$BAD" -ne 0 ]; then echo "aborting: a .gz exceeds 100 MB"; exit 1; fi
echo "   all results/ .gz < 100 MB"

echo "== 3. force-add the 5 figure PNGs (figures/ is gitignored) =="
git add -f figures/Fig1_geneset_programme.png figures/Fig2_hub_convergence.png \
          figures/Fig3_DRG_neuron_subtype_localisation.png \
          figures/Fig4_spinal_lineage_visium.png figures/Fig5_docking_honest_null.png

echo "== 4. CURATED add of science-deposit scope (explicit paths only) =="
# Derived tables (all public-data-derived; P4_* here = MVP human-reanalysis stage, NOT the grant)
git add results/tables results/figures results/checks
git add results/P2_RESULTS.md results/P3_RESULTS.md results/P5_RESULTS.md \
        results/P6_RESULTS.md results/P5_GSE325938_note.md
# Final submission documents (the source of truth)
git add reports/MVP_ScientificReports_submission.md \
        reports/MVP_ScientificReports_supplementary.md \
        reports/MVP_ScientificReports_reporting_summary.md \
        reports/MVP_ScientificReports_cover_letter.md \
        reports/P6_manuscript_draft.md
# Pipeline code (P4_*/p4_* and p6_v1x_* are MVP pipeline, public data — safe)
git add scripts .github
# Repo metadata / legal / deposit docs
git add README.md PROJECT_PLAN.md CITATION.cff LICENSE GITHUB_DEPOSIT_SOP.md \
        author_verification_statement.md .gitignore push_github.sh

echo "== 5. STAGED leak re-scan (data/ docking/ submission_pack/ .workbuddy/) =="
STAGED_LEAK=$(git diff --cached --name-only | grep -iE "data/|docking/|submission_pack/|\.workbuddy/" || true)
if [ -n "$STAGED_LEAK" ]; then echo "STAGED LEAK — aborting:"; echo "$STAGED_LEAK"; exit 1; fi
echo "   staged set clean"

echo "== 6. SENSITIVE scan (REAL leaks: FJNSF / 标书 / 提交版 / REVIEW_PANEL / RESPONSE_round / REVIEW_round / _v14_source / _v15_source / _QC_) =="
SENS=$(git diff --cached --name-only | grep -iE "FJNSF|标书|提交版|journal_recommendation|novelty_check|REVIEW_PANEL|RESPONSE_round|REVIEW_round|_v14_source|_v15_source|_QC_|P6_FJNSF|MVP_FJNSF" || true)
if [ -n "$SENS" ]; then echo "SENSITIVE LEAK — aborting:"; echo "$SENS"; exit 1; fi
echo "   no sensitive files staged"

echo "== 7. dry summary =="
git diff --cached --name-only | wc -l | sed 's/^/   files to commit: /'
git diff --cached --name-only | grep -iE "\.(pdbqt|gz|h5|nbc|pdb|tar|zip|exe)$" | grep -viE "tools/vina.exe" || echo "   no unexpected binaries staged"

echo "== 8. commit (only if there is a diff to commit) =="
if git diff --cached --quiet; then echo "   nothing staged to commit"; else
  git commit -m "Sync science deposit to post-Round-6 MVP manuscript: honest-null full-library docking, DerSimonian-Laird random-effects + set-level BH, non-circular incision-translation test, ref renumber (p8), inline display-item citations, p9 Nature-limit checks; add GSE325938 Visium dorsal-horn regionalisation, 5 figure PNGs, final cover letter + submission docs"
fi

echo "== 9. push to origin main =="
git push origin main

echo "== DONE ==  last commit:"; git log --oneline -1
echo "   total tracked files:"; git ls-files | wc -l
