import pandas as pd
from cyvcf2 import VCF

def parse_vcf(vcf_path: str, sample_id: str = None) -> pd.DataFrame:
    """Parse a VCF file into a tidy DataFrame with additive dosage encoding."""
    vcf = VCF(vcf_path)
    samples = vcf.samples
    target = sample_id if sample_id and sample_id in samples else samples[0]
    idx = samples.index(target)
    
    records = []
    for variant in vcf:
        gt = variant.genotypes[idx]
        # Dosage calculation: sum of alternative alleles (0, 1, or 2)
        dosage = sum([a for a in gt[:2] if a >= 0])
        
        records.append({
            "rsid": variant.ID if variant.ID else f"{variant.CHROM}:{variant.POS}",
            "chrom": variant.CHROM,
            "pos": variant.POS,
            "ref": variant.REF,
            "alt": str(variant.ALT[0]),
            "dosage": dosage,
            "qual": variant.QUAL
        })
    return pd.DataFrame(records)

def parse_csv_variants(csv_path: str) -> pd.DataFrame:
    """Accept flat CSV with columns: rsid, chrom, pos, ref, alt, dosage."""
    df = pd.read_csv(csv_path)
    required = ['rsid', 'chrom', 'pos', 'ref', 'alt', 'dosage']
    missing = set(required) - set(df.columns)
    if missing:
        raise ValueError(f'Missing required columns: {missing}')
    df['dosage'] = pd.to_numeric(df['dosage'], errors='coerce').fillna(0).clip(0, 2)
    return df
    
