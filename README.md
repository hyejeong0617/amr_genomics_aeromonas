# AMR Genomics | Seafood-Associated *Aeromonas*

**Whole-genome sequencing · Antimicrobial resistance · Bioinformatics · Scientific data analysis**

[![Publication](https://img.shields.io/badge/Peer--reviewed-Frontiers%20in%20Microbiology-blue)](https://doi.org/10.3389/fmicb.2023.1175304)
[![NCBI BioProject](https://img.shields.io/badge/NCBI-PRJNA877469-green)](https://www.ncbi.nlm.nih.gov/bioproject/PRJNA877469)
[![Live Demo](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://amrgenomicsaeromonas.streamlit.app/)

**[Explore the interactive dashboard](https://amrgenomicsaeromonas.streamlit.app/)** · **[Read the publication](https://doi.org/10.3389/fmicb.2023.1175304)** · **[View public genome data](https://www.ncbi.nlm.nih.gov/bioproject/PRJNA877469)**

## Project overview

How can whole-genome sequencing and antimicrobial susceptibility data reveal species diversity, resistance patterns, and mobile genetic elements in food-associated bacteria?

This project connects **peer-reviewed research on *Aeromonas*** from ready-to-eat seafood and a salmon-processing environment with subsequent Python analyses and a four-page Streamlit data explorer. It illustrates the transition from microbiological research to traceable, interactive scientific data analysis while distinguishing published results from later exploratory work.

| Study scope | Verified evidence |
|---|---|
| **79** phenotyped isolate records | **15** antibiotics; **1,185** susceptibility observations |
| **22** sequenced isolates | **8** *Aeromonas* species; **22** verified NCBI assembly mappings |
| **19** representative isolates | Published downstream genomic analysis subset |
| **57.0% (45/79)** study-operational MDR | Recalculated using the corrected nine-category, R-only study rule; matches all original MDR labels |

*These findings describe a selected isolate collection, not population-level resistance prevalence, demonstrated consumer risk, or independently validated clinical predictions.*

## Interactive dashboard

**[Launch the Streamlit explorer](https://amrgenomicsaeromonas.streamlit.app/)**

The dashboard makes the published dataset more accessible through four sections:

1. **The Story:** research context, study design and interpretation boundaries.
2. **The Bacteria:** species identification, isolate overview and ANI exploration.
3. **Antibiotic Resistance:** phenotype/genotype summaries, resistance patterns and strain-level selection.
4. **How Resistance Spreads:** supported mobile-element observations and a carefully qualified SU4 case study. The title denotes the research question, **not proof of observed transmission**.

Verified SU4 results distinguish **15 IS entries**, **one MITEAeme1 entry with six copies**, and **one separate Tn521 transposon**. In total, the original supplementary table supports **16 distinct IS/MITE entries and 21 table-derived copies**, not a verified recount of 21 independent genomic loci. Other-isolate quantitative MGE comparisons and speculative genomic-coordinate schematics are not shown.

The application uses committed processed tables and figures. It does not require rerunning the historical WGS workflow to explore the saved data.

## Key scientific findings

- **Species diversity:** MLPA and average nucleotide identity (ANI) supported identification across eight *Aeromonas* species among 22 sequenced isolates.
- **Resistance phenotype:** 45 of 79 records meet the repository's study-specific MDR rule (57.0%), using resistance in at least three of nine antibiotic categories. Intermediate observations are excluded. The publication reports approximately 58%; its original calculation has not been reconstructed.
- **AMR and mobile elements:** the study reports a plasmid-associated *qnrS2* resistance gene in *A. rivipollensis* A539 and investigates genetic contexts of resistance-associated elements. Presence or co-localisation is **not direct evidence of horizontal transfer or human infection**.
- **SU4 case study:** supplementary Table S4 supports 15 IS entries plus six copies of MITEAeme1. Tn521 is a **separate** transposon; its name corrects the preserved Tn512 typographical entry in the source table.
- **Public research data:** 22 genome assemblies can be traced through [NCBI BioProject PRJNA877469](https://www.ncbi.nlm.nih.gov/bioproject/PRJNA877469).

Detailed definitions, source-level checks and figure provenance: **[DATA_CORRECTIONS.md](DATA_CORRECTIONS.md)**.

## Research and project contributions

**Original published research (PhD):** The publication credits Hye-Jeong Lee with **methodology, bioinformatics analysis, manuscript preparation, editing and submission**. This was collaborative academic research; the repository does not imply sole ownership of every experiment, pipeline stage or analysis. See the [paper's Author Contributions](https://www.frontiersin.org/journals/microbiology/articles/10.3389/fmicb.2023.1175304/full).

**Subsequent data exploration:** The repository contains five Python notebooks and a Streamlit interface that organise published/supplementary evidence into accessible tables, figures and interactive views. These additions are distinct from the original peer-reviewed analyses and are not a claim to have reproduced the entire historical WGS pipeline.

**Quality and provenance work (2026):** Targeted corrections to isolate identity matching, reference-strain classification, antibiotic category mapping, accession aliases and SU4 MGE counts were completed with AI-assisted coding and source checks. The original raw workbooks and historical derived outputs were preserved. Contributions to earlier Python/Streamlit implementation are not assigned to an individual where independent attribution is unavailable.

## Methods and technologies

| Area | Methods / tools |
|---|---|
| **Microbial genomics (published study)** | WGS, assembly and annotation, MLPA, ANI, AMR/virulence-associated gene screening, mobile genetic element interpretation |
| **Bioinformatics** | SPAdes, PGAP, MEGA, FastANI, AMRFinderPlus, ResFinder, VFDB, PlasmidFinder, MobileElementFinder, Proksee (see published Methods and [pipeline notes](pipeline/README_pipeline.md)) |
| **Python analysis and visualisation** | Python, pandas, NumPy, matplotlib, seaborn, SciPy, Plotly, Jupyter |
| **Interactive delivery** | Streamlit |

The `pipeline/` scripts illustrate related procedures and manual steps; they are **not a fully validated executable reconstruction of the original PhD workflow**.

## Repository guide

| Path | Contents |
|---|---|
| [`analysis/00_data_prep.ipynb`](analysis/00_data_prep.ipynb) | Supplementary-table preparation and derived tables |
| [`analysis/01_species_id.ipynb`](analysis/01_species_id.ipynb) | Species/ANI re-visualisation and verified accession mapping |
| [`analysis/02_amr_profiling.ipynb`](analysis/02_amr_profiling.ipynb) | Phenotypic and genotypic AMR summaries; exploratory concordance |
| [`analysis/03_virulence_analysis.ipynb`](analysis/03_virulence_analysis.ipynb) | Extended virulence-factor matrix: 22 isolates + 7 references |
| [`analysis/04_mge_amr_colocalization.ipynb`](analysis/04_mge_amr_colocalization.ipynb) | IS/MGE exploration, source-based SU4 reconciliation and conceptual case diagrams |
| [`pipeline/`](pipeline/) | Historical method documentation and illustrative scripts |
| [`data/processed/`](data/processed/) | Committed data tables and selected figures for the explorer |
| [`data/historical/`](data/historical/) | Preserved pre-correction derived outputs |
| [`streamlit_app.py`](streamlit_app.py) | Four-page interactive application |
| [`DATA_CORRECTIONS.md`](DATA_CORRECTIONS.md) | Source reconciliation, validation results, limitations and figure provenance |

**Figure provenance:** Paper figures, later Python re-visualisations, expanded analyses and conceptual diagrams are distinct. Notebooks may contain historical inline outputs; rely on dated correction documentation and current processed datasets for corrected values.

## Run the app locally

Requires Python 3.10+.

```bash
git clone https://github.com/hyejeong0617/amr_genomics_aeromonas.git
cd amr_genomics_aeromonas
python -m pip install -r requirements.txt
streamlit run streamlit_app.py
```

For optional notebook work, install `requirements-analysis.txt` and launch Jupyter from `analysis/`:

```bash
python -m pip install -r requirements-analysis.txt
cd analysis
python -m jupyterlab
```

The dependencies are not a locked historical environment. A clean-room install, complete notebook rerun and complete WGS reconstruction were **not** included in the final QA. Notebook execution may regenerate derived outputs and is unnecessary to launch the dashboard.

## Scientific interpretation and limitations

- **Study scope:** observational, selected and potentially related isolates; findings do not establish general population prevalence or consumer risk.
- **MDR definition:** repository value 45/79 (57.0%) uses a nine-category, R-only study rule (AMP included, intermediate excluded). It is **not** independently validated as an acquired-resistance clinical classification.
- **Genotype–phenotype concordance:** manual exploratory agreement within the same collection, **not** independent predictive accuracy.
- **Virulence and transmission:** gene presence does not prove expression, pathogenicity, disease or horizontal transmission.
- **MGE counts:** SU4 counts are derived from source-table notation; genome positions, overlapping features and other-isolate copy numbers have not been revalidated.
- **Reproducibility:** saved notebooks and illustrative scripts do not demonstrate a fresh execution of the original publication workflow.

For the detailed audit trail, see [DATA_CORRECTIONS.md](DATA_CORRECTIONS.md).

## Publication and data

**Lee H-J, et al. (2023).** *Whole genome sequence analysis of Aeromonas spp. isolated from ready-to-eat seafood: antimicrobial resistance and virulence factors.* **Frontiers in Microbiology**, 14, 1175304. [DOI: 10.3389/fmicb.2023.1175304](https://doi.org/10.3389/fmicb.2023.1175304).

- [Full text](https://www.frontiersin.org/journals/microbiology/articles/10.3389/fmicb.2023.1175304/full) and supplementary tables
- [NCBI BioProject PRJNA877469](https://www.ncbi.nlm.nih.gov/bioproject/PRJNA877469) — 22 publicly deposited assemblies
- Selected press coverage: [Nautilus](https://nautil.us/is-sushi-a-health-hazard-421668) · [IFLScience](https://www.iflscience.com/how-safe-is-the-sushi-you-eat-really-70899)

## Related portfolio projects

- [RASFF Risk Predictor](https://github.com/hyejeong0617/rasff_risk_predictor) — EU food safety alerts and machine learning
- [Foodborne Outbreaks EDA](https://github.com/hyejeong0617/foodborne_outbreaks_eda) — SQL and outbreak surveillance
- [Aeromonas Growth Predictor](https://github.com/hyejeong0617/aeromonas-growth-predictor) — predictive microbiology

---

**Scientific data science for food safety, microbiology and applied AI**

[GitHub profile](https://github.com/hyejeong0617) · [LinkedIn](https://www.linkedin.com/in/hyejeong-lee-75887465/)
