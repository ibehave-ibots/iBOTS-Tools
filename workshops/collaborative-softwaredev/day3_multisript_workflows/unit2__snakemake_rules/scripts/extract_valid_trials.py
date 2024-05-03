import sys
import pandas as pd

# Command-line inputs
input_csv_path = sys.argv[1]
output_csv_path = sys.argv[2]

# Load the csv file and extract active trials
df = pd.read_csv(input_csv_path)
df_valid = df[df.valid].copy()

# Save the new dataframe as a csv file
df_valid.to_csv(output_csv_path, index=False)