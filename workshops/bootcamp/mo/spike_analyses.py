# %% Spike data analyses
import itertools
import numpy as np
import pandas as pd
import xarray as xr
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import ttest_ind
from sklearn.model_selection import train_test_split,GridSearchCV
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score
from sklearn.preprocessing import StandardScaler
# import shap

# %% 
# ### Load the data
# dataset = xr.load_dataset("data/steinmetz_2017-11-01_Forssmann.nc")
dataset = xr.load_dataset("data/steinmetz_2016-12-14_Cori.nc")

# %% 
# ### Create a dataframe containing spike times
list_of_variables = ["spike_trial", "spike_cell", "spike_time"]
spike_df = dataset[list_of_variables].to_dataframe()
spike_df

# %% 
# ### Collect the spike data of all cells into a single list.

trial_idx = 1
ids = np.arange(1, spike_df['spike_cell'].max()+1)
spike_times = []
for cell_idx in ids:
    cell_x_spike_time = spike_df['spike_time'][(spike_df['spike_cell'] == cell_idx) & (spike_df['spike_trial'] == trial_idx)]
    spike_times.append(cell_x_spike_time)

spike_times = list(spike_df[spike_df.spike_trial==trial_idx].groupby("spike_cell").apply(lambda x: list(x.spike_time)))

"""
Discussion point: Which one of the above approach should be used?
First appraoch goes through all cells and if they have not spiked, it adds an empty list.
Second approach only goes through the neurons that have spiked.
"""

# %% 
# ### Plot spike events of a single trial for all cells

plt.figure(figsize=(5, 2), dpi=150)
plt.eventplot(spike_times, linelengths=.8, colors="k");
plt.xlabel("Spiking time (s)")
plt.ylabel("Cell ID")
sns.despine(trim=True)

# %% 
# ### Which brain areas were recorded from?
np.unique(dataset.brain_area.values)

# %%
trial_idx = 1
spike_df_trial_x = spike_df[spike_df.spike_trial == trial_idx]

# %% 
# ## Plot spike events for a single trial for all cells

spike_times_all_cells = []
for cell_id in spike_df_trial_x.spike_cell.unique():
    spike_times = spike_df_trial_x.spike_time[spike_df_trial_x.spike_cell == cell_id]
    spike_times_all_cells.append(spike_times)

# %%
plt.figure(figsize=(3, 8))
plt.eventplot(spike_times_all_cells, linelengths=.8, colors="k");

# %% Color each brain area in the plot differently 

cols = ["brain_area"]
area_df = dataset[cols].to_dataframe().reset_index().rename(columns={"cell": "spike_cell"})
area_df

# %%
spike_area_df_trial_x = pd.merge(spike_df_trial_x, area_df).sort_values(by="brain_area")
spike_area_df_trial_x

# %%
all_colors = {
    'ACA' : "red",
    'CA3' : "navy",
    'DG' : "crimson",
    'LS' : "darkorange",
    'MOs' : "dodgerblue",
    'SUB' : "gold",
    'VISp' : "deeppink",
    'root' : ".3",
}

# %%
spike_times_all_cells = []
colors = []
for cell_id in spike_area_df_trial_x.spike_cell.unique():
    spike_times = spike_area_df_trial_x.spike_time[spike_area_df_trial_x.spike_cell == cell_id]
    spike_times_all_cells.append(spike_times)
    
    area = spike_area_df_trial_x.brain_area[spike_area_df_trial_x.spike_cell == cell_id].iloc[0]
    area_color = all_colors[area]
    colors.append(area_color)

# %%
plt.figure(figsize=(1.5, 4), dpi=150)
plt.eventplot(spike_times_all_cells, linelengths=.8, colors=colors);
plt.xlabel("Time (s)")
plt.ylabel("Neurons")
sns.despine(trim=True)

# %% Is there any learning going on?

# %%
cols = ["response_time", "active_trials", "feedback_type"]
df = dataset[cols].to_dataframe().reset_index()
df = df[df.active_trials]
df

# %%
sns.lmplot(data=df, x="trial", y="response_time")

# %%
sns.lmplot(data=df, x="trial", y="response_time", hue="feedback_type")

# CONCLUSION: Cori is not learning during the task

# %%
# # 2. Algnment of neural responses to experimental variables

# %%
cell_idx = 3
spike_df_cell_x = spike_df[spike_df.spike_cell == cell_idx]
spike_df_cell_x

# %%
cols = ["active_trials", "response_time", "response_type", "feedback_time", "feedback_type"]
experimental_df = dataset[cols].to_dataframe().reset_index()
experimental_df = experimental_df[experimental_df.active_trials]
experimental_df.rename(columns={"trial": "spike_trial"}, inplace=True)
experimental_df

# %%
spike_exp_df_cell_x = pd.merge(spike_df_cell_x, experimental_df)
spike_exp_df_cell_x.shape

# %%
sns.scatterplot(data=spike_df_cell_x, x="spike_time", y="spike_trial")

# %%
len(spike_exp_df_cell_x)

# %%
spike_exp_df_cell_x_sorted = spike_exp_df_cell_x.sort_values(by="response_time")
spike_exp_df_cell_x_sorted["trials_sorted"] = np.arange(len(spike_exp_df_cell_x_sorted))

# %%
plt.figure(figsize=(4, 3), dpi=150)
sns.scatterplot(data=spike_exp_df_cell_x_sorted, x="spike_time", y="trials_sorted", ec="None", color="k", s=5, label="Spike time")
sns.scatterplot(data=spike_exp_df_cell_x_sorted, x="response_time", y="trials_sorted", ec="None", color="crimson", s=15, label="Response time")
plt.xlabel("Time (s)")
plt.ylabel("Trials")
plt.legend(loc=(.65, 0.03), frameon=True, fontsize=8, handletextpad=-.5)
sns.despine(trim=True)

# %% ---
# ## Analyze spiking profile depending on feedback type and brain region

# %%
# ### Get spike counts for each cell in each trial
cols = ["spike_trial", "spike_cell", "spike_time"]
spike_data = dataset[cols].to_dataframe().reset_index()
spike_count_df = spike_data.groupby(["spike_trial", "spike_cell"]).apply(len).reset_index(name="spike_counts")
spike_count_df

# %%
# ### Get the brain area for each cell and rename columsn to match the spike_count_df
cols = ["brain_area", "feedback_type", "active_trials"]
brain_region_df = dataset[cols].to_dataframe().reset_index()
brain_region_df = brain_region_df[brain_region_df.active_trials]
brain_region_df.rename(columns={"cell": "spike_cell", "trial": "spike_trial"}, inplace=True)
brain_region_df

# %% 
# ### Merge the two dataframes
df = pd.merge(spike_count_df, brain_region_df)
df

# %% 
plt.figure(dpi=150)
sns.violinplot(data=df, x="brain_area", y="spike_counts", split=True, hue="feedback_type", palette=[".3", "crimson"])
plt.ylim(-15, 50)

# %%
plt.figure(dpi=150)
sns.boxenplot(data=df, x="brain_area", y="spike_counts", hue="feedback_type")


# %% [markdown]
# ---

# %% [markdown]
# # Ken's analysis

# %% [markdown]
# preprocessing

# %%
# Convert to dataframe
spk = dataset[['spike_trial', 'spike_time', 'spike_cell']].to_dataframe()
ba = dataset['brain_area'].to_dataframe()

# Filter cells from the 'VISp' brain area
cell_label = ba[ba['brain_area'] == 'VISp'].index
filtered_cells = spk[spk['spike_cell'].isin(cell_label)]

# Compute average spike time
average_spike_time = (filtered_cells.groupby(['spike_trial', 'spike_cell'])
                      .mean()['spike_time'])

average_by_cell = average_spike_time.groupby('spike_trial').mean()

# %% [markdown]
# indexing
# 

# %%
# Convert to dataframe and extract feedback types
feedback_df = dataset['feedback_type'].to_dataframe()

# Extract positive and negative feedback indices
positive_feedback_indices = feedback_df[feedback_df['feedback_type'] == 1].index.to_list()
negative_feedback_indices = feedback_df[feedback_df['feedback_type'] == -1].index.to_list()

# Filter the average_by_cell based on feedback type
f1 = average_by_cell[positive_feedback_indices]
f2 = average_by_cell[negative_feedback_indices]

# %% [markdown]
# statistics

# %%

t_stat, p_val = ttest_ind(f1, f2)

# %%
# Plot histograms
plt.hist(f1,  alpha=0.5, color='blue', label='Reward 1')
plt.hist(f2,  alpha=0.5, color='red', label='Reward -1')

# Add legend and title
plt.legend(loc='upper right')
plt.title('Spike time - reward - pVal:' + str(round(p_val,4)))
# Display the plot
plt.show()

# %% [markdown]
# preprocessing


# Extract 'brain_area' data and identify 'SUB' cells
brain_areas = dataset['brain_area'].to_dataframe()
sub_cell_indices = brain_areas[brain_areas['brain_area'] == 'SUB'].index

# Process 'spike_rate' data for 'SUB' cells
spike_rate_data = dataset['spike_rate'].to_dataframe().reset_index()
sub_spike_rate = spike_rate_data[spike_rate_data['cell'].isin(sub_cell_indices)]
avg_spike_rate_per_trial = sub_spike_rate.groupby(['trial', 'cell']).mean()['spike_rate']
avg_spike_rate = avg_spike_rate_per_trial.groupby('trial').mean()

# Process 'spike_time' data for 'SUB' cells
spike_time_data = dataset[['spike_time', 'spike_cell', 'spike_trial']].to_dataframe()
sub_spike_time = spike_time_data[spike_time_data['spike_cell'].isin(sub_cell_indices)]
avg_spike_time_per_trial = sub_spike_time.groupby(['spike_trial', 'spike_cell']).mean()['spike_time']
avg_spike_time = avg_spike_time_per_trial.groupby('spike_trial').mean()

# Extract 'reaction_time' data
reaction_times = dataset['reaction_time'].to_dataframe().values.flatten()

# Construct the final dataframe
df = pd.DataFrame({
    'reaction_time': reaction_times,
    'spike_time': avg_spike_time,
    'spike_rate': avg_spike_rate
})


# %%
df = df.reset_index()
df

# %%
# Extract feedback types and identify positive and negative indices
feedback_types = dataset['feedback_type'].to_dataframe()
positive_indices = feedback_types[feedback_types['feedback_type'] == 1].index.to_list()
negative_indices = feedback_types[feedback_types['feedback_type'] == -1].index.to_list()

# Filter the main dataframe based on feedback type indices
f1 = df.iloc[positive_indices, :]
f2 = df.iloc[negative_indices, :]


# %%

plt.subplot(3, 1, 1)  # (nrows, ncols, index)
plt.plot(f1.index, f1.reaction_time)
plt.title('reaction time')
plt.grid(True, which='both', linestyle='--', linewidth=0.5)

# Second subplot
plt.subplot(3, 1, 2)
plt.plot(f1.index, f1.spike_time, color='green')
plt.title('Spike time')
plt.grid(True, which='both', linestyle='--', linewidth=0.5)

# Third subplot
plt.subplot(3, 1, 3)
plt.plot(f1.index, f1.spike_rate, color='red')
plt.title('spike rate')
plt.xlabel('x')
plt.grid(True, which='both', linestyle='--', linewidth=0.5)

# Adjust the layout to prevent overlap
plt.tight_layout()

# Display the subplots
plt.show()

# %%
df = dataset['lfp'].to_dataframe().reset_index()
df

# %%


s = sorted(list(set(df.brain_area_lfp)))
pairs = list(itertools.combinations(s, 2))
pairs

# %%
conn_mat = np.array([1,2,3,4,5,6,7,8,9,10,11])
name_list = ['SUB-ACA',	'SUB-CA3',	'SUB-DG',	'SUB-LS',	'SUB-Mos',	'SUB-VISp',	'VISp-ACA',	'VISp-CA3',	'VISp-DG',	'VISp-LS',	'VISp-Mos',]

# %%
conn_mat_trial = np.zeros((7,7,1))


# %%
for i in set(df.trial):
    i_trial = df[df.trial==i]
    tmp_time_trial = i_trial[['lfp']].values.reshape((7,-1))
    correlation_matrix = np.corrcoef(tmp_time_trial)
    sub_mat = correlation_matrix[np.r_[0:5, 6],5]
    v_mat = correlation_matrix[:-2,6]
    merge_mat = np.hstack([sub_mat, v_mat])
    conn_mat = np.vstack([conn_mat,merge_mat])
    conn_mat_trial = np.concatenate((conn_mat_trial, correlation_matrix.reshape((7,7,1))), axis=2)

# Compute the correlation matrix


# %%
sns.heatmap(conn_mat_trial.mean(axis=2), annot=True, cmap='viridis')
# Sample labels
labels_list = list(set(df.brain_area_lfp))

# Create a heatmap with labels
sns.heatmap(conn_mat_trial.mean(axis=2), annot=True, cmap='viridis',
            xticklabels=labels_list, yticklabels=labels_list)

# Display the plot
plt.show()

# %%
data = conn_mat[1:,:]
feedback_df = dataset['feedback_type'].to_dataframe()
non_nan_indices = feedback_df.notna()
data = data[non_nan_indices.feedback_type.values,:]
label = feedback_df.dropna().values


X_train, X_test, y_train, y_test = train_test_split(data, label, test_size=0.2, random_state=42)

scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)
# clf = SVC(kernel='rbf',probability=True)
# clf.fit(X_train_scaled, y_train)

# y_pred = clf.predict(X_test_scaled)
# accuracy = accuracy_score(y_test.ravel(), y_pred)
# accuracy

# %%
# Hyperparameter tuning with GridSearchCV
parameters = {
    'C': np.linspace(0.1,100,1000),
    'kernel': ['rbf'],
    'gamma': ['scale', 'auto']
}

svc = SVC(probability=True)
clf = GridSearchCV(svc, parameters, cv=5)
clf.fit(X_train_scaled, y_train)

# Train the SVM with best parameters
best_svc = clf.best_estimator_

# Predict on the test set
y_pred = best_svc.predict(X_test_scaled)
accuracy = accuracy_score(y_test.reshape((-1,)), y_pred)

# %%
accuracy


# %%



# %%
# Use SHAP's KernelExplainer for non-tree models
explainer = shap.KernelExplainer(best_svc.predict_proba, X_train_scaled, link="logit")
shap_values = explainer.shap_values(X_test_scaled)

# Plot the SHAP values
shap.summary_plot(shap_values, X_test_scaled, feature_names=name_list, class_names=['Reward','Not Reward'])
