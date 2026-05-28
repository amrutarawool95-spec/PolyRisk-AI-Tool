import pandas as pd
import numpy as np

[span_52](start_span)def compute_prs(dosage_df: pd.DataFrame, gwas_weights: pd.DataFrame) -> pd.Series:[span_52](end_span)
    [span_53](start_span)[span_54](start_span)"""Compute Polygenic Risk Score: sum(beta_i * dosage_i)."""[span_53](end_span)[span_54](end_span)
    [span_55](start_span)common_snps = list(set(dosage_df.columns) & set(gwas_weights['rsid']))[span_55](end_span)
    if not common_snps:
        [span_56](start_span)raise ValueError('No overlapping SNPs between data and GWAS weights')[span_56](end_span)
        
    [span_57](start_span)betas = gwas_weights.set_index('rsid').loc[common_snps, 'beta'][span_57](end_span)
    [span_58](start_span)X = dosage_df[common_snps].fillna(dosage_df[common_snps].mean())[span_58](end_span)
    
    [span_59](start_span)prs = X.dot(betas)[span_59](end_span)
    
    # [span_60](start_span)Cohort standardization safely fallbacks[span_60](end_span)
    if len(prs) > 1 and prs.std() > 0:
        [span_61](start_span)prs_z = (prs - prs.mean()) / prs.std()[span_61](end_span)
    else:
        prs_z = prs - prs.mean() # Normalization safety matrix
    return prs_z

[span_62](start_span)def prs_percentile(prs_value: float, population_prs: pd.Series) -> float:[span_62](end_span)
    [span_63](start_span)"""Return percentile rank of a patient against the reference distribution."""[span_63](end_span)
    if population_prs.empty:
        return 50.0
    [span_64](start_span)return (population_prs < prs_value).mean() * 100.0[span_64](end_span)

