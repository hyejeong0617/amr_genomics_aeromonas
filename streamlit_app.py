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
    page_title="The Silent Pandemic on Your Plate",
    page_icon="🍣",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── CSS ───────────────────────────────────────────────────────
st.markdown("""
<style>
/* Section headers — white text on coloured background */
.section-header {
    font-size: 1.05rem;
    font-weight: 700;
    color: #ffffff !important;
    background: #0f3460;
    padding: 0.5rem 1rem;
    border-radius: 6px;
    margin: 1.4rem 0 0.8rem 0;
    display: block;
}
/* Coloured insight boxes */
.insight-box {
    background: #e8f4fd !important;
    border-left: 4px solid #2196F3;
    padding: 0.75rem 1rem;
    border-radius: 0 8px 8px 0;
    margin: 0.7rem 0;
    font-size: 0.9rem;
    color: #1a1a2e !important;
}
.warning-box {
    background: #fff3e0 !important;
    border-left: 4px solid #FF9800;
    padding: 0.75rem 1rem;
    border-radius: 0 8px 8px 0;
    margin: 0.7rem 0;
    font-size: 0.9rem;
    color: #1a1a2e !important;
}
.critical-box {
    background: #fce4ec !important;
    border-left: 4px solid #e91e63;
    padding: 0.75rem 1rem;
    border-radius: 0 8px 8px 0;
    margin: 0.7rem 0;
    font-size: 0.9rem;
    color: #1a1a2e !important;
}
.green-box {
    background: #e8f5e9 !important;
    border-left: 4px solid #4CAF50;
    padding: 0.75rem 1rem;
    border-radius: 0 8px 8px 0;
    margin: 0.7rem 0;
    font-size: 0.9rem;
    color: #1a1a2e !important;
}
/* Strain tag */
.strain-tag {
    display: inline-block;
    background: #f0f4f8;
    border: 1px solid #d0dde8;
    border-radius: 4px;
    padding: 2px 6px;
    font-size: 0.78rem;
    font-family: monospace;
    color: #0f3460;
}
/* Number badge */
.num-badge {
    display: inline-block;
    background: #0f3460;
    color: white;
    border-radius: 50%;
    width: 28px; height: 28px;
    text-align: center;
    line-height: 28px;
    font-weight: 700;
    font-size: 0.9rem;
    margin-right: 6px;
}
</style>
""", unsafe_allow_html=True)

# ── Data ──────────────────────────────────────────────────────
PROC = Path("data/processed")
RAW  = Path("data/raw")

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
    "AMP":"Beta-lactams","MEL":"Beta-lactams",
    "CTX":"Cephalosporins","CRO":"Cephalosporins",
    "CIP":"Quinolones","OA":"Quinolones",
    "DO":"Tetracyclines","TE":"Tetracyclines",
    "IPM":"Carbapenems","MEM":"Carbapenems",
    "GM":"Aminoglycosides","TOB":"Aminoglycosides",
    "EM":"Macrolides","FEC":"Amphenicols","STX":"Amphenicols",
}
CLASS_COLOR = {
    "Beta-lactams":"#E07B54","Cephalosporins":"#D4A843",
    "Quinolones":"#C4706A","Carbapenems":"#9B7BB8",
    "Tetracyclines":"#6BAF92","Aminoglycosides":"#5B8DB8",
    "Macrolides":"#7BA87B","Amphenicols":"#8AA6C4",
}
species_fix = {
    "A.salmonicida":"A. salmonicida","A.bestiarum":"A. bestiarum",
    "A. bestarium":"A. bestiarum","A. media ?":"A. media",
}
amr_long["abx_label"] = amr_long["antibiotic"].str.strip().map(ABX_SHORT)
amr_long["abx_class"] = amr_long["abx_label"].map(ABX_CLASS)
amr_long["species"]   = amr_long["species_id"].replace(species_fix)
amr_wide["species"]   = amr_wide["species_id"].replace(species_fix)

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
        The Silent Pandemic
on Your Plate
      </p>
      <p style="font-size:0.78rem; color:#a8c8e8; text-align:center; margin:0;">
        Antibiotic resistance in<br>ready-to-eat seafood
      </p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("### Navigate")
    page = st.radio("section", [
        "🍣  The Story",
        "🦠  The Bacteria",
        "💊  Antibiotic Resistance",
        "🧬  How Resistance Spreads",
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
        "[![GitHub](https://img.shields.io/badge/💻_GitHub-Code-black)](https://github.com/hyejeong0617/amr-genomics-aeromonas)  \n"
        "[![Nautilus](https://img.shields.io/badge/🔬_Nautilus-Article-green)](https://nautil.us/is-sushi-a-health-hazard-421668)  \n"
        "[![IFLScience](https://img.shields.io/badge/🌐_IFLScience-Article-orange)](https://www.iflscience.com/how-safe-is-the-sushi-you-eat-really-70899)"
    )


# ════════════════════════════════════════════════════════════
# PAGE 1 — THE STORY
# ════════════════════════════════════════════════════════════
if page == "🍣  The Story":

    st.title("🍣 Is Your Sushi Safe?")
    st.markdown(
        "Sushi is one of the world's most popular foods — "
        "but what's living inside it that you can't see?"
    )
    st.divider()


    # ── Research overview — visual diagram ───────────────────
    st.markdown('<span class="section-header">🔬 From Grocery Store to Genome — Research Overview</span>',
                unsafe_allow_html=True)

    st.markdown(
        "*Norwegian researchers bought retail sushi, salmon, oysters and scallops — "
        "and instead of eating them, sequenced the bacteria inside. "
        "They found* ***Aeromonas*** *strains carrying* **antibiotic-resistance genes** "
        "*— with no visible warning sign at the grocery store.*  \n"
        "*† AMR: the ability of a microorganism to resist antimicrobial agents (WHO, 2023)*"
    )
    st.write("")

    # HTML flexbox pipeline — large readable text
    pipe_html = """
    <div style="display:flex;gap:6px;margin:0.5rem 0 1rem 0;">

      <div style="flex:1;background:#5B8DB8;border-radius:10px;padding:1rem 0.5rem;
                  text-align:center;color:white;">
        <div style="font-size:1.5rem;">🛒</div>
        <div style="font-size:1rem;font-weight:700;margin:0.3rem 0;">Collect</div>
        <div style="font-size:0.85rem;line-height:1.5;">Retail sushi,<br>salmon loins,<br>oysters &amp; scallops<br>— Norway</div>
      </div>

      <div style="display:flex;align-items:center;color:#888;font-size:1.2rem;padding:0 2px;">→</div>

      <div style="flex:1;background:#6BAF92;border-radius:10px;padding:1rem 0.5rem;
                  text-align:center;color:white;">
        <div style="font-size:1.5rem;">🧫</div>
        <div style="font-size:1rem;font-weight:700;margin:0.3rem 0;">Culture &amp;<br>Identify</div>
        <div style="font-size:0.85rem;line-height:1.5;">Isolated Aeromonas<br>gyrB sequencing<br><b>79 isolates</b></div>
      </div>

      <div style="display:flex;align-items:center;color:#888;font-size:1.2rem;padding:0 2px;">→</div>

      <div style="flex:1;background:#D4A843;border-radius:10px;padding:1rem 0.5rem;
                  text-align:center;color:white;">
        <div style="font-size:1.5rem;">💉</div>
        <div style="font-size:1rem;font-weight:700;margin:0.3rem 0;">Antibiotic<br>Resistance Test</div>
        <div style="font-size:0.85rem;line-height:1.5;">Disk diffusion<br>15 antibiotics<br>CLSI standard<br>→ MDR classif.<br><b>79 isolates</b></div>
      </div>

      <div style="display:flex;align-items:center;color:#888;font-size:1.2rem;padding:0 2px;">→</div>

      <div style="flex:1.1;background:#E07B54;border-radius:10px;padding:1rem 0.5rem;
                  text-align:center;color:white;border:3px solid #fffde7;">
        <div style="font-size:1.5rem;">🔍</div>
        <div style="font-size:1rem;font-weight:700;margin:0.3rem 0;">Select 22<br>for WGS</div>
        <div style="font-size:0.85rem;line-height:1.5;">Species diversity<br>+ resistance pattern<br>→ <b>22 strains</b> chosen</div>
      </div>

      <div style="display:flex;align-items:center;color:#888;font-size:1.2rem;padding:0 2px;">→</div>

      <div style="flex:1;background:#9B7BB8;border-radius:10px;padding:1rem 0.5rem;
                  text-align:center;color:white;border:3px dashed #E07B54;">
        <div style="font-size:1.5rem;">🧬</div>
        <div style="font-size:1rem;font-weight:700;margin:0.3rem 0;">Sequence<br>Genomes</div>
        <div style="font-size:0.85rem;line-height:1.5;">Illumina MiSeq<br>2×300 bp<br>SPAdes assembly<br><b>22 genomes</b></div>
      </div>

      <div style="display:flex;align-items:center;color:#888;font-size:1.2rem;padding:0 2px;">→</div>

      <div style="flex:1;background:#C4706A;border-radius:10px;padding:1rem 0.5rem;
                  text-align:center;color:white;border:3px dashed #E07B54;">
        <div style="font-size:1.5rem;">💻</div>
        <div style="font-size:1rem;font-weight:700;margin:0.3rem 0;">Molecular<br>Analysis</div>
        <div style="font-size:0.85rem;line-height:1.5;">AMRFinderPlus<br>VFDB · FastANI<br>MobileElementFinder<br><b>22 genomes</b></div>
      </div>

    </div>
    <p style="font-size:0.78rem;color:#888;margin-top:0.2rem;">
    ↑ Orange dashed border = whole-genome sequencing phase (22 strains only)
    </p>
    """
    st.markdown(pipe_html, unsafe_allow_html=True)

    # ── Key numbers ──────────────────────────────────────────
    c1,c2,c3,c4,c5 = st.columns(5)
    stats = [
        ("79","Seafood samples","Retail sushi, salmon, oysters, scallops — Norway"),
        ("22","Genomes sequenced","Full WGS: Illumina MiSeq 2×300 bp, SPAdes assembly"),
        ("8","Aeromonas species","Identified by MLPA (6 housekeeping genes) + ANI"),
        ("57%","Multidrug-resistant","MDR = resistant to ≥3 antibiotic classes"),
        ("2","Mobile resistance\ngenes found","Plasmid + transposon-linked transferable AMR genes"),
    ]
    for col,(val,lab,tip) in zip([c1,c2,c3,c4,c5], stats):
        col.markdown(f"""
        <div style="text-align:center;background:white;border:1px solid #e0e0e0;
                    border-radius:10px;padding:0.9rem 0.5rem;
                    box-shadow:0 2px 6px rgba(0,0,0,0.07);">
            <div style="font-size:1.9rem;font-weight:800;color:#0f3460;">{val}</div>
            <div style="font-size:0.8rem;color:#555;margin-top:0.2rem;">{lab}</div>
        </div>
        """, unsafe_allow_html=True)
        col.caption(tip)

    st.markdown("""
    <div class="insight-box" style="margin-top:1rem;">
    💡 <strong>Navigate the sections</strong> using the sidebar to explore:
    the bacteria found (🦠), their antibiotic resistance profiles (💊),
    and how resistance genes travel through the food chain (🧬).
    </div>
    """, unsafe_allow_html=True)
    
    st.divider()

    # ── AMR — why it matters (from lecture) ──────────────────
    st.markdown('<span class="section-header">🌍 Antimicrobial Resistance — The Silent Pandemic</span>',
                unsafe_allow_html=True)

    col_def, col_stats = st.columns([1.2, 1])
    with col_def:
        st.markdown("""
**Antimicrobial resistance (AMR)** is the ability of a microorganism to
resist the action of an antimicrobial agent — ranked by WHO as one of the
**top 10 global public health threats** facing humanity.

**How does resistance arise?**
- **Intrinsic resistance** — naturally present in the species
- **Acquired resistance** — gained through mutation or horizontal gene transfer (HGT)

**How does it spread?**
Bacteria share resistance genes via **mobile genetic elements** (MGEs):
plasmids, transposons, integrons — the molecular vehicles of AMR.

**Why food matters:**
The food chain is a **silent highway** connecting aquaculture → seafood →
your gut bacteria → potential pathogens.
        """)

    with col_stats:
        fig_amr = go.Figure()
        categories = ["Directly caused\nby AMR (2019)", "Associated with\nAMR (2019)",
                      "Projected deaths\nby 2050"]
        values     = [1.27, 4.95, 10.0]
        colors     = ["#E07B54", "#C4706A", "#9B7BB8"]
        fig_amr.add_trace(go.Bar(
            y=categories, x=values, orientation="h",
            marker_color=colors,
            text=[f"{v}M" for v in values], textposition="outside",
            hovertemplate="%{y}: %{x}M deaths per year<extra></extra>",
        ))
        fig_amr.update_layout(
            title=dict(text="Global AMR Death Burden<br><sup>Source: Murray et al. 2022 (The Lancet); UNEP 2023</sup>",
                       font_size=12),
            xaxis=dict(title="Deaths (millions)", range=[0, 13]),
            height=240, margin=dict(l=10, r=80, t=50, b=10),
            plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
        )
        st.plotly_chart(fig_amr, use_container_width=True)

        st.markdown("""
        <div class="warning-box">
        ⚠️ AMR kills more people than HIV/AIDS and tuberculosis <strong>combined</strong>.
        Without action, it could claim <strong>10 million lives per year by 2050</strong> —
        rivalling cancer.
        </div>
        """, unsafe_allow_html=True)

    st.divider()


# ════════════════════════════════════════════════════════════
# PAGE 2 — THE BACTERIA
# ════════════════════════════════════════════════════════════
elif page == "🦠  The Bacteria":

    st.title("🦠 The Bacteria Found in Retail Seafood")
    st.markdown(
        "22 *Aeromonas* strains were whole-genome sequenced. "
        "They represent **8 different species**, each with a distinct profile "
        "of virulence factors and antibiotic resistance genes."
    )

    # ── Species + source overview ─────────────────────────────
    st.markdown('<span class="section-header">📍 Species found in retail seafood</span>',
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
        st.plotly_chart(fig_sp, use_container_width=True)

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
        st.plotly_chart(fig_src, use_container_width=True)

    with st.expander("🔍 View all 22 strains"):
        disp = strain_sum.copy()
        disp.columns = ["Strain ID","Species","Isolation Source","NCBI Accession"]
        st.dataframe(disp, use_container_width=True, hide_index=True)
        st.caption(
            "Strain IDs reflect origin: SU = retail sushi, SL = salmon loin, "
            "OY = oyster, SC = scallop, LJP/A = salmon processing environment or archived isolates."
        )

    st.divider()

    # ── ANI interactive heatmap ───────────────────────────────
    st.markdown('<span class="section-header">🧬 Are they really 8 different species? — ANI Analysis</span>',
                unsafe_allow_html=True)

    st.markdown("""
    **Average Nucleotide Identity (ANI)** compares the DNA sequences of two genomes
    to determine if they belong to the same species. For *Aeromonas*, a threshold
    of **ANI ≥ 96%** confirms same-species assignment.
    Hover over cells to inspect pairwise ANI values.
    """)

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
        width=900, height=750,
        xaxis=dict(tickangle=45, tickfont=dict(size=8)),
        yaxis=dict(tickfont=dict(size=8), autorange="reversed"),
        margin=dict(l=160, b=160, r=60, t=70),
    )
    st.plotly_chart(fig_ani, use_container_width=True)

    st.markdown("""
    <div class="insight-box">
    💡 <strong>Key finding from ANI:</strong>
    Strains A533 & A536 (<i>A. dhakensis</i>) and SU3, SU9 & SU15
    (<i>A. rivipollensis</i>) show ANI ≥ 99.9% — they are
    <strong>genetically identical strains</strong> isolated from different sushi products.
    Only one representative per identical pair was used in downstream analysis
    (final dataset: <strong>19 representative strains</strong>).
    </div>
    """, unsafe_allow_html=True)

    st.divider()

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

**More factors = potentially more dangerous.**
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
        st.plotly_chart(fig_vfhm, use_container_width=True)

    st.markdown("""
    <div class="warning-box">
    ⚠️ <strong>Key finding:</strong> <i>A. piscicola</i>, <i>A. bestiarum</i>,
    <i>A. salmonicida</i>, <i>A. hydrophila</i>, and <i>A. dhakensis</i>
    carry significantly more virulence factors than <i>A. caviae</i>,
    <i>A. media</i>, and <i>A. rivipollensis</i> — consistent with their
    known roles as human pathogens in clinical settings.
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
    st.plotly_chart(fig_vf, use_container_width=True)


# ════════════════════════════════════════════════════════════
# PAGE 3 — ANTIBIOTIC RESISTANCE
# ════════════════════════════════════════════════════════════
elif page == "💊  Antibiotic Resistance":

    st.title("💊 Antibiotic Resistance in *Aeromonas*")
    st.markdown("""
    Two complementary analyses were performed:
    - **22 WGS strains** → both phenotypic (disk diffusion) and genotypic (AMR genes) profiles
    - **79 isolates** → phenotypic resistance to map MDR distribution across all retail seafood samples
    """)

    st.divider()

    # ── SECTION 1: 22-strain genotypic vs phenotypic ─────────
    st.markdown('<span class="section-header">🔬 22 WGS strains — Phenotypic vs Genotypic AMR profiles</span>',
                unsafe_allow_html=True)

    st.markdown("""
    For the 22 genome-sequenced strains, we compared:
    **phenotypic resistance** (disk diffusion — what happens in the lab)
    vs **genotypic resistance** (AMR genes detected in the genome).
    This comparison reveals which genes drive observed resistance — and
    highlights cases of **discordance** (resistance not explained by known genes,
    or genes present without phenotypic effect).
    """)

    # Genotypic heatmap (Table 1)
    table1_data = [
        ["SU4",    "A. caviae",        "",            "blaMOX-15",   "blaOXA-780",  "tet(E),qacEΔ1","sul1,aadA1"],
        ["A533",   "A. dhakensis",     "cphA2",       "blaAQU",      "blaOXA-12",   "",""],
        ["A537",   "A. hydrophila",    "cphA2",       "cepS",        "blaOXA-12",   "tet(E)",""],
        ["A539",   "A. rivipollensis", "",            "",            "blaOXA-427",  "","qnrS2"],
        ["SU3",    "A. rivipollensis", "",            "",            "blaOXA-427",  "",""],
        ["SC42",   "A. rivipollensis", "",            "",            "blaOXA-427",  "",""],
        ["OY1",    "A. rivipollensis", "",            "",            "blaOXA-427",  "",""],
        ["OY52",   "A. media",         "",            "blaMOX-9",    "blaOXA-427",  "",""],
        ["SU6",    "A. bestiarum",     "cphA1",       "",            "blaOXA-956",  "",""],
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
    st.plotly_chart(fig_geno, use_container_width=True)

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
- *A. rivipollensis / media* → blaOXA-427 only
- *A. caviae / dhakensis / hydrophila* → mixed profile

**All 19 strains carry at least one AMR gene.**
        """)

    st.markdown('<span class="section-header">🔎 Individual strain phenotypic profile</span>',
                unsafe_allow_html=True)

    wgs_strains = t1["strain"].tolist()
    sel_iso = st.selectbox("Select a WGS strain", wgs_strains)
    iso_row = amr_wide[amr_wide["isolate_id"]==sel_iso]
    if len(iso_row) == 0:
        iso_row = amr_wide[amr_wide["isolate_id"].str.startswith(sel_iso[:3])]
    if len(iso_row) > 0:
        iso_row = iso_row.iloc[0]
        iso_long = amr_long[amr_long["isolate_id"]==sel_iso]
        if len(iso_long)==0:
            iso_long = amr_long[amr_long["isolate_id"].str.startswith(sel_iso[:3])]
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
        st.plotly_chart(fig_iso, use_container_width=True)

    st.divider()

    # ── SECTION 2: 79-strain MDR overview ────────────────────
    st.markdown('<span class="section-header">📊 79 isolates — MDR overview across all retail seafood</span>',
                unsafe_allow_html=True)

    st.markdown("""
    All 79 isolates were tested against 15 antibiotics by disk diffusion.
    This broader dataset captures the **full scope of MDR** in retail seafood —
    across all sources and years sampled.
    """)

    # MDR summary
    n_tot = amr_wide["isolate_id"].nunique()
    n_mdr = int(amr_wide["MDR"].sum())
    c1,c2,c3,c4 = st.columns(4)
    c1.metric("Total isolates", n_tot)
    c2.metric("MDR isolates", n_mdr, f"{n_mdr/n_tot*100:.0f}% of total")
    c3.metric("Antibiotics tested", 15, "8 classes")
    c4.metric("100% resistant to", "Ampicillin", "intrinsic in Aeromonas")

    # MDR by species
    iso_meta = amr_long[["isolate_id","species","MDR"]].drop_duplicates("isolate_id")
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
        st.plotly_chart(fig_mdr, use_container_width=True)

    with col_m2:
        fig_pct = go.Figure(go.Bar(
            y=mdr_sp["species"], x=mdr_sp["mdr_pct"], orientation="h",
            marker_color=mdr_sp["color"],
            text=mdr_sp["mdr_pct"].apply(lambda v:f"{v:.0f}%"), textposition="outside"))
        fig_pct.add_vline(x=57, line_dash="dash", line_color="#555",
            annotation_text="Overall 57%", annotation_position="top")
        fig_pct.update_layout(
            title="MDR rate (%) per species",
            xaxis=dict(title="MDR rate (%)", range=[0,120]),
            height=280, margin=dict(t=40,b=10,r=60),
            plot_bgcolor="rgba(0,0,0,0)")
        st.plotly_chart(fig_pct, use_container_width=True)

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
    st.plotly_chart(fig_r, use_container_width=True)

    with st.expander("📖 Antibiotic abbreviations"):
        st.dataframe(
            pd.DataFrame([{"Abbr.":k,"Full name":v,"Class":ABX_CLASS.get(k,"")}
                          for k,v in ABX_FULL.items()]),
            hide_index=True, use_container_width=True)

    st.markdown("""
    <div class="critical-box">
    🚨 <strong>Concerning findings:</strong>
    <b>100%</b> resist Ampicillin (intrinsic).
    <b>57%</b> resist Erythromycin — used for atypical pneumonia.
    <b>48%</b> resist Florfenicol — a veterinary antibiotic marker for food-chain contamination.
    <b>10%</b> resist Imipenem — a last-resort carbapenem antibiotic for life-threatening infections.
    </div>
    """, unsafe_allow_html=True)


# ════════════════════════════════════════════════════════════
# PAGE 4 — HOW RESISTANCE SPREADS
# ════════════════════════════════════════════════════════════
elif page == "🧬  How Resistance Spreads":

    st.title("🧬 How Resistance Genes Travel Through the Food Chain")
    st.markdown("""
    Some *Aeromonas* strains carry **mobile genetic elements (MGEs)** —
    molecular vehicles that move resistance genes between bacteria,
    even across different species.
    This is how resistance spreads silently from aquaculture
    through the food chain into human pathogens.
    """)
    st.markdown("""
    <div class="warning-box">
    ⚠️ <strong>Why MGEs matter:</strong>
    Chromosomal resistance stays within one species.
    <strong>MGEs can jump to other bacteria</strong> — including pathogens like
    <i>Salmonella</i>, <i>E. coli</i>, or <i>Klebsiella</i> —
    making those infections untreatable with the antibiotics we rely on.
    </div>
    """, unsafe_allow_html=True)

    st.divider()

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
    st.plotly_chart(fig_mge, use_container_width=True)

    st.divider()

    # ── Case studies side by side ─────────────────────────────
    st.markdown('<span class="section-header">⭐ Two critical case studies</span>',
                unsafe_allow_html=True)

    col_su4, col_gap, col_a539 = st.columns([1, 0.04, 1])

    with col_su4:
        st.markdown("""
        ### ⭐ *A. caviae* SU4
        **Source:** Retail sushi &nbsp;|&nbsp; **Species:** *A. caviae*
        """)
        st.markdown("""
        **What was found:**
        A **Tn521 transposon** carrying a **mercury resistance operon**,
        co-localised with a **Class I integron** carrying antibiotic resistance genes.
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
        🚨 <strong>Co-selection mechanism:</strong><br>
        Mercury contamination in aquatic environments selects for bacteria
        carrying Tn521 — and these bacteria <strong>simultaneously maintain
        antibiotic resistance genes</strong> in the same genetic element.
        <br><br>
        <strong>No antibiotic pressure needed — mercury does the job.</strong>
        This is a direct link between <em>environmental pollution</em>
        and <em>antibiotic resistance in food</em>.
        </div>
        """, unsafe_allow_html=True)
        try:
            st.image(str(PROC/"fig_case_SU4.png"),
                     caption="SU4: Tn521 + Class I integron + AMR gene cluster",
                     use_column_width=True)
        except Exception:
            st.info("fig_case_SU4.png not found.")

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
        An **IncQ1 plasmid** (6,535 bp) — a small, self-mobilisable piece of DNA —
        carrying **qnrS2**, which confers quinolone resistance.
        """)
        st.markdown("""
        | Element | Role |
        |---|---|
        | IncQ1 plasmid | Highly mobile — transfers between species |
        | `repA/B/C` | Replication proteins |
        | `mobA` | Mobilisation — enables transfer |
        | `qnrS2` | **Quinolone resistance** |
        """)
        st.markdown("""
        <div class="critical-box">
        🚨 <strong>Why quinolone resistance matters:</strong><br>
        Quinolones (ciprofloxacin, oxolinic acid) treat serious infections —
        UTIs, pneumonia, sepsis.
        <br><br>
        The IncQ1 plasmid is one of the <strong>most promiscuous</strong>
        plasmid types — it can transfer to <em>unrelated bacterial species</em>
        in the same environment (e.g. gut, seafood surface, water).
        <br><br>
        <strong>qnrS2 was the most commonly used antibiotic in Norwegian aquaculture.</strong>
        This is a direct link from aquaculture → retail food → human health risk.
        </div>
        """, unsafe_allow_html=True)
        try:
            st.image(str(PROC/"fig_case_A539.png"),
                     caption="A539: IncQ1 plasmid carrying qnrS2 (quinolone resistance)",
                     use_column_width=True)
        except Exception:
            st.info("fig_case_A539.png not found.")

    st.divider()

    # ── One Health + Policy ───────────────────────────────────
    st.markdown('<span class="section-header">🌍 What does this mean? — One Health & Policy implications</span>',
                unsafe_allow_html=True)

    col_pol, col_sol = st.columns([1.3, 1])
    with col_pol:
        st.markdown("""
        | Research finding | Policy implication |
        |---|---|
        | 57% of retail seafood bacteria are MDR | AMR surveillance must include **food-borne non-pathogens**, not only clinical isolates |
        | Mercury contamination co-selects for antibiotic resistance | **Environmental pollution control = AMR control** |
        | Plasmid-mediated quinolone resistance in retail sushi | **Stricter AMR monitoring** of ready-to-eat seafood at point of sale |
        | 8 *Aeromonas* species, all carrying virulence genes | **One Health approach** — aquatic, food, and clinical environments must be monitored together |
        | Norway's strict antibiotic regulation works | Restrict aquaculture antibiotic use: from **48 tonnes (1987)** to **<1 tonne (2021)** |
        """)

    with col_sol:
        st.markdown("""
        <div class="green-box">
        <strong>💡 The solution is not to stop eating sushi.</strong>
        <br><br>
        It's to build cleaner, more sustainable food production systems
        and to integrate food chain monitoring into national and
        European AMR surveillance programmes.
        <br><br>
        Norway's aquaculture model shows it's possible:
        strict regulation + vaccination + monitoring =
        dramatic reduction in antibiotic use without sacrificing production.
        <br><br>
        <em>— Lee et al. (2023); WHO Global Action Plan on AMR; EU Commission 2021</em>
        </div>
        """, unsafe_allow_html=True)

    st.divider()
    st.caption(
        "📚 **Read more:** "
        "[Nautilus — Is Sushi a Health Hazard?](https://nautil.us/is-sushi-a-health-hazard-421668)  ·  "
        "[IFLScience](https://www.iflscience.com/how-safe-is-the-sushi-you-eat-really-70899)  ·  "
        "[Full paper (Open Access)](https://doi.org/10.3389/fmicb.2023.1175304)"
    )
