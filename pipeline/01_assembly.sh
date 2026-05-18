#!/bin/bash
# ============================================================
# 01_assembly.sh — Read QC, trimming, and genome assembly
# ------------------------------------------------------------
# Tools  : BBDuk (BBTools), SPAdes v3.15.4
# Paper  : Lee et al. (2023), Front. Microbiol. 14:1175304
#          Methods section 2.4
# Input  : Paired-end Illumina reads (*_R1_001.fastq.gz,
#          *_R2_001.fastq.gz), 2×300 bp MiSeq chemistry
# Output : Assembled contigs (contigs.fasta) per isolate
# ============================================================

# ── Usage ────────────────────────────────────────────────────
# bash 01_assembly.sh <sample_name>
# Example: bash 01_assembly.sh A539

SAMPLE=$1
R1="${SAMPLE}_L001_R1_001.fastq.gz"
R2="${SAMPLE}_L001_R2_001.fastq.gz"

echo "Processing sample: $SAMPLE"

# ── Step 1a: Adapter trimming (left adapter) ─────────────────
# ktrim=l  : trim from left end
# k=28     : k-mer length for adapter matching
# mink=13  : minimum k-mer length at end of read
# hdist=1  : allow 1 mismatch in adapter k-mer
# tbo      : trim adapters based on pair overlap
# tpe      : trim both reads to same length when adapter found
bbduk.sh \
    -Xmx1g \
    in1="${R1}" \
    in2="${R2}" \
    out1=lclean1.fastq \
    out2=lclean2.fastq \
    ref=adapters \
    ktrim=l \
    k=28 \
    mink=13 \
    hdist=1 \
    overwrite=true \
    tbo tpe

# ── Step 1b: Quality trimming ─────────────────────────────────
# qtrim=rl : trim both ends
# trimq=30 : minimum quality score Q30
bbduk.sh \
    -Xmx1g \
    in1=lclean1.fastq \
    in2=lclean2.fastq \
    out1=trim1.fastq \
    out2=trim2.fastq \
    qtrim=rl \
    trimq=30

# ── Step 2: Genome assembly ───────────────────────────────────
# --careful        : reduces mismatches and indels (MiSeq data)
# --only-assembler : skip read error correction (already trimmed)
# --cov-cutoff auto: automatically remove low-coverage contigs
spades.py \
    -1 trim1.fastq \
    -2 trim2.fastq \
    --careful \
    --only-assembler \
    --cov-cutoff auto \
    -o "${SAMPLE}_assembled"

echo "Assembly complete: ${SAMPLE}_assembled/contigs.fasta"

# ── Clean up intermediate files ───────────────────────────────
rm -f lclean1.fastq lclean2.fastq trim1.fastq trim2.fastq

# ============================================================
# !! 확인 필요 !!
# ------------------------------------------------------------
# BBDuk adapter trimming 방향 (ktrim=l vs ktrim=r):
#
# 현재 코드는 ktrim=l (left trimming, 5' 어댑터 제거)을 사용하나,
# BBDuk 공식 문서 및 대부분의 Illumina paired-end 실사용 사례는
# ktrim=r (right trimming, 3' 어댑터 제거)을 표준으로 권장합니다.
#   - BBDuk 공식: ktrim=r k=23 mink=11
#   - 현재 코드:  ktrim=l k=28 mink=13
#
# 논문에 "Nextera DNA Flex Library Prep kit (Illumina)"가 명시되어
# 있습니다. Nextera Flex 라이브러리의 어댑터 방향에 따라 ktrim=l이
# 맞을 수도 있으나, 실제 당시 분석에서 의도한 방향이 맞는지 확인이
# 필요합니다. k=28, mink=13 값도 표준(k=23, mink=11)과 다릅니다.
# ============================================================
