"""
AMR in Ready-to-Eat Seafood — Interactive Research Dashboard
=============================================================
Lee et al. (2023), Frontiers in Microbiology 14:1175304
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from pathlib import Path

st.set_page_config(
    page_title="Aeromonas Genomics — Research Explorer",
    page_icon="🍣",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Plotly figures inherit the previous dark default unless styling is fixed per figure.
# Preserve data traces, axes and scientific annotations; change presentation only.
def research_chart(fig, **kwargs):
    fig.update_layout(
        template="plotly_white",
        paper_bgcolor="#F9FBFC",
        plot_bgcolor="#F9FBFC",
        font=dict(color="#17344A", size=13),
        title_font=dict(color="#17344A", size=15),
        legend=dict(font=dict(color="#17344A")),
    )
    fig.update_xaxes(tickfont=dict(color="#41586A", size=11), title_font=dict(color="#17344A"))
    fig.update_yaxes(tickfont=dict(color="#41586A", size=11), title_font=dict(color="#17344A"))
    st.plotly_chart(fig, **kwargs)

# ── CSS ───────────────────────────────────────────────────────
st.markdown("""
<style>
/* Accessible light research theme: presentation only, no data transformations. */
.stApp, [data-testid="stAppViewContainer"] { background:#F7FAFC; color:#183044; }
[data-testid="stSidebar"] { background:#EAF1F5; border-right:1px solid #D8E4EC; }
[data-testid="stSidebar"] * { overflow-wrap:anywhere; }
.block-container { max-width:1160px; padding-top:2.5rem; padding-bottom:4rem; }
h1,h2,h3 { color:#17344A !important; letter-spacing:-.025em; }
h1 {font-size:2.15rem !important; margin-bottom:.6rem;}
h2 {font-size:1.4rem !important; }
p,li {line-height:1.6;}
.section-header {
    font-size:1.13rem;font-weight:700;color:#17344A !important;
    background:transparent;border-left:4px solid #167D8D;
    padding:.45rem .85rem; margin:1.5rem 0 .8rem;display:block;
}
.insight-box,.warning-box,.critical-box,.green-box {
    padding:.9rem 1rem;border-radius:8px;margin:.9rem 0;
    font-size:.93rem;line-height:1.65;color:#17344A !important;
    border-left:3px solid #167D8D;background:#EAF5F7 !important;
}
.warning-box {border-left-color:#B58341;background:#FFF5E5 !important;}
.critical-box {border-left-color:#BD6B63;background:#FFF1EE !important;}
.green-box {border-left-color:#3B8E72;background:#EAF7EF !important;}
.strain-tag {display:inline-block;padding:2px 6px;border-radius:5px;
background:#E4EEF2;color:#17344A;font-family:monospace;font-size:.78rem;}
.num-badge {display:inline-block;padding:.15rem .5rem;color:#167D8D;font-weight:700;}
.research-flow {display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:.75rem;margin:1.2rem 0;}
.research-flow .step {padding:1.1rem;background:white;border:1px solid #DDE8ED;
border-top:3px solid #167D8D;border-radius:10px;color:#183044;min-height:136px;}
.research-flow .step b{display:block;margin:.3rem 0;font-size:1rem;}
.research-flow .step span{font-size:.85rem;line-height:1.5;color:#526C7D;}
[data-testid="stMetric"] {background:white;border:1px solid #DDE8ED;border-radius:10px;padding:.7rem 1rem;}
[data-testid="stMetricValue"] {color:#17465B;}
[data-testid="stPlotlyChart"] {background:#fff;border:1px solid #E1E9ED;border-radius:10px;padding:.6rem;}
[data-testid="stExpander"] {border-radius:9px;background:white;}
@media(max-width:800px){.research-flow{grid-template-columns:repeat(2,1fr)}}
@media(max-width:540px){.research-flow{grid-template-columns:1fr}.block-container{padding:1rem}h1{font-size:1.75rem!important;}}
/* UI contrast repair: Streamlit theme may still be dark underneath CSS light canvas. */
[data-testid="stAppViewContainer"] {background:#F4F7FA !important;}
[data-testid="stMainBlockContainer"] {color:#183044 !important;}
[data-testid="stAppViewContainer"] .stMarkdown,
[data-testid="stAppViewContainer"] .stMarkdown p,
[data-testid="stAppViewContainer"] .stMarkdown li,
[data-testid="stAppViewContainer"] .stCaption,
[data-testid="stAppViewContainer"] [data-testid="stCaptionContainer"],
[data-testid="stAppViewContainer"] [data-testid="stCaptionContainer"] p,
[data-testid="stAppViewContainer"] [data-testid="stHeadingWithActionElements"] {
 color:#183044 !important;
}
[data-testid="stSidebar"] {background:#E6EEF4 !important;}
[data-testid="stSidebar"] [data-testid="stMarkdownContainer"] p,
[data-testid="stSidebar"] label,
[data-testid="stSidebar"] label p,
[data-testid="stSidebar"] [role="radiogroup"] p,
[data-testid="stSidebar"] [data-testid="stCaptionContainer"] p,
[data-testid="stSidebar"] [data-testid="stWidgetLabel"] p {
 color:#17344A !important;opacity:1 !important;
}
[data-testid="stSidebar"] [role="radiogroup"] label {background:#F5F9FB;border-radius:8px;padding:.4rem .5rem;}
[data-testid="stSidebar"] [role="radiogroup"] label:has(input:checked) {background:#D3EDF0;}
[data-testid="stSidebar"] .stMarkdown a {color:#146C80 !important;}
[data-testid="stMetric"] {background:#E8F3F6 !important;border:1px solid #C9E0E5 !important;box-shadow:none;border-radius:12px;}
[data-testid="stMetricLabel"] *,
[data-testid="stMetricDelta"] *,
[data-testid="stMetricValue"] * {color:#17344A !important;opacity:1 !important;}
[data-testid="stMetricValue"] {font-size:1.7rem !important;}
[data-testid="stExpander"] {border:1px solid #D6E3E9;background:#EAF1F5 !important;}
[data-testid="stExpander"] summary, [data-testid="stExpander"] summary p {color:#17344A !important;}
[data-testid="stPlotlyChart"] {background:#E9F0F4 !important;border:1px solid #D8E5EA !important;box-shadow:none;}
[data-testid="stDataFrame"] {border:1px solid #D4E1E8;border-radius:8px;}
[data-testid="stAlert"] p {color:#17344A !important;}
.stApp a {color:#116C7D;}
</style>
""", unsafe_allow_html=True)

# ── Data ──────────────────────────────────────────────────────
ROOT = Path(__file__).resolve().parent
PROC = ROOT / "data/processed"
RAW = ROOT / "data/raw"

@st.cache_data
def load_data():
    amr_long     = pd.read_csv(PROC / "amr_phenotype_long.csv")
    amr_wide     = pd.read_csv(PROC / "amr_phenotype_wide.csv")
    vf_scores    = pd.read_csv(PROC / "virulence_scores.csv")
    mge_burden   = pd.read_csv(PROC / "mge_burden_summary.csv")
    sp_virulence = pd.read_csv(PROC / "species_virulence_profile.csv", index_col=0)
    strain_sum   = pd.read_csv(PROC / "strain_summary.csv")
    ani          = pd.read_csv(RAW / "ANIclustermap_matrix.tsv", sep="\t", index_col=None)
    ani.index    = ani.columns.tolist()
    return amr_long, amr_wide, vf_scores, mge_burden, sp_virulence, strain_sum, ani

amr_long, amr_wide, vf_scores, mge_burden, sp_virulence, strain_sum, ani_df = load_data()

# ── Constants ─────────────────────────────────────────────────
SPECIES_PALETTE = {
    "A. salmonicida":"#E07B54","A. piscicola":"#5B8DB8",
    "A. bestiarum":"#6BAF92","A. media":"#9B7BB8",
    "A. rivipollensis":"#D4A843","A. caviae":"#C4706A",
    "A. hydrophila":"#7BA87B","A. dhakensis":"#8AA6C4",
}
SOURCE_PALETTE = {
    "Retail sushi":"#2196F3","Salmon loin":"#FF9800",
    "Oyster":"#9C27B0","Scallop":"#00BCD4","SPE":"#607D8B",
}
ABX_FULL = {
    "AMP":"Ampicillin","MEL":"Mecillinam","CTX":"Cefotaxime",
    "CRO":"Ceftriaxone","CIP":"Ciprofloxacin","OA":"Oxolinic acid",
    "DO":"Doxycycline","TE":"Tetracycline","IPM":"Imipenem",
    "MEM":"Meropenem","GM":"Gentamicin","TOB":"Tobramycin",
    "EM":"Erythromycin","FEC":"Florfenicol",
    "STX":"Trimethoprim/Sulfamethoxazole",
}
ABX_SHORT = {
    "Ampicillin AMP10":"AMP","Mecillinam MEL10":"MEL",
    "Cefotaxime CTX30":"CTX","ceftriaxone CRO30":"CRO",
    "Ciprofloxacin CIP1":"CIP","Oxolinic acid OA":"OA",
    "Doxycycline DO30":"DO","Tetracycline TE30":"TE",
    "Imipenem IPM10":"IPM","Meropenem MEM10":"MEM",
    "Gentamycin  GM10":"GM","Tobramycin TOB30":"TOB",
    "Erythromycin  EM15":"EM","Florfenicol  FEC30":"FEC",
    "Trimethoprim/sulfamethoxazole  STX 25":"STX",
}
ABX_CLASS = {
    "AMP":"Penicillins","MEL":"Penicillins",
    "CTX":"Cephalosporins","CRO":"Cephalosporins",
    "CIP":"Quinolones","OA":"Quinolones",
    "DO":"Tetracyclines","TE":"Tetracyclines",
    "IPM":"Carbapenems","MEM":"Carbapenems",
    "GM":"Aminoglycosides","TOB":"Aminoglycosides",
    "EM":"Macrolides","FEC":"Amphenicols","STX":"Folate pathway inhibitors",
}
CLASS_COLOR = {
    "Penicillins":"#E07B54","Cephalosporins":"#D4A843",
    "Quinolones":"#C4706A","Carbapenems":"#9B7BB8",
    "Tetracyclines":"#6BAF92","Aminoglycosides":"#5B8DB8",
    "Macrolides":"#7BA87B","Amphenicols":"#8AA6C4",
}
species_fix = {
    "A.salmonicida":"A. salmonicida","A.bestiarum":"A. bestiarum",
    "A. bestarium":"A. bestiarum","A. media ?":"A. media",
}
CLASS_COLOR["Folate pathway inhibitors"] = "#607D8B"
amr_long["abx_label"] = amr_long["antibiotic"].str.strip().map(ABX_SHORT)
amr_long["abx_class"] = amr_long["abx_label"].map(ABX_CLASS)
amr_long["species"]   = amr_long["species_id"].replace(species_fix)
amr_wide["species"]   = amr_wide["species_id"].replace(species_fix)

# Isolate IDs are reused across years/species: never join on isolate_id alone.
ISOLATE_KEY = ["source", "year", "isolate_id", "species"]
assert len(amr_wide) == 79 and not amr_wide.duplicated(ISOLATE_KEY).any()
assert not amr_long.duplicated(ISOLATE_KEY + ["abx_label"]).any()
assert amr_long.groupby(ISOLATE_KEY).size().eq(15).all()


# species map for ANI
ANI_SPECIES = {
    "LJP441":"A. salmonicida","OY59":"A. salmonicida","OY56":"A. salmonicida",
    "SU2":"A. salmonicida","SL21":"A. salmonicida","SC45":"A. salmonicida",
    "SL19":"A. salmonicida","LJP308":"A. piscicola","SL22":"A. bestiarum",
    "SU6":"A. bestiarum","SU58-3":"A. bestiarum","OY52":"A. media",
    "SU15":"A. rivipollensis","SU3":"A. rivipollensis","SU9":"A. rivipollensis",
    "A539":"A. rivipollensis","SC42":"A. rivipollensis","OY1":"A. rivipollensis",
    "SU4":"A. caviae","A537":"A. hydrophila","A533":"A. dhakensis","A536":"A. dhakensis",
    "A.salmonicida_NCTC12959":"A. salmonicida (ref)","A.piscicola_LMG24783":"A. piscicola (ref)",
    "A.bestiarum_CECT4227":"A. bestiarum (ref)","A.media_CECT4232":"A. media (ref)",
    "A.rivipollensis_KN_Mc_11N1":"A. rivipollensis (ref)","A.caviae_NCTC12244":"A. caviae (ref)",
    "A.hydrophila_ATCC7966":"A. hydrophila (ref)","A.dhakensis_CIP107500":"A. dhakensis (ref)",
}

# ════════════════════════════════════════════════════════════
# SIDEBAR
# ════════════════════════════════════════════════════════════
with st.sidebar:
    # ── Banner in sidebar ─────────────────────────────────────
    st.markdown("""
    <div style="background:linear-gradient(135deg,#1a1a2e,#0f3460);
                border-radius:10px; padding:1.1rem 1rem; margin-bottom:1rem;">
      <div style="font-size:2rem; text-align:center;">🍣</div>
      <p style="font-size:1.15rem; font-weight:800; color:#fff;
                margin:0.3rem 0 0.2rem; text-align:center; line-height:1.3;">
        Aeromonas Genomics
Research Explorer
      </p>
      <p style="font-size:0.78rem; color:#a8c8e8; text-align:center; margin:0;">
        Seafood and processing-environment<br>isolate collection
      </p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("### Explore")
    page = st.radio("section", [
        "🍣  The Story",
        "🦠  The Bacteria",
        "💊  Antibiotic Resistance",
        "🧬  Mobile Elements & Cases",
    ], label_visibility="collapsed")

    st.divider()
    st.markdown("**Research**")
    st.caption(
        "Lee et al. (2023)  \n"
        "*Whole genome sequence analysis of Aeromonas spp. "
        "isolated from ready-to-eat seafood*  \n"
        "Frontiers in Microbiology · 14:1175304"
    )
    st.markdown(
        "[![Paper](https://img.shields.io/badge/📄_Paper-Open_Access-blue)](https://doi.org/10.3389/fmicb.2023.1175304)  \n"
        "[![GitHub](https://img.shields.io/badge/💻_GitHub-Code-black)](https://github.com/hyejeong0617/amr_genomics_aeromonas)  \n"
        "[![Nautilus](https://img.shields.io/badge/🔬_Nautilus-Article-green)](https://nautil.us/is-sushi-a-health-hazard-421668)  \n"
        "[![IFLScience](https://img.shields.io/badge/🌐_IFLScience-Article-orange)](https://www.iflscience.com/how-safe-is-the-sushi-you-eat-really-70899)"
    )


# ════════════════════════════════════════════════════════════
# PAGE 1 — THE STORY
# ════════════════════════════════════════════════════════════
if page == "🍣  The Story":

    st.title("Aeromonas Genomics in Seafood & Processing Environments")
    st.markdown(
        "Explore a selected isolate collection; these results do not estimate consumer risk."
    )
    st.divider()


    # ── Research overview — visual diagram ───────────────────
    st.markdown('<span class="section-header">🔬 From Grocery Store to Genome — Research Overview</span>',
                unsafe_allow_html=True)

    st.write("**Research question:** What do selected seafood-associated *Aeromonas* isolates reveal about species diversity, antimicrobial resistance and resistance-associated genomic elements? The study does not measure consumer risk or demonstrate transmission.")
    st.write("")

    # Concise research workflow — four stages for portfolio audiences
    pipe_html = """
    <div class="research-flow">
      <div class="step">🛒 <b>01 · Collect & identify</b><span>Ready-to-eat seafood and processing environment · 79 isolate records · phenotypic identification</span></div>
      <div class="step">💊 <b>02 · Test susceptibility</b><span>15 antibiotics across 79 isolates · source-level MDR reconciliation</span></div>
      <div class="step">🧬 <b>03 · Sequence genomes</b><span>22 selected strains · Illumina sequencing · genome assemblies and ANI</span></div>
      <div class="step">🔬 <b>04 · Interpret evidence</b><span>19 genomic representatives · AMR, virulence-associated genes and MGE case studies</span></div>
    </div>
    """
    st.markdown(pipe_html, unsafe_allow_html=True)

    st.caption("MDR correction note: corrected nine-category, R-only study-operational classification confirms 45/79 records (57.0%), matching all 79 original source labels. AMP is included and intermediate results are excluded; this is not a validated acquired-resistance clinical classification. The published article reports approximately 58%, preserved as historical wording rather than a computational target. A publication calculation/rounding error is the author's proposed explanation; the original calculation has not been reconstructed. See DATA_CORRECTIONS.md for the record-level comparison and definition.")

    # Headline study-scoped figures; labels avoid population prevalence claims.
    c1,c2,c3,c4 = st.columns(4)
    c1.metric("Isolate records", "79")
    c2.metric("WGS isolates", "22")
    c3.metric("Identified species", "8")
    c4.metric("Study-specific MDR", "45/79 · 57.0%")
    st.caption("79 isolate records, 22 sequenced genomes, 19 representatives in published downstream gene analysis. MDR is the corrected study-specific nine-category R-only rule, not population prevalence.")

    st.markdown("""
    <div class="insight-box" style="margin-top:1rem;">
    💡 <strong>Navigate the sections</strong> using the sidebar to explore:
    the bacteria found (🦠), their antibiotic resistance profiles (💊),
    and genomic features associated with potential resistance mobility (🧬).
    </div>
    """, unsafe_allow_html=True)
    
    st.divider()

    st.markdown("**Key takeaway:** Published genomic evidence supports descriptive AMR and species-level findings; mobile-element observations raise testable hypotheses, not proof of transmission to humans or clinical outcomes.")


# ════════════════════════════════════════════════════════════
# PAGE 2 — THE BACTERIA
# ════════════════════════════════════════════════════════════
elif page == "🦠  The Bacteria":

    st.title("Species & Genomic Diversity")
    st.caption("22 selected study isolates · 8 species · 19 representatives in the published downstream gene analysis")
    st.markdown(
        "22 *Aeromonas* strains were whole-genome sequenced. "
        "They represent **8 different species**, each with a distinct profile "
        "of virulence factors and antibiotic resistance genes."
    )

    # ── Species + source overview ─────────────────────────────
    st.markdown('<span class="section-header">📍 Species in the study collection</span>',
                unsafe_allow_html=True)

    col_bar, col_pie = st.columns(2)
    sp_counts = (strain_sum.groupby("Species")["Strain ID"].count()
                 .reset_index().rename(columns={"Strain ID":"count","Species":"species"})
                 .sort_values("count", ascending=True))
    sp_counts["color"] = sp_counts["species"].map(SPECIES_PALETTE)

    with col_bar:
        fig_sp = go.Figure(go.Bar(
            x=sp_counts["count"], y=sp_counts["species"], orientation="h",
            marker_color=sp_counts["color"], text=sp_counts["count"],
            textposition="outside",
            hovertemplate="<b>%{y}</b><br>%{x} isolates<extra></extra>",
        ))
        fig_sp.update_layout(
            title="Isolates per species (n=22)",
            xaxis=dict(title="Number of isolates", range=[0,10]),
            height=300, margin=dict(l=10,r=40,t=40,b=10),
            plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
        )
        research_chart(fig_sp, use_container_width=True)

    src_df = strain_sum["Isolation source"].value_counts().reset_index()
    src_df.columns = ["source","count"]
    with col_pie:
        fig_src = go.Figure(go.Pie(
            labels=src_df["source"], values=src_df["count"], hole=0.4,
            marker_colors=[SOURCE_PALETTE.get(s,"#999") for s in src_df["source"]],
            hovertemplate="<b>%{label}</b><br>%{value} isolates (%{percent})<extra></extra>",
        ))
        fig_src.update_layout(title="Isolation source (n=22)", height=300,
                              margin=dict(t=40,b=10))
        research_chart(fig_src, use_container_width=True)

    st.caption("All 22 WGS isolates have unique NCBI assembly mappings verified against BioProject PRJNA877469 and source S1. Analysis IDs are preserved; four aliases were confirmed by the research author. WGS master and assembly accessions are shown separately.")
    with st.expander("🔍 View all 22 strains"):
        disp = strain_sum.copy()
        disp = disp.rename(columns={"Isolation source": "Isolation Source", "NCBI accession": "NCBI Accession"})
        st.dataframe(disp, use_container_width=True, hide_index=True)
        st.caption(
            "Strain IDs reflect origin: SU = retail sushi, SL = salmon loin, "
            "OY = oyster, SC = scallop, LJP/A = salmon processing environment or archived isolates."
        )

    st.divider()

    # ── ANI interactive heatmap ───────────────────────────────
    st.markdown('<span class="section-header">🧬 Are they really 8 different species? — ANI Analysis</span>',
                unsafe_allow_html=True)

    st.write("**Average nucleotide identity (ANI)** compares genome sequence similarity. The study used an approximately 96% ANI criterion to support species assignment. Hover over the heatmap to inspect individual comparisons; source identities and references are labeled.")

    strains_ani = ani_df.index.tolist()
    z_ani = ani_df.values.astype(float)

    hover_ani = []
    for i, s1 in enumerate(strains_ani):
        row_h = []
        for j, s2 in enumerate(strains_ani):
            sp1 = ANI_SPECIES.get(s1,"Unknown").replace(" (ref)","")
            sp2 = ANI_SPECIES.get(s2,"Unknown").replace(" (ref)","")
            val = z_ani[i,j]
            same = "✅ Same species" if val>=96 and i!=j else ("—" if i==j else "❌ Different")
            row_h.append(
                f"<b>{s1}</b> ({sp1})<br><b>{s2}</b> ({sp2})<br>"
                f"ANI: <b>{val:.2f}%</b><br>{same}"
            )
        hover_ani.append(row_h)

    row_colors_ani = [SPECIES_PALETTE.get(
        ANI_SPECIES.get(s,"Unknown").replace(" (ref)",""), "#CCCCCC")
        for s in strains_ani]

    fig_ani = go.Figure(data=go.Heatmap(
        z=z_ani, x=strains_ani, y=strains_ani,
        colorscale="YlOrRd", zmin=84, zmax=100,
        text=hover_ani, hoverinfo="text",
        colorbar=dict(title="ANI (%)", thickness=12),
    ))
    fig_ani.update_layout(
        title=dict(
            text="ANI Matrix — 22 isolates + 8 reference genomes<br>"
                 "<sup>≥96% = same species | ~100% = identical strains</sup>",
            font_size=12),
        height=610,
        xaxis=dict(tickangle=45, tickfont=dict(size=10)),
        yaxis=dict(tickfont=dict(size=10), autorange="reversed"),
        margin=dict(l=145, b=125, r=35, t=65),
    )
    research_chart(fig_ani, use_container_width=True)

    st.markdown("""
    <div class="insight-box">
    💡 <strong>Key finding from ANI:</strong>
    Strains A533 & A536 (<i>A. dhakensis</i>) and SU3, SU9 & SU15
    (<i>A. rivipollensis</i>) show ANI ≥ 99.9% — they are
    <strong>highly similar genomes</strong> isolated from different sushi products.
    One representative per highly similar group was used in downstream analysis
    (final dataset: <strong>19 representative strains</strong>).
    </div>
    """, unsafe_allow_html=True)

    st.divider()

    with st.expander("Explore additional virulence-associated profiles (expanded 22-isolate analysis)", expanded=False):
        # ── Virulence factors ─────────────────────────────────────
        st.markdown('<span class="section-header">⚔️ Virulence factors — the bacterial weapons kit</span>',
                    unsafe_allow_html=True)

        col_def, col_vfhm = st.columns([1, 1.4])
        with col_def:
            st.markdown("""
    **Virulence factors** are molecular tools bacteria use to infect a host.
    We analysed **18 categories** across 5 functional groups:

    | Function | Examples |
    |---|---|
    | 🟢 **Adherence** | Type IV pili (attach to cells) |
    | 🟡 **Motility** | Flagella (swim toward host) |
    | ⚪ **Secretion** | T2SS, T3SS, T6SS (inject toxins) |
    | 🔴 **Toxins** | Hemolysins, enterotoxins |
    | 🔵 **Immune evasion** | Capsule, O-antigen |

    **Category counts describe detected features, not clinical danger or validated pathogenicity.**
            """)

        with col_vfhm:
            fig_vfhm = px.imshow(
                sp_virulence, color_continuous_scale="Blues",
                zmin=0, zmax=100, text_auto=".0f", aspect="auto",
                labels={"color":"Mean presence (%)"},
            )
            fig_vfhm.update_layout(
                title="Mean VF presence (%) by species",
                height=320, margin=dict(t=40,b=100),
                xaxis_tickangle=40,
                coloraxis_colorbar=dict(title="Mean<br>presence (%)")
            )
            research_chart(fig_vfhm, use_container_width=True)

        st.markdown("""
        <div class="warning-box">
        <strong>Expanded repository analysis:</strong> 22 study isolates and 7 references.
        The summaries below exclude all 7 references, including GA97_22.
        Near-identical study isolates remain included; these descriptive summaries
        are not an independent replication of the paper's 19-representative analysis.
        </div>
        """, unsafe_allow_html=True)



        # strain explorer
        st.markdown('<span class="section-header">🔎 Explore individual strain virulence profiles</span>',
                    unsafe_allow_html=True)

        st.markdown("""
        <div class="insight-box">
        <span class="strain-tag">SU</span> = retail Sushi &nbsp;
        <span class="strain-tag">SL</span> = Salmon Loin &nbsp;
        <span class="strain-tag">OY</span> = Oyster &nbsp;
        <span class="strain-tag">SC</span> = Scallop &nbsp;
        <span class="strain-tag">LJP/A</span> = SPE / archived isolates
        </div>
        """, unsafe_allow_html=True)

        sel_sp = st.selectbox("Filter by species", ["All species"] + list(SPECIES_PALETTE.keys()))
        vf_iso = vf_scores[vf_scores["is_ref"]=="isolate"].copy()
        vf_iso["species"] = vf_iso["species"].replace(species_fix)
        if sel_sp != "All species":
            vf_iso = vf_iso[vf_iso["species"]==sel_sp]
        vf_iso = vf_iso.sort_values("vf_score", ascending=False)
        vf_iso["color"] = vf_iso["species"].map(SPECIES_PALETTE)

        fig_vf = go.Figure(go.Bar(
            x=vf_iso["strain"], y=vf_iso["vf_score"],
            marker_color=vf_iso["color"],
            hovertemplate="<b>%{x}</b><br>Species: %{customdata}<br>VF categories: %{y}/18<extra></extra>",
            customdata=vf_iso["species"],
        ))
        fig_vf.add_hline(y=vf_iso["vf_score"].mean(), line_dash="dash", line_color="#555",
            annotation_text=f"Mean ({vf_iso['vf_score'].mean():.1f})", annotation_position="top right")
        fig_vf.update_layout(
            title="Virulence factor burden per strain (max 18 categories)",
            yaxis_title="VF categories present", xaxis_tickangle=45,
            height=320, plot_bgcolor="rgba(0,0,0,0)", margin=dict(t=40,b=80),
        )
        research_chart(fig_vf, use_container_width=True)


# ════════════════════════════════════════════════════════════
# PAGE 3 — ANTIBIOTIC RESISTANCE
# ════════════════════════════════════════════════════════════
elif page == "💊  Antibiotic Resistance":

    st.title("Antimicrobial Resistance in *Aeromonas*")
    st.caption("Phenotypic susceptibility in 79 records · published genotypic profiles for 19 WGS representatives")
    st.markdown("""
    Two complementary analyses were performed:
    - **22 sequenced isolates, 19 representatives** → published genotypic profiles
    - **79 isolate records** → phenotypes from seafood and processing environments; not population prevalence
    """)

    st.divider()

    st.info("**45 of 79 isolate records (57.0%)** meet the study-specific MDR rule. The sample is selected; this is not population prevalence.")
    # ── SECTION 2: 79-strain MDR overview ────────────────────
    st.markdown('<span class="section-header">📊 79 isolate records — supplied MDR labels</span>',
                unsafe_allow_html=True)

    st.markdown("""
    All 79 isolates were tested against 15 antibiotics by disk diffusion.
    This selected collection includes seafood and processing-environment isolates; it does not estimate MDR prevalence across retail seafood.
    """)

    st.caption("MDR labels were recalculated against the corrected nine-category R-only rule: 45/79 (57.0%), matching the original source labels. Intermediate results are excluded; this is not a clinical acquired-resistance classification.")
    # MDR summary
    n_tot = len(amr_wide)
    n_mdr = int(amr_wide["MDR"].sum())
    c1,c2,c3,c4 = st.columns(4)
    c1.metric("Total isolates", n_tot)
    c2.metric("MDR isolates", n_mdr, f"{n_mdr/n_tot*100:.1f}% under the study rule")
    c3.metric("Antibiotics tested", 15, "9 corrected categories")
    c4.metric("100% resistant to", "Ampicillin", "intrinsic in Aeromonas")

    # MDR by species
    iso_meta = amr_long[ISOLATE_KEY + ["MDR"]].drop_duplicates(ISOLATE_KEY)
    mdr_sp = (iso_meta.groupby("species")["MDR"]
              .agg(total="count", mdr_n="sum")
              .assign(mdr_pct=lambda x: x["mdr_n"]/x["total"]*100)
              .reset_index().sort_values("mdr_pct", ascending=True))
    mdr_sp["color"] = mdr_sp["species"].map(SPECIES_PALETTE)

    col_m1, col_m2 = st.columns(2)
    with col_m1:
        fig_mdr = go.Figure()
        fig_mdr.add_trace(go.Bar(
            y=mdr_sp["species"], x=mdr_sp["total"]-mdr_sp["mdr_n"],
            name="Non-MDR", orientation="h", marker_color="#CCCCCC"))
        fig_mdr.add_trace(go.Bar(
            y=mdr_sp["species"], x=mdr_sp["mdr_n"],
            name="MDR", orientation="h", marker_color=mdr_sp["color"].tolist()))
        fig_mdr.update_layout(
            barmode="stack", title="MDR count per species",
            xaxis_title="Number of isolates", height=280,
            margin=dict(t=40,b=10), plot_bgcolor="rgba(0,0,0,0)",
            legend=dict(orientation="h", y=-0.2))
        research_chart(fig_mdr, use_container_width=True)

    with col_m2:
        fig_pct = go.Figure(go.Bar(
            y=mdr_sp["species"], x=mdr_sp["mdr_pct"], orientation="h",
            marker_color=mdr_sp["color"],
            text=mdr_sp["mdr_pct"].apply(lambda v:f"{v:.0f}%"), textposition="outside"))
        fig_pct.add_vline(x=n_mdr/n_tot*100, line_dash="dash", line_color="#555",
            annotation_text="Overall 57.0%", annotation_position="top")
        fig_pct.update_layout(
            title="MDR rate (%) per species",
            xaxis=dict(title="MDR rate (%)", range=[0,120]),
            height=280, margin=dict(t=40,b=10,r=60),
            plot_bgcolor="rgba(0,0,0,0)")
        research_chart(fig_pct, use_container_width=True)

    # Key resistance rates — simplified
    st.markdown('<span class="section-header">📉 Which antibiotics are they resistant to?</span>',
                unsafe_allow_html=True)

    resist_rate = (
        amr_long[amr_long["phenotype"].notna()]
        .assign(is_R=lambda x:(x["phenotype"]=="R").astype(int))
        .groupby(["abx_class","abx_label"])["is_R"]
        .mean().mul(100).round(1).reset_index()
        .rename(columns={"is_R":"resistance_pct"})
        .sort_values(["abx_class","resistance_pct"], ascending=[True,False])
    )
    resist_rate["color"] = resist_rate["abx_class"].map(CLASS_COLOR)
    resist_rate["label"] = resist_rate["abx_label"] + "\n" + \
        resist_rate["abx_label"].map(ABX_FULL).fillna("")

    fig_r = go.Figure(go.Bar(
        x=resist_rate["abx_label"], y=resist_rate["resistance_pct"],
        marker_color=resist_rate["color"],
        hovertemplate="<b>%{x}</b> (%{customdata[0]})<br>%{customdata[1]}<br>Resistance: %{y:.1f}%<extra></extra>",
        customdata=list(zip(resist_rate["abx_label"].map(ABX_FULL).fillna(""),
                            resist_rate["abx_class"])),
    ))
    fig_r.update_layout(
        yaxis_title="Resistant isolates (%)", xaxis_tickangle=45,
        height=340, plot_bgcolor="rgba(0,0,0,0)", margin=dict(t=10,b=80))
    research_chart(fig_r, use_container_width=True)

    with st.expander("📖 Antibiotic abbreviations"):
        st.dataframe(
            pd.DataFrame([{"Abbr.":k,"Full name":v,"Class":ABX_CLASS.get(k,"")}
                          for k,v in ABX_FULL.items()]),
            hide_index=True, use_container_width=True)

    st.markdown("""
    <div class="critical-box">
    <strong>Descriptive resistance frequencies in this selected collection:</strong>
    <b>100%</b> resist Ampicillin (intrinsic).
    <b>57%</b> resist Erythromycin.
    <b>48%</b> resist Florfenicol.
    <b>10%</b> resist Imipenem.
    </div>
    """, unsafe_allow_html=True)


    st.divider()
    with st.expander("Explore the detailed published 19-strain AMR gene panel and individual isolates", expanded=False):
        # ── SECTION 1: 22-strain genotypic vs phenotypic ─────────
        st.markdown('<span class="section-header">🔬 19 representative strains — published AMR gene profiles</span>',
                    unsafe_allow_html=True)

        st.markdown("""
        The publication compares 19 representative strains:
        **phenotypic resistance** (disk diffusion — what happens in the lab)
        vs **genotypic resistance** (AMR genes detected in the genome).
        This descriptive comparison does not establish causation; it
        highlights cases of **discordance** (resistance not explained by known genes,
        or genes present without phenotypic effect).
        """)

        # Genotypic heatmap (Table 1)
        table1_data = [
            ["SU4-2",  "A. caviae",        "",            "blaMOX-15",   "blaOXA-780",  "tet(E),qacEΔ1","sul1,aadA1"],
            ["A533",   "A. dhakensis",     "cphA2",       "blaAQU",      "blaOXA-12",   "",""],
            ["A537",   "A. hydrophila",    "cphA2",       "cepS",        "blaOXA-12",   "tet(E)",""],
            ["A539",   "A. rivipollensis", "",            "",            "blaOXA-427",  "","qnrS2"],
            ["SU3",    "A. rivipollensis", "",            "",            "blaOXA-427",  "",""],
            ["SC42",   "A. rivipollensis", "",            "",            "blaOXA-427",  "",""],
            ["OY1",    "A. rivipollensis", "",            "",            "blaOXA-427",  "",""],
            ["OY52",   "A. media",         "",            "blaMOX-9",    "blaOXA-427",  "",""],
            ["SU6-2",  "A. bestiarum",     "cphA1",       "",            "blaOXA-956",  "",""],
            ["SL22",   "A. bestiarum",     "cphA1",       "",            "blaOXA-956",  "",""],
            ["SU58-3", "A. bestiarum",     "cphA1",       "",            "blaOXA-956",  "",""],
            ["LJP308", "A. piscicola",     "cphA1",       "",            "blaOXA-956",  "",""],
            ["SU2",    "A. salmonicida",   "cphA1",       "",            "blaOXA-956",  "",""],
            ["SL19",   "A. salmonicida",   "cphA1/cphA3", "",            "blaOXA-956",  "",""],
            ["SL21",   "A. salmonicida",   "cphA5",       "",            "blaOXA-956",  "",""],
            ["SC45",   "A. salmonicida",   "cphA5",       "",            "blaOXA-956",  "",""],
            ["OY56",   "A. salmonicida",   "cphA1",       "",            "blaOXA-956",  "",""],
            ["OY59",   "A. salmonicida",   "cphA5",       "",            "blaOXA-956",  "",""],
            ["LJP441", "A. salmonicida",   "cphA1",       "",            "blaOXA-956",  "",""],
        ]
        t1 = pd.DataFrame(table1_data,
            columns=["strain","species","Class B","Class C","Class D","Efflux pump","Other genes"])

        # ── Full-width annotated gene chart ───────────────────────
        gene_cols  = ["Class B","Class C","Class D","Efflux pump","Other genes"]
        col_labels = [
            "Class B<br>β-lactamase","Class C<br>β-lactamase",
            "Class D<br>β-lactamase","Efflux pump","Other genes"
        ]
        class_col_map = {
            "Class B<br>β-lactamase":"#BBDEFB",
            "Class C<br>β-lactamase":"#C8E6C9",
            "Class D<br>β-lactamase":"#E1BEE7",
            "Efflux pump":"#FFE0B2",
            "Other genes":"#CFD8DC",
        }

        fig_geno = go.Figure()
        n_strains = len(t1)
        n_cols    = len(gene_cols)

        # Cell width/height in data units
        CW, CH = 0.9, 0.85

        for j, (col_key, col_label) in enumerate(zip(gene_cols, col_labels)):
            for i_row in range(n_strains):
                gene_val = t1.iloc[i_row][col_key]
                present  = gene_val != ""
                bg       = class_col_map[col_label] if present else "#F8F8F8"
                txt_col  = "#1A237E" if present else "#BDBDBD"
                disp     = gene_val if present else "—"
                fig_geno.add_shape(
                    type="rect",
                    x0=j-CW/2, x1=j+CW/2,
                    y0=i_row-CH/2, y1=i_row+CH/2,
                    fillcolor=bg, line_color="white", line_width=2,
                )
                fig_geno.add_annotation(
                    x=j, y=i_row,
                    text=f"<b>{disp}</b>",
                    showarrow=False,
                    font=dict(color=txt_col, size=12),
                    align="center",
                )

        # Species colour bar on left
        for i_row, sp in enumerate(t1["species"]):
            clr = SPECIES_PALETTE.get(sp, "#CCCCCC")
            fig_geno.add_shape(type="rect",
                x0=-0.95, x1=-0.65,
                y0=i_row-CH/2, y1=i_row+CH/2,
                fillcolor=clr, line_color="white", line_width=0.5)

        fig_geno.update_layout(
            title=dict(
                text="Genotypic AMR profile — 19 representative WGS strains"
                     "<br><sup>Each cell shows the AMR gene(s) present. — = absent. Left colour bar = species.</sup>",
                font_size=15,
            ),
            xaxis=dict(
                tickmode="array",
                tickvals=list(range(n_cols)),
                ticktext=col_labels,
                tickfont=dict(size=13),
                showgrid=False, zeroline=False,
                side="top",
            ),
            yaxis=dict(
                tickmode="array",
                tickvals=list(range(n_strains)),
                ticktext=t1["strain"].tolist(),
                tickfont=dict(size=12),
                showgrid=False, zeroline=False,
                autorange="reversed",
            ),
            height=680,
            margin=dict(t=110, b=30, l=110, r=30),
            plot_bgcolor="white",
        )
        research_chart(fig_geno, use_container_width=True)

        st.caption("Later manual re-visualization of published Table 1. Gene-family descriptions below are biological context, not independently validated phenotype predictions. Gene presence does not establish resistance to every drug in a class.")

        # Key observations below the chart
        col_obs1, col_obs2 = st.columns(2)
        with col_obs1:
            st.markdown("""
    **β-Lactamase classes:**

    | Class | Genes | Resistance |
    |---|---|---|
    | **B** (Metallo) | cphA1/2/5 | Carbapenems (IPM, MEM) |
    | **C** | blaMOX, blaAQU, cepS | Cephalosporins |
    | **D** (OXA) | blaOXA-12/427/780/956 | Penicillins + broad-spectrum |
            """)
        with col_obs2:
            st.markdown("""
    **Species-specific patterns:**
    - *A. salmonicida / bestiarum / piscicola* → cphA (Class B) + blaOXA-956
    - *A. rivipollensis / media* → blaOXA-427; A. media also carries blaMOX-9 in this table
    - *A. caviae / dhakensis / hydrophila* → mixed profile

    **All 19 strains carry at least one AMR gene.**
            """)

        st.markdown('<span class="section-header">🔎 Individual strain phenotypic profile</span>',
                    unsafe_allow_html=True)

        wgs_strains = t1["strain"].tolist()
        sel_iso = st.selectbox("Select a WGS strain", wgs_strains)
        selected_species = t1.set_index("strain").loc[sel_iso, "species"]
        matches = amr_wide[(amr_wide["isolate_id"] == sel_iso) &
                           (amr_wide["species"] == selected_species)]
        if len(matches) != 1:
            st.error("This strain does not have one unambiguous phenotype record.")
            st.stop()
        iso_row = matches.iloc[0]
        iso_long = amr_long.copy()
        for field in ISOLATE_KEY:
            iso_long = iso_long[iso_long[field] == iso_row[field]]
        if len(iso_long) != 15 or iso_long["abx_label"].nunique() != 15:
            st.error("The selected isolate does not have a complete, unique antibiotic panel.")
            st.stop()
        if len(iso_long) == 15:
            mdr_txt = "⛔ MDR" if iso_row["MDR"]==1 else "✅ Non-MDR"
            n_R = int((iso_long["phenotype"]=="R").sum())
            ca,cb,cc = st.columns(3)
            ca.metric("Species", t1[t1["strain"]==sel_iso]["species"].values[0] if sel_iso in t1["strain"].values else "—")
            cb.metric("MDR status", mdr_txt)
            cc.metric("Resistant to", f"{n_R} / 15 antibiotics")
            ph_color = {"R":"#C0392B","I":"#E8A838","S":"#27AE60"}
            ph_name  = {"R":"Resistant","I":"Intermediate","S":"Susceptible"}
            iso_ph = iso_long[["abx_label","phenotype"]].dropna()
            iso_ph["score"] = iso_ph["phenotype"].map({"R":2,"I":1,"S":0})
            iso_ph["color"] = iso_ph["phenotype"].map(ph_color)
            iso_ph["full"]  = iso_ph["abx_label"].map(ABX_FULL)
            fig_iso = go.Figure(go.Bar(
                x=iso_ph["abx_label"], y=iso_ph["score"],
                marker_color=iso_ph["color"],
                hovertemplate="<b>%{x}</b> (%{customdata[0]})<br>%{customdata[1]}<extra></extra>",
                customdata=list(zip(iso_ph["full"], iso_ph["phenotype"].map(ph_name))),
            ))
            fig_iso.update_layout(
                title=f"Phenotypic profile — {sel_iso}",
                yaxis=dict(tickvals=[0,1,2], ticktext=["Susceptible","Intermediate","Resistant"]),
                xaxis_tickangle=45, height=260,
                plot_bgcolor="rgba(0,0,0,0)", margin=dict(t=40,b=80),
            )
            research_chart(fig_iso, use_container_width=True)

        st.divider()


# ════════════════════════════════════════════════════════════
# PAGE 4 — HOW RESISTANCE SPREADS
# ════════════════════════════════════════════════════════════
elif page == "🧬  Mobile Elements & Cases":

    st.title("Mobile Genetic Elements & Case Studies")
    st.caption("Source-supported observations; presence or co-localisation does not establish horizontal transfer")
    st.markdown("The paper reports mobile genetic elements and resistance-associated genes. Their presence suggests potential mobility; transfer to human pathogens, clinical harm and treatment failure were not demonstrated in this study.")
    st.divider()

    st.markdown('### SU4 / SU4-2: reconciled Table S4 counts')
    su4_counts = pd.read_csv(PROC / 'su4_mge_summary.csv').set_index('category')
    su4_entries = pd.read_csv(PROC / 'su4_mge_reconciliation.csv').fillna('')
    is_mite = su4_counts.loc[['IS','MITE']]
    count_cols = st.columns(3)
    count_cols[0].metric('Distinct IS/MITE entries', int(is_mite['distinct_entries'].sum()))
    count_cols[1].metric('IS/MITE copies (Table S4)', int(is_mite['table_copy_count'].sum()))
    count_cols[2].metric('Separate transposon', int(su4_counts.loc['Transposon','distinct_entries']), 'Tn521')
    st.caption('15 single IS entries + MITEAeme1 (6 copies) = 21 IS/MITE copies across 16 distinct entries. Tn521 is counted separately, never as an IS. This reconciles the published number arithmetically when MITEs are included; it does not reconstruct the original counting workflow or validate genomic coordinates. The arithmetic sum including Tn521 is 22, not a verified non-overlapping genomic-locus total.')
    st.image(str(PROC / 'fig_su4_mge_counts.png'), width=650)
    with st.expander('View source cells and counting rules'):
        st.dataframe(su4_entries[['source_cell','source_text','element_name','category','table_copy_count','copy_basis']], hide_index=True)
    st.info("**Interpretation:** SU4 counts are reconciled from the supplied source table. Other-isolate MGE comparisons and coordinate-level genomic diagrams remain withheld pending verification.")
    if False:  # Phase 1 hold: pending separate Phase 2 approval.
        # ── MGE burden ────────────────────────────────────────────
        st.markdown('<span class="section-header">📊 Mobile element burden — which strains carry the most?</span>',
                    unsafe_allow_html=True)

        mge_s = mge_burden.sort_values("is_copies", ascending=True).copy()
        mge_s["color"]  = mge_s["species"].map(SPECIES_PALETTE)
        mge_s["is_key"] = mge_s["strain"].isin(["SU4","A539"])
        mge_s["label"]  = mge_s.apply(lambda r: f"⭐ {r['strain']}" if r["is_key"] else r["strain"], axis=1)

        fig_mge = go.Figure(go.Bar(
            x=mge_s["is_copies"], y=mge_s["label"], orientation="h",
            marker=dict(color=mge_s["color"],
                        line=dict(color=["#000" if k else "rgba(0,0,0,0)" for k in mge_s["is_key"]], width=2)),
            hovertemplate="<b>%{y}</b><br>Species: %{customdata}<br>IS copies: %{x}<extra></extra>",
            customdata=mge_s["species"],
        ))
        fig_mge.add_vline(x=mge_s["is_copies"].mean(), line_dash="dash", line_color="#555",
            annotation_text=f"Mean ({mge_s['is_copies'].mean():.1f})", annotation_position="top")
        fig_mge.update_layout(
            title="IS element copy number per strain (⭐ = case study strains)",
            xaxis_title="Total IS element copy number",
            height=500, plot_bgcolor="rgba(0,0,0,0)", margin=dict(t=50,b=10,l=120))
        research_chart(fig_mge, use_container_width=True)

        st.divider()

    # ── Case studies side by side ─────────────────────────────
    st.markdown('<span class="section-header">Two evidence-bounded genomic case studies</span>',
                unsafe_allow_html=True)

    col_su4, col_gap, col_a539 = st.columns([1, 0.04, 1])

    with col_su4:
        st.markdown("""
        ### ⭐ *A. caviae* SU4
        **Source:** Retail sushi &nbsp;|&nbsp; **Species:** *A. caviae*
        """)
        st.markdown("""
        **Published account (not revalidated here):**
        A **Tn521 transposon** carrying a **mercury resistance operon**,
        co-localised with a **Class I integron** carrying antibiotic resistance genes.
        **Author-confirmed correction:** Tn521 is the correct designation.
        The preserved repository Table S4 cell D57 says Tn512; the current article already says Tn521.
        Derived labels use Tn521, with the source spelling retained in the reconciliation table.
        """)
        st.markdown("""
        | Gene | Resistance |
        |---|---|
        | `mer operon` | Mercury (heavy metal) |
        | `sul1` | Sulfonamides |
        | `qacEΔ1` | Efflux pump (disinfectants) |
        | `aadA1` | Aminoglycosides |
        | `tet(E)` | Tetracyclines |
        | `blaOXA-780` | β-lactams (Class D) |
        | `blaMOX-15` | β-lactams (Class C) |
        """)
        st.markdown("""
        <div class="critical-box">
        <strong>Potential co-selection:</strong><br>
        Genomic co-localisation is consistent with a co-selection hypothesis.
        Mercury exposure and selection of antibiotic resistance were not experimentally tested here.
        </div>
        """, unsafe_allow_html=True)
        st.caption("Conceptual schematic withheld pending verification of depicted genes and genomic context; the historical image file is preserved.")

    with col_gap:
        st.markdown("<div style='border-left:2px solid #e0e0e0;height:100%;'></div>",
                    unsafe_allow_html=True)

    with col_a539:
        st.markdown("""
        ### ⭐ *A. rivipollensis* A539
        **Source:** Retail sushi &nbsp;|&nbsp; **Species:** *A. rivipollensis*
        """)
        st.markdown("""
        **What was found:**
        An **IncQ1 plasmid** (6,535 bp) — a plasmid with mobilization-associated features —
        carrying **qnrS2**, which confers quinolone resistance.
        """)
        st.markdown("""
        | Element | Role |
        |---|---|
        | IncQ1 plasmid | Potentially mobilizable; transfer not tested here |
        | `repA/repC` | Replication proteins |
        | `mobA` | Mobilization-associated protein |
        | `qnrS2` | **Quinolone resistance** |
        """)
        st.markdown("""
        <div class="critical-box">
        <strong>Interpretation:</strong><br>
        qnrS2 is a quinolone-resistance gene, not an antibiotic.
        Its presence on the reported IncQ1 plasmid indicates potential mobility,
        not demonstrated aquaculture-to-human transmission or resistance to every quinolone.
        </div>
        """, unsafe_allow_html=True)
        st.caption("Conceptual schematic withheld pending verification of depicted genes and genomic context; the historical image file is preserved.")

    st.divider()

    st.markdown("### Interpretation boundary & One Health relevance")
    st.markdown("These observations motivate further surveillance and experimental work. They do not demonstrate the effectiveness of a regulation, establish population prevalence or constitute a regulatory recommendation or endorsement.")
    st.divider()
    st.caption(
        "📚 **Read more:** "
        "[Nautilus — Is Sushi a Health Hazard?](https://nautil.us/is-sushi-a-health-hazard-421668)  ·  "
        "[IFLScience](https://www.iflscience.com/how-safe-is-the-sushi-you-eat-really-70899)  ·  "
        "[Full paper (Open Access)](https://doi.org/10.3389/fmicb.2023.1175304)"
    )
