import pandas as pd
import numpy as np

def compute_prs(dosage_df: pd.DataFrame, gwas_weights: pd.DataFrame) -> pd.Series:
    """Compute Polygenic Risk Score: sum(beta_i * dosage_i)."""
    common_snps = list(set(dosage_df.columns) & set(gwas_weights['rsid']))
    if not common_snps:
        raise ValueError('No overlapping SNPs between data and GWAS weights')
        
    betas = gwas_weights.set_index('rsid').loc[common_snps, 'beta']
    X = dosage_df[common_snps].fillna(dosage_df[common_snps].mean())
    
    prs = X.dot(betas)
    
    if len(prs) > 1 and prs.std() > 0:
        prs_z = (prs - prs.mean()) / prs.std()
    else:
        prs_z = prs - prs.mean() 
    return prs_z

def prs_percentile(prs_value: float, population_prs: pd.Series) -> float:
    """Return percentile rank of a patient against the reference distribution."""
    if population_prs.empty:
        return 50.0
    return (population_prs < prs_value).mean() * 100.0
    
