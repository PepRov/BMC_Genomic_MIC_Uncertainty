# Bayesian Uncertainty in Genomic MIC Prediction (BMC)

Research code and selected, validated intermediate data accompanying the manuscript **“Bayesian Uncertainty in Genomic MIC Prediction.”** This work extends unchanged Model C point predictions of antibiotic minimum inhibitory concentration (MIC) to posterior predictive MIC distributions and antibiotic-specific resistance-threshold exceedance probabilities.

The evaluation comprises **9,058 *Escherichia coli* BioSamples**, **26 antibiotics**, **50,460 independently held-out pathogen–antibiotic MIC observations**, and **five pathogen-disjoint outer folds**. The models are **BMC-N** (normal error), **BMC-T** (Student's t error, degrees of freedom 4), and **BMC-AT** (asymmetric t error, degrees of freedom 4). The probability analyses cover **18 antibiotic-specific threshold scenarios** and **27,315 held-out observations**.

This package contains **14 source notebooks**, **11 reviewed data files**, an independently tested standalone Figure 4 notebook, and a validation utility. The source notebooks recovered from the author's ChatGPT Library preserve the source-cell content; they are reconstructed from valid text exports rather than raw byte-for-byte notebook downloads. Computed notebook outputs are not embedded in the original notebooks.

## Repository contents

- `01_Notebooks/`: notebooks 39–43, 47, 50–55, Figure02 v0.3 and Figure04 v0.5.
- `03_Results/`: reviewed input/intermediate datasets, retaining the subdirectory names expected by the notebooks.
- `Figures/`: regenerated Figure 4 (PNG/PDF), reliability-bin CSV and a validation report.
- `verify_package.py`: quick checks of counts, links, and reported outcomes; **does not refit Bayesian models**.
- `docs/REPRODUCIBILITY_SCOPE.md`: what can and cannot be rerun without original upstream Model C resources.
- `docs/DATA_AND_LICENSE.md`: source attribution, data provenance and release cautions.
- `MANIFEST_SHA256.txt`: SHA-256 hashes of archive contents (excluding this manifest).

## Setup

Install Python (3.10 or newer recommended) and the dependencies:

```bash
python -m pip install -r requirements.txt
```

Set `BMC_PROJECT_ROOT` to **the extracted repository directory** before starting Jupyter. For example, open a terminal in that directory:

```bash
export BMC_PROJECT_ROOT="$(pwd)"
python -m jupyter lab
```

The notebooks were originally written for Google Colab, but most support local Jupyter through `BMC_PROJECT_ROOT`; their original scientific code has not been edited. In a Colab session, set the environment variable to a location containing this repository's `03_Results/` folder before executing the notebook. See `docs/REPRODUCIBILITY_SCOPE.md` for upstream exceptions.

Check the packaged data without fitting models:

```bash
python verify_package.py
```

**Note:** The figure-generation notebook `Figure04_BMCN_Probability_Calibration_v0.5.ipynb` contains only audited aggregate plotting bins and can run by itself in an otherwise empty notebook directory. The underlying record-level NB55 dataset is provided separately in `03_Results/` for auditability. There is no need to set `BMC_PROJECT_ROOT` for this notebook.

## Notebook sequence

The data in `03_Results/` are already computed, so each downstream notebook can be run from its appropriate predecessor's stored output; you do **not** need to recompute the expensive upstream Model C steps.

| Notebook | Purpose | Inputs / conditions |
|---|---|---|
| NB39 | Original Model C data audit | **Upstream original Model C files required; not supplied here** |
| NB40 | Reconstruct training-only predictions | **Three original Model C archives required; not supplied here**; its two final outputs are included |
| NB41 | Fit and validate BMC-N | Two NB40 datasets (included) |
| NB42 | Fit and validate BMC-T | Two NB40 datasets (included) |
| NB43 | Fit and validate BMC-AT | NB40 datasets and NB41–42 outputs (included) |
| NB47 | Define genomic groups | **Original genomic embedding and interaction files required; not supplied here**; its group assignments are included |
| NB50 | Genomic-group uncertainty audit | NB41–43 predictions and NB47 assignments (included) |
| NB51 | Compare four interval methods | NB40 calibration/test and NB41–43 predictions (included) |
| NB52 v0.3 | Draw manuscript Figure 3 | NB41 predictions (included) |
| NB53 | Resistance-threshold coverage, Table S1 | NB41 predictions (included) |
| NB54 | Estimate BMC-N threshold-exceedance probabilities | NB40 calibration, NB41 predictions and posterior summaries, NB53 threshold table (included) |
| NB55 | Training-only probability recalibration, Table 2 and Table S2 | NB40 calibration, NB54 probabilities, NB53 thresholds (included) |
| Figure02 v0.3 | Draw manuscript Figure 2 | NB51 four-method interval file (included) |
| Figure04 v0.5 | Draw manuscript Figure 4 | **Self-contained**, with 60 aggregated reliability-bin rows; runs independently |

Each notebook is intended to be executed top to bottom; the numbered cells should not be reordered. Rerunning a notebook **writes to its matching `03_Results/` directory**, so preserve a pristine copy of the released results for comparison.

## Manuscript outputs and source notebooks

| Output | Source |
|---|---|
| Figure 1, conceptual workflow | Diagram in manuscript; not a computational plot |
| Figure 2, BMC-N predictive error ranges | `Figure02_BMCN_Rectangles_4mm_v0.3.ipynb`, using NB51 |
| Figure 3, cefepime and gentamicin intervals | NB52 v0.3, using NB41 |
| Figure 4, original vs recalibrated probability reliability | `Figure04_BMCN_Probability_Calibration_v0.5.ipynb` |
| Table 1, interval comparison | NB51 |
| Table 2, original vs recalibrated probabilities | NB55 |
| Supplementary Table S1, threshold coverage | NB53 |
| Supplementary Table S2, per-antibiotic recalibration | NB55 |
| Genomic-group performance (Results 3.5) | NB50 with NB47 assignments |

## Reproduction expectations

The two NB40 data files contain **201,840 cross-fitted calibration records across overlapping outer-training sets** and **50,460 unique independently held-out MIC observations**, respectively. The 201,840 records are not independent observations. The 50,460 held-out observations each appear in one outer fold.

BMC-N/T/AT 95% predictive interval coverage is approximately nominal overall, but differs by antibiotic and subgroup. Antibiotic-specific BMC-N threshold-exceedance probabilities were recalibrated using **training-only** data with an intercept on the log-odds scale and a **normal penalty of standard deviation 2 (variance 4)**. Posterior predictive probabilities in NB54 come from the Bayesian mixture CDF, not approximated 95% interval endpoints.

EUCAST **v16.1 (2026)** scenarios are taken from NB53 and include indication-specific restrictions. Because the original dataset lacks infection indication, threshold-defined observations do **not** necessarily establish categorical clinical resistance in every context. In particular, TMP–SMX component-unit verification and piperacillin–tazobactam technical uncertainty are explicitly noted in NB53–55. These analyses are research results, not clinical decision support or a replacement for laboratory MIC testing.

## Citation

If referring to the underlying unchanged Model C predictor, cite the preceding publication:

Mikawa, Y. G. (2026). *A sequence-informed hybrid framework for predicting antibiotic minimum inhibitory concentrations in previously unseen Escherichia coli pathogens*. **Journal of Microbiological Methods**, 251, 107767. DOI: 10.1016/j.mimet.2026.107767.

Earlier code: <https://github.com/GMikawa/ModelC_MIC_Prediction>. The preceding repository is separate and should not be changed to use this release.

**Original MIC data source:** the NCBI Pathogen Detection Antibiotic Susceptibility Test (AST) Browser, as identified in the Model C publication cited above. The BioSample identifiers link the preserved MIC records to their public scientific source. NCBI makes AST records downloadable and places no restrictions of its own on use or redistribution of its molecular database data, while noting that original submitters may assert separate rights. See `docs/DATA_AND_LICENSE.md` for source links, attribution guidance and remaining qualification. No third-party rights are asserted or relicensed by this repository.


### Figure 4 privacy note

`Figure04_BMCN_Probability_Calibration_v0.5.ipynb` embeds only 60 aggregated plotting-bin rows: no BioSample accessions, individual MIC values, or record-level predictions are embedded in that notebook. The 27,315-record NB55 output remains available as a separate reviewed dataset for full numerical reproduction. The notebook regenerates Figure 4 from its published bin summary.
