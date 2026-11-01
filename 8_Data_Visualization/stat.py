import pandas as pd
import scipy.stats as stats
import numpy as np
import statsmodels.stats.anova as anova
from itertools import combinations
import scikit_posthocs as sp
import researchpy as rp

# Load the data
df = pd.read_csv('./data/NonIX-results.csv')
df = df.dropna(how='all')
df = df.iloc[:, 1:]


# +
tct_cols = ['Other_TCT_Otext', 'Other_TCT_Owidget', 'Other_TCT_Itext']

# Divide the values in the TCT columns by 1000 as requested
for col in tct_cols:
    df[col] = df[col] / 1000

    
suffixes = ['Otext', 'Owidget', 'Itext']

# Create the new 'Other_Active' columns by subtracting 'Deactive' from 'Total'
for suffix in suffixes:
    df[f'Other_Active_{suffix}'] = df[f'Other_Total_{suffix}'] - df[f'Other_Deactive_{suffix}']

# -

# Identify the groups of columns for each metric
nasa_cols = ['NASA_Mental', 'NASA_Physical', 'NASA_Temporal', 'NASA_Perform', 'NASA_Effort', 'NASA_Frustration', 'NASA_Overall']
ueq_cols = ['UEQ_Attractive', 'UEQ_Efficiency', 'UEQ_Perspicuity', 'UEQ_Dependency', 'UEQ_Stimulation', 'UEQ_Novelty']
flow_cols = ['Flow_Control', 'Flow_Positive', 'Flow_Concentrating']
other_cols = ['Other_Read1', 'Other_Read2', 'Other_Read3', 'Other_Read4', 'Other_ReadOverall', 
              'Other_Fatigue', 'Other_SUS', 'Other_TCT', 'Other_Total', 'Other_Deactive', 'Other_Active', 'Other_Prefer',
             ] #'Other_Error'

all_metrics = {
    'NASA-TLX': nasa_cols,
    'UEQ': ueq_cols,
    'Flow': flow_cols,
    'Other': other_cols
}

# 1. Shapiro-Wilk Normality Test
print("--- Shapiro-Wilk Normality Test Results ---")
normality_results = {}
for metric_group, metrics in all_metrics.items():
    for metric in metrics:
        normality_results[metric] = {
            'Otext': {'W': None, 'p_value': None},
            'Owidget': {'W': None, 'p_value': None},
            'Itext': {'W': None, 'p_value': None}
        }
        for suffix in ['Otext', 'Owidget', 'Itext']:
            col_name = f"{metric}_{suffix}"
            if col_name in df.columns:
                data = df[col_name].dropna()
                
                stat, p = stats.shapiro(data)

                mean = data.mean()
                sd = data.std()
                    
                normality_results[metric][suffix]['W'] = stat
                normality_results[metric][suffix]['p_value'] = p
                
                print(f"\nNormality Test for {col_name}")
                print(f"W={stat:.3f}, p={p:.3f}")
                print(f"mean={mean:.2f}, SD={sd:.2f}")

# +
# 2. Within-Subject Comparison based on Normality
print("\n--- Within-Subject Comparison Results ---")
significant_results = {}
for metric_group, metrics in all_metrics.items():
    for metric in metrics:
        data_o = df[f"{metric}_Otext"].dropna()
        data_w = df[f"{metric}_Owidget"].dropna()
        data_i = df[f"{metric}_Itext"].dropna()

        if len(data_o) != len(data_w) or len(data_o) != len(data_i):
            print(f"Skipping {metric} due to unequal sample sizes.")
            continue

        # Check for normality for all three columns
        is_normal = all(
            normality_results[metric][suffix]['p_value'] > 0.05
            for suffix in ['Otext', 'Owidget', 'Itext']
            if normality_results[metric][suffix]['p_value'] is not None
        )

        # Reshape data for within-subject tests
        data = pd.DataFrame({
            'score': pd.concat([data_o, data_w, data_i]),
            'group': ['Otext'] * len(data_o) + ['Owidget'] * len(data_w) + ['Itext'] * len(data_i),
            'subject': list(range(len(data_o))) * 3
        })

        if is_normal:
            # Parametric test: Repeated Measures ANOVA
            try:
                aovrm = anova.AnovaRM(data, 'score', 'subject', within=['group'])
                res = aovrm.fit()
                f_stat = res.anova_table['F Value'][0]
                p_value = res.anova_table['Pr > F'][0]
                test_type = "Repeated Measures ANOVA"
            except Exception as e:
                print(f"Could not perform Repeated Measures ANOVA for {metric}. Error: {e}")
                continue
        else:
            # Non-parametric test: Friedman Test
            try:
                f_stat, p_value = stats.friedmanchisquare(data_o, data_w, data_i)
                test_type = "Friedman Test"
            except ValueError:
                print(f"Could not perform non-parametric test for {metric}. Skipping.")
                continue

        
        if p_value < 0.05:
            significant_results[metric] = is_normal
            print(f"Comparison for {metric}: {test_type} F-stat={f_stat:.4f}, p={p_value:.4f}")
            print(f"  -> Significant difference found for {metric} (p < 0.05).\n")
    # -

# 3. Pairwise Comparison and Effect Size (Cohen's d)
print("\n--- Pairwise Comparison with Bonferroni Correction & Effect Size ---")
for metric, is_normal in significant_results.items():
    print(f"\nPerforming post-hoc analysis for {metric}...")
    data_o = df[f"{metric}_Otext"].dropna()
    data_w = df[f"{metric}_Owidget"].dropna()
    data_i = df[f"{metric}_Itext"].dropna()
    
    # Effect Size Function (Cohen's d for paired samples)
    def cohen_d_paired(x, y):
        diff = x - y
        d = np.mean(diff) / np.std(diff, ddof=1)
        return d

    if is_normal:
        # Parametric Post-hoc: Paired T-tests with Bonferroni
        print("Using Paired T-tests with Bonferroni correction.")
        alpha = 0.05 / 3  # Bonferroni correction for 3 comparisons
        comparisons = list(combinations(['Otext', 'Owidget', 'Itext'], 2))

        for group1, group2 in comparisons:
            data1 = df[f"{metric}_{group1}"].dropna()
            data2 = df[f"{metric}_{group2}"].dropna()
            t_stat, p_val = stats.ttest_rel(data1, data2)
            d = cohen_d_paired(data1, data2)
            print(f"  - {group1} vs {group2}: t={t_stat:.4f}, p={p_val:.4f}, d={d:.4f} (significant if p < {alpha:.4f})")
    else:
        # Non-parametric Post-hoc: Conover's Test with Bonferroni
        print("Using Conover's Test (non-parametric) with Bonferroni correction.")
        
        # Reshape data for scikit_posthocs
        data_long = pd.DataFrame({
            'score': pd.concat([data_o, data_w, data_i]),
            'group': ['Otext'] * len(data_o) + ['Owidget'] * len(data_w) + ['Itext'] * len(data_i),
            'subject': list(range(len(data_o))) * 3
        })
        
        # Perform Conover's post-hoc test
        try:
            conover_results = sp.posthoc_conover(data_long, val_col='score', group_col='group', p_adjust='bonferroni')
            print("  - Conover's Test Results (p-values with Bonferroni):")
            print(conover_results)

            # Manually calculate effect sizes for non-parametric tests (e.g., Rosenthal's r or Cliff's delta)
            def cliffs_delta(x, y):
                x = np.array(x)
                y = np.array(y)
                num_x_greater = np.sum(np.outer(x, np.ones(y.shape)) > np.outer(np.ones(x.shape), y))
                num_y_greater = np.sum(np.outer(x, np.ones(y.shape)) < np.outer(np.ones(x.shape), y))
                return (num_x_greater - num_y_greater) / (len(x) * len(y))
            
            comparisons = list(combinations(['Otext', 'Owidget', 'Itext'], 2))
            for group1, group2 in comparisons:
                data1 = df[f"{metric}_{group1}"].dropna()
                data2 = df[f"{metric}_{group2}"].dropna()
                delta = cliffs_delta(data1, data2)
                print(f"  - {group1} vs {group2}: Cliff's Delta={delta:.4f}")
        except Exception as e:
            print(f"  - Could not perform Conover's test. Error: {e}")

.006681908
