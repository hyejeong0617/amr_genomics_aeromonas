#!/bin/bash
# ============================================================
# 04_ani.sh — Average Nucleotide Identity (ANI) analysis
# ------------------------------------------------------------
# Tools  : FastANI, ANIclustermap
# Paper  : Lee et al. (2023), Methods 2.5
#          "ANI values were calculated using FastANI (Jain et al., 2018)"
#          "ANIclustermap was created using ANIclustermap pipeline
#           (Shimoyama, 2022)"
# Input  : Genome assemblies (contigs.fasta) — 22 isolates + 8 refs
# Output : ANI matrix (TSV), clustered heatmap (PNG/SVG)
# ============================================================

GENOME_DIR="query+reference_genomes"
QUERY_LIST="${GENOME_DIR}/query+reference_list.txt"
OUTPUT_DIR="fastani_results"
mkdir -p "$OUTPUT_DIR"

# ── Step 1: Prepare genome file list ─────────────────────────
# List all .fasta files (22 isolates + 8 reference genomes)
ls ${GENOME_DIR}/*.fasta > "$QUERY_LIST"
echo "Genome list: $(wc -l < $QUERY_LIST) genomes"

# ── Step 2: All-vs-all ANI (many-to-many) ────────────────────
# --ql : query genome list
# --rl : reference genome list (same as query for all-vs-all)
# --matrix : output lower-triangular distance matrix
fastANI \
    --ql "$QUERY_LIST" \
    --rl "$QUERY_LIST" \
    --matrix \
    -o "${OUTPUT_DIR}/fastani_all.out.txt" \
    -t 8

echo "FastANI complete: ${OUTPUT_DIR}/fastani_all.out.txt"
echo "Matrix file: ${OUTPUT_DIR}/fastani_all.out.txt.matrix"

# ── Step 3: ANIclustermap — hierarchical clustering + heatmap ─
# --fig_width / --fig_height : figure dimensions
# --cmap_colors              : color scale
# --annotation               : show ANI values in cells
ANIclustermap \
    -i "$GENOME_DIR" \
    -o "${OUTPUT_DIR}/ANIclustermap_result" \
    --fig_width 20 \
    --fig_height 15 \
    --cmap_colors white,orange,red \
    --annotation

echo "ANIclustermap complete: ${OUTPUT_DIR}/ANIclustermap_result/"

# ── Species boundary interpretation ──────────────────────────
# ANI ≥ 96% → same species (Colston et al., 2014 for Aeromonas)
# ANI = 99.9–100% → identical strains
#   Confirmed identical pairs in this study:
#     A533 ↔ A536      (A. dhakensis)
#     SU3  ↔ SU9 ↔ SU15 (A. rivipollensis)
# → Only one representative per identical pair used in
#   downstream virulence/AMR analysis (n=19 strains)
