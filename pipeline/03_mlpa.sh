#!/bin/bash
# ============================================================
# 03_mlpa.sh — Species identification: gyrB + MLPA + MEGA11
# ------------------------------------------------------------
# Tools  : BLAST+, MEGA11 v11.0.10
# Paper  : Lee et al. (2023), Methods 2.2 + 2.5
#          Methods 2.2: gyrB single-gene NJ tree (79 isolates)
#          Methods 2.5: MLPA of 6 housekeeping genes (22 WGS)
# Genes  : gyrB, rpoD, gyrA, recA, dnaJ, dnaX
#          Concatenated length: 4,172 bp
# Output : Phylogenetic tree files (.nwk, .meg)
# ============================================================

# ── Step 1: Build BLAST database from reference sequences ────
# reference_hk6.fasta: concatenated 6 housekeeping gene sequences
# from 10 reference strains (see Supp. Table S1A for accessions)
# Download reference sequences from NCBI GenBank first.

makeblastdb \
    -in reference_hk6.fasta \
    -out hk6_db \
    -dbtype nucl

echo "BLAST database created: hk6_db"

# ── Step 2: Extract housekeeping genes from each assembly ─────
# Run blastn against each assembled genome.
# Output format 6 returns: query, subject, %identity, length,
#   start/end positions, e-value, bitscore, query/subject sequences.

ASSEMBLIES=(
    "A539" "SU3" "SU9" "SU15" "SC42" "OY1"              # A. rivipollensis
    "OY52"                                                 # A. media
    "SU6" "SL22" "SU58-3"                                 # A. bestiarum
    "LJP308"                                               # A. piscicola
    "SU2" "SL19" "SL21" "SC45" "OY56" "OY59" "LJP441"   # A. salmonicida
    "SU4"                                                  # A. caviae
    "A537"                                                 # A. hydrophila
    "A533" "A536"                                          # A. dhakensis
)

mkdir -p blast_results

for SAMPLE in "${ASSEMBLIES[@]}"; do
    CONTIG="${SAMPLE}_assembled/contigs.fasta"
    if [ -f "$CONTIG" ]; then
        blastn \
            -db hk6_db \
            -query "$CONTIG" \
            -out "blast_results/${SAMPLE}_hk6.txt" \
            -outfmt "6 qseqid sseqid pident length sstart send qstart qend evalue bitscore qseq sseq" \
            -perc_identity 90 \
            -num_threads 4
        echo "BLAST done: $SAMPLE"
    else
        echo "WARNING: $CONTIG not found"
    fi
done

# ── Step 3: MEGA11 — construct phylogenetic tree ──────────────
# MEGA11 was used via GUI (downloaded from https://www.megasoftware.net/).
# The following describes the steps performed in the GUI,
# consistent with Methods 2.2 and 2.5.
#
# 1. Multiple sequence alignment: CLUSTAL W (in MEGA11)
#    - Align each housekeeping gene separately
#    - Concatenate aligned sequences (total 4,172 bp)
#
# 2. Phylogenetic tree construction (Methods 2.5):
#    - Method   : Neighbor-Joining (NJ)
#    - Model    : Kimura 2-parameter
#    - Bootstrap: 1,000 replicates
#    - Confirm  : Maximum-likelihood (ML), 100 replicates
#
# 3. Species boundary confirmation:
#    - ANI ≥ 96% cutoff for Aeromonas (Colston et al., 2014)
#
# ── MEGA11 CLI equivalent (method B — for reproducibility) ────
# MEGA11 also supports command-line execution via megacc.
# The following is the CLI equivalent of the GUI steps above.
# Parameter file (.mao) can be exported from the MEGA11 GUI
# after setting the analysis options.
#
# megacc \
#     -a NJ_Kimura2p_bootstrap1000.mao \
#     -d concatenated_aligned.meg \
#     -o mlpa_NJ_tree
#
# megacc \
#     -a ML_bootstrap100.mao \
#     -d concatenated_aligned.meg \
#     -o mlpa_ML_tree
#
# Note: .mao files must be generated from MEGA11 GUI first:
#   Phylogeny → Set Analysis Options → Save Settings As .mao

echo "MLPA pipeline complete."
echo "See Supp. Table S1A for reference strain accession numbers."
echo "See MEGA11 GUI for tree visualization and bootstrap analysis."
