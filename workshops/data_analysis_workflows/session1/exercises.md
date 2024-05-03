## Python Scripts

In data analysis, often there are standard steps that one needs to run before being able to explore the data and generate results. These steps are often focused around preprocessing and standardization of the data. Ideally, we want to write the code for these steps once, and as new datasets come in, just run them without having to rewrite or manually process the data each time. This is where Python scripts come into play, offering a powerful solution for automating these repetitive but essential preprocessing tasks.

### What are Python Scripts? And why use them?

Python scripts are essentially text files containing Python code that automate tasks by instructing the Python interpreter to execute a series of commands. They are invaluable in data analysis for several reasons:

- **Efficiency**: Scripts save time by automating repetitive tasks, such as data cleaning, merging datasets, and performing standard analyses. This allows analysts to focus on more complex problems and exploratory data analysis.
- **Consistency**: Automating tasks with scripts ensures that the same procedures are applied to the data in a consistent manner, reducing the risk of human error and ensuring that results are reliable and reproducible.
- **Scalability**: Scripts can easily be scaled to handle larger datasets or more complex analysis pipelines, making them suitable for both small and large-scale data analysis projects.
- **Shareability**: Scripts can be shared with other researchers or analysts, facilitating collaboration and peer review. This also aids in reproducing research findings, as others can execute the same scripts to verify results.

Here is an example for creating a basic Python script, and running it. The script will simply print "Hello, World!" to the console. While this example might seem simple and basic, it introduces the foundational skills of writing, saving, and executing Python scripts, setting the stage for more complex and data-focused tasks.

**Creating the Script**

Create a new file with a `.py` extension (i.e. a Python file), for example `hello_world.py`. Inside this file we can write any Python code, for instance:
```python
print("Hello, World!")
```
and save the file.

**Running the Script**
- Open a terminal (e.g. Command Prompt or Anaconda Prompt).
- Navigate to the directory where you saved the script.
- Execute the script by typing `python hello_world.py` in the terminal and pressing Enter.

Note that, inside the script we simply have Python code and it can contain any code that you would like to run. It could be a piece of code that cleans the data, transforms the data, combine files, save plots, etc. 

By going through the following exercises, let's explore different aspects of creating and executing python scripts.

Also, you might find some of the code/functions in the [cheatsheet](cheatsheet.md) useful. Let's start!

---

### Creating and executing Python scripts

In this section, we'll practice creating and executing python scripts.

**Exercise**: Hello, Python! 

Create a python script, called `hello_python.py`, that when we run it, it simply prints "Hello, Python!".

<br>

**Exercise**: 30-second counter

Create a script, called `timer_30s.py`, that functions as a 30-second timer. As we run the script with `python timer_30s.py`, we should see numbers printed in the terminal starting from 1 all the way to 30, with a 1-sec delay between them.

**Hint**: To implement a 1-second delay, you can you the `time` package:
```python
import time
time.sleep(1) # sleep for 1 second
```

---

### Python scripts with command-line arguments

Now that we know how to create and execute scripts, let's explore how we can pass information from the terminal to the script (i.e. command-line arguments).

**Example**: Hello Python with a twist

Create a `greet_user.py` script that accepts the NAME as an input argument. Here is how the content of this script would look like:

```python
import sys

# Get the name through argument passed in the console
name = sys.argv[1]

# print the name
print(f"Hello, {name}!")
```

Run the script with `python scripts/greet_user.py NAME` and see if it works. NAME can be any name you want.

<br>

**Example**: Square an integer value and print the result.

Create a python script, called `square_int.py`, that accepts a single integer as input, and prints the square of it. Here is how the content of this script would look like:

```python
import sys

# Get the number through argument passed in the console
# NOTE that we need to turn it into an integer (by default it is a string)
number = int(sys.argv[1])

# Perform the operation
number_squared = number ** 2

# print the name
print(f"Square of {number} is {number_squared}.")
```

Run the script with `python scripts/square_int.py NUMBER` and see if it works. NUMBER can be any number you want.

<br>

**Exercise**: Flexible Timer

Create a `timer.py` script that accepts the number of seconds as an argument. This is similar to `timer_30s.py`, but instead of being fixed to 30 seconds it depends on the number specified by the user.

<br>

**Exercise**: Add two numbers

Create a script, called `add_two_numbers.py`, that takes two numbers as input and prints the addition of them.

<br>

**Keep track of the development**: We have ceated some new files, let's commit the changes (with a short message) and push to GitHub.

---

### Loading, processing, and saving data files

Now that we have familiarized ourself with how to create and run Python scripts with input arguments, let's try some more realistic situations where we will be dealing with data files. For instance, reading a file and saving a transformed version of it.

Note that this is very similar to what we have done so far. That is, we still have python code in the script, but the inputs are mostly the path to where to current data is and the path where the new data should be saved to. We then use these paths that were given as input to the script and load and save the data accordingly.

Let's go through an example.

**Example**: Load numpy array, standardize it, and save the new version

We have a numpy array in the folder `data/raw` and we want to create a standardized version (mean=0 and std=1) of it, using the command:
```
python scripts/standardize_array.py data/raw/array.npy  data/processed/standardized_array.npy
```
**Note** that the standardized array is being saved in a folder called `data/processed`.

And here is the script `standardize_array.py` for this:
```python
import sys
import numpy as np

# Command-line inputs
input_array_path = sys.argv[1] # grab the first input
output_array_path = sys.argv[2] # grab the second input

# Load the input and standardize it
input_array = np.load(input_array_path)
output_array = (input_array - input_array.mean()) / input_array.std()

# Save the standardized array
np.save(output_array_path, output_array)
```

Run it and see if it works: was the `standardized_array.npy` successfully created?

<br>

**Exercise**: Load numpy array, normalize it, and save the new version

Create a python script, very similar to the previous one, but instead of saving a standardized version of the data, save a normalized version (all values should be between 0 and 1).

Here is how we want to run this script:
```
python scripts/normalized_array.py data/raw/array.npy  data/processed/normalized_array.npy
```

Did it work?

<br>

**Exercise**: Load CSV file, save a new CSV file only containing valid trials

We have CSV file in the `data` directory, that contains data from an experimental session. In total we had 100 trials, but not all of them are valid trials. The csv file has a column named `valid` which is either `True` or `False`. 

Create a script, called `extract_valid_trials.py`, that creates a new CSV file that only contains the valid trials.

Here is how we want to run this script:
```
python scripts/extract_valid_trials.py data/raw/session.csv  data/processed/session_valid.csv
```

<br>

**Keep track of the development**: We have ceated some new files, let's commit the changes (with a short message) and push to GitHub.

---

### Running python scripts in Jupyter Notebooks

Let's take this even a step further: let's imagine a situation where we have some data, we would like to process it, and explore the processed data in jupyter notebook. Using our scripts, we can do all of these steps in a jupyter notbook! 

Let's go through an example where we run a scipt to generate the processed data and then continue exploring this processed data in the notebook.

<br>

**Example**: In a Jupyter notebook, use the script `standardize_array.np` to create a standardized version (mean=0 and std=1) of the data and compare it with the original version. Please see (and run) the `standardize_array_script_demo.ipynb` in the `notebooks` directory.

<br>

**Exercise**: In a new notebook check if the `normalize_data.py` CLI works correclty.
- what are the min and max values of the original data?
- did the normalization work correctly? i.e. is data min value 0 and max value 1?

<br>

**Exercise**: In the same notebook, use the script `extract_valid_trials.py` to create a CSV file containing only valid trials, and use the resulting CSV file to compute the proportion of active trials where the subject's response was correct (i.e. `response=1`)

<br>

**Keep track of the development**: We have ceated some new files, let's commit the changes (with a short message) and push to GitHub.