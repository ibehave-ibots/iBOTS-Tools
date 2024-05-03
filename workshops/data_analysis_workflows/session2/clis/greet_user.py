import argparse

# Create a parser object
parser = argparse.ArgumentParser(description='Greet the user')

# Add an argument
parser.add_argument('name', type=str, help='Name of the user')

# Parse the arguments
args = parser.parse_args()

# Print the greeting
print(f'Hello, {args.name}!')