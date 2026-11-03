#!/bin/bash
# Phase 1 provenance: illustrative repository script; execution of these exact
# commands and historical parameters is not independently evidenced here.
# ============================================================
# 07_abricate.sh — Multi-database AMR/virulence screening
# ------------------------------------------------------------
# Tool   : Abricate (Seemann, https://github.com/tseemann/abricate)
# Role   : Optional screening example (historical use unverified)
#          Screens against multiple databases in one run:
#          VFDB, NCBI, ResFinder, PlasmidFinder, CARD, ARG-ANNOT
#          May support comparisons with primary tools; archived evidence absent.
# Paper  : Not reported in published Methods; historical use unconfirmed.
# Input  : Assembled contigs (*.fasta) — 19 WGS strains
# Output : Per-database result tables + summary
# ============================================================

# ── Installation ─────────────────────────────────────────────
# conda config --add channels defaults
# conda config --add channels bioconda
# conda create -n abricate abricate
# conda activate abricate

# Verify available databases:
# abricate --list
# → ncbi, vfdb, resfinder, plasmidfinder, card, argannot, ecoh, megares

# Update databases (run once after installation):
# abricate-get_db --db vfdb --force
# abricate-get_db --db ncbi --force
# abricate-get_db --db resfinder --force
# abricate-get_db --db plasmidfinder --force
#
# If update fails with SSL error:
#   conda install perl-lwp-protocol-https
#   then re-run abricate-get_db

# ── Run all databases against all assemblies ─────────────────
mkdir -p abricate_results

# Multiple fasta files at once (*.fasta in current directory):
abricate --db vfdb        *.fasta > abricate_results/vfdb_results.tab
abricate --db ncbi        *.fasta > abricate_results/ncbi_amr_results.tab
abricate --db resfinder   *.fasta > abricate_results/resfinder_results.tab
abricate --db plasmidfinder *.fasta > abricate_results/plasmidfinder_results.tab
abricate --db card        *.fasta > abricate_results/card_results.tab
abricate --db argannot    *.fasta > abricate_results/argannot_results.tab

echo "All database screens complete"

# ── Single file run (alternative) ────────────────────────────
# abricate --db vfdb  --csv A539_contigs.fasta > abricate_results/A539_vfdb.csv
# abricate --db ncbi  --csv A539_contigs.fasta > abricate_results/A539_amr.csv

# ── Summarise results across all samples ─────────────────────
# Creates a presence/absence matrix for each database:
abricate --summary abricate_results/vfdb_results.tab        \
    > abricate_results/vfdb_summary.tab
abricate --summary abricate_results/ncbi_amr_results.tab    \
    > abricate_results/ncbi_summary.tab
abricate --summary abricate_results/resfinder_results.tab   \
    > abricate_results/resfinder_summary.tab
abricate --summary abricate_results/plasmidfinder_results.tab \
    > abricate_results/plasmidfinder_summary.tab

echo "Summary tables written to abricate_results/"

# Historical cross-validation and database agreement are not established here.
# Database releases and thresholds must be recorded before any future comparison.
