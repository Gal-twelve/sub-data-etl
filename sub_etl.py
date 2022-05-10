
import pandas as pd
import os
import numpy as np
import seaborn as sns
import matplotlib as mpl
import matplotlib.pyplot as plt

# Paths:
data_path = 'data'
rep_path = os.getcwd()
file_name = 'subscription_data.csv'

# Read data:
df = pd.read_csv(os.path.join(data_path, file_name), header=1, index_col=0)

# Fix index (if needed)
if df.iloc[:,0].reset_index()['index'].str.lower().str.contains('customer').any():
    df = pd.read_csv(os.path.join(data_path,file_name),header=1,index_col=0)
else:
    pass


# Fix nulls
df = df.replace([0,'nan'], np.NaN)
df = df.dropna(axis=1, how='all')

# Drop cols with strings:

# Calculate metrics:
df_sum = df.sum().round(2)
df_std = df.std().round(2)

# Concat rollup data by month:
#TODO: Option to add Cohort (month/Q of subscription)
df_agg = pd.concat([df_sum,df_std,df.mean(),df.count()], axis=1)
df_agg.columns = ['m_sum','m_std','m_avg','m_count']

# Plot monthly revenue:
#TODO: Check if that is MRR / ARR with Itamar
# Plot
df_select  = df_agg['m_sum']
n_std = 2
#plt.figure(figsize=(10,6), tight_layout=True)
fig, ax = plt.subplots(figsize=(10,7))
#plotting
plt.plot(df_select, 'o-', linewidth=2)
plt.fill_between(df_select.index, df_select - n_std*df_std, df_select + n_std*df_std, color='b', alpha=0.2)
#customization
#plt.xticks(np.arange(min(x), max(x)+1, 1.0))
ax.set_xticklabels(df_select.index, rotation=70)
plt.xlabel('months')
plt.ylabel('MRR')
plt.title('MRR troughtout the months (with {} * std )'.format(n_std))
plt.show()

print('ok')