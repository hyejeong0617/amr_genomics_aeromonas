#!/bin/bash
# ============================================================
# 05_amr_profiling.sh — AMR gene prediction
# ------------------------------------------------------------
# Tools  : NCBI AMRFinderPlus v3.10.45
#          ResFinder v4.1 (web)
# Paper  : Lee et al. (2023), Methods 2.6
#          AMRFinderPlus : default settings
#          ResFinder     : 90% identity threshold (default)
# Input  : Assembled contigs (contigs.fasta) — 19 WGS strains
# Output : AMR gene tables → Supp. Table S2, Table 1
# ============================================================

OUTPUT_DIR="amr_results"
mkdir -p "$OUTPUT_DIR"

# ── NCBI AMRFinderPlus v3.10.45 ───────────────────────────────
# Installation:
#   conda install -c bioconda ncbi-amrfinderplus
#   amrfinder --update   # update database before first run
#
# NOTE: Aeromonas is NOT in the AMRFinderPlus --organism list.
#   Supported organisms are human pathogens only
#   (Escherichia, Klebsiella, Salmonella, Vibrio, etc.)
#   Run WITHOUT --organism flag for Aeromonas.

STRAINS=(
    "SU4"   "A533"   "A536"   "A537"   "A539"
    "SU3"   "SU9"    "SC42"   "OY1"    "OY52"
    "SU6"   "SL22"   "SU58-3" "LJP308"
    "SU2"   "SL19"   "SL21"   "SC45"   "OY56" "OY59" "LJP441"
)

for STRAIN in "${STRAINS[@]}"; do
    CONTIG="${STRAIN}_assembled/contigs.fasta"
    amrfinder \
        --nucleotide "$CONTIG" \
        --output "${OUTPUT_DIR}/${STRAIN}_amrfinder.tsv"
    echo "AMRFinderPlus done: $STRAIN"
done

# Merge all results into one table:
head -1 "${OUTPUT_DIR}/SU4_amrfinder.tsv" \
    > "${OUTPUT_DIR}/combined_amrfinder.tsv"
for f in "${OUTPUT_DIR}"/*_amrfinder.tsv; do
    tail -n +2 "$f" >> "${OUTPUT_DIR}/combined_amrfinder.tsv"
done
echo "Combined: ${OUTPUT_DIR}/combined_amrfinder.tsv"

# ── ResFinder v4.1 (web interface) ────────────────────────────
# URL      : https://cge.cbs.dtu.dk/services/ResFinder/
# Settings : Identity threshold 90% (default), all gene classes
# Species  : Aeromonas
# Output   : → cross-checked against AMRFinderPlus results
echo ""
echo "ResFinder: run via web at https://cge.cbs.dtu.dk/services/ResFinder/"
echo "  Settings used: identity threshold 90%, species = Aeromonas"
