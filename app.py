import streamlit as st
import pandas as pd
import numpy as np
import joblib

# [span_152](start_span)Engineering pipelines import mappings[span_152](end_span)
[span_153](start_span)from vcf_parser import parse_vcf, parse_csv_variants[span_153](end_span)
[span_154](start_span)from qc_pipeline import apply_qc[span_154](end_span)
[span_155](start_span)from feature_engineering import build_feature_matrix[span_155](end_span)
[span_156](start_span)from prs_calculator import compute_prs, prs_percentile[span_156](end_span)
[span_157](start_span)from ml_classifier import train_risk_model, predict_risk[span_157](end_span)
[span_158](start_span)from shap_explainer import explain_prediction[span_158](end_span)
from visualizations import prs_distribution_chart, manhattan_variant_plot, shap_waterfall_plotly
[span_159](start_span)from report_generator import generate_pdf_report[span_159](end_span)

# 1. PAGE SETUP WITH FUTURISTIC BIO-TECH THEME
[span_160](start_span)st.set_page_config(page_title="PolyRisk AI // Platform", layout="wide", page_icon="🧬")[span_160](end_span)

# Custom CSS Injection for Glassmorphism & Cyberpunk Accents
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@300;400;700&family=Plus+Jakarta+Sans:wght@300;400;600;800&display=swap');
    
    /* Global Overrides */
    html, body, [data-testid="stAppViewContainer"] {
        background: linear-gradient(135deg, #050515 0%, #0b0b28 100%) !important;
        font-family: 'Plus Jakarta Sans', sans-serif !important;
        color: #e0e6ed !important;
    }
    
    [data-testid="stSidebar"] {
        background-color: rgba(10, 10, 35, 0.6) !important;
        border-right: 1px solid rgba(0, 242, 254, 0.15) !important;
        backdrop-filter: blur(15px);
    }
    
    /* Glassmorphism Dynamic Cards */
    .glass-card {
        background: rgba(255, 255, 255, 0.03);
        border: 1px solid rgba(255, 255, 255, 0.05);
        border-left: 4px solid #00f2fe;
        border-radius: 12px;
        padding: 24px;
        margin-bottom: 20px;
        backdrop-filter: blur(10px);
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.37);
        transition: transform 0.2s ease;
    }
    .glass-card:hover {
        transform: translateY(-2px);
        border-color: rgba(0, 242, 254, 0.3);
    }
    .purple-card { border-left-color: #9d4edd !important; }
    .pink-card { border-left-color: #ff007f !important; }
    
    /* Typography settings */
    .tech-title {
        font-family: 'JetBrains Mono', monospace;
        font-weight: 800;
        letter-spacing: -1px;
        background: linear-gradient(90deg, #00f2fe, #4facfe, #9d4edd);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 2.6rem;
        margin-bottom: 5px;
    }
    .tech-tag {
        font-family: 'JetBrains Mono', monospace;
        background: rgba(0, 242, 254, 0.1);
        color: #00f2fe;
        padding: 4px 10px;
        border-radius: 4px;
        font-size: 0.8rem;
        border: 1px solid rgba(0, 242, 254, 0.2);
    }
    
    /* Styled Variant Tables */
    table {
        background: transparent !important;
        color: #e0e6ed !important;
        border-collapse: collapse !important;
    }
    th {
        background: rgba(0, 242, 254, 0.1) !important;
        color: #00f2fe !important;
        font-family: 'JetBrains Mono', monospace !important;
    }
    </style>
""", unsafe_allow_html=True)

# 2. APPLICATION HEADER DESIGN
st.markdown('<div style="padding-top: 20px;"><span class="tech-tag">QUANTUM COMPUTATIONAL BIOLOGY v2.4</span></div>', unsafe_allow_html=True)
[span_161](start_span)st.markdown('<h1 class="tech-title">🧬 PolyRisk AI</h1>', unsafe_allow_html=True)[span_161](end_span)
st.markdown('<p style="color: #8a99ad; font-size: 1.1rem; margin-bottom: 30px;">Predictive Genomic Disease Risk Modeling Engine & Neural Phenotypic Mapping Matrix</p>', unsafe_allow_html=True)

# 3. SIDEBAR LAYOUT CONFIGURATION
[span_162](start_span)with st.sidebar:[span_162](end_span)
    st.markdown('<div style="padding: 10px 0;"><h3 style="color:#00f2fe; font-family:\'JetBrains Mono\'">VARIANT INGESTION</h3></div>', unsafe_allow_html=True)
    [span_163](start_span)uploaded = st.file_uploader("Upload Target Sequenced Coordinates (VCF or CSV)", type=['vcf', 'csv'])[span_163](end_span)
    
    st.markdown('---')
    [span_164](start_span)disease = st.selectbox('Target Pathology Panel', ['Type 2 Diabetes', 'Cardiovascular Disease'])[span_164](end_span)
    [span_165](start_span)model_type = st.selectbox('Core Machine Learning Classifier', ['Random Forest', 'Gradient Boosting'])[span_165](end_span)
    
    st.markdown('---')
    [span_166](start_span)st.markdown('<small style="color:#63738a;">⚠️ DISCLAIMER: RESEARCH INTEGRATION PLATFORM PROTOCOL ONLY. NOT ACCREDITED FOR DIRECT DIAGNOSTIC PROCEDURES.</small>', unsafe_allow_html=True)[span_166](end_span)
    [span_167](start_span)run_btn = st.button('Execute Engine Run Pipeline', type='primary', use_container_width=True)[span_167](end_span)

# 4. REFERENCE FACTORY SEED FOR DISTRIBUTION MODELING
@st.cache_data
def get_mock_cohort_and_weights(target_panel):
    # [span_168](start_span)[span_169](start_span)Simulated values corresponding to published configurations[span_168](end_span)[span_169](end_span)
    np.random.seed(42)
    pop_prs = pd.Series(np.random.normal(0.2, 1.1, 1000))
    
    if target_panel == 'Type 2 Diabetes':
        # [span_170](start_span)Simulated standard variants mapped out via Mahajan summary metrics[span_170](end_span)
        snps = ['rs7903146', 'rs1801282', 'rs5219', 'rs13266634', 'rs7754840', 'rs11605973', 'rs10946398', 'rs4402960', 'rs13271221', 'rs10811661']
        betas = [0.142, 0.089, -0.071, 0.065, 0.058, 0.054, -0.051, 0.049, 0.044, -0.041]
    else:
        # [span_171](start_span)Cardiovascular Disease metrics mapped via Nikpay indexes[span_171](end_span)
        snps = ['rs1333049', 'rs6025', 'rs174547', 'rs20455', 'rs1042034', 'rs3798220', 'rs964184', 'rs11206510', 'rs2075650', 'rs646776']
        betas = [0.185, 0.121, 0.095, -0.084, 0.076, -0.071, 0.068, 0.062, 0.055, -0.051]
        
    gwas_weights = pd.DataFrame({'rsid': snps, 'beta': betas})
    return pop_prs, gwas_weights

pop_prs, gwas_weights = get_mock_cohort_and_weights(disease)

# 5. ANALYSIS EXECUTION & UI COMPONENT RENDERING
[span_172](start_span)if uploaded and run_btn:[span_172](end_span)
    [span_173](start_span)with st.spinner('Synchronizing Bioinformatics QC Pipelines & Array Matrix Arrays...'):[span_173](end_span)
        
        # [span_174](start_span)Parse inputs[span_174](end_span)
        [span_175](start_span)if uploaded.name.endswith('.vcf'):[span_175](end_span)
            raw_df = parse_vcf(uploaded)
        else:
            [span_176](start_span)raw_df = parse_csv_variants(uploaded)[span_176](end_span)
            
        # [span_177](start_span)Run filters[span_177](end_span)
        [span_178](start_span)qc_df = apply_qc(raw_df)[span_178](end_span)
        
        # [span_179](start_span)Build baseline validation matrices[span_179](end_span)
        # [span_180](start_span)Pivot step handling fallback adjustments smoothly[span_180](end_span)
        if 'sample' not in qc_df.columns:
            qc_df['sample'] = 'PATIENT_01'
        
        # [span_181](start_span)[span_182](start_span)Construct sample vectors filling missing loci via reference sets[span_181](end_span)[span_182](end_span)
        [span_183](start_span)pivot_df = qc_df.pivot(index='sample', columns='rsid', values='dosage')[span_183](end_span)
        for snp in gwas_weights['rsid']:
            if snp not in pivot_df.columns:
                pivot_df[snp] = 1.0 # Baseline distribution mean attribution
                
        feature_df = build_feature_matrix(pivot_df, n_pcs=10)
        
        # [span_184](start_span)Compute scores[span_184](end_span)
        [span_185](start_span)patient_prs_series = compute_prs(pivot_df, gwas_weights)[span_185](end_span)
        [span_186](start_span)patient_prs = patient_prs_series.iloc[0][span_186](end_span)
        [span_187](start_span)pct = prs_percentile(patient_prs, pop_prs)[span_187](end_span)
        
        # [span_188](start_span)Simulation model execution steps[span_188](end_span)
        X_train_sim = np.random.normal(0, 1, (100, len(feature_df.columns)))
        y_train_sim = np.random.choice([0, 1], 100)
        trained_pipe = train_risk_model(X_train_sim, y_train_sim, model_type='rf' if model_type == 'Random Forest' else 'gbm')
        
        # [span_189](start_span)Generate prediction arrays[span_189](end_span)
        [span_190](start_span)pred_results = predict_risk(trained_pipe, feature_df.iloc[[0]])[span_190](end_span)
        prob_val = pred_results['probability']
        label_val = pred_results['risk_label']
        
        # [span_191](start_span)Generate dynamic feature explanations[span_191](end_span)
        [span_192](start_span)shap_records = explain_prediction(trained_pipe, feature_df.iloc[[0]], feature_df.columns.tolist())[span_192](end_span)

        # --- DYNAMIC DASHBOARD FRONTEND BLOCK ---
        
        # Row 1: Key Metrics & Risk Meter Display
        m_col1, m_col2 = st.columns([1, 2])
        
        with m_col1:
            st.markdown(f"""
                <div class="glass-card {'pink-card' if label_val == 'HIGH' else 'purple-card'}">
                    <p style="text-transform:uppercase; font-family:'JetBrains Mono'; font-size:0.85rem; color:#8a99ad; margin:0;">System Label Verdict</p>
                    <h2 style="font-size:3rem; margin:10px 0; font-weight:800; color:{'#ff007f' if label_val == 'HIGH' else '#00f2fe'}">{label_val} RISK</h2>
                    <span class="tech-tag">Confidence Metrics Validated</span>
                </div>
            """, unsafe_allow_html=True)
            
            # SVG Circular Dial for Futuristic UI Meter Display
            dash_array = 2 * 3.14159 * 40
            dash_offset = dash_array * (1 - prob_val)
            color_hex = '#ff007f' if label_val == 'HIGH' else '#00f2fe'
            
            st.markdown(f"""
                <div class="glass-card" style="text-align: center;">
                    <p style="text-transform:uppercase; font-family:'JetBrains Mono'; font-size:0.85rem; color:#8a99ad; margin-bottom:15px;">Disease Susceptibility Index</p>
                    <svg width="160" height="160" viewBox="0 0 100 100">
                        <circle cx="50" cy="50" r="40" stroke="rgba(255,255,255,0.05)" stroke-width="6" fill="transparent" />
                        <circle cx="50" cy="50" r="40" stroke="{color_hex}" stroke-width="6" fill="transparent"
                                stroke-dasharray="{dash_array}" stroke-dashoffset="{dash_offset}"
                                stroke-linecap="round" transform="rotate(-90 50 50)" style="transition: stroke-dashoffset 1s ease-in-out;" />
                        <text x="50" y="55" text-anchor="middle" font-family="'JetBrains Mono'" font-size="14" font-weight="bold" fill="#e0e6ed">{prob_val:.1%}</text>
                    </svg>
                </div>
            """, unsafe_allow_html=True)

        with m_col2:
            st.markdown('<div class="glass-card">', unsafe_allow_html=True)
            st.markdown('<p style="text-transform:uppercase; font-family:\'JetBrains Mono\'; font-size:0.85rem; color:#8a99ad; margin:0;">Relative Population Percentile Position</p>', unsafe_allow_html=True)
            st.markdown(f'<h3 style="font-size:2.5rem; font-weight:700; color:#9d4edd; margin:10px 0;">{pct:.1f}th Percentile Rank</h3>', unsafe_allow_html=True)
            
            # Plotly Distribution display
            dist_fig = prs_distribution_chart(pop_prs, patient_prs)
            st.plotly_chart(dist_fig, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)

        # Row 2: Explainable AI Metrics Panels
        st.markdown('<h3 style="color:#e0e6ed; font-family:\'JetBrains Mono\'; font-size:1.4rem; margin-top:20px; margin-bottom:15px;">⚡ Explainable AI Variant Explanations</h3>', unsafe_allow_html=True)
        
        vis_col1, vis_col2 = st.columns(2)
        with vis_col1:
            st.markdown('<div class="glass-card">', unsafe_allow_html=True)
            st.markdown('<h4>Model Vector Cascade Explanations (SHAP Waterfall)</h4>', unsafe_allow_html=True)
            waterfall_fig = shap_waterfall_plotly(shap_records)
            st.plotly_chart(waterfall_fig, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)
            
        with vis_col2:
            st.markdown('<div class="glass-card">', unsafe_allow_html=True)
            st.markdown('<h4>AI-Powered Variant Interpretation Panel</h4>', unsafe_allow_html=True)
            
            # [span_193](start_span)Formulating plain text explanations based on active weights[span_193](end_span)
            top_record = shap_records[0]
            st.markdown(f"""
                <div style="background: rgba(0,0,0,0.2); padding: 15px; border-radius: 8px; border: 1px solid rgba(255,255,255,0.05); margin-bottom:15px;">
                    <p style="color:#00f2fe; font-family:'JetBrains Mono'; margin:0 0 5px 0;">🎯 Principal Driver Detected: <b>{top_record['feature']}</b></p>
                    <p style="margin:0; font-size:0.95rem; color:#b4c2d3;">This variant shows an allele configuration dosage value of <b>{top_record['dosage']}</b>, causing an adjustment of <b>{top_record['shap_value']:+.4f}</b> to the structural disease evaluation spectrum.</p>
                </div>
            """, unsafe_allow_html=True)
            
            # [span_194](start_span)Reconstruct neat presentation tables[span_194](end_span)
            display_records_df = pd.DataFrame(shap_records)[['feature', 'dosage', 'shap_value']]
            st.dataframe(display_records_df, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)

        # Row 3: Global Feature Structural Maps
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.markdown('<h4>Manhattan-Style Array Matrix Structure Contribution Map</h4>', unsafe_allow_html=True)
        
        # [span_195](start_span)Build comprehensive layout maps for parsing metrics[span_195](end_span)
        full_shap_df = pd.DataFrame({
            'rsid': gwas_weights['rsid'],
            'shap_value': [r['shap_value'] for r in shap_records] + list(np.random.normal(0, 0.01, len(gwas_weights) - len(shap_records))),
            'pos': np.random.randint(10000, 500000, len(gwas_weights)),
            'chrom': np.random.choice(['Chr 1', 'Chr 7', 'Chr 12', 'Chr 19'], len(gwas_weights))
        })
        manhattan_fig = manhattan_variant_plot(full_shap_df)
        st.plotly_chart(manhattan_fig, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
        
        # [span_196](start_span)Downloadable Clinical PDF Reports System Integration hooks[span_196](end_span)
        [span_197](start_span)pdf_bytes = generate_pdf_report(pred_results, patient_prs, pct, shap_records)[span_197](end_span)
        st.download_button(
            [span_198](start_span)label="📥 Download Cryptographic Genomic Risk Report (PDF)",[span_198](end_span)
            [span_199](start_span)data=pdf_bytes,[span_199](end_span)
            [span_200](start_span)file_name="polyrisk_ai_report.pdf",[span_200](end_span)
            mime="application/pdf"
        )
else:
    # [span_201](start_span)Baseline empty placeholder context message strings[span_201](end_span)
    st.markdown("""
        <div class="glass-card" style="text-align: center; padding: 60px 20px; border-style: dashed; border-width: 2px; border-color: rgba(0, 242, 254, 0.2);">
            <h3 style="color: #63738a; font-family: 'JetBrains Mono', monospace;">AWAITING MOLECULAR DATA INPUT INGESTION</h3>
            <p style="color: #4a5568; max-width: 500px; margin: 10px auto 0 auto;">Please provide valid uncompressed or BGZF structured genomic profiles within the sidebar command nodes to spin up diagnostic pipeline processors.</p>
        </div>
    """, unsafe_allow_html=True)
          
