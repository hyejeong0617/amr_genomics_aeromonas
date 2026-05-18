#!/bin/bash
# ============================================================
# 06_virulence_mge.sh — Virulence factors, plasmids, MGEs
# ------------------------------------------------------------
# Tools  : VFanalyzer / VFDB (web)
#          PlasmidFinder v2.1 (web)
#          MobileElementFinder v1.0.3 (web)
#          Proksee (web) — circular genome maps
# Paper  : Lee et al. (2023), Methods 2.6
# Input  : Assembled contigs (contigs.fasta) — 19 WGS strains
# Output : Virulence profiles (Fig. 3), plasmid types,
#          MGE tables (Supp. S4), circular maps (Fig. 4)
# ============================================================

# ── VFanalyzer / VFDB ─────────────────────────────────────────
# URL       : http://www.mgc.ac.cn/cgi-bin/VFs/v5/main.cgi
# Database  : VFDB (Liu et al., 2019)
# Threshold : 80% identity (Methods 2.6)
# Output    : → Supp. Table S3, Figure 3
# Results   : >250 virulence genes identified across 19 strains
echo "VFanalyzer: http://www.mgc.ac.cn/cgi-bin/VFs/v5/main.cgi"
echo "  Threshold: 80% identity"

# ── PlasmidFinder v2.1 ────────────────────────────────────────
# URL       : https://cge.cbs.dtu.dk/services/PlasmidFinder/
# Threshold : 80% identity (Methods 2.6)
# Key result: IncQ1 plasmid detected in A. rivipollensis A539
#             carrying qnrS2 (quinolone resistance)
echo ""
echo "PlasmidFinder v2.1: https://cge.cbs.dtu.dk/services/PlasmidFinder/"
echo "  Threshold: 80% identity"
echo "  Key finding: IncQ1 plasmid in A539 carrying qnrS2"

# ── MobileElementFinder v1.0.3 ────────────────────────────────
# URL       : https://cge.cbs.dtu.dk/services/MobileElementFinder/
# Settings  : Default (minimum sequence identity 90%)
# Output    : → Supp. Table S4
# Key results:
#   SU4  — 21 IS elements (highest burden) + Tn521 + Class I integron
#   A539 — composite transposon + IS elements
echo ""
echo "MobileElementFinder v1.0.3: https://cge.cbs.dtu.dk/services/MobileElementFinder/"
echo "  Settings: default, minimum identity 90%"
echo "  Key finding: Tn521 + IntI1 co-localization in A. caviae SU4"

# ── Proksee — circular genome maps ────────────────────────────
# URL    : https://proksee.ca/
# Input  : GenBank format from NCBI PGAP annotation
# Output : Figure 4A (A539 chromosome + IncQ1 plasmid)
#          Figure 4B (SU4 chromosome — Tn521 + IntI1 + AMR cluster)
echo ""
echo "Proksee: https://proksee.ca/ (web only)"
echo "  Input: GenBank files from NCBI PGAP annotation"
echo "  Output: Figure 4A (A539) and Figure 4B (SU4)"
