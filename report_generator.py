from reportlab.platypus import SimpleDocTemplate, Paragraph, Table, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.pagesizes import A4
from io import BytesIO
import datetime

[span_128](start_span)def generate_pdf_report(prediction: dict, prs: float, prs_pct: float, shap_records: list) -> bytes:[span_128](end_span)
    [span_129](start_span)"""Creates a scientific-grade PDF report document."""[span_129](end_span)
    [span_130](start_span)buf = BytesIO()[span_130](end_span)
    [span_131](start_span)doc = SimpleDocTemplate(buf, pagesize=A4)[span_131](end_span)
    [span_132](start_span)styles = getSampleStyleSheet()[span_132](end_span)
    [span_133](start_span)story = [][span_133](end_span)
    
    [span_134](start_span)story.append(Paragraph('PolyRisk AI — Genomic Risk Report', styles['Title']))[span_134](end_span)
    [span_135](start_span)story.append(Paragraph(f'Generated: {datetime.datetime.now().strftime("%Y-%m-%d %H:%M")} | Research Isolation Protocol', styles['Normal']))[span_135](end_span)
    [span_136](start_span)story.append(Spacer(1, 12))[span_136](end_span)
    
    summary = [
        [span_137](start_span)['Metric', 'Value'],[span_137](end_span)
        [span_138](start_span)['Risk Label', prediction['risk_label']],[span_138](end_span)
        [span_139](start_span)['Risk Probability', f"{prediction['probability']:.1%}"],[span_139](end_span)
        [span_140](start_span)['PRS (z-score)', f'{prs:.3f}'],[span_140](end_span)
        [span_141](start_span)['PRS Percentile', f'{prs_pct:.0f}th percentile'],[span_141](end_span)
    ]
    [span_142](start_span)story.append(Table(summary))[span_142](end_span)
    [span_143](start_span)story.append(Spacer(1, 12))[span_143](end_span)
    
    [span_144](start_span)story.append(Paragraph('Top Contributing Variants (SHAP Local Model Validation)', styles['Heading2']))[span_144](end_span)
    [span_145](start_span)snp_data = [['Rank', 'SNP / Feature', 'SHAP Value', 'Dosage']][span_145](end_span)
    [span_146](start_span)for i, r in enumerate(shap_records, 1):[span_146](end_span)
        [span_147](start_span)snp_data.append([i, r['feature'], f"{r['shap_value']:+.4f}", r['dosage']])[span_147](end_span)
    [span_148](start_span)story.append(Table(snp_data))[span_148](end_span)
    
    [span_149](start_span)doc.build(story)[span_149](end_span)
    [span_150](start_span)return buf.getvalue()[span_150](end_span)

