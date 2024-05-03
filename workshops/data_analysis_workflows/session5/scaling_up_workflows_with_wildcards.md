## Scaling up Snakemake workflows with wildcards

One of the benefits of Snakemake as a workflow management system is that it provides an easy way to apply the same workflow as new data comes in. By leveraging wildcards, a feature in Snakemake, we can adapt our existing workflows to process multiple datasets with minimal additional effort.

Wildcards in Snakemake are placeholders or variables used in rules that can match multiple file names or data identifiers, allowing for the flexible and dynamic generation of workflow tasks. When you define a rule in Snakemake, you can use wildcards to specify parts of file names that vary between different instances of the same type of file. For example, if you have multiple datasets named `dataset1.csv`, `dataset2.csv`, instead of explicitly specifying `path/to/dataset1.csv` in the rule you can use a wildcard in your rule to match all these files by making the variable portion of the name a wildcard: `path/to/dataset{session_id}.csv`. In this case Snakemake knows that `{session_id}` is not fixed.

This is how the complete rule could look like using wildcards:
```python
rule clean_dataset:
    input: "data/raw/dataset{session_id}.csv"
    output: "data/processed/dataset{session_id}_clean.csv"
    run:
        import pandas as pd
        df = pd.read_csv(input[0])              # Use indexing since 'input' can contain multiple items
        df_clean = df.dropna()                  # remove rows with NaN values
        df_clean.to_csv(output[0], index=False) # Use indexing since 'output' can contain multiple items
```

The last component that we need to add to this Snakemake workflow is the `rule all` where we list all the outputs we expect the workflow to generate:

```python
rule all:
    input:
        "data/processed/dataset1_clean.csv",
        "data/processed/dataset2_clean.csv"
```

Putting these two components together we have our complete Snakefile:
```python
workdir: "../.."

rule all:
    input:
        "data/processed/dataset1_clean.csv",
        "data/processed/dataset2_clean.csv"

rule clean_dataset:
    input: "data/raw/dataset{session_id}.csv"
    output: "data/processed/dataset{session_id}_clean.csv"
    run:
        import pandas as pd
        df = pd.read_csv(input[0])              # Use indexing since 'input' can contain multiple items
        df_clean = df.dropna()                  # remove rows with NaN values
        df_clean.to_csv(output[0], index=False) # Use indexing since 'output' can contain multiple items
```

**Exercise**: The above Snakefile is already in `workflows/workflow1` folder. Run it and see if it works. We should see that the `processed` folder is created and we have two csv files in it.

<br>

**Exercise**: Create a rule that takes the `dataset{session_id}.csv` (in the `data/raw` folder) and saves a new file `dataset{session_id}_valid.csv` (in the `data/processed` folder) only containing valid trials. You can use the following Python code directly in the rule:
```python
df = pd.read_csv(input[0])
df_valid = df[df.valid].copy()
df_valid.to_csv(output[0], index=False)
``` 
Please run the rule and check if it works.

<br>

**Exercise**: In the `data/raw` folder we have some subject-specific data for two subjects. Create a rule that takes the `task{session_id}.csv` for each subject and saves a new file `task{session_id}_valid.csv` (in the `data/processed` folder) only containing valid trials. Note that we want the output files to also be stored in subject-specific folders, just like how it is in the `data/raw` folder. Use can use the same Python code as in the previous exercise. Please run the rule and check if it works.

<br>

**Exercise**: In our subject-specific data we also have the reponse time for each session. Create a histogram for each `response_time.npy` file and save them in the `figures` folder, while maintaining the subject-specific folder structure. You can use the following Python code directly in the rule to save a histogram for a specific response time file:
```python
import numpy as np
import matplotlib.pyplot as plt
data = np.load(input[0])
plt.hist(data)
plt.savefig(output[0])
```
Please run the rule and check if it works.

---

### Accessing wildcards inside the code

We can also access specific values of the wildcards that we define in the file path. We can access the specific value of the wildcard either inside the python code or pass it to a python scripts as additional arguments. Going back to our first example, let's assume we would like to additionally add the `session_id`, which is a wildcard, as a new column to our data as we clean it. We can get the specific value of `session_id` in our code using `wildcards.session_id`:

```python
rule clean_dataset:
    input: "data/raw/dataset{session_id}.csv"
    output: "data/processed/dataset{session_id}_clean.csv"
    run:
        import pandas as pd
        df = pd.read_csv(input[0])                      # Use indexing since 'input' can contain multiple items
        df_clean = df.dropna()                          # remove rows with NaN values
        df_clean["session_id"] = wildcards.session_id   # add session_id as a column
        df_clean.to_csv(output[0], index=False)         # Use indexing since 'output' can contain multiple items
```

**Exercise**: Change the rule from the very first exercise to the above version and see if the `session_id` is indeed added as a new column.

<br>

**Exercise**: Change the rule for creating histogram for the response time such that the histogram has a different color for each subject.

---

### Workflow for the Steinmetz dataset

Let's create a workflow for the Steinmetz dataset. We have a workflow folder called `workflow_steinmetz`. Inside it you'll find a Snakefile that already contains rules to create figures for some of the behavioral variables using some of the functions we create together during the workshop. 

It's time to put it all together, but there is one last step that is missing: the current version of the workflow is only designed to work with the data from a specific recording session. First check if the current workflow works properly, and then let's changes it such that it runs for all the recording sessions we have 🎉