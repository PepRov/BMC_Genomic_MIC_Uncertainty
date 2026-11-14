#!/usr/bin/env python3
"""Quick independently rerunnable audit for packaged BMC results (no Bayesian refitting)."""
from pathlib import Path
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parent
D = ROOT / '03_Results'


def get(subdir, fname):
    p = D / subdir / fname
    if not p.is_file():
        raise FileNotFoundError(f'Required package file missing: {p}')
    return pd.read_csv(p)


def require(condition, message):
    if not bool(condition):
        raise AssertionError(message)

train = get('40_BMC_Training_Only_Calibration', '40_BMC_training_only_inner_predictions_all_outer_folds.csv.gz')
test = get('40_BMC_Training_Only_Calibration', '40_BMC_independent_outer_test_predictions.csv.gz')
require((len(train),len(test),test.biosample.nunique(),test.antibiotic.nunique()) == (201840,50460,9058,26), 'NB40 sizes')
require(set(test.outer_fold) == set(range(1,6)), 'Five outer folds')
require(not test.interaction_row.duplicated().any(), 'Unique test observation IDs')
for f in range(1,6):
    t=set(test.loc[test.outer_fold == f,'biosample'])
    c=set(train.loc[train.outer_fold_for_calibration == f,'biosample'])
    require(not t.intersection(c), f'Outer fold {f}: train/test leakage')
print('PASS: NB40 sizes, identities and pathogen-disjoint folds')

groups = get('47_ModelC_Genomic_Group_Slope_Audit', '47_fold_genomic_group_assignments.csv.gz')
require(len(groups) == 5*9058 and not groups.duplicated(['outer_fold','biosample']).any(), 'NB47 assignments')
require(groups.loc[groups.partition == 'test','biosample'].nunique() == 9058, 'NB47 test assignments')
print('PASS: 45,290 fold-defined genomic assignments')

base_keys=['interaction_row','biosample','antibiotic','outer_fold']
for method, prefix, folder in [('BMC-N','bmc_n','41_BMC_N_Pathogen_Out_Validation'),
                               ('BMC-T','bmc_t','42_BMC_T_Pathogen_Out_Validation'),
                               ('BMC-AT','bmc_at','43_BMC_AT_Pathogen_Out_Validation')]:
    df = get(folder, {'BMC-N':'41_BMC_N_independent_outer_test_predictions.csv.gz',
                      'BMC-T':'42_BMC_T_independent_outer_test_predictions.csv.gz',
                      'BMC-AT':'43_BMC_AT_independent_outer_test_predictions.csv.gz'}[method])
    require(len(df) == 50460 and not df.interaction_row.duplicated().any(), method+' test rows')
    merged = test[base_keys+['observed_log2_mic','model_c_outer_test_predicted_log2_mic']].merge(
        df, on=base_keys, how='inner', validate='one_to_one', suffixes=('_base',''))
    require(len(merged)==50460,'Observation links '+method)
    require(np.allclose(merged.observed_log2_mic,merged.observed_log2_mic_base),method+' observed MICs')
    require(np.allclose(merged.model_c_outer_test_predicted_log2_mic,
                        merged.model_c_outer_test_predicted_log2_mic_base),method+' Model C predictions')
    y=df.observed_log2_mic.to_numpy(float)
    lower=df[f'{prefix}_lower95_log2'].to_numpy(float)
    upper=df[f'{prefix}_upper95_log2'].to_numpy(float)
    coverage=float(np.mean((y>=lower)&(y<=upper)))
    print(f'PASS: {method:6s} 50,460 predictions, 95% interval coverage {100*coverage:.2f}%')

post=get('41_BMC_N_Pathogen_Out_Validation','41_BMC_N_training_only_posterior_by_antibiotic_and_fold.csv')
require(len(post)==130 and not post.duplicated(['outer_fold','antibiotic']).any(),'NB41 posterior')

interval = get('51_BMC_Final_Comparison','51_All_Four_Methods_Independent_Heldout_Intervals.csv.gz')
require(len(interval) == 4*50460, 'Four-method intervals')
for method,expected_cov,expected_width,expected_score in [
    ('BMC-N',95.78,3.200,4.326),('BMC-T',96.30,3.392,4.452),
    ('BMC-AT',96.00,3.363,4.398),('Empirical',95.23,3.096,4.229)]:
    f = interval.loc[interval.method==method]
    require(len(f)==50460,method+' entries')
    cov=100*f.covered_95pct.mean()
    width=f.interval_width_log2.mean()
    score=f.interval_score95_log2.mean()
    require(abs(cov-expected_cov)<0.006 and abs(width-expected_width)<0.0006 and abs(score-expected_score)<0.0006,
            method+' Table 1 agreement')
    print(f'PASS: {method:9s} Table 1: coverage={cov:.2f}% width={width:.3f} score={score:.3f}')

s1=get('53_BMC_Resistance_Threshold_Coverage','53_Supplementary_Resistance_Coverage_18_Antibiotics.csv')
require(len(s1)==18 and s1.antibiotic.is_unique,'NB53 18 threshold scenarios')
require(int(s1.n_tested.sum())==27315, 'NB53 27,315 held-out MIC observations')
require(int(s1.n_above_r_cutoff.sum())==4643, 'NB53 4,643 threshold exceedances')
for abx,n_r,n_in in [('cefepime',449,421),('gentamicin',416,308)]:
    row=s1.loc[s1.antibiotic == abx].iloc[0]
    require(int(row.n_above_r_cutoff)==n_r and int(row.n_within95)==n_in,abx+' threshold coverage')
print('PASS: 18 EUCAST-v16.1 threshold scenarios and supplementary coverage')

raw=get('54_BMC_Breakpoint_Exceedance_Probability','54_BMCN_Breakpoint_Probabilities_HeldOut.csv.gz')
recal=get('55_BMC_Probability_Training_Only_Recalibration','55_BMCN_Probabilities_OuterTest_Original_Vs_Recalibrated.csv.gz')
require(len(raw)==len(recal)==27315 and raw.interaction_row.is_unique and recal.interaction_row.is_unique,
        '27,315 unique threshold-probability outcomes')
comp=raw[['interaction_row','prob_mic_exceeds_r','observed_exceeds_r']].merge(
    recal[['interaction_row','prob_original_bmc_n','prob_recalibrated','actual_exceeds_r']],
    on='interaction_row',how='inner',validate='one_to_one')
require(len(comp)==27315,'NB54–55 matching')
require(np.array_equal(comp.observed_exceeds_r.astype(int),comp.actual_exceeds_r.astype(int)), 'Threshold outcomes')
require(np.allclose(comp.prob_mic_exceeds_r.to_numpy(),comp.prob_original_bmc_n.to_numpy(),rtol=0,atol=1e-12),'Unchanged raw BMC-N probabilities')
y=comp.actual_exceeds_r.to_numpy(float)
p0=comp.prob_original_bmc_n.to_numpy(float)
p1=comp.prob_recalibrated.to_numpy(float)
require(np.all(np.isfinite(p1)) and np.all((p1>=0)&(p1<=1)), 'Valid probabilities')
for lab,p,expected_brier in [('raw',p0,0.0684),('recalibrated',p1,0.0542)]:
    brier=float(np.mean((p-y)**2))
    require(abs(brier-expected_brier)<0.00006,'NB55 Brier score '+lab)
    print(f'PASS: {lab} probability Brier score {brier:.4f}')
print('ALL CHECKS PASSED: no upstream model refitting was performed.')
