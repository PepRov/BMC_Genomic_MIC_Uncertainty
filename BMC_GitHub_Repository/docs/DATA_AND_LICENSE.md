# Data provenance and public-release checks

The selected files derive from the prior Model C MIC-prediction workflow and its Bayesian follow-up, and include BioSample accession identifiers, antibiotic names, fold assignments, observed MIC values, model predictions and posterior summaries. They do not include raw genomic sequence files. A content and structural review found no embedded personal computer paths, email addresses or credentials in these distributed datasets or notebook code. This check does not establish every source's legal redistribution rights.

## Verified original data source and attribution

The original laboratory MIC observations used by Model C were obtained from the **NCBI Pathogen Detection Antibiotic Susceptibility Test (AST) Browser**, as stated in the published Model C article. The Browser presents submitter-provided isolate AST measurements associated with NCBI BioSample records, including downloadable MIC data. The files in this repository are derived analytical tables: they combine observed MIC values and public BioSample accession identifiers with this study's Model C/BMC predictions, calibration records, fold assignments and aggregate summaries. No raw sequences or patient-level metadata are included.

Primary references and policies:

- NCBI Pathogen Detection AST Browser documentation: https://www.ncbi.nlm.nih.gov/pathogens/docs/ast/
- NCBI BioSample database: https://www.ncbi.nlm.nih.gov/biosample/
- NCBI Policies and Disclaimers, section **Molecular Data Usage**: https://www.ncbi.nlm.nih.gov/home/about/policies/
- NCBI guidance on citing Pathogen Detection and acknowledging original submitters: https://www.ncbi.nlm.nih.gov/core/assets/pathogens/files/HowTo/how_to_cite_pathogen_detection.pdf
- Source study: Mikawa YG (2026). *A sequence-informed hybrid framework for predicting antibiotic minimum inhibitory concentrations in previously unseen Escherichia coli pathogens*. Journal of Microbiological Methods, 251:107767. https://doi.org/10.1016/j.mimet.2026.107767

**Use and redistribution distinction:** NCBI says it imposes no restrictions of its own on use and distribution of molecular database content, but some original submitters may retain intellectual-property claims; NCBI cannot grant those third-party rights. This is not a blanket, independently verified licence for every original record. BioSample accessions are biological specimen references, not patient identifiers; nevertheless, clinical sample provenance should be handled as public BioSample data rather than as de-identified patient-level data.

In any public repository, retain the accession identifiers and cite NCBI's AST Browser and the Model C publication. Where practicable, also acknowledge any identifiable original data submitters or linked studies. If a specific record is later discovered to carry an applicable restriction, assess or remove that record rather than assuming all submitters have granted unrestricted sublicensing rights.

## Release considerations

- Source attribution is documented here; no individual-submitters' permissions have been established or represented as granted.
- Do not assign a Creative Commons licence to upstream NCBI/submitter data on their behalf. A future licence for the author's original code and derived materials should explicitly exclude upstream third-party content unless rights have been established.
- NCBI's AST Browser is updated over time; this repository's validation cohort is a fixed historic analytical subset, not necessarily identical to a fresh AST Browser download.
- Avoid committing unreviewed new notebook outputs, especially `*.json` provenance reports containing absolute local filesystem paths. The reviewed CSVs and clean notebook source have undergone separate privacy screening.

## Biological and clinical interpretation

Five pathogen-disjoint outer folds yield 50,460 independently evaluated pathogen–antibiotic MIC observations for 9,058 BioSamples; the 201,840 NB40 calibration records correspond to overlapping outer-training sets and are not 201,840 independent samples. The threshold-exceedance analyses apply to 18 EUCAST v16.1 scenario-specific thresholds, with 27,315 held-out MIC observations. Infection indication and specimen source are unknown; exceedance of an indication-specific numerical breakpoint does not, by itself, demonstrate clinical resistance for all infections. Further external validation is required before any clinical deployment.

Additional cautions: trimethoprim–sulfamethoxazole MIC interpretation depends on the trimethoprim component scale; piperacillin–tazobactam has an area of technical uncertainty; and groups with sparse positive outcomes can have unstable calibration estimates.
