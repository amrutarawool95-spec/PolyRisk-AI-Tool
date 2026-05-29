import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from vcf_parser import universal_file_parser
from qc_pipeline import run_quality_control
from feature_engineering import build_feature_matrix
from prs_calculator import calculate_prs_score
from ml_classifier import predict_disease_risk
from shap_explainer import generate_shap_values
from visualizations import plot_manhattan, plot_cohort_distribution
from report_generator import generate_pdf_report

# -------------------------------------------------------------
# 1. PLATFORM CONFIGURATION & CONFIG MATRIX
# -------------------------------------------------------------
st.set_page_config(
    page_title="PolyRisk AI // Computational Genome Engine",
    page_icon="🧬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom inject glassmorphic theme styling variables 
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght=300;400;600;700&family=JetBrains+Mono:wght=300;400;500&display=swap');
    
    html, body, [data-testid="stAppViewContainer"] {
        background-color: #050515 !important;
        color: #e0e6ed !important;
        font-family: 'Space Grotesk', sans-serif !important;
    }
    [data-testid="stSidebar"] {
        background-color: rgba(10, 10, 30, 0.7) !important;
        backdrop-filter: blur(20px) !important;
        border-right: 1px solid rgba(0, 242, 254, 0.15) !important;
    }
    div[data-testid="stBlock"] {
        background: rgba(255, 255, 255, 0.02) !important;
        backdrop-filter: blur(12px) !important;
        border-radius: 16px !important;
        border: 1px solid rgba(255, 255, 255, 0.05) !important;
        padding: 24px !important;
        margin-bottom: 20px !important;
    }
    h1, h2, h3 {
        font-family: 'Space Grotesk', sans-serif !important;
        font-weight: 700 !important;
        letter-spacing: -0.5px !important;
    }
    code, pre {
        font-family: 'JetBrains Mono', monospace !important;
    }
    .stButton>button {
        background: linear-gradient(135deg, #ff007f 0%, #7928ca 100%) !important;
        color: white !important;
        border: none !important;
        border-radius: 8px !important;
        font-weight: 600 !important;
        letter-spacing: 0.5px !important;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
        box-shadow: 0 4px 15px rgba(255, 0, 127, 0.3) !important;
    }
    .stButton>button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 6px 20px rgba(255, 0, 127, 0.5) !important;
    }
    </style>
""", unsafe_allow_html=True)

# -------------------------------------------------------------
# 2. APPLICATION HEADER CORE
# -------------------------------------------------------------
st.markdown("""
    <div style='margin-bottom: 35px;'>
        <p style='font-family: monospace; color: #00f2fe; font-weight: bold; font-size: 11px; margin-bottom: 4px;'>
            QUANTUM COMPUTATIONAL BIOLOGY v2.4 // ENGINE CORE
        </p>
        <h1 style='font-size: 42px; margin: 0; background: linear-gradient(to right, #fff, #8a99ad); -webkit-background-clip: text; -webkit-text-fill-color: transparent;'>
            🧬 PolyRisk AI
        </h1>
        <p style='color: #8a99ad; font-size: 16px; margin-top: 5px; font-weight: 300;'>
            Polygenic Risk Scoring & Machine Learning-Based Disease Susceptibility Prediction Engine
        </p>
    </div>
""", unsafe_allow_html=True)

# -------------------------------------------------------------
# 3. SIDEBAR COMPONENT: FILE INGESTION & CONFIGURATIONS
# -------------------------------------------------------------
with st.sidebar:
    st.markdown("### 📥 Variant Ingestion Panel")
    uploaded = st.file_uploader(
        "Upload Target Sequenced Coordinates", 
        type=["vcf", "csv", "gz", "vfc", "cvs"], 
        help="Accepts clinical variants formatted as standard or compressed files."
    )
    
    st.markdown("---")
    st.markdown("### ⚙️ Pipeline Tuning Matrices")
    target_disease = st.selectbox(
        "Select Target Pathology Evaluation",
        ["Type 2 Diabetes (T2D)", "Cardiovascular Disease (CVD)", "Alzheimer's Disease (AD)"]
    )
    model_type = st.selectbox(
        "Classification Engine Logic",
        ["Gradient Boosting Matrix", "Random Forest Classifier", "Standard PRS Summation"]
    )
    
    st.markdown("---")
    st.markdown("### 🧬 Quality Control Sieve (QC)")
    maf_threshold = st.slider("Minor Allele Frequency (MAF)", 0.00, 0.10, 0.01, step=0.005)
    call_rate = st.slider("Call Rate Filter Threshold", 0.80, 1.00, 0.95, step=0.01)

# -------------------------------------------------------------
# 4. DEFAULT SCREEN / INSTRUCTION MARGIN
# -------------------------------------------------------------
if uploaded is None:
    st.info("💡 Operational Status: Awaiting Ingestion Array. Drop a sample format data matrix inside the sidebar layout to initialize engine tasks.")
    
    col_info1, col_info2 = st.columns(2)
    with col_info1:
        st.markdown("""
            ### 🛠️ Execution Requirements
            Your sample variant files must explicitly present standard genomic position keys:
            - **VCF / VCF.GZ Structure:** Conforming to genomic specification arrays containing variant nodes.
            - **CSV Data Blocks:** Must feature column declarations including `rsid`, `chrom`, `pos`, `ref`, `alt`, and `dosage` measurements.
        """)
    with col_info2:
        st.markdown("""
            ### 🔬 Prototype Engine Parameters
            - **Core Process Engine:** Real-time alignment against vetted multi-locus GWAS weights.
            - **Transparency Track:** Individual asset assessments backed by Shapley game-theoretic vector traces.
        """)

# -------------------------------------------------------------
# 5. ANALYSIS EXECUTION & UI COMPONENT RENDERING
# -------------------------------------------------------------
else:
    with st.spinner("⏳ Engine Processing... Decompressing and parsing variant configurations..."):
        try:
            # Route through unified robust parsing layer
            raw_df = universal_file_parser(uploaded)
            
            # Execute Pipeline Sequence Modules
            qc_df = run_quality_control(raw_df, maf_threshold, call_rate)
            feature_matrix = build_feature_matrix(qc_df)
            prs_score, percentile = calculate_prs_score(feature_matrix, target_disease)
            risk_probability = predict_disease_risk(feature_matrix, target_disease, model_type)
            shap_values, feature_names = generate_shap_values(feature_matrix, target_disease)
            
            # -------------------------------------------------------------
            # METRIC METERS RENDER BLOCKS
            # -------------------------------------------------------------
            col_m1, col_m2, col_m3 = st.columns(3)
            
            with col_m1:
                verdict = "HIGH RISK" if risk_probability >= 0.65 else ("MODERATE" if risk_probability >= 0.35 else "LOW RISK")
                color_v = "#ff007f" if verdict == "HIGH RISK" else ("#ffaa00" if verdict == "MODERATE" else "#00f2fe")
                st.markdown(f"""
                    <div style='text-align: center;'>
                        <p style='font-size: 11px; font-family: monospace; color: #8a99ad; margin: 0;'>SYSTEM DIAGNOSTIC VERDICT</p>
                        <h2 style='color: {color_v}; font-size: 38px; margin: 10px 0;'>{verdict}</h2>
                        <p style='font-size: 12px; color: #63738a; margin: 0;'>Confidence Status: Validated Array Matrix</p>
                    </div>
                """, unsafe_allow_html=True)
                
            with col_m2:
                stroke_dash = int(2 * np.pi * 45)
                filled_dash = int((risk_probability) * stroke_dash)
                remain_dash = stroke_dash - filled_dash
                
                st.markdown(f"""
                    <div style='text-align: center; position: relative;'>
                        <p style='font-size: 11px; font-family: monospace; color: #8a99ad; margin: 0 0 5px 0;'>SUSCEPTIBILITY PROBABILITY</p>
                        <svg width="100" height="100" viewBox="0 0 100 100">
                            <circle cx="50" cy="50" r="45" fill="none" stroke="rgba(255,255,255,0.03)" stroke-width="7"/>
                            <circle cx="50" cy="50" r="45" fill="none" stroke="#ff007f" stroke-width="6" 
                                    stroke-dasharray="{filled_dash} {remain_dash}" stroke-linecap="round" transform="rotate(-90 50 50)"/>
                            <text x="50" y="55" font-family="'JetBrains Mono', monospace" font-size="18" fill="#fff" font-weight="bold" text-anchor="middle">
                                {risk_probability * 100:.1f}%
                            </text>
                        </svg>
                    </div>
                """, unsafe_allow_html=True)
                
            with col_m3:
                st.markdown(f"""
                    <div style='text-align: center;'>
                        <p style='font-size: 11px; font-family: monospace; color: #8a99ad; margin: 0;'>POPULATION PERCENTILE</p>
                        <h2 style='color: #ffffff; font-size: 38px; margin: 10px 0;'>{percentile}th</h2>
                        <p style='font-size: 12px; color: #63738a; margin: 0;'>Relative positioning within global cohort scale</p>
                    </div>
                """, unsafe_allow_html=True)
                
            # -------------------------------------------------------------
            # INTERACTIVE VISUALIZATION COMPONENT LAYOUTS
            # -------------------------------------------------------------
            st.markdown("### 📊 Distribution Profile Matrix & Genomic Loci Scans")
            col_v1, col_v2 = st.columns([3, 2])
            
            with col_v1:
                fig_dist = plot_cohort_distribution(prs_score, target_disease)
                st.plotly_chart(fig_dist, use_container_width=True)
                
            with col_v2:
                fig_man = plot_manhattan(qc_df)
                st.plotly_chart(fig_man, use_container_width=True)
                
            # -------------------------------------------------------------
            # EXPLAINABLE AI (SHAP ENGINE WATERFALL RENDER)
            # -------------------------------------------------------------
            st.markdown("### ⚡ AI-Powered Variant Interpretation (SHAP Overview)")
            
            shap_df = pd.DataFrame({'Variant Locus': feature_names, 'SHAP Value': shap_values})
            shap_df['Direction'] = np.where(shap_df['SHAP Value'] > 0, 'Risk Driver (+)', 'Protective Node (-)')
            shap_df = shap_df.sort_values(by='SHAP Value', key=abs, ascending=False).head(8)
            
            fig_shap = px.bar(
                shap_df,
                x='SHAP Value',
                y='Variant Locus',
                color='Direction',
                orientation='h',
                color_discrete_map={'Risk Driver (+)': '#ff007f', 'Protective Node (-)': '#00f2fe'},
                template='plotly_dark'
            )
            fig_shap.update_layout(
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                xaxis_title="Impact Score Dimension (Log-Odds Weighting)",
                yaxis_title=None,
                margin=dict(l=20, r=20, t=10, b=20),
                legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
            )
            fig_shap.update_xaxes(showgrid=True, gridcolor='rgba(255,255,255,0.05)', zeroline=True, zerolinecolor='rgba(255,255,255,0.2)')
            fig_shap.update_yaxes(showgrid=False)
            st.plotly_chart(fig_shap, use_container_width=True)
            
            # -------------------------------------------------------------
            # PROGRAMMATIC PDF REPORT DOWNLOAD
            # -------------------------------------------------------------
            st.markdown("---")
            st.markdown("### 🗃️ Client Export Center center")
            
            pdf_bytes = generate_pdf_report(qc_df, risk_probability, percentile, target_disease, model_type)
            st.download_button(
                label="📥 Download Cryptographic PDF Research Summary",
                data=pdf_bytes,
                file_name=f"PolyRisk_AI_Report_{target_disease.split()[0]}.pdf",
                mime="application/pdf"
            )
            
        except Exception as e:
            st.error(f"❌ Critical Pipeline Failure Event: {str(e)}")
            st.exception(e)
                
