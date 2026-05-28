import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np

def prs_distribution_chart(population_prs: pd.Series, patient_prs: float) -> go.Figure:
    """Generates futuristic cohort distribution histograms."""
    fig = px.histogram(
        population_prs, nbins=40,
        title='Polygenic Risk Score (PRS) Distribution Across Cohort',
        labels={'value': 'PRS (z-score)'},
        template='plotly_dark'
    )
    fig.add_vline(x=patient_prs, line_color='#00f2fe', line_width=3,
                  annotation_text='PATIENT PRS', annotation_position='top right')
    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
        font_color='#e0e6ed', title_font_color='#00f2fe'
    )
    return fig

def manhattan_variant_plot(shap_df: pd.DataFrame) -> go.Figure:
    """Manhattan-style plot assessing relative feature contributions."""
    if 'pos' not in shap_df.columns:
        shap_df['pos'] = np.arange(len(shap_df))
    if 'chrom' not in shap_df.columns:
        shap_df['chrom'] = '1'
        
    fig = px.scatter(
        shap_df, x='pos', y=shap_df['shap_value'].abs(),
        color='chrom', hover_data=['rsid', 'shap_value'],
        title='Variant Contribution Weights (|SHAP|)',
        labels={'y': '|SHAP Value|', 'x': 'Genomic Coordinate'},
        template='plotly_dark'
    )
    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
        font_color='#e0e6ed', title_font_color='#9d4edd'
    )
    return fig

def shap_waterfall_plotly(shap_records: list) -> go.Figure:
    """Produces the individual localized feature effect diagrams."""
    features = [r['feature'] for r in shap_records]
    values = [r['shap_value'] for r in shap_records]
    colors = ['#ff007f' if v > 0 else '#00f2fe' for v in values]
    
    fig = go.Figure(go.Bar(
        x=values, y=features, orientation='h',
        marker_color=colors
    ))
    fig.update_layout(
        title='Top Variant Local Vector Adjustments',
        xaxis_title='SHAP Value (Risk Variance Contribution)',
        template='plotly_dark', height=380,
        paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
        font_color='#e0e6ed'
    )
    return fig
    
