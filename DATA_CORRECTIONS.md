# Phase 2 data corrections — 2026-11-03

Scope: E02, E03, E11, E07 and E08 only. Raw workbooks and publication files are unchanged. No full notebook, WGS pipeline, training, commit, push or deployment was performed. Phase 1 changes are retained.

## Verified results and limitations

| Issue | Before | Current result |
|---|---|---|
| E02 | ID-only dashboard deduplication: 77 records / 43 MDR labels; reused SU2 and SU12 | Composite key (source, year, isolate ID, normalized species): 79 records / 45 labels. All 19 published-table selections uniquely match 15 phenotype observations. No source records deleted. |
| E03 | 23 isolates + 6 references; GA97_22 treated as isolate | 22 isolates + 7 references using explicit Sheet2 reference membership. Mean category count 13.3043 → 13.1818. All 29 individual category counts unchanged; other species summaries unchanged. Expanded cohort includes near-identical isolates and is not the paper’s 19-representative cohort. |
| E11 | STX grouped as amphenicol; penicillins called generic beta-lactams | Nine mutually exclusive study categories. Record-level R-only recalculation: 45/79 = 56.9620253%, reported 57.0%; zero disagreements with original labels. |
| E07 | Four blank accession matches | Final review: author-confirmed aliases and NCBI PRJNA877469 metadata give 22 unique assembly mappings, each matched to the S1 species and WGS master accession. Analysis IDs remain unchanged. |
| E08 | Prep notebook excluded IS5; IS-only and IS/MITE totals were not distinguished | IS5 normalization retained. Final SU4 reconciliation: 15 single IS entries + one MITE entry with 6 copies = 16 entries / 21 table-derived copies. Tn521 separate. Existing IS-only matrices and burden CSV remain unchanged. No sequence-coordinate recount. |

## E11 definition and source evidence

The study-operational rule is resistance (R) to at least one agent in at least three of the nine categories below. Intermediate (I) is excluded; ampicillin is included. Source S/R/I calls are not reinterpreted against current breakpoints. The original MDR column is preserved, with separate source/recalculated columns in `data/processed/mdr_recalculation.csv`.

| Category | Drugs |
|---|---|
| Penicillins | AMP, MEL |
| Cephalosporins | CTX, CRO |
| Quinolones | CIP, OA |
| Tetracyclines | DO, TE |
| Carbapenems | IPM, MEM |
| Aminoglycosides | GM, TOB |
| Macrolides | EM |
| Amphenicols | FEC |
| Folate pathway inhibitors | STX (trimethoprim/sulfamethoxazole combination) |

Drug grouping uses chemistry/mode of action: [WHO ATC J01](https://atcddd.fhi.no/atc_ddd_index/?code=J01&showdescription=yes), [penicillins J01CA](https://atcddd.fhi.no/atc_ddd_index/?code=J01CA&showdescription=yes), and [sulfonamide/trimethoprim combinations J01EE](https://atcddd.fhi.no/atc_ddd_index/?code=J01EE&showdescription=yes). ATC categories support drug grouping, not validation of this study’s MDR threshold.

The [paper, Methods 2.3](https://www.frontiersin.org/journals/microbiology/articles/10.3389/fmicb.2023.1175304/full) describes a resistance-based threshold. The [Magiorakos et al. proposal](https://doi.org/10.1111/j.1469-0691.2011.03570.x) concerns acquired non-susceptibility and organism-specific categories; this limited Aeromonas panel, including intrinsic resistance, must not be presented as a validated acquired-resistance clinical MDR classification.

Publication correction note: the paper reports approximately 58%; the confirmed repository calculation is 57.0%. The author proposes a publication calculation/rounding error, but the original calculation has not been reconstructed. The paper’s historical wording is not altered. The corrected STX category contains no R observations, so the source-label classification is unchanged.

## E07 final accession verification

The research author confirmed SU4 → SU4-2, SU6 → SU6-2, LJP308 → LP308 and LJP441 → LP441. These alias bridges come from author confirmation; NCBI independently supplies strain, species, project, assembly and WGS master identifiers.

The [NCBI Datasets BioProject API](https://api.ncbi.nlm.nih.gov/datasets/v2/genome/bioproject/PRJNA877469/dataset_report?page_size=100) was retrieved successfully on 2026-11-03. It returned 44 records: 22 GenBank GCA assemblies and 22 paired RefSeq GCF assemblies. Only the 22 GCA records are counted as isolate assemblies; paired records are not additional isolates. `ncbi_assembly_metadata.csv` records the selected source fields and retrieval URL/date for offline notebook use. The API response SHA-256 is a1796f5807f62f78587f9f5c4f4865b9a7377044cac8e96a73dd4122aca71bd8.

| Analysis ID | NCBI strain | Assembly | S1 WGS master |
|---|---|---|---|
| SU4 | SU4-2 | GCA_030386335.1 | JAOPLN000000000 |
| SU6 | SU6-2 | GCA_030386355.1 | JAOPLM000000000 |
| LJP308 | LP308 | GCA_030386495.1 | JAOPLU000000000 |
| LJP441 | LP441 | GCA_030386415.1 | JAOPLT000000000 |

Notebook 01 cell 14 defines the explicit alias dictionary and checks uniqueness, project, source species and WGS master identity. All 22 analysis IDs, assembly accessions and WGS master accessions are unique and complete. The original 18 direct WGS values and all 22 original analysis labels remain intact. Four missing WGS fields are filled; assembly accessions are added in a distinct column, not mixed with WGS accessions. The four-row `accession_mapping_review.csv` now records verified mappings rather than unresolved candidates. Original raw S1 and `strain_metadata.csv` are unchanged.

## E08 final SU4 reconciliation

The original S4 SU4 column contains **15 IS entries plus one MITE entry**, not 15 combined IS/MITE entries. After this difference was raised, the author explicitly approved using the source-table total of **16 distinct entries**. No row was dropped to force the earlier count.

| Category | Distinct entries | Table-derived copies |
|---|---:|---:|
| IS | 15 | 15 |
| MITE (MITEAeme1) | 1 | 6 |
| IS + MITE subtotal | **16** | **21** |
| Separate transposon (Tn521) | 1 | 1 |

Each unmultiplied named IS cell is counted as one table-listed copy; MITEAeme1 (6), in D25, is explicitly six and was confirmed by the author. This is a reconstruction of table notation, not fresh verification of genomic coordinates. All 15 other IS entries are individually traceable below and in `su4_mge_reconciliation.csv`.

| Source cell | Source entry | Derived label | Category | Table copies |
|---|---|---|---|---:|
| D6 | ISKpn3 | ISKpn3 | IS | 1 |
| D9 | ISAs17 | ISAs17 | IS | 1 |
| D14 | ISAs20 | ISAs20 | IS | 1 |
| D18 | ISAs32 | ISAs32 | IS | 1 |
| D19 | ISAs22 | ISAs22 | IS | 1 |
| D22 | ISAs19 | ISAs19 | IS | 1 |
| D25 | MITEAeme1 (6) | MITEAeme1 | MITE | 6 |
| D26 | ISAeme15 | ISAeme15 | IS | 1 |
| D28 | ISAeme4 | ISAeme4 | IS | 1 |
| D34 | ISAs25 | ISAs25 | IS | 1 |
| D35 | IS5 | IS5 | IS | 1 |
| D39 | ISAs34 | ISAs34 | IS | 1 |
| D43 | ISAs27 | ISAs27 | IS | 1 |
| D44 | ISAs29 | ISAs29 | IS | 1 |
| D48 | ISAs16 | ISAs16 | IS | 1 |
| D52 | ISAs3 | ISAs3 | IS | 1 |
| D57 | Tn512 | Tn521 | Transposon | 1 |


**Publication reconciliation:** 15 IS copies + 6 MITE copies gives 21 without adding Tn521. This reconciles the published number arithmetically under an inclusive IS/MITE convention. It does not prove that this was the original publication’s counting workflow, nor that the 21 are strictly IS copies under a definition excluding MITEs. The paper’s historical wording is preserved.

**Combined total:** 21 + 1 transposon = 22 is a table-category arithmetic sum (17 distinct named entries). It is not asserted as 22 independent, non-overlapping genomic loci: coordinates and possible nesting were not revalidated. Tn521 is never counted as an IS.

**Name correction:** the author confirmed Tn521. The local original S4 cell D57 says Tn512; the currently accessible article already says Tn521 in its abstract and discussion. Therefore the repository corrects the S4-derived label, without claiming the current article says Tn512. The raw workbook and historical publication remain unchanged. The reconciliation CSV contains both original and corrected labels.

Only SU4 numerical results are restored in the dashboard. The existing all-strain chart remains hidden because other isolates’ copy interpretation was not revalidated. Its IS-only values remain unchanged, while its caption now distinguishes the six SU4 MITE copies. Conceptual genomic schematics remain hidden for their existing independent limitations.

## Targeted execution and files

Cell numbers below are 1-based positions including Markdown cells. Execution was in isolated Python contexts with a noninteractive plotting backend; notebook JSON inline outputs and execution counters were not replaced.

### E02

Cells executed: Dashboard/static checks only.

Files:
- `streamlit_app.py`

### E03

Cells executed: [2, 4, 6, 10, 12, 14, 15].

Files:
- `analysis/03_virulence_analysis.ipynb`
- `streamlit_app.py`
- `data/processed/virulence_scores.csv`
- `data/processed/species_virulence_profile.csv`
- `data/processed/fig3_virulence_heatmap.png`
- `data/processed/fig_virulence_scores.png`
- `data/processed/fig_vf_prevalence.png`
- `data/processed/fig_species_virulence.png`

### E11

Cells executed: {'00': [2, 6, 7], '02': [2, 4, 6, 7, 9, 11]}.

Files:
- `README.md`
- `streamlit_app.py`
- `analysis/00_data_prep.ipynb`
- `analysis/02_amr_profiling.ipynb`
- `data/processed/amr_phenotype_long.csv`
- `data/processed/mdr_recalculation.csv`
- `data/processed/fig_amr_overview.png`
- `data/processed/fig_mdr_by_species.png`
- `data/processed/fig_resistance_heatmap.png`

### E07

Cells executed: [2, 4, '13 metadata assignments only', 14].

Files:
- `streamlit_app.py`
- `analysis/01_species_id.ipynb`
- `data/processed/strain_summary.csv`
- `data/processed/accession_mapping_review.csv`

### E08

Cells executed: {'00': [2, 15, 16, 17], '04': [2, 4, 6]}.

Files:
- `analysis/00_data_prep.ipynb`
- `analysis/04_mge_amr_colocalization.ipynb`
- `streamlit_app.py`
- `data/processed/mge_binary.csv`
- `data/processed/mge_copy_number.csv`
- `data/processed/is_elements_binary.csv`
- `data/processed/fig_mge_burden.png`

The E11 resistance heatmap was regenerated but is byte-identical to its previous image; it does not appear in the final Git diff. E03 heatmap spacing and reference-outline wording, and E11 legend placement, were adjusted only to make the affected regenerated figures legible. The IS family heatmap and MGE burden CSV did not require changes.

Shared additions: this document and `data/historical/README.md`, `data/historical/pre_phase2_outputs.zip`. README summarizes current status. The historical zip contains the exact pre-Phase-2 processed CSV/PNG files.

## Scientific boundaries

Genotype–phenotype concordance remains exploratory, uses the same collection and unverified rules, and is not independent predictive accuracy. No re-estimated clinical virulence, population prevalence, consumer safety, regulatory compliance, or transmission conclusion is supported. Original research authorship is documented by the paper; ownership of later Python work and AI-assisted development must be described separately, not inferred from Git commits.

## Virulence prevalence changes

| Category | Before (%) | After (%) |
|---|---:|---:|
| Flp type IV | 43.4783 | 45.4545 |
| Lateral flagella | 47.8261 | 45.4545 |
| T3SS | 17.3913 | 13.6364 |
| T6SS | 82.6087 | 81.8182 |
| aerA/act | 65.2174 | 63.6364 |
| ast | 43.4783 | 40.9091 |
| ahh1 | 65.2174 | 63.6364 |
| RTX | 65.2174 | 68.1818 |
| toxA | 43.4783 | 40.9091 |
| capsule | 95.6522 | 95.4545 |
| O-antigen | 60.8696 | 59.0909 |

For A. bestiarum, exclusion of GA97_22 changes the denominator from 4 to 3. All other species profiles and all individual scores are unchanged.


## Initial Phase 2 validation — historical stage

| Check | Result |
|---|---|
| Exact-byte preservation: 19 raw/assets/pipeline/dependency files; no baseline files deleted | PASSED |
| Only approved paths changed; 23/37 processed files byte-identical | PASSED |
| All notebook inline outputs, metadata and execution counters preserved; code syntax valid | PASSED |
| Historical archive contains all 37 original processed files exactly | PASSED |
| Independent raw-S2 recomputation: 79 composite records, 1,185 observations, 45 MDR (57.0%), 0 label disagreements, all zones/phenotypes unchanged | PASSED |
| Corrected STX group has 0 R observations; no class-based MDR reassignments | PASSED |
| Explicit VF reference membership: 22 isolates + 7 references | PASSED |
| Streamlit page: 🍣  The Story | PASSED |
| Streamlit page: 🦠  The Bacteria | PASSED |
| Streamlit page: 💊  Antibiotic Resistance | PASSED |
| All 19 phenotype selections render without ambiguous matches | PASSED |
| Streamlit page: 🧬  How Resistance Spreads | PASSED |
| Unresolved numerical MGE display and conceptual schematics remain withheld | PASSED |
| Full notebooks, WGS pipeline, retraining, clean dependency installation | NOT RUN (outside approved scope) |
| External alias verification; physical MGE copy reconciliation | BLOCKED / unresolved evidence |

An initial dashboard test exposed a column-count mismatch after the E07 status column was added. It was corrected using a name-based rename; all four pages and all 19 phenotype selections then passed. The first IS5 validation assertion expected a descriptive family label rather than the actual source value `IS5`; it stopped before derived writes and passed after correction. No failing required checks remain.

Installed pandas/numexpr and Streamlit deprecation warnings were non-blocking; dependency upgrades are deferred. This validates the installed environment, not a clean installation or the hosted deployment. All seven changed PNGs were visually reviewed; the unchanged resistance heatmap was also regenerated. The AMR plot width was adjusted after review to separate the corrected category labels.

The source phenotype collection contains records from 2015, 2018 and 2019: 44 retail-sushi, 18 oyster, 4 scallop, 3 salmon-loin and 10 processing-environment records. These are collection counts, not representative population sampling.


## Final E07/E08 targeted execution

Notebook 01: cells 2, 4, metadata assignments only from 13, and 14. Notebook 04: cells 2, 4 and 6. No other notebook, WGS pipeline or training was run. Existing inline outputs and execution counters are preserved; current tables and PNGs are authoritative. Prior Phase 1/2 notes remain as dated history and are superseded by the final E07/E08 sections above.

Changed existing files: README.md; DATA_CORRECTIONS.md; streamlit_app.py; analysis/01_species_id.ipynb; analysis/04_mge_amr_colocalization.ipynb; data/processed/strain_summary.csv; data/processed/accession_mapping_review.csv; data/processed/fig_mge_burden.png.

New files: data/processed/ncbi_assembly_metadata.csv; data/processed/su4_mge_reconciliation.csv; data/processed/su4_mge_summary.csv; data/processed/fig_su4_mge_counts.png.

The starting working tree matched the previous Phase 2 report except for a user Excel lock file, data/raw/~$Table_4.XLSX. It was not edited or deleted. A pre-final snapshot was saved outside the repository before edits. No commits, pushes or deployments were performed.

## Portfolio Evidence Sheet — current

| Field | Evidence / scope |
|---|---|
| Question | Describe Aeromonas species, antimicrobial resistance and virulence-associated features in a selected seafood/processing-environment collection. |
| Data | 79 phenotype records, 15 antibiotics, 1,185 observations; 22 WGS isolates; expanded VF matrix of 22 isolates + 7 references. |
| Methods | Original published research is distinguished from later Python analyses, descriptive summaries and an exploratory Streamlit dashboard. |
| MDR | 45/79 = 57.0% under the corrected nine-category, R-only study rule; AMP included, I excluded. All original labels agree. Unchanged in this final correction. |
| Accessions | 22 unique NCBI GCA assemblies linked to the 22 original WGS master records; four aliases confirmed by the author. |
| SU4 MGE evidence | 16 distinct IS/MITE entries, 21 table-derived copies; Tn521 is one separate transposon. Original S4 labels and copy notation are traceable per cell. |
| Validation limits | No complete pipeline rerun, genomic-coordinate recount, independent predictive evaluation or population-risk validation. Other-strain MGE comparisons and conceptual maps remain withheld. |
| Contribution | Published authorship, later Python work and these AI-assisted corrections must be described separately; sole authorship is not inferred from commits. |
| Links | NCBI BioProject API and article accessed; hosted dashboard not deployed or revalidated by this change. |
| Readiness | READY WITH CAVEATS: suitable for a descriptive scientific portfolio, with definitions and limits retained. |


## Final E07/E08 QA results

| Check | Result |
|---|---|
| Only the eight intended existing files changed; every other baseline file is byte-identical | PASSED |
| All notebook outputs, execution counters and metadata preserved; notebook/app syntax passes | PASSED |
| All eight raw files remain byte-identical to the pre-Phase-2 originals | PASSED |
| All 22 unique assembly / strain / species / project / WGS mappings match NCBI and original S1; 18 existing accessions and all analysis IDs preserved | PASSED |
| All 17 SU4 source cells verified: IS 15/15, MITE 1/6, Tn521 1/1; IS/MITE subtotal 16 entries / 21 copies excludes transposon | PASSED |
| MDR, virulence, all-strain MGE burden, existing IS matrices, original source names and historical archives unchanged | PASSED |
| Affected Streamlit page: 🦠  The Bacteria | PASSED |
| Affected Streamlit page: 🧬  How Resistance Spreads | PASSED |
| Git whitespace check passes; HEAD unchanged; no staged changes | PASSED |
| Two affected PNGs visually reviewed | PASSED |
| Full notebook/WGS execution, genomic-coordinate revalidation, clean dependency installation, deployment | NOT RUN |

The first image-visibility check used the older AppTest element key `imgs`; the installed version exposes `image`. The test was corrected without changing app behavior, and both affected pages passed. There are no remaining failed required checks. Existing non-blocking pandas/numexpr and Streamlit deprecation warnings remain outside scope.

This final correction changed eight existing files and added four files. All other files from the pre-final snapshot are byte-identical. The user Excel lock file is preserved. Git remains on main at 32ab42d182ff0ae8973424b876e554c1ac7d5cc6 with no staged changes. The cumulative tracked diff, including Phase 1/2, is 27 files, 1,297 insertions and 1,224 deletions; untracked files are excluded from that Git statistic.
