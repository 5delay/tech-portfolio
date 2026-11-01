import pandas as pd
import scipy.stats as stats
import numpy as np

# +
# Load the two datasets
try:
    df_ix = pd.read_csv('./data/IX-results.csv').dropna(how='all')
    df_nonix = pd.read_csv('./data/NonIX-results.csv').dropna(how='all')
    
    suffixes = ['Otext', 'Owidget', 'Itext']

    # Create the new 'Other_Active' columns by subtracting 'Deactive' from 'Total'
    for suffix in suffixes:
        df_ix[f'Other_Active_{suffix}'] = df_ix[f'Other_Total_{suffix}'] - df_ix[f'Other_Deactive_{suffix}']
        df_nonix[f'Other_Active_{suffix}'] = df_nonix[f'Other_Total_{suffix}'] - df_nonix[f'Other_Deactive_{suffix}']

    
except FileNotFoundError as e:
    print(f"Error: {e}. Make sure both './data/IX-results.csv' and './data/NonIX-results.csv' are in the correct directory.")
    exit()
# -

# Identify the columns to compare
# Assuming the column names are the same across both files, excluding 'Pid'
columns_to_compare = df_ix.columns[1:]

# Merge the two dataframes based on 'Pid'
merged_df = pd.merge(df_nonix, df_ix, on='Pid', suffixes=('_NonIX', '_IX'))

print("--- 데이터 병합 완료 ---")
print(f"총 참가자 수: {len(merged_df)}")

print("--- Within-Subjects 비교 결과 ---")

# Define a function to calculate Cohen's d for paired samples
def cohen_d_paired(group1, group2):
    diff = group1 - group2
    d = np.mean(diff) / np.std(diff, ddof=1)
    return d

# Define a function to calculate Rosenthal's r for Wilcoxon test
def rosenthal_r(z_score, n):
    return z_score / np.sqrt(n)

for col in columns_to_compare:
    # Get data for each condition
    data_nonix = merged_df[f"{col}_NonIX"].dropna()
    data_ix = merged_df[f"{col}_IX"].dropna()

    if len(data_nonix) != len(data_ix):
        print(f"Skipping {col} due to unequal sample sizes after merge.")
        continue

    # Calculate difference scores
    difference_scores = data_ix - data_nonix
    
    # Perform Shapiro-Wilk normality test on the difference scores
    shapiro_stat, shapiro_p = stats.shapiro(difference_scores)
    is_normal = shapiro_p > 0.05
    
    print(f"\n차이 점수에 대한 정규성 검정 ({col}): W={shapiro_stat:.4f}, p={shapiro_p:.4f}")
    
    if is_normal:
        # Parametric test: Paired T-test
        t_stat, p_value = stats.ttest_rel(data_ix, data_nonix)
        d_effect = cohen_d_paired(data_ix, data_nonix)
        test_type = "Paired T-test"
        
        print(f"'{col}' 비교: {test_type} | 통계량={t_stat:.4f}, p={p_value:.4f}")
        if p_value < 0.05:
            print(f"  -> 유의미한 차이 발견. Cohen's d={d_effect:.4f}")

    else:
        # Non-parametric test: Wilcoxon signed-rank test
        try:
            wilcoxon_stat, p_value = stats.wilcoxon(data_ix, data_nonix)
            # Calculate Rosenthal's r effect size
            n = len(data_ix)
            z_score = stats.norm.ppf(p_value/2) if p_value < 1 else 0
            r_effect = rosenthal_r(abs(z_score), n)
            test_type = "Wilcoxon Signed-Rank Test"
            
            print(f"'{col}' 비교: {test_type} | 통계량={wilcoxon_stat:.4f}, p={p_value:.4f}")
            if p_value < 0.05:
                print(f"  -> 유의미한 차이 발견. Rosenthal's r={r_effect:.4f}")
        except ValueError as e:
            print(f"  - Skipping {col} due to issues with Wilcoxon test: {e}")

# +
for col in columns_to_compare:
    # Get data for each condition
    data_nonix = merged_df[f"{col}_NonIX"].dropna()
    data_ix = merged_df[f"{col}_IX"].dropna()

    if len(data_nonix) != len(data_ix):
        print(f"Skipping {col} due to unequal sample sizes after merge.")
        continue

    # Calculate difference scores
    difference_scores = data_ix - data_nonix
    
    # Perform Shapiro-Wilk normality test on the difference scores
    shapiro_stat, shapiro_p = stats.shapiro(difference_scores)
    is_normal = shapiro_p > 0.05
    
    # Determine significance stars for normality test p-value
    norm_stars = ""
    if shapiro_p <= 0.001:
        norm_stars = "***"
    elif shapiro_p <= 0.01:
        norm_stars = "**"
    elif shapiro_p <= 0.05:
        norm_stars = "*"
    
#     print(f"\n차이 점수에 대한 정규성 검정 ({col}): W={shapiro_stat:.4f}, p={shapiro_p:.4f}")
#     print(f"  -> 정규성: {is_normal} {norm_stars}")
    
    if is_normal:
        # Parametric test: Paired T-test
        t_stat, p_value = stats.ttest_rel(data_ix, data_nonix)
        d_effect = cohen_d_paired(data_ix, data_nonix)
        test_type = "Paired T-test"
        
        # Determine significance stars for the test p-value
        test_stars = ""
        if p_value <= 0.001:
            test_stars = "***"
        elif p_value <= 0.01:
            test_stars = "**"
        elif p_value <= 0.05:
            test_stars = "*"
        
        
        if p_value < 0.05:
            print(f"'{col}' 비교: {test_type} | 통계량={t_stat:.4f}, p={p_value:.4f} {test_stars}")
            print(f"  -> 유의미한 차이 발견. Cohen's d={d_effect:.4f}")
#         else:
#             print("  -> 유의미한 차이 없음.")

    else:
        # Non-parametric test: Wilcoxon signed-rank test
        try:
            wilcoxon_stat, p_value = stats.wilcoxon(data_ix, data_nonix)
            # Calculate Rosenthal's r effect size
            n = len(data_ix)
            # The z-score calculation needs to be for a two-tailed test
            z_score = stats.norm.ppf(p_value) if p_value < 1 else 0
            r_effect = abs(z_score) / np.sqrt(n)
            test_type = "Wilcoxon Signed-Rank Test"
            
            # Determine significance stars for the test p-value
            test_stars = ""
            if p_value <= 0.001:
                test_stars = "***"
            elif p_value <= 0.01:
                test_stars = "**"
            elif p_value <= 0.05:
                test_stars = "*"
            
            
            if p_value < 0.05:
                print(f"'{col}' 비교: {test_type} | 통계량={wilcoxon_stat:.4f}, p={p_value:.4f} {test_stars}")
                print(f"  -> 유의미한 차이 발견. Rosenthal's r={r_effect:.4f}")
#             else:
#                 print("  -> 유의미한 차이 없음.")
        except ValueError as e:
            print(f"  - Skipping {col} due to issues with Wilcoxon test: {e}")

# +
import numpy as np

def cliffs_delta(x, y):
    """
    Calculates Cliff's Delta for two lists of data.
    """
    x, y = np.array(x), np.array(y)
    len_x, len_y = len(x), len(y)
    
    delta = 0
    for i in range(len_x):
        for j in range(len_y):
            if x[i] > y[j]:
                delta += 1
            elif x[i] < y[j]:
                delta -= 1
    
    return delta / (len_x * len_y)


# -

for col in columns_to_compare:
    # Get data for each condition
    data_nonix = merged_df[f"{col}_NonIX"].dropna()
    data_ix = merged_df[f"{col}_IX"].dropna()

    if len(data_nonix) != len(data_ix):
        print(f"Skipping {col} due to unequal sample sizes after merge.")
        continue

    # Calculate difference scores
    difference_scores = data_ix - data_nonix
    
    # Perform Shapiro-Wilk normality test on the difference scores
    shapiro_stat, shapiro_p = stats.shapiro(difference_scores)
    is_normal = shapiro_p > 0.05
    
    # Determine significance stars for normality test p-value
    norm_stars = ""
    if shapiro_p <= 0.001:
        norm_stars = "***"
    elif shapiro_p <= 0.01:
        norm_stars = "**"
    elif shapiro_p <= 0.05:
        norm_stars = "*"
    
    if is_normal:
        # Parametric test: Paired T-test
        t_stat, p_value = stats.ttest_rel(data_ix, data_nonix)
        d_effect = cohen_d_paired(data_ix, data_nonix)
        test_type = "Paired T-test"
        
        # Determine significance stars for the test p-value
        test_stars = ""
        if p_value <= 0.001:
            test_stars = "***"
        elif p_value <= 0.01:
            test_stars = "**"
        elif p_value <= 0.05:
            test_stars = "*"
        
        if p_value < 0.05:
            print(f"'{col}' 비교: {test_type} | 통계량={t_stat:.4f}, p={p_value:.4f} {test_stars}")
            print(f"  -> 유의미한 차이 발견. Cohen's d={d_effect:.4f}")
    
    else:
        # Non-parametric test: Wilcoxon signed-rank test
        # Note: Conover's Test is for multiple comparisons (post-hoc),
        # so Wilcoxon is the correct non-parametric paired test here.
        try:
            wilcoxon_stat, p_value = stats.wilcoxon(data_ix, data_nonix)
            # Calculate Cliff's Delta effect size
            delta = cliffs_delta(data_ix, data_nonix)
            test_type = "Wilcoxon Signed-Rank Test"
            
            # Determine significance stars for the test p-value
            test_stars = ""
            if p_value <= 0.001:
                test_stars = "***"
            elif p_value <= 0.01:
                test_stars = "**"
            elif p_value <= 0.05:
                test_stars = "*"
            
            if p_value < 0.05:
                print(f"'{col}' 비교: {test_type} | 통계량={wilcoxon_stat:.4f}, p={p_value:.4f} {test_stars}")
                print(f"  -> 유의미한 차이 발견. Cliff's Delta={delta:.4f}")
        except ValueError as e:
            print(f"  - Skipping {col} due to issues with Wilcoxon test: {e}")


