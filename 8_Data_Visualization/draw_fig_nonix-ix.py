import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Load the two datasets
try:
    df_ix = pd.read_csv('./data/IX-results.csv').dropna(how='all').iloc[:, 1:]
    df_nonix = pd.read_csv('./data/NonIX-results.csv').dropna(how='all').iloc[:, 1:]
except FileNotFoundError as e:
    print(f"Error: {e}. Make sure both './data/IX-results.csv' and './data/NonIX-results.csv' are in the correct directory.")
    exit()

tct_cols = ['Other_TCT_Otext', 'Other_TCT_Owidget', 'Other_TCT_Itext']
for col in tct_cols:
    df_ix[col] = df_ix[col] / 1000

suffixes = ['Otext', 'Owidget', 'Itext']
for suffix in suffixes:
    df_ix[f'Other_Active_{suffix}'] = df_ix[f'Other_Total_{suffix}'] - df_ix[f'Other_Deactive_{suffix}']

for col in tct_cols:
    df_nonix[col] = df_ix[col] / 1000

for suffix in suffixes:
    df_nonix[f'Other_Active_{suffix}'] = df_nonix[f'Other_Total_{suffix}'] - df_nonix[f'Other_Deactive_{suffix}']


nasa_cols = ['NASA_Mental', 'NASA_Physical', 'NASA_Temporal', 'NASA_Perform', 'NASA_Effort', 'NASA_Frustration']
ueq_cols = ['UEQ_Attractive', 'UEQ_Efficiency', 'UEQ_Perspicuity', 'UEQ_Dependency', 'UEQ_Stimulation', 'UEQ_Novelty']
flow_cols = ['Flow_Control', 'Flow_Positive', 'Flow_Concentrating']
other_cols = ['Other_Read1', 'Other_Read2', 'Other_Read3', 'Other_Read4', 'Other_ReadOverall', 
              'Other_Fatigue', 'Other_SUS', 'Other_TCT', 'Other_Total', 'Other_Deactive', 'Other_Active']

nonIX_colors = ["#E4004B", "#ED775A", "#FFB200"] # Non-IX
IX_colors = ["#134B70", "#419FA1", "#9ACBD0"] # IX

other_read_cols= ['Other_Read1', 'Other_Read2', 'Other_Read3', 'Other_Read4']



system_idx = 0
system = suffixes[system_idx]
color_IX = IX_colors[system_idx]
color_NonIX = nonIX_colors[system_idx]

# +
# Set the bar width and spacing
bar_width = 0.4 # 더 얇은 막대
spacing_within_group = 0
spacing_between_groups = 0.5 # 그룹 간 간격 조정

x_labels = ['Mental\nDemand', 'Physical\nDemand', 'Temporal\nDemand', 'Performance', 'Effort', 'Frustration']
x = np.arange(len(x_labels)) * (bar_width * 2 + spacing_within_group + spacing_between_groups)

# Calculate means and standard errors for Otext
means_ix = [df_ix[f'{col}_{system}'].mean() for col in nasa_cols]
sems_ix = [df_ix[f'{col}_{system}'].std() / np.sqrt(len(df_ix)) for col in nasa_cols]
means_nonix = [df_nonix[f'{col}_{system}'].mean() for col in nasa_cols]
sems_nonix = [df_nonix[f'{col}_{system}'].std() / np.sqrt(len(df_nonix)) for col in nasa_cols]


# +
# Set the bar width and spacing
bar_width = 0.2 # 더 얇은 막대
spacing_within_group = 0
spacing_between_groups = 0.5 # 그룹 간 간격 조정


x_labels = ['Appr. of\nText Position', 'Visual\nNon-Interference', 'Text Clarity', 'Overall Readability']
x = np.arange(len(x_labels)) * (bar_width * 2 + spacing_within_group + spacing_between_groups)

# Calculate means and standard errors for Otext
means_ix = [df_ix[f'{col}_{system}'].mean() for col in other_read_cols]
sems_ix = [df_ix[f'{col}_{system}'].std() / np.sqrt(len(df_ix)) for col in other_read_cols]
means_nonix = [df_nonix[f'{col}_{system}'].mean() for col in other_read_cols]
sems_nonix = [df_nonix[f'{col}_{system}'].std() / np.sqrt(len(df_nonix)) for col in other_read_cols]


# +
# Set the bar width and spacing
bar_width = 0.2 # 더 얇은 막대
spacing_within_group = 0
spacing_between_groups = 0.5 # 그룹 간 간격 조정

x_labels = ['Sense of Control', 'Positive Emotion', 'Concentration']
x = np.arange(len(x_labels)) * (bar_width * 2 + spacing_within_group + spacing_between_groups)

# Calculate means and standard errors for Otext
means_ix = [df_ix[f'{col}_{system}'].mean() for col in flow_cols]
sems_ix = [df_ix[f'{col}_{system}'].std() / np.sqrt(len(df_ix)) for col in flow_cols]
means_nonix = [df_nonix[f'{col}_{system}'].mean() for col in flow_cols]
sems_nonix = [df_nonix[f'{col}_{system}'].std() / np.sqrt(len(df_nonix)) for col in flow_cols]

# +
fig, ax = plt.subplots(figsize=(10,2.7))


# Create the bar chart
# Position the bars to be closer together within each group
rects2 = ax.bar(x - bar_width/2 + spacing_within_group/2, means_nonix, bar_width, yerr=sems_nonix, label='Non-IX',
                color=color_NonIX, edgecolor='none', capsize=8, zorder=2)

rects1 = ax.bar(x + bar_width/2 - spacing_within_group/2, means_ix, bar_width, yerr=sems_ix, label='IX',
                color=color_IX, edgecolor='none', capsize=8, zorder=2)

# Set the y-axis ticks and labels
plt.yticks(np.arange(0, 7.2, 1), fontsize=12)

# Add a y-grid
plt.grid(axis='y', linestyle='-', alpha=0.7, zorder=0)

# Hide chart spines
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['left'].set_visible(False)
ax.spines['bottom'].set_linewidth(2.0)

# Add individual x-axis labels centered below each bar group
ax.set_xticks(x)
ax.set_xticklabels(x_labels, fontsize=15, fontweight='500')

plt.tight_layout()
plt.savefig('./NASA-NonIX-IX.png')
# -


