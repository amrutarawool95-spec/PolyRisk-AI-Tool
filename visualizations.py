import plotly.express as px
import plotly.graph_objects as go
import numpy as np
import pandas as pd

def plot_manhattan(df):
    """Generates an interactive genomic Manhattan Plot across tracking blocks."""
    plot_df = df.copy()
    plot_df['-log10_p'] = -np.log10(plot_df['p_value'])
    
    fig = px.scatter(
        plot_df, x='pos', y='-log10_p', color='chrom',
        title="Genomic Association Loci (Manhattan Plot)",
        color_discrete_sequence=['#ff007f', '#00f2fe', '#7928ca', '#ffaa00'],
        template="plotly_dark"
    )
    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
        xaxis_title="Chromosomal Position Coordinate", yxaxis_title="-log10(p-value)"
    )
    return fig

def plot_cohort_distribution(prs_score, target_disease):
    """Generates a smooth Gaussian curve isolating where this genetic sample balances."""
    x = np.linspace(-4, 4, 100)
    y = np.exp(-x**2 / 2) / np.sqrt(2 * np.pi)
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=x, y=y, mode='lines', name='Global Cohort Distribution', line=dict(color='rgba(255,255,255,0.2)', width=2)))
    
    # Trace specific individual line flag marker
    fig.add_vline(x=max(-3.5, min(3.5, (prs_score % 4) - 2)), line_width=4, line_color="#ff007f", annotation_text="Target Patient Trajectory")
    
    fig.update_layout(
        title="Population Genetic Trajectory",
        template="plotly_dark", paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
        margin=dict(l=20, r=20, t=40, b=20)
    )
    return fig
    
