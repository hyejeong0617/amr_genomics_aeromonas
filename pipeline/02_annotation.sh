#!/bin/bash
# ============================================================
# 02_annotation.sh — Genome annotation via NCBI PGAP
# ------------------------------------------------------------
# Tool   : NCBI Prokaryotic Genome Annotation Pipeline (PGAP)
# Paper  : Lee et al. (2023), Methods 2.4
#          "Draft genome assemblies were annotated using the
#           NCBI Prokaryotic Genome Annotation Pipeline"
#          (Tatusova et al., 2016)
# Method : Assembled contigs submitted to NCBI GenBank via
#          web submission portal, with PGAP annotation
#          requested at submission time.
# Output : Annotated genome assemblies deposited to NCBI
#          BioProject: PRJNA877469
#          Accessions: JAOPLB000000000 – JAOPLW000000000
# ============================================================

# ── How annotation was performed (original study) ────────────
# Genome assemblies were submitted to NCBI via the web
# submission portal (https://submit.ncbi.nlm.nih.gov/),
# with PGAP annotation requested during submission.
# NCBI ran PGAP automatically and returned annotated GenBank
# files, which were then used for downstream MGE and
# AMR gene analyses.
#
# Submission steps:
#   1. Create BioProject at https://submit.ncbi.nlm.nih.gov/
#   2. Create BioSample entries (one per isolate)
#   3. Upload assembled contigs (FASTA) via Genome submission
#   4. Select "Request NCBI annotation (PGAP)" during submission
#   5. Receive annotated GenBank (.gbk) files from NCBI
#
# The annotated assemblies are publicly available:
#   https://www.ncbi.nlm.nih.gov/bioproject/PRJNA877469

# ── Retrieve annotated assemblies from NCBI ──────────────────
# To download the deposited annotated genomes:
#
# Using NCBI Datasets CLI (conda install -c conda-forge ncbi-datasets-cli):
#
# datasets download genome accession \
#     JAOPLB000000000 JAOPLC000000000 JAOPLD000000000 \
#     JAOPLE000000000 JAOPLF000000000 JAOPLG000000000 \
#     JAOPLH000000000 JAOPLI000000000 JAOPLJ000000000 \
#     JAOPLK000000000 JAOPLL000000000 JAOPLM000000000 \
#     JAOPLN000000000 JAOPLO000000000 JAOPLP000000000 \
#     JAOPLQ000000000 JAOPLR000000000 JAOPLS000000000 \
#     JAOPLT000000000 JAOPLU000000000 JAOPLV000000000 \
#     JAOPLW000000000 \
#     --include gbff,gff3,sequence \
#     --filename aeromonas_annotated_genomes.zip

echo "Annotation was performed by NCBI PGAP at submission."
echo "See BioProject PRJNA877469 for all annotated assemblies."
echo "  https://www.ncbi.nlm.nih.gov/bioproject/PRJNA877469"
