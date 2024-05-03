## Data Analysis Workflows with Snakemake

Data analysis often contains many steps before we are able to produce our final results and figures. Using a workflow management system that allows us to explicitly define our data analysis steps can help making the dependency between different steps more clear, allows us to apply the workflow on multiple datasets, and generally make our data analysis more reproducible, scalable, and easily shareable. 

**Snakemake** is a powerful tool for building these workflows. It leverages the simplicity of Python to create workflows that are not only easy to understand but also flexible and adaptable. By using Snakemake, we'll be equipped with a tool that streamlines the process of going from data to insights, making our research more efficient and effective.

### How does Snakemake work?

Snakemake operates on the principle of defining **"rules"** that specify how to produce one or more output files from one or more input files. Each rule outlines a specific step in our analysis, such as running some Python code, a script, or executing a command. These rules collectively form a workflow that Snakemake can execute in an optimized manner, automatically determining the order of tasks based on their dependencies and executing them in parallel where possible.

- **Rules**: At the heart of Snakemake, rules define the operations to perform. Each rule has inputs (the data you start with), outputs (the result of the rule), and a command or a script that transforms the input into the output.

- **Dependencies**: Snakemake automatically figures out which rules depend on which others by looking at their inputs and outputs. If the output of one rule is the input to another, Snakemake runs them in the correct order.

- **Parallel Execution**: When possible, Snakemake runs independent tasks in parallel, speeding up the analysis.

<br>

Let's start by focusing on defining single rules in Snakemake.

**Example Snakemake Rule**

Imagine a single step of data analysis where we want to clean the data (e.g. remove NaNs). Below are two examples of how this step can be implemented using a snakemake rule:

**Example1**: directly using Python code to perform the operation:

```python
rule clean_data:
    input: "path/to/data/data/raw/dataset.csv"
    output: "path/to/data/processed/clean_dataset.csv"
    run:
        import pandas as pd
        df = pd.read_csv(input[0])              # Use indexing since 'input' can contain multiple items
        df_clean = df.dropna()                  # remove rows with NaN values
        df_clean.to_csv(output[0], index=False) # Use indexing since 'output' can contain multiple items
```

**Example2**: Using a Python script or CLI:

```python
rule clean_data:
    input: "path/to/data/raw/dataset.csv"
    output: "path/to/data/processed/clean_dataset.csv"
    shell:
        "python path/to/scripts/clean_data.py {input} {output}"
```

In this rule, called `clean_data`, we used either directly Python code (example 1) or a Python script (example 2) to clean the raw dataset (`raw_dataset.csv`), producing a cleaned dataset (`cleaned_dataset.csv`).

**Where are these rules written?** snakemake rules are written inside a `Snakefile` that is usually stored in a workflow folder inside our project folder.

**Running the snakemake rule**: to run the snakemake rule (in this case `clean_data`) we use the following command in the terminal while being in the folder that contains the `Snakefile`:
```
snakemake --cores 1 clean_data
```

Let's get some practice creating Snakemake rule!

---
### Rules with a single input and single output

**Example**: Create a rule that takes the `array.npy` (in the `data/raw` folder) and simply saves a renamed version of it called `array_renamed.npy` (in the `data/processed` folder)

Steps:
- Inside the `workflows` folder, create a new folder called `workflow1`
- Inside `workflow1` create a file called `Snakefile`
- Define the rule inside the `Snakefile`
- In the terminal, navigate to the `workflow1` folder
- Run the rule with the command `snakemake --cores 1 rename_array`

**Did it work?** To make sure things worked out correctly, check if the file was actually created in the desired location. In this case, we should see that inside the  `data` folder, there is a new folder called `processed`, and inside that there is a file called `array_renamed.npy`.

<br>

**Setup**: For the following exercises, define the rules inside the same `Snakefile` - we can have multiple rules in the same `Snakefile` and there is no need to create a new one for the following exercises.

<br>

**Exercise**: Create a single rule that takes the `session.csv` (in the `data/raw` folder) and saves it as a `.parquet` file (in the `data/processed` folder). Directly use Python code in the rule.

Steps:
- Define the rule `change_csv_to_parquet` inside the `Snakefile` in `workflow1` folder
- In the terminal, navigate to the `workflow1` folder (you are probably already there)
- Run the rule with the command `snakemake --cores 1 change_csv_to_parquet`

<br>

**Exercise**: Create a rule that takes the `array.npy` (in the `data/raw` folder) and saves a standardized version of it called `array_standardized.npy` (in the `data/processed` folder). Directly use Python code in the rule. Please run the rule and check if it works.

<br>

**Exercise**: Create a rule that takes the `array.npy` (in the `data/raw` folder) and saves a normalized version of it called `array_normalized.npy` (in the `data/processed` folder). Use the corresponding script for this rule (look into the `scripts` folder). Please run the rule and check if it works.

<br>

**Exercise** Create a rule that takes the `session.csv` (in the `data/raw` folder) and saves a new file `session_valid.csv` (in the `data/processed` folder) only containing valid trials. Use the corresponding script for this rule (look into the `scripts` folder). Please run the rule and check if it works.

---

### Rules with multiple inputs or outputs

**Example**: Create a rule that combines `array1.npy` and `array2.npy` (both in the `data/raw` folder) into a single array and saves the result as a new file called `combined_array.npy` (in the `data/processed` folder). You can find this rule in the `Snakefile` already. Please run the rule and check if it works.

<br>

**Exercise**: Create a rule that takes `array1.npy` and `array2.npy` and saves a CSV file called `combined_data.csv` (in the `data/processed` folder) where each array is a single column. Directly use Python code in the rule. Please run the rule and check if it works.

<br>

**Exercise**: Create a rule that takes the `session.csv` (in the `data/raw` folder) and saves two files: `session_valid.csv` and `session_not_valid.csv` (both in the `data/processed` folder). Create a new script to use for this rule. Please run the rule and check if it works.

