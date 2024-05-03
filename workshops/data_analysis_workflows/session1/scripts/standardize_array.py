import sys
import numpy as np

# Command-line inputs
input_array_path = sys.argv[1] # grab the first input
output_array_path = sys.argv[2] # grab the second input

# Load the input and standardize it
input_array = np.load(input_array_path)
output_array = (input_array - np.mean(input_array)) / np.std(input_array)

# Save the standardized array
np.save(output_array_path, output_array)