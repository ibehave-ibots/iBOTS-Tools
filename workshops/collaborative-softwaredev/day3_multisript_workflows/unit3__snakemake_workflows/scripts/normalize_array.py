import sys
import numpy as np

# Command-line inputs
input_array_path = sys.argv[1]
output_array_path = sys.argv[2]

# Load the input and normalize it
input_array = np.load(input_array_path)
output_array = input_array - np.min(input_array)
output_array = output_array / np.max(output_array)

# Save the normalized array
np.save(output_array_path, output_array)