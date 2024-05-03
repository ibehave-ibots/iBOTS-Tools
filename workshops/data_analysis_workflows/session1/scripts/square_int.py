import sys

# Get the number through argument passed in the console
# NOTE that we need to turn it into an integer (by default it is a string)
number = int(sys.argv[1])

# Perform the operation
number_squared = number ** 2

# print the name
print(f"Square of {number} is {number_squared}.")