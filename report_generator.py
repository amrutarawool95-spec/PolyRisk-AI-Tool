from reportlab.platypus import SimpleDocTemplate, Paragraph, Table, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.pagesizes import A4
from io import BytesIO
import datetime

def generate_pdf_report(prediction: dict, prs: float, prs_pct: float, shap_records: list) -> bytes:
    """Creates a scientific-grade PDF report document."""
    buf = BytesIO()
    doc = SimpleDocTemplate(buf, pagesize=A4)
    styles = getSampleStyleSheet()
    story = []
    
    story.append(Paragraph('PolyRisk AI — Genomic Risk Report', styles['Title']))
    story.append(Paragraph(f'Generated: {datetime.datetime.now().strftime("%Y-%m-%d %H:%M")} | Research Isolation Protocol', styles['Normal']))
    story.append(Spacer(1, 12))
    
    summary = [
        ['Metric', 'Value'],
        ['Risk Label', prediction['risk_label']],
        ['Risk Probability', f"{prediction['probability']:.1%}"],
        ['PRS (z-score)', f'{prs:.3f}'],
        ['PRS Percentile', f'{prs_pct:.0f}th percentile'],
    ]
    story.append(Table(summary))
    story.append(Spacer(1, 12))
    
    story.append(Paragraph('Top Contributing Variants (SHAP Local Model Validation)', styles['Heading2']))
    snp_data = [['Rank', 'SNP / Feature', 'SHAP Value', 'Dosage']]
    for i, r in enumerate(shap_records, 1):
        snp_data.append([i, r['feature'], f"{r['shap_value']:+.4f}", r['dosage']])
    story.append(Table(snp_data))
    
    doc.build(story)
    return buf.getvalue()
    
