import glob
import numpy as np
from tqdm import tqdm
from scipy.io import loadmat
from pathlib import Path

def merge_behavioral_data_npy(input_data_folder):
    
    data_label = Path(input_data_folder).name
    all_npy_files = glob.glob(input_data_folder + "*.npy")

    npy_data = []
    for filename in tqdm(all_npy_files, desc=f"Merging the {data_label} data"):
        npy_data_per_trial = np.load(filename)
        npy_data.append(npy_data_per_trial)

    npy_data = np.stack(npy_data)
    return npy_data

def merge_behavior_data_mat_as_npy(input_data_folder, variable_name):
    
    all_mat_files = glob.glob(input_data_folder + "*.mat")

    mat_data = []
    for filename in tqdm(all_mat_files, desc=f"Merging the {variable_name} position data"):
        mat_data_per_trial = loadmat(filename)[variable_name].squeeze()
        mat_data.append(mat_data_per_trial)

    mat_data = np.stack(mat_data)
    return mat_data