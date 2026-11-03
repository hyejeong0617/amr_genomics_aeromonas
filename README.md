# 🧬 AMR Genomics — *Aeromonas* spp. in Ready-to-Eat Seafood

### *Whole-genome sequencing · Antimicrobial resistance · Virulence factors · Peer-reviewed publication*

[![Publication](https://img.shields.io/badge/DOI-10.3389%2Ffmicb.2023.1175304-blue)](https://doi.org/10.3389/fmicb.2023.1175304)
[![NCBI BioProject](https://img.shields.io/badge/NCBI-PRJNA877469-green)](https://www.ncbi.nlm.nih.gov/bioproject/PRJNA877469)
[![Python](https://img.shields.io/badge/Python-3.10+-3776AB?logo=python&logoColor=white)](https://python.org)
[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://amrgenomicsaeromonas.streamlit.app/)
[![Journal](https://img.shields.io/badge/Frontiers%20in%20Microbiology-2023-orange)](https://www.frontiersin.org/articles/10.3389/fmicb.2023.1175304)

---

> **Lee H-J, et al. (2023)**. Whole genome sequence analysis of *Aeromonas* spp. isolated from ready-to-eat seafood: antimicrobial resistance and virulence factors. *Frontiers in Microbiology*, 14:1175304.

Published research on *Aeromonas* from ready-to-eat seafood and a salmon processing environment, accompanied by later Python analyses and a Streamlit explorer. The paper is the historical research record; repository scripts and exploratory extensions are not proof of a freshly reproduced research pipeline.

---

## 🖥️ Streamlit Application

[![Open in Streamlit](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://amrgenomicsaeromonas.streamlit.app/)

**Live app →** [amrgenomicsaeromonas.streamlit.app](https://amrgenomicsaeromonas.streamlit.app/)

The saved dashboard preview is historical and is not displayed while public-facing corrections are pending deployment.

An interactive 4-page data explorer for the WGS dataset: the research story, species distribution + ANI heatmap, AMR gene profiles (phenotypic + genotypic), and MGE co-localisation case studies.

---

## 📌 Overview

This observational genomics study characterises species diversity, AMR and virulence-associated features in a selected isolate collection. It provides scientific context for One Health surveillance, not a population prevalence estimate, consumer risk assessment, regulatory endorsement or demonstration of transmission to humans.

| Capability | What this project demonstrates |
|---|---|
| **Domain knowledge → analysis design** | AMR gene interpretation, MGE co-localisation logic, and ANI species boundary decisions all derived from microbiology domain expertise |
| **Bioinformatics pipeline** | Documentation of WGS methods and illustrative commands; manual steps and historical parameters are not fully verified |
| **Python analysis** | Five notebooks containing data preparation, Python re-visualizations and exploratory extensions; saved outputs are historical, not fresh reproducibility evidence |
| **Scientific communication** | Peer-reviewed publication; findings linked to EU food safety regulatory context |

> **Press coverage:** [Nautilus Magazine](https://nautil.us/is-sushi-a-health-hazard-421668) · [IFLScience](https://www.iflscience.com/how-safe-is-the-sushi-you-eat-really-70899)

---

## 🔬 Key Findings

| Dimension | Finding |
|---|---|
| **Species diversity** | 8 *Aeromonas* species identified across 22 isolates — MLPA + ANI (≥96% cutoff) |
| **AMR burden** | **57.0% (45/79)** after corrected nine-category, R-only study-operational reclassification; all original labels agree. The paper reports approximately 58% |
| **Virulence** | >250 virulence genes characterised via VFDB; species-specific profiles resolved |
| **Plasmid-associated resistance gene** | *qnrS2* (quinolone resistance) on IncQ1 plasmid in *A. rivipollensis* A539 |
| **Co-selection signal** | The paper reports Tn521 + Class I integron co-localisation in *A. caviae* SU4-2. The author confirmed Tn521, correcting the preserved S4 spelling Tn512 in derived labels. Co-selection remains a hypothesis, not experimentally demonstrated |
| **Public data** | All 22 genome assemblies deposited at NCBI: [PRJNA877469](https://www.ncbi.nlm.nih.gov/bioproject/PRJNA877469) |

---

> MDR correction note: corrected nine-category, R-only study-operational classification confirms 45/79 records (57.0%), matching all 79 original source labels. AMP is included and intermediate results are excluded; this is not a validated acquired-resistance clinical classification. The published article reports approximately 58%, preserved as historical wording rather than a computational target. A publication calculation/rounding error is the author's proposed explanation; the original calculation has not been reconstructed. See DATA_CORRECTIONS.md for the record-level comparison and definition.

## 🗂️ Repository Structure

```
amr_genomics_aeromonas/
│
├── assets/
│   └── dashboard_preview.png      # Dashboard screenshot (README preview)
│
├── pipeline/                      # Upstream WGS analysis — documented bash scripts
│   ├── 01_assembly.sh             # Read QC (BBDuk) + assembly (SPAdes v3.15.4)
│   ├── 02_annotation.sh           # NCBI PGAP annotation (web submission)
│   ├── 03_mlpa.sh                 # Species ID: BLAST+ + MEGA11 (MLPA, NJ/ML trees)
│   ├── 04_ani.sh                  # ANI: FastANI + ANIclustermap
│   ├── 05_amr_profiling.sh        # AMR genes: AMRFinderPlus v3.10.45 + ResFinder v4.1
│   ├── 06_virulence_mge.sh        # Virulence (VFDB), plasmids, MGEs, genome maps
│   ├── 07_abricate.sh             # Optional multi-database screening (historical use unverified) (Abricate)
│   └── README_pipeline.md         # Tool versions, environment setup, web tool URLs
│
├── analysis/                      # Later Python analyses — environment and limitations documented
│   ├── 00_data_prep.ipynb         # Supplementary tables → clean DataFrames
│   ├── 01_species_id.ipynb        # ANI heatmap + species boundary validation (Fig. 2)
│   ├── 02_amr_profiling.ipynb     # Phenotypic + genotypic AMR; concordance analysis
│   ├── 03_virulence_analysis.ipynb# Virulence factor heatmap + species comparison (Fig. 3)
│   └── 04_mge_amr_colocalization.ipynb  # MGE burden + AMR co-occurrence network (Fig. 4)
│
├── data/
│   ├── raw/                       # Supplementary tables (S1–S4) + pipeline outputs
│   │                              # Genome assemblies: download from NCBI PRJNA877469
│   └── processed/                 # Clean CSVs + figures generated by notebooks (committed)
│
├── streamlit_app.py               # Interactive data explorer
├── requirements.txt
└── README.md
```

---

## ⚙️ WGS Pipeline

Raw Illumina paired-end reads (2×300 bp MiSeq, 22 isolates) → assembled genomes → annotated → species-resolved → AMR + virulence characterised.

```
Raw Illumina reads (2×300 bp MiSeq)
        │
        ▼
01_assembly.sh         BBDuk (adapter/quality trimming) + SPAdes v3.15.4
        │               → contigs.fasta (22 assemblies)
        ▼
02_annotation.sh       NCBI PGAP (web submission)
        │               → annotated GenBank files → deposited to NCBI
        ▼
03_mlpa.sh             BLAST+ + MEGA11 v11.0.10
        │               → MLPA tree (6 housekeeping genes, 4,172 bp)
        │               → NJ + ML, 1,000 / 100 bootstrap replicates
        ▼
04_ani.sh              FastANI + ANIclustermap
        │               → ANI matrix (30×30) + clustered heatmap
        │               → 19 representative strains selected (ANI < 99.9%)
        ▼
05_amr_profiling.sh    AMRFinderPlus v3.10.45 + ResFinder v4.1 (web)
        │               → AMR gene profiles (Table 1, Supp. S2)
        ▼
06_virulence_mge.sh    VFanalyzer/VFDB · PlasmidFinder v2.1
        │               MobileElementFinder v1.0.3 · Proksee
        │               → Virulence profiles · plasmid types · MGE tables
        ▼
07_abricate.sh         Optional multi-database screening (historical use unverified)
                        VFDB · NCBI · ResFinder · PlasmidFinder · CARD · ARG-ANNOT
```

---

## 📊 Analysis Notebooks

The publication contains the original research figures. Notebook 01 re-visualizes supplied ANI values; notebook 02 manually encodes Table 1 and summarizes supplied phenotype labels. Notebook 03 uses an expanded VF matrix and is not an exact Figure 3 reproduction. Notebook 04 contains conceptual schematics inspired by Figure 4, not verified sequence-coordinate maps. Figure 1 is not reconstructed here.

**Exploratory concordance:** notebook 02 compares manually specified strain-level rules with the same collection, treating intermediate observations as non-resistant. Rules have unverified exceptions and no independent validation. Agreement is not predictive accuracy and should not be used as a portfolio performance headline.

**Phase 2 corrections (2026-11-03):** composite isolate matching (E02), reference classification (E03), and study-operational MDR recalculation (E11) are validated. E07 now has 22 unique NCBI-verified assembly mappings, including four author-confirmed aliases. E08 separates SU4’s 16 distinct IS/MITE entries from 21 table-derived copies and one separate Tn521 transposon. Only the SU4 numerical display is restored; other-strain comparisons and conceptual schematics remain hidden. No genomic-coordinate validation is claimed. See [DATA_CORRECTIONS.md](DATA_CORRECTIONS.md) for exact scope, validation, limitations and figure provenance. Original derived files are archived in `data/historical/pre_phase2_outputs.zip`; notebook inline outputs remain historical, while corrected CSVs/PNGs are current.

| Notebook | Relationship to publication | Extended Analysis |
|---|---|---|
| `00_data_prep.ipynb` | — | Parses supplementary tables (S1–S4), ANI matrix, and VF heatmap source into 14 clean DataFrames in `data/processed/` |
| `01_species_id.ipynb` | ANI re-visualization related to Figure 2 | Interactive Plotly heatmap; species boundary validation (ANI ≥ 96%); strain overview → `strain_summary.csv` |
| `02_amr_profiling.ipynb` | Manual Table 1 encoding; supplied S2 labels | MDR distribution by species; species × antibiotic resistance heatmap; **genotype–phenotype concordance scoring** for 19 WGS strains |
| `03_virulence_analysis.ipynb` | Expanded VF analysis; 22 isolates + 7 explicitly classified references | Interactive heatmap; virulence score per strain → `virulence_scores.csv`; species-level VF category prevalence |
| `04_mge_amr_colocalization.ipynb` | Conceptual Figure 4-inspired schematics; IS5 classified consistently; SU4 IS/MITE counts reconciled at source-table level | IS family × strain distribution heatmap; **AMR gene co-occurrence network** (Jaccard); IS element burden ranking |

All notebooks include cell-level comments linking code decisions to the published Methods section.

**Notebook execution order:**

```
00_data_prep.ipynb
    → data/processed/*.csv (required by all downstream notebooks)

01_species_id.ipynb
02_amr_profiling.ipynb        ← downstream notebooks use processed and/or raw files
03_virulence_analysis.ipynb
04_mge_amr_colocalization.ipynb
```

---


### Phase 1 validation record — 2026-11-03

Read-only inspection of `data/raw/Table_2.XLSX`, sheet `Table_S2`, found 79 data records with isolate IDs (column C) and 45 MDR labels equal to 1 (column T). All labels matched `data/processed/amr_phenotype_wide.csv` using source, year, isolate ID and species together. The verified arithmetic is 56.9620253164557%, or 57.0% to one decimal place. At Phase 1 this was a source-label check only. The subsequent E11 reclassification is documented above and in DATA_CORRECTIONS.md.

Lightweight validation: Python syntax and all four Streamlit pages passed local AppTest checks. Data, saved figures, notebook code/output cells and pipeline executable commands were preserved. No full notebook run, clean dependency installation, upstream pipeline execution or deployment was performed.

## 🧰 Tech Stack

| Layer | Tools |
|---|---|
| **Language** | Python 3.10+ · R (original statistical analysis) |
| **Data wrangling** | pandas · numpy |
| **Visualisation (notebooks)** | matplotlib · seaborn · plotly |
| **Dashboard** | Streamlit |
| **Bioinformatics (pipeline)** | BBTools · SPAdes · BLAST+ · MEGA11 · FastANI · ANIclustermap · AMRFinderPlus · Abricate |
| **Web-based tools** | ResFinder v4.1 · VFanalyzer/VFDB · PlasmidFinder v2.1 · MobileElementFinder v1.0.3 · Proksee |

---

## ▶️ Setup and Run

```bash
# Clone the repository
git clone https://github.com/hyejeong0617/amr_genomics_aeromonas.git
cd amr_genomics_aeromonas

# Install Python dependencies
pip install -r requirements.txt

# Launch the interactive explorer
streamlit run streamlit_app.py
```

**Optional notebook environment** (Python 3.10+):

```bash
python -m pip install -r requirements-analysis.txt
cd analysis
python -m jupyterlab
```

Open notebooks from `analysis/` so relative paths resolve. Install dependencies before use; the requirements are not a locked historical environment. No clean-environment installation or full notebook execution is claimed. Notebooks write derived files when executed; do not run all notebooks merely to launch the dashboard.

**Bioinformatics tools** (documented versions/examples, not an automatic installation recipe for reproducing history):

| Tool | Version | Install |
|---|---|---|
| BBTools (BBDuk) | latest | `conda install -c bioconda bbtools` |
| SPAdes | v3.15.4 | `conda install -c bioconda spades` |
| BLAST+ | latest | `conda install -c bioconda blast` |
| MEGA | v11.0.10 | [megasoftware.net](https://www.megasoftware.net/) |
| FastANI | latest | `conda install -c bioconda fastani` |
| ANIclustermap | latest | `pip install ANIclustermap` |
| AMRFinderPlus | v3.10.45 | `conda install -c bioconda ncbi-amrfinderplus` |
| Abricate | latest | `conda create -n abricate abricate` (bioconda) |

Steps 05–06 also use web-based tools. URLs and thresholds are documented in `pipeline/README_pipeline.md`.

Historical execution of these exact repository scripts, the HPC environment and internal Abricate/Kraken2 checks is not independently evidenced here. See pipeline documentation for manual steps and unresolved parameters.

---

## 📂 Data Access

All genome assemblies are publicly available at NCBI.

| Resource | Link |
|---|---|
| NCBI BioProject | [PRJNA877469](https://www.ncbi.nlm.nih.gov/bioproject/PRJNA877469) |
| Genome accessions | JAOPLB000000000 – JAOPLW000000000 (22 assemblies) |
| Supplementary tables | [Paper DOI](https://doi.org/10.3389/fmicb.2023.1175304) (open access) |

```bash
# Download annotated assemblies via NCBI Datasets CLI
# conda install -c conda-forge ncbi-datasets-cli
datasets download genome accession JAOPLB000000000 JAOPLC000000000 \
    --include gbff,gff3,sequence \
    --filename aeromonas_genomes.zip
```

> **Note:** Committed processed files support dashboard use; notebooks also read supplied raw tables. Dependencies are still required. The download example retrieves only two assemblies, not raw sequencing reads or the complete pipeline inputs. Full upstream reconstruction is outside this repository correction scope.

---

## 🔗 Related Projects

| Project | Domain | Type | Status |
|---|---|---|---|
| [rasff_risk_predictor](https://github.com/hyejeong0617/rasff_risk_predictor) | EU regulatory notifications | ML pipeline · NLP · Streamlit | ✅ Live |
| [foodborne_outbreaks_eda](https://github.com/hyejeong0617/foodborne_outbreaks_eda) | Food safety surveillance | EDA · SQL · entity normalisation · Streamlit | ✅ Live |
| [aeromonas-growth-predictor](https://github.com/hyejeong0617/aeromonas-growth-predictor) | Predictive microbiology · food safety | ML · GPR · SHAP · Streamlit | ✅ Live |
| **This repo** | Microbial genomics · One Health | WGS pipeline · Python analysis · Streamlit | ✅ Live |

**The four projects form a connected portfolio** — analysing food safety risk at four scales: real-time EU regulatory signal (RASFF ML), population-level surveillance (foodborne EDA), growth kinetics modelling (Aeromonas predictor), and molecular genomics (this repo).

---

## 📄 Citation

```bibtex
@article{lee2023aeromonas,
  author  = {Lee, Hye-Jeong and others},
  title   = {Whole genome sequence analysis of {Aeromonas} spp. isolated from
             ready-to-eat seafood: antimicrobial resistance and virulence factors},
  journal = {Frontiers in Microbiology},
  volume  = {14},
  pages   = {1175304},
  year    = {2023},
  doi     = {10.3389/fmicb.2023.1175304}
}
```

---

## 📬 Contact

**Hyejeong Lee** — PhD · Food Microbiology & Data Science

[![LinkedIn](https://img.shields.io/badge/LinkedIn-Hyejeong%20Lee-0077B5?logo=linkedin&logoColor=white)](https://www.linkedin.com/in/hyejeong-lee-75887465/)
[![GitHub](https://img.shields.io/badge/GitHub-hyejeong0617-181717?logo=github&logoColor=white)](https://github.com/hyejeong0617)

*Open to Domain Data Scientist / Regulatory Data Analyst roles in food safety, pharma, and biotech — Remote / Hybrid · Germany-based.*
