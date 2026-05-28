import pandas as pd
from cyvcf2 import VCF

def parse_vcf(vcf_path: str, sample_id: str = None) -> pd.DataFrame:
    """Parse a VCF file into a tidy DataFrame with additive dosage encoding."""
    vcf = VCF(vcf_path)
    samples = vcf.samples
    [span_1](start_span)target = sample_id if sample_id and sample_id in samples else samples[0][span_1](end_span)
    [span_2](start_span)idx = samples.index(target)[span_2](end_span)
    
    records = []
    for variant in vcf:
        [span_3](start_span)gt = variant.genotypes[idx][span_3](end_span)
        # Dosage calculation: sum of alternative alleles (0, 1, or 2)
        [span_4](start_span)dosage = sum([a for a in gt[:2] if a >= 0])[span_4](end_span)
        
        records.append({
            [span_5](start_span)"rsid": variant.ID if variant.ID else f"{variant.CHROM}:{variant.POS}",[span_5](end_span)
            [span_6](start_span)"chrom": variant.CHROM,[span_6](end_span)
            [span_7](start_span)"pos": variant.POS,[span_7](end_span)
            [span_8](start_span)"ref": variant.REF,[span_8](end_span)
            [span_9](start_span)"alt": str(variant.ALT[0]),[span_9](end_span)
            [span_10](start_span)"dosage": dosage,[span_10](end_span)
            [span_11](start_span)"qual": variant.QUAL[span_11](end_span)
        })
    return pd.DataFrame(records)

[span_12](start_span)def parse_csv_variants(csv_path: str) -> pd.DataFrame:[span_12](end_span)
    [span_13](start_span)"""Accept flat CSV with columns: rsid, chrom, pos, ref, alt, dosage."""[span_13](end_span)
    [span_14](start_span)df = pd.read_csv(csv_path)[span_14](end_span)
    [span_15](start_span)required = ['rsid', 'chrom', 'pos', 'ref', 'alt', 'dosage'][span_15](end_span)
    [span_16](start_span)missing = set(required) - set(df.columns)[span_16](end_span)
    if missing:
        [span_17](start_span)raise ValueError(f'Missing required columns: {missing}')[span_17](end_span)
    [span_18](start_span)df['dosage'] = pd.to_numeric(df['dosage'], errors='coerce').fillna(0).clip(0, 2)[span_18](end_span)
    return df
      
