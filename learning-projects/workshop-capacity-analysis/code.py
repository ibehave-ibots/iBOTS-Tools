# %% Setup


import random
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt



def simulate_proportion_interactions_varying_formations(P, team_sizes, N_values, simulations=30):
    """
    Simulate team formation with varying team sizes and number of team formations,
    and calculate the average proportion of other participants each participant interacted with.
    """
    experiment_data = []

    for S in team_sizes:
        for N in N_values:
            for _ in range(simulations):
                participants = list(range(P))
                interactions = {p: set() for p in participants}

                for _ in range(N):
                    random.shuffle(participants)
                    teams = [participants[i:i + S] for i in range(0, P, S)]
                    for team in teams:
                        for member in team:
                            interactions[member].update(set(team) - {member})

                proportions = [len(interactions[p]) / (P - 1) for p in participants]
                
                experiment_data.append({
                    "team_size": S, 
                    "N_formations": N, 
                    "avg_proportion": np.median(proportions),
                    "25_proportion": np.percentile(proportions, 25),
                    "75_proportion": np.percentile(proportions, 75),
                    "N_Participants": P
                })

    return experiment_data

# %% 
# Constants
team_sizes = [2, 3, 4, 5]  # Team sizes
N_values = [3, 4, 5]  # Number of team formations
P_range = list(range(5, 31))  # Participant range from 5 to 30
n_simulations = 400

# Collecting experiment data
all_experiment_data_varying_formations = []
for P in P_range:
    experiment_data = simulate_proportion_interactions_varying_formations(P, team_sizes, N_values, n_simulations)
    all_experiment_data_varying_formations.extend(experiment_data)

# %% Creating a DataFrame for the experiment data
df = pd.DataFrame(all_experiment_data_varying_formations)
df.to_parquet('participant_interactions_simulation.parquet')
df

# %% Plotting using seaborn
import pandas as pd

df = pd.read_parquet('participant_interactions_simulation.parquet')
g = sns.FacetGrid(df, col="N_formations", hue="team_size", col_wrap=3, height=5)
g.map(sns.lineplot, "N_Participants", "avg_proportion").add_legend()
g.set_titles("Team Formations: {col_name}")
g.set_axis_labels("Number of Participants (N)", "Average Proportion (%)")
g.set(ylim=(0, 1), xlim=(0, max(P_range)))
plt.show()

# %% Plotting what 75% of people will at least experience
g = sns.FacetGrid(df, col="N_formations", hue="team_size", col_wrap=3, height=5)
g.map(sns.lineplot, "N_Participants", "25_proportion").add_legend()
g.set_titles("Team Formations: {col_name}")
g.set_axis_labels("Number of Participants (N)", "Average Proportion (%)")
g.set(ylim=(0, 1), xlim=(0, max(P_range)))
plt.show()