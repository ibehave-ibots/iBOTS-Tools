# %%
# pip install --upgrade xarray seaborn pandas numpy

# %%
import xarray as xr
import matplotlib.pyplot as plt 
import numpy as np
import pandas as pd
import seaborn as sns

# %% [markdown]
# 1. Extracting XArray data into Tidy Pandas DataFrames
#   - Multiple columns
#  (dset['column1'].to_dataframe().reset_index();  sns.catplot(kind=))
# 2. Plotting Subsets of your data using Logical Indexing
#   - `visp = lfp[lfp['brain_area_lfp'] == 'VISp']; sns.relplot(data=, x=, y=, estimator=, errorbar=, col=, col_wrap=, kind='line')`
# 3. Making and Displaying Pivot Tables (`df.groupby().agg().unstack()`), (`df.pivot_table(index='col1', columns='col2', values='col3', agg='mean')`
#   - `sns.heatmap`
#     - 'annot=' and 'fmt=
#     - normalize along different axes?
#   - `style.background_gradient()`



# %%

# %%

# %% [markdown]
# ### Download the dataset

# %%
from pathlib import Path
import requests
from tqdm import tqdm

def download_from_sciebo(public_url, to_filename, is_file=True):
    """
    Downloads a file or folder from a shared URL on Sciebo.
    """
    # Create the folder if a longer path was described
    path = Path(to_filename)
    if len(path.parts) > 1:
        Path(to_filename).parent.mkdir(parents=True, exist_ok=True)

    r = requests.get(public_url + "/download", stream=True)

    if 'Content-Length' in r.headers and is_file:
        total_size = int(r.headers['Content-Length'])
        progress_bar = tqdm(desc=f"Downloading {to_filename}", unit='B', unit_scale=True, total=total_size)
    else:
        progress_bar = None

    with open(to_filename, 'wb') as f:
        for chunk in r.iter_content(chunk_size=8192):
            f.write(chunk)
            if progress_bar:
                progress_bar.update(len(chunk))

    if progress_bar:
        progress_bar.close()

download_from_sciebo('https://uni-bonn.sciebo.de/s/JFeueaaWCTVhTZh', 'data/steinmetz_2016-12-14_Cori.nc')

# %% [markdown]
# # ERP Analysis With Pandas And Seaborn

# %% [markdown]
# ---
# 
# ## Overview
# 
# We will continue to use [Steinmetz et al, 2019 in Nature](https://www.nature.com/articles/s41586-019-1787-x) dataset. The experiment involved a mouse being presented with two gradients of varying intensities. The mouse's task was to adjust a wheel to center the brighter gradient on the screen. Simultaneously, Local Field Potential (LFP) measurements were recorded across various brain areas. These measurements were taken 250 times in 2.5 seconds, with data collected at 0.01-second intervals. 
# 
# 
# **Analysis goals**
# 
# In these exercises, our primary objective is to analyze and visualize Local Field Potential (LFP) data collected from distinct brain regions separately. Through this analysis, we aim to:
#   - compute trial statistics on LFP amplitudes (e.g. mean, min, max)
#   - compare these statistics between different brain areas
#   
# 
# **Learning goals**
# 
# In this notebook, we'll focus on learning Seaborn's:
#   - `sns.lineplot()` function for plotting time series models
#   - `sns.relplot()` for making faceted rows and columns of data of figures effectively using relplot and
#   - `sns.heatmap()` for using colors to compare trends.

# %% [markdown]
# ---
# ## Extracting Data from XArray Datasets into Tidy DataFrames
# ### Load Dataset
# 
# In this section, we'll work with a dataset from a single session recording of Cori the mouse ('steinmetz_2016-12-14_Cori.nc'). 
# 
# Our primary objective is to read this data and convert it into a Pandas dataframe, which will serve as the foundation for the subsequent exercises.
# 
# **Load dataset and convert to Pandas dataframe:**
# 
# | Method/Code                                             | Description                                                                   |
# |--------------------------------------------------------|-------------------------------------------------------------------------------|
# | `dset = xr.load_dataset("path/to/file/like/this.nc")` | Loads the dataset from the specified file path using xarray (`xr`).      |
# | `df = dset['column1'].to_dataframe()`                    | Extracts the 'column1' data variable from the dataset and converts it into a Pandas DataFrame (`df`). |
# | `df.reset_index()`                                   | Resets the index of the 'df' DataFrame to create a default integer index.   |
# | `dset['column1'].to_dataframe().reset_index()` | All of it, together! |

# %% [markdown]
# **Exercises**

# %% [markdown]
# Make a variable called `dset` by calling by Xarray's `xr.load_dataset()` function on the 'steinmetz_2016-12-14_Cori.nc' session file.  Confirm that the "lfp" data variable is there.

# %%
dset = xr.load_dataset('data/steinmetz_2016-12-14_Cori.nc')
dset

# %% [markdown]
# **Example** Extract 'brain_area' data variable to Pandas dataframe and store it in ba variable

# %%
ba = dset['brain_area'].to_dataframe()
ba

# %% [markdown]
# Hmm! It might be good to have a separate index instead of using cell as index
# 
# **Example** reset_index of ba and display first five rows of the data

# %%
ba = ba.reset_index()
ba.head(5)

# %% [markdown]
# You can actually do the above two steps into a single step using `dset['brain_area].to_dataframe().reset_index()`. Can you try that out below?

# %%
ba = dset['brain_area'].to_dataframe().reset_index()
ba.head(5)

# %% [markdown]
# Great! Now, let's do this to the data we are going to use for the exercises

# %% [markdown]
# Convert 'lfp' data to Pandas dataframe and store it in lfp variable

# %%
lfp = dset['lfp'].to_dataframe().reset_index()
lfp.head(5)

###########################################################
# Learning goals
# Single dset['single_column']
# Sin


###########################################################

# %% [markdown]
# ## Explore and Visualize LFP Data for VISp Area
# 
# What was the variation of LFP measured from VISp brain area? 
# 
# Seaborn combined with some data extraction from Pandas dataframe provides an easy way to visualize this. First we will learn how to extract trials only from VISp area. Then we will warm up to Seaborn and visualization by plotting measurements from only one trial. Finally in this section, we will plot all trials together
# 
# | Code / Method                           | Description                                                         |
# |----------------------------------------|---------------------------------------------------------------------|
# | `df[df["col_1"] == 'val_1']`          | Filters and displays rows from the DataFrame where 'col_1' equals 'val_1'. |
# | `df[(df["col_1"] == 'val_1') & (df["col_2"] == number)]` | Filters and displays rows from the DataFrame where 'col_1' equals 'val_1' and 'col_2' equals a specified number. |
# | `sns.lineplot(data=df, x="column1", y="column2", hue="column3", ...)` | In Seaborn, this code is used to create a line plot. It specifies the DataFrame (`data`), the x-axis column (`x`), the y-axis column (`y`), and the column for splitting the data into different colors (`hue`). Additional columns can be added to create more complex plots. |

# %% [markdown]
# **Exercises**: Using the Pandas DataFrame Below, Make Line Plots that only  extract only 'trial' column

# %%
lfp = dset['lfp'].to_dataframe().reset_index()
lfp.head(5)
lfp['trial']


# %% [markdown]
# Extract only 'brain_area_lfp' 

# %%
lfp['brain_area_lfp']

# %% [markdown]
# **Example** Can we see what are the different brain areas?

# %%
lfp['brain_area_lfp'].unique()

# %% [markdown]
# There are 7 brain areas

# %% [markdown]
# **Example** Extract all rows where 'trial' == 5

# %%
lfp[lfp['trial'] == 5]

# %% [markdown]
# Extract all rows where 'trial' == 1

# %%
lfp[lfp['trial'] == 1]

# %% [markdown]
# Extract all rows where 'brain_area_lfp' == 'VISp'

# %%
lfp[lfp['brain_area_lfp'] == 'VISp']

# %% [markdown]
# Great! Now let's combine the two column conditions together to extract all rows where 'trial' == 1 and 'brain_area_lfp' == 'VISp'
# 
# Hint: Use df[(df['col_1'] == value) & (df['col_2'] == value)] to combine the two conditions

# %%
lfp[(lfp['trial'] == 1) & (lfp['brain_area_lfp'] == 'VISp')]

# %% [markdown]
# **Example** Plot trial 1 LFP measurements from VISp brain area

# %%
visp_trial_1 = lfp[(lfp['trial'] == 1) & (lfp['brain_area_lfp'] == 'VISp')]
sns.lineplot(data=visp_trial_1, x='time', y='lfp')

# %% [markdown]
# Can you do the same for the second trial?

# %%
visp_trial_2 = lfp[(lfp['trial'] == 2) & (lfp['brain_area_lfp'] == 'VISp')]
sns.lineplot(data=visp_trial_2, x='time', y='lfp')

# %% [markdown]
# Good! One more for trial 3?

# %%
visp_trial_3 = lfp[(lfp['trial'] == 3) & (lfp['brain_area_lfp'] == 'VISp')]
sns.lineplot(data=visp_trial_3, x='time', y='lfp')

# %% [markdown]
# It will take a long time to plot all the trials individually? Is there a way to plot all trials in a single plot? 
# 
# Spoiler alert! Yes
# 
# Seaborn has a way of knowing that you want to plot each trial in different color by setting hue parameter.
# 
# sns.lineplot(data=, x=, y=, hue='trial')

# %% [markdown]
# **Example** Extract only VISp brain area and plot all trials in the same plot using hue='trial'. How does it look? Does it make sense? 

# %%
visp = lfp[lfp['brain_area_lfp'] == 'VISp']
sns.lineplot(data=visp, x='time', y='lfp', hue='trial')

# %% [markdown]
# Extract only ACA brain area and plot all trials in the same plot using hue='trial' 

# %%
aca = lfp[lfp['brain_area_lfp'] == 'ACA']
sns.lineplot(data=aca, x='time', y='lfp', hue='trial')

# %% [markdown]
# Once more: Extract only SUB brain area and plot all trials in the same plot using hue='trial'

# %%
sub = lfp[lfp['brain_area_lfp'] == 'SUB']
sns.lineplot(data=sub, x='time', y='lfp', hue='trial')

# %% [markdown]
# The plot is over-crowded and even the legend of trials does not display all the trials. Seaborn likely groups the unique trials into a smaller number of aggregated entries, making it easier to visualize and interpret. Can we try to use statistical measures like mean to simplify this plot?

# %% [markdown]
# ## Visualize LFP Data for VISp Area (mean/median of all trials in a time bin)

# %% [markdown]
# We will aggregate LFP for all trials and plotting a single line that represents the overall trend of 'lfp' values over time across all trials.
# 
# The following steps have to be performed for this
# 1. Group and aggregate the data such that there is only one measurement per time bin (mean LFP across all trials at a given time)
# 2. Estimate a range of values within which the aggregation metric (mean/median) is likely to fall with 90/95/99 percent confidence (Confidence Interval)
# 3. Plot the resulting time series
# 4. Also plot the confidence interval
# 
# **Luckily, Seaborn can do all these for us in a single line of code. Phew!**

# %% [markdown]
# | Method/Code       | Description                                                         |
# |-------------------|---------------------------------------------------------------------|
# | `sns.lineplot()`  | Creates a line plot using Seaborn. Specifies the following parameters:
# |                   | - `data`: DataFrame variable that the plot will be made from.
# |                   | - `x`: Column to use for the x-axis of the plot.
# |                   | - `y`: Column to use for the y-axis of the plot.
# |                   | - `errorbar`: Metric to display as error bar or error band.
# |                   | - `n_boot`: Number of bootstrap resampling to compute confidence intervals.
# |                   | - `estimator`: Metric to aggregate values for plot ('mean'/'median'/'min'/'max'/'size' ...) . 
# | `sns.relplot()`   | Creates a relational plot using Seaborn. Specifies the following parameters:
# |                   | - `data`: DataFrame variable that the plot will be made from.
# |                   | - `x`: Column to use for the x-axis of the plot.
# |                   | - `y`: Column to use for the y-axis of the plot.
# |                   | - `errorbar`: Metric to display as an error bar or error band.
# |                   | - `n_boot`: Number of bootstrap resampling to compute confidence intervals.
# |                   | - `col`: Different panels for each unique value in the specified column.
# |                   | - `kind`: Specifies the type of plot; "line" for a line plot, "scatter" for a scatter plot.
# |                   | - `col_wrap`: Defines the layout of panels, creating a new row of panels after every 'n' unique categories. 

# %% [markdown]
# **Example** Plot aggregate LFP values at each time bin along with error band representing the confidence interval

# %%
visp = lfp[lfp['brain_area_lfp'] == 'VISp']
sns.lineplot(data=visp, x='time', y='lfp', errorbar='ci')

# %% [markdown]
# That must have taken a while! The parameter `errorbar='ci'` specifies that confidence intervals should be added to the lineplot to indicate the uncertainty in the data. Seaborn will compute and add error bars to the plot to represent the confidence intervals for the data points. We can make this quicker by setting the parameter `n_boot` to a numerical value which sets the number of bootstrap resampling iterations used to compute the confidence intervals. 

# %% [markdown]
# Repeat the same plot but set n_boot=100

# %%
sns.lineplot(data=visp, x='time', y='lfp', errorbar='ci', n_boot=100)

# %% [markdown]
# Seaborn provides different ways to represent the uncertainty (errorbar) apart from 'ci'. 

# %% [markdown]
# Set errorbar='sd' to plot standard deviation instead of confidence intervals

# %%
sns.lineplot(data=visp, x='time', y='lfp', errorbar='sd', n_boot=100)

# %% [markdown]
# Set errorbar='se' to plot standard error 

# %%
sns.lineplot(data=visp, x='time', y='lfp', errorbar='se', n_boot=100)

# %% [markdown]
# Let's do the same for ACA brain area

# %%
aca = lfp[lfp['brain_area_lfp'] == 'ACA']
sns.lineplot(data=aca, x='time', y='lfp', errorbar='ci', n_boot=100)

# %% [markdown]
# One more for LS 

# %%
ls = lfp[lfp['brain_area_lfp'] == 'LS']
sns.lineplot(data=ls, x='time', y='lfp', errorbar='ci', n_boot=100)

# %% [markdown]
# You can even set confidence intervals. By default, it is 95%. We can set it to 99% (the chance of us being wrong about the mean lying within this range is 1%)
# 
# Set errorbar=('ci', 99)

# %%
ls = lfp[lfp['brain_area_lfp'] == 'LS']
sns.lineplot(data=ls, x='time', y='lfp', errorbar=('ci', 99), n_boot=100)

# %% [markdown]
# Set 90% confidence interval

# %%
ls = lfp[lfp['brain_area_lfp'] == 'LS']
sns.lineplot(data=ls, x='time', y='lfp', errorbar=('ci', 90), n_boot=100)

# %% [markdown]
# You can also set different estimator instead of mean using `estimator` parameter. It takes in any of the Pandas method like 'mean', 'median', 'size', 'std' etc!

# %% [markdown]
# **Example** Use estimator='median' for 'LS' brain area

# %%
ls = lfp[lfp['brain_area_lfp'] == 'LS']
sns.lineplot(data=ls, x='time', y='lfp', estimator='median', errorbar='ci', n_boot=100)

# %% [markdown]
# Use estimator='median' for 'ACA' brain area

# %%
aca = lfp[lfp['brain_area_lfp'] == 'ACA']
sns.lineplot(data=aca, x='time', y='lfp', estimator='median', errorbar='ci', n_boot=100)

# %% [markdown]
# Just for the fun of it, use estimator='size' for 'ACA' brain area

# %%
aca = lfp[lfp['brain_area_lfp'] == 'ACA']
sns.lineplot(data=aca, x='time', y='lfp', estimator='size', errorbar='ci', n_boot=100)

# %% [markdown]
# That's a funny plot where it shows that there are 364 values available at each time measurement. The choice of estimator depends on what you are interested in. Generally mean or median are enough to get meaningful information about the data!

# %% [markdown]
# 
# We plotted each brain area separately. Wouldn't it be great if we can have this plot for all brain areas separated into different panels with a single line?
# 
# Seaborn has this capability with the help of relational plot or `relplot`.

# %% [markdown]
# Plot line plots with columns where each column is for a different brain area. 
# 
# Seaborn relational plot (relplot) with line plots with x='time', y='lfp', col='brain_area_lfp', errorbar='ci' computed from 10 resamples (n_boot=10).

# %%
sns.relplot(data=lfp, x='time', y='lfp', col='brain_area_lfp', kind='line', errorbar='ci', n_boot=10)

# %% [markdown]
# That plot looks a bit too wide. Wouldn't it be nice to have only three columns? We can let relplot know this by using the argument `col_wrap=3`

# %%
sns.relplot(data=lfp, x='time', y='lfp', col='brain_area_lfp', col_wrap=3, kind='line', errorbar='ci', n_boot=10)

# %% [markdown]
# Use estimator='median' to plot medians instead of means

# %%
sns.relplot(data=lfp, x='time', y='lfp', col='brain_area_lfp', col_wrap=3, kind='line', estimator='median', errorbar='ci', n_boot=10)

# %% [markdown]
# Use estimator 'min'

# %%
sns.relplot(data=lfp, x='time', y='lfp', col='brain_area_lfp', col_wrap=3, kind='line', estimator='min', errorbar='ci', n_boot=10)

# %% [markdown]
# For the sake of completion, use estimator='max'

# %%
sns.relplot(data=lfp, x='time', y='lfp', col='brain_area_lfp', col_wrap=3, kind='line', estimator='max', errorbar='ci', n_boot=10)

# %% [markdown]
# ## Visualizing Average LFP Data with Heatmap

# %% [markdown]
# Let's try to visualize same information for all brain area in a different format. Sometimes, it might be enough to only see variations in terms of color change rather than number. This case, heatmap could be very informative to identify patterns in the time series of mean LFP signal across all trials.
# 
# We will make use of group-by method of Pandas dataframe to aggregate LFP and Seaborn heatmap method to visualize

# %% [markdown]
# `sns.heatmap()`: Create a heatmap visualization to display the mean LFP data using a color gradient. </br>
# `df.groupby()`: Aggregate colums with respect to a categorical valued column. </br>
# `df.unstack()`: Convert multi-index dataframe to wide format table. </br>

# %% [markdown]
# **Example** Find mean lfp of each brain_area 

# %%
lfp.groupby('brain_area_lfp')['lfp'].mean()

# %% [markdown]
# Find mean lfp of each time

# %%
lfp.groupby('time')['lfp'].mean()

# %% [markdown]
# There are other aggregation methods too like median(), std() for standard deviation, min() for minimum, max() for maximum, etc

# %% [markdown]
# Find median LFP of each brain area

# %%
lfp.groupby('brain_area_lfp').median()

# %% [markdown]
# Find minimum lfp of each brain_area

# %%
lfp.groupby('brain_area_lfp')['lfp'].min()

# %% [markdown]
# Find maximum lfp of each brain_area

# %%
lfp.groupby('brain_area_lfp')['lfp'].max()

# %% [markdown]
# Find standard deviation of LFP in each brain area

# %%
lfp.groupby('brain_area_lfp')['lfp'].std()

# %% [markdown]
# **Example** Let's find mean lfp value of each trial of each brain area

# %%
lfp.groupby(['brain_area_lfp', 'trial'])['lfp'].mean()

# %% [markdown]
# Find mean lfp value of each time bin of each brain area

# %%
lfp.groupby(['brain_area_lfp', 'time'])['lfp'].mean()

# %% [markdown]
# We can convert this table to a wide format using `.unstack()` method. Can we try that?

# %%
lfp.groupby(['brain_area_lfp', 'time'])['lfp'].mean().unstack()

# %% [markdown]
# Amazing! Put this result in a dataframe

# %%
group = lfp.groupby(['brain_area_lfp', 'time'])['lfp'].mean().unstack()
group

# %% [markdown]
# Visualize this using heatmap with the help of below code
# 
# sns.heatmap(name_of_the_grouped_dataframe)

# %%
sns.heatmap(group)

# %% [markdown]
# We can select color map by specifying 'cmap'. There are many color maps to choose from like
# 
# 'viridis'
# 
# 'inferno'
# 
# 'Greys'
#  
# etc

# %% [markdown]
# 
# Plot a heatmap and set cmap='viridis'

# %%
sns.heatmap(group, cmap='viridis')

# %% [markdown]
# We can set minimum and maximum values to anchor the colormap using vmin and vmax 
# 
# Set vmin=-6 and vmax=6

# %%
sns.heatmap(group, cmap='viridis', vmin=-6, vmax=6)

# %% [markdown]
# **Example** try plotting medians?

# %%
group = lfp.groupby(['brain_area_lfp', 'time'])['lfp'].median().unstack()
sns.heatmap(group, cmap='viridis')

# %% [markdown]
# Try plotting minimum LFP values? 

# %%
group = lfp.groupby(['brain_area_lfp', 'time'])['lfp'].min().unstack()
sns.heatmap(group, cmap='viridis')

# %% [markdown]
# Try plotting maximum LFP values? 

# %%
group = lfp.groupby(['brain_area_lfp', 'time'])['lfp'].max().unstack()
sns.heatmap(group, cmap='viridis')


