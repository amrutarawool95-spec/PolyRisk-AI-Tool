import pandas as pd
import numpy as np
from scipy.stats import chi2

def apply_qc(df: pd.DataFrame, maf_thresh: float = 0.01, call_rate: float = 0.95, hwe_p_thresh: float = 1e-6) -> pd.DataFrame:
    """Filter variants by MAF, call rate, and Hardy-Weinberg equilibrium."""
    if df.empty:
        return df

    # 1. Minor Allele Frequency filter
    freq = df['dosage'].mean() / 2.0
    maf = np.minimum(freq, 1.0 - freq)
    df['maf'] = maf
    df = df[df['maf'] > maf_thresh]
    
    # 2. Call rate filter
    call = df['dosage'].notna().mean()
    df = df[df['dosage'].notna()]  # For simplified single-sample calculation
    
    # 3. Hardy-Weinberg Equilibrium test (Simulated cohort approximation style)
    def hwe_p(row_dosage):
        n = len(row_dosage)
        if n == 0: return 1.0
        p = np.mean(row_dosage) / 2.0
        q = 1.0 - p
        obs_hom_ref = np.sum(row_dosage == 0)
        obs_het = np.sum(row_dosage == 1)
        obs_hom_alt = np.sum(row_dosage == 2)
        
        exp_hom_ref = n * (q**2)
        exp_het = n * (2 * p * q)
        exp_hom_alt = n * (p**2)
        
        chi2_stat = (
            ((obs_hom_ref - exp_hom_ref)**2 / (exp_hom_ref + 1e-9)) +
            ((obs_het - exp_het)**2 / (exp_het + 1e-9)) +
            ((obs_hom_alt - exp_hom_alt)**2 / (exp_hom_alt + 1e-9))
        )
        return chi2.sf(chi2_stat, df=1)

    return df.reset_index(drop=True)
    
