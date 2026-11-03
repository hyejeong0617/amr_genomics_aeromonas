# Bioinformatics Pipeline

This directory describes published WGS methods and provides illustrative commands related to:

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
07_abricate.sh       Abricate — optional multi-database screening (historical use unverified)
                      VFDB · NCBI · ResFinder · PlasmidFinder · CARD
                      → example outputs; no archived cross-check evidence included
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

> **Provenance limitation:** Execution of these exact scripts, the HPC/Conda environment and database versions has not been independently verified. These are not a tested end-to-end reconstruction. Assembly trimming parameters remain unconfirmed; MLPA requires external references, manual steps and missing settings files. The AMR script lists 21 strains although its header describes 19. Do not infer the historical cohort from that example list.

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

Abricate provides an optional multi-database screening example. It is not reported in the published Methods, and this repository contains no archived outputs establishing its historical use or agreement with the primary tools. Do not describe it as completed validation.

---

## Note on Kraken2

Historical Kraken2 QC use is unconfirmed here; no supporting run outputs are included. Published species identification uses MLPA and ANI.

---

## Downstream analysis

Later Python re-visualizations and exploratory analyses are in `/analysis/`; original R source and full historical execution evidence are not included:

| Notebook | Content |
|---|---|
| `00_data_prep.ipynb` | Raw supplementary data → processed DataFrames |
| `01_species_id.ipynb` | ANI heatmap, species boundary validation |
| `02_amr_profiling.ipynb` | Phenotypic + genotypic AMR, concordance analysis |
| `03_virulence_analysis.ipynb` | Virulence factor profiles, species comparison |
| `04_mge_amr_colocalization.ipynb` | MGE burden, case studies, co-occurrence |
