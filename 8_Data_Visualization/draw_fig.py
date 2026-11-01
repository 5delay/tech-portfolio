import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

df = pd.read_csv('./data/NonIX-results.csv')
df = df.dropna(how='all')
df = df.iloc[:, 1:]

colors = ["#E4004B", "#ED775A", "#FFB200"] # Non-IX
# colors = ["#134B70", "#419FA1", "#9ACBD0"] # IX
# -

# Divide the values in the TCT columns by 1000 as requested
tct_cols = ['Other_TCT_Otext', 'Other_TCT_Owidget', 'Other_TCT_Itext']
for col in tct_cols:
    df[col] = df[col] / 1000

    
suffixes = ['Otext', 'Owidget', 'Itext']
# Create the new 'Other_Active' columns by subtracting 'Deactive' from 'Total'
for suffix in suffixes:
    df[f'Other_Active_{suffix}'] = df[f'Other_Total_{suffix}'] - df[f'Other_Deactive_{suffix}']

# Identify the groups of columns for each metric
nasa_cols = ['NASA_Mental', 'NASA_Physical', 'NASA_Temporal', 'NASA_Perform', 'NASA_Effort', 'NASA_Frustration', 'NASA_Overall']
ueq_cols = ['UEQ_Attractive', 'UEQ_Efficiency', 'UEQ_Perspicuity', 'UEQ_Dependency', 'UEQ_Stimulation', 'UEQ_Novelty']
flow_cols = ['Flow_Control', 'Flow_Positive', 'Flow_Concentrating']
other_cols = ['Other_Read1', 'Other_Read2', 'Other_Read3', 'Other_Read4', 'Other_ReadOverall', 
              'Other_Fatigue', 'Other_SUS', 'Other_TCT', 'Other_Total', 'Other_Deactive', 'Other_Active']


measure = "UEQ_Attractive"

# Select the specific columns
otext_col = f"{measure}_Otext"
owidget_col = f"{measure}_Owidget"
itext_col = f"{measure}_Itext"

# Extract the data and remove any NaN values from the selected columns
data_o = df[otext_col].dropna()
data_w = df[owidget_col].dropna()
data_i = df[itext_col].dropna()

def calculate_metrics(data_series):
    mean = data_series.mean()
    sem = data_series.std(ddof=1) / np.sqrt(len(data_series))
    return mean, sem

mean_otext, sem_otext = calculate_metrics(data_o)
mean_owidget, sem_owidget = calculate_metrics(data_w)
mean_itext, sem_itext = calculate_metrics(data_i)

labels = ['O.Text', 'O.Widget', 'I.Text']
means = [mean_otext, mean_owidget, mean_itext]
sems = [sem_otext, sem_owidget, sem_itext]



# +
plt.figure(figsize=(3.2, 4))
plt.bar(labels, means, yerr=sems, capsize=8, color=colors, 
        edgecolor='none', width=0.8, 
        error_kw={'ecolor': 'black', 'elinewidth': 1.7}, zorder=2)

# plt.ylabel('Mental Demand', fontsize=13)
# plt.ylim(0, 7)
plt.yticks(np.arange(-0.5,0.52, 0.25), fontsize=12) 
plt.grid(axis='y', linestyle='-', alpha=0.7, zorder=0)

ax = plt.gca()
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['left'].set_visible(False)
ax.spines['bottom'].set_linewidth(2.0) 

plt.xticks(fontsize=12)
plt.xticks([])

# Add a single x-axis label
plt.xlabel('Attractive', fontsize=15, fontweight=500)
plt.savefig('./UEQ_Attractive.png')
