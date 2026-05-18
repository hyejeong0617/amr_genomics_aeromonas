# Bioinformatics Pipeline

This directory documents the upstream WGS analysis pipeline used in:

> Lee H-J et al. (2023) *Whole genome sequence analysis of Aeromonas spp. isolated from ready-to-eat seafood: antimicrobial resistance and virulence factors.*  
> **Frontiers in Microbiology** 14:1175304. doi: [10.3389/fmicb.2023.1175304](https://doi.org/10.3389/fmicb.2023.1175304)

All 22 genome assemblies are publicly available at NCBI:  
**BioProject:** [PRJNA877469](https://www.ncbi.nlm.nih.gov/bioproject/PRJNA877469)  
**Accessions:** JAOPLB000000000 – JAOPLW000000000

---

## Pipeline overview

```
Raw Illumina reads (2×300 bp MiSeq)
        │
        ▼
01_assembly.sh       BBDuk + SPAdes v3.15.4
        │             → contigs.fasta (22 genomes)
        ▼
02_annotation.sh     NCBI PGAP
        │             → annotated GenBank files (deposited to NCBI)
        ▼
03_mlpa.sh           BLAST+ + MEGA11 v11.0.10
        │             → MLPA tree, species identification (Fig. 1)
        ▼
04_ani.sh            FastANI + ANIclustermap
        │             → ANI matrix + heatmap (Fig. 2)
        │             → 19 representative strains selected
        ▼
05_amr_profiling.sh  AMRFinderPlus v3.10.45
        │             ResFinder v4.1 (web)
        │             → AMR gene profiles (Table 1, Supp. S2)
        ▼
06_virulence_mge.sh  VFanalyzer/VFDB (web) + PlasmidFinder v2.1 (web)
        │             MobileElementFinder v1.0.3 (web) + Proksee (web)
        │             → Virulence profiles (Fig. 3, Supp. S3)
        │             → MGE profiles (Fig. 4, Supp. S4)
        ▼
07_abricate.sh       Abricate — multi-database cross-validation
                      VFDB · NCBI · ResFinder · PlasmidFinder · CARD
                      → cross-check of AMR/virulence gene calls
```

---

## Environment requirements

| Tool | Version | Installation |
|---|---|---|
| BBTools (BBDuk) | latest | `conda install -c bioconda bbtools` |
| SPAdes | v3.15.4 | `conda install -c bioconda spades` |
| NCBI PGAP | latest | [github.com/ncbi/pgap](https://github.com/ncbi/pgap) |
| BLAST+ | latest | `conda install -c bioconda blast` |
| MEGA | v11.0.10 | [megasoftware.net](https://www.megasoftware.net/) |
| FastANI | latest | `conda install -c bioconda fastani` |
| ANIclustermap | latest | `pip install ANIclustermap` |
| AMRFinderPlus | v3.10.45 | `conda install -c bioconda ncbi-amrfinderplus` |
| Abricate | latest | `conda create -n abricate abricate` (bioconda) |

> **HPC environment:** Scripts were run on a Linux HPC cluster (NTNU, Norway).  
> Conda environments were used to manage tool dependencies.

---

## Web-based tools (steps 05–06)

Steps 05 and 06 include tools that were used via web interfaces.

| Tool | URL | Threshold used |
|---|---|---|
| ResFinder v4.1 | [cge.cbs.dtu.dk/services/ResFinder](https://cge.cbs.dtu.dk/services/ResFinder/) | 90% identity (default) |
| VFanalyzer / VFDB | [mgc.ac.cn/VFs](http://www.mgc.ac.cn/cgi-bin/VFs/v5/main.cgi) | 80% identity |
| PlasmidFinder v2.1 | [cge.cbs.dtu.dk/services/PlasmidFinder](https://cge.cbs.dtu.dk/services/PlasmidFinder/) | 80% identity |
| MobileElementFinder v1.0.3 | [cge.cbs.dtu.dk/services/MobileElementFinder](https://cge.cbs.dtu.dk/services/MobileElementFinder/) | 90% identity (default) |
| Proksee | [proksee.ca](https://proksee.ca/) | — |

---

## Note on Abricate (step 07)

Abricate was used as a **cross-validation tool** to verify AMR and virulence gene calls from the primary tools (AMRFinderPlus, ResFinder, VFanalyzer). It was not reported as a primary analysis tool in the paper, but provides a convenient way to screen against multiple databases (VFDB, NCBI, ResFinder, PlasmidFinder, CARD, ARG-ANNOT) in a single command-line run. Results were used to confirm consistency across databases.

---

## Note on Kraken2

Kraken2 was used internally as a **QC step** to verify taxonomic purity of assemblies. It is not described in the published Methods because final species identification was based on MLPA + ANI (Methods 2.2 and 2.5), which provide higher phylogenetic resolution for *Aeromonas* species boundaries.

---

## Downstream analysis

All downstream statistical analysis and visualisation are in `/analysis/`:

| Notebook | Content |
|---|---|
| `00_data_prep.ipynb` | Raw supplementary data → processed DataFrames |
| `01_species_id.ipynb` | ANI heatmap, species boundary validation |
| `02_amr_profiling.ipynb` | Phenotypic + genotypic AMR, concordance analysis |
| `03_virulence_analysis.ipynb` | Virulence factor profiles, species comparison |
| `04_mge_amr_colocalization.ipynb` | MGE burden, case studies, co-occurrence |
