import argparse
import pandas as pd
import glob
from tqdm import tqdm
import pathlib
import json

# Create a parser object
parser = argparse.ArgumentParser(description='Collect CSV files')

# Add an argument
parser.add_argument('input_path', type=str, help='Path to where single CSV files are located')
parser.add_argument('output_path', type=str, help='Path where to save the final CSV file in')

# Parse the arguments
args = parser.parse_args()

path_to_data = args.input_path
output_path = args.output_path

# Collect all the csv files
all_paths = glob.glob(path_to_data + "*.csv")
dfs = []
for path in tqdm(all_paths):
    df_per_trial = pd.read_csv(path)
    dfs.append(df_per_trial)

beh_df = pd.concat(dfs)

# Add the metadata
metadata_path = pathlib.Path(path_to_data).with_name("metadata.json")
metadata = json.loads(metadata_path.read_text())

beh_df["session_date"] = metadata["session_date"]

beh_df.to_csv(output_path)