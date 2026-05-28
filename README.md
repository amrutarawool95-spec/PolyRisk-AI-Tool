# 🧬 PolyRisk AI

### Polygenic Risk Scoring & Machine Learning-Based Disease Susceptibility Prediction Engine
*Quantum Computational Biology Platform (v2.4) — Research & Educational Use Only*

---

## 📋 Project Abstract
**PolyRisk AI** is an advanced, end-to-end genomic analytics platform designed to calculate polygenic risk scores (PRS) and deploy machine learning classifiers to evaluate individual multi-disease liabilities. The system accepts genetic variants in either uncompressed VCF or flat CSV formats, synchronizes strict quality control (QC) filtration parameters, and constructs integrated genomic feature matrices. 

By analyzing specific single nucleotide polymorphisms (SNPs) against established Genome-Wide Association Study (GWAS) weights, the tool provides predictive liability metrics alongside explainable AI feature interpretations via localized SHAP tree vectors. The responsive glassmorphic frontend UI offers real-time visualization dashboards (Manhattan plots, interactive cohort distributions) and builds downloadable cryptographic PDF research summaries.

---

## ⚡ Core Features
- **Flexible Variant Ingestion:** Dynamically parses and aligns genetic coordinates using automated uncompressed VCF mapping or flat CSV variant dosage schemas.
- **Strict Quality Control (QC):** Filters variant datasets by Minor Allele Frequency (MAF) thresholds, high call-rate integrity checks, and simulated Hardy-Weinberg Equilibrium (HWE) calculations.
- **Machine Learning Classifiers:** Combines classical polygenic risk scoring with a trained Random Forest or Gradient Boosting configuration pipeline to deliver risk probabilities.
- **Explainable AI (XAI):** Unpacks localized variant structural adjustments using a SHAP TreeExplainer module to determine top risk-driving loci.
- **Futuristic Visualization Dashboard:** Implements interactive Plotly population charts, custom HTML5 dynamic SVG risk gauges, and multi-locus scatter charts.
- **Automated Report Generation:** Automatically compiles patient analytics into structured, scientific-grade downloadable PDF risk summaries.

---

## 📂 Repository Architecture & Module Structure

The project code space is divided into modular, testable python components designed for smooth compilation pipeline routines:

* `app.py`: The core application framework establishing page parameters, handling sidebar selections, executing pipeline integration, and constructing the frontend layout.
* `vcf_parser.py`: Ingests and processes target coordinates; maps VCF inputs into memory-efficient dataframes via additive dosage (`0`, `1`, `2`) encoding.
* `qc_pipeline.py`: Handles validation checks across input markers, screening structural artifacts against baseline filter requirements.
* `feature_engineering.py`: Evaluates matrix profiles, scaling values and integrating multi-component ancestry Principal Components (PCs) for structural balance.
* `prs_calculator.py`: Executes standard polygenic calculations and maps results to standard reference scores to determine population percentile rankings.
* `ml_classifier.py`: Manages the pipeline training operations, scoring validation tasks, and translating inputs into explicit predictive probabilities.
* `shap_explainer.py`: Interfaces with the machine learning models to isolate weight behaviors, sorting localized features based on relative impact.
* `visualizations.py`: Constructs plot elements using customized template layouts matching the dark cybernetic aesthetic.
* `report_generator.py`: Generates the structured file byte stream for localized client distribution report requests.

---

## 🚀 Installation & Local Environment Setup

Ensure you have **Python 3.10+** configured on your local workstation before running the following commands in your terminal:

### 1. Clone the Repository
```bash
git clone [https://github.com/YOUR_USERNAME/polyrisk-ai.git](https://github.com/YOUR_USERNAME/polyrisk-ai.git)
cd polyrisk-ai
