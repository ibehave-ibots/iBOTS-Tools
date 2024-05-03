
## Creating workflows with Snakemake

So far we have been creating single rules (representing a single step in our analysis) which are the building blocks of a Snakemake workflow. Now let's practice connecting mulitple rules to each other to create a workflow.

As an example, let's expand the `clean_data` rule from the previous section. Once we have the cleaned data, we might want to extract specific columns of it for downstream analysis. This means that we will have a new rule that as input needs the clean version of the data.

```python
rule clean_data:
    input: "data/raw/dataset.csv"
    output: "data/processed/clean_dataset.csv"
    run:
        import pandas as pd
        df = pd.read_csv(input[0])
        df_clean = df.dropna()
        df_clean.to_csv(output[0], index=False)

rule extract_columns:
    input: "data/processed/clean_dataset.csv"
    output: "data/processed/specific_columns.csv"
    run:
        import pandas as pd
        df = pd.read_csv(input[0])
        # Assuming we want columns 'A' and 'B'
        df_extracted = df[['A', 'B']]
        df_extracted.to_csv(output[0], index=False)
```

**No need to run every single rule**: Since the second rule depends on the first rule (i.e. the input to the second rule is the output of the first rule) if we only run the second rule, Snakemake will automallically detect this dependency and run the first rule as well. So the command to run the whole workflow would be:
```
snakemake --cores 1 extract_columns
```

Let's go through some exercises and practice creating Snakemake workflows.

---

### Creating Workflows

**Setup**: Let's create a new `Snakefile` for the following exercises:
- inside the `workflows` folder create a new folder called `workflow2`
- inside the `workflow2` folder create a `Snakefile`
- as you go through the exerices, please implement the rules inside this newly created `Snakefile`
- also, feel free to re-use the rules we created in the previous session when applicable

**Exercise**: Create a workflow that contains two rules:
1. the first rule combines `array1.npy` and `array2.npy` and saves as a new file called `combined_array.npy` 
2. the second rule depends on the first rule such that it takes the `combined_array.npy` and save the standardized verion of it as `combined_array_standardized.npy`.

Please run the workflow and check if it works.

**Exercise**: Create a workflow that contains two rules:
1. the first rule combines `array1.npy` and `array2.npy` and saves as a new file called `combined_array.npy`. **Note** that we do not need to create this rule again since we already implemented it in the previous exercise.
2. the second rule depends on the first rule such that it takes the `combined_array.npy` and save the normalized verion of it as `combined_array_normalized.npy`.

Please run the workflow and check if it works.

**Exercise**: Create a workflow that contains two rules:
1. the first rule takes the `session.csv` (in the `data/raw` folder) and saves a new file `session_valid.csv` (in the `data/processed` folder) only containing valid trials.
2. the second rule takes `session_valid.csv` and saves a new file `session_valid_correct_response.csv` (in the `data/processed` folder) only containing valid trials in which the subjects' response was correct (i.e. response=1).

Please run the workflow and check if it works.

---

### Running multiple workflows together

So far we have created multiple workflows that are independent of each other (i.e. parallel workflows). And we can run each one of them by simply calling the name of the last rule in the workflow. But can we run multiple workflows that are independent from each other using just one command?

Yes! to do this we can use `rule all`. All we need to do is to add a new rule at the very top of our `Snakefile` called `rule all` and we list the final outputs of all workflows as input for `rule all`:

```python
# Define the rule all with all final output files as inputs
rule all:
    input:
        "data/other_workflow/combined_array_standardized.npy",
        "data/processed/session_valid_correct_response.csv"
```

With this example, now if we run the following command, worflows that are responsible to create the listed ouputs files will run:
```
snakemake --cores 1
```

<br>

**Exercise**: Modify the existing Snakefile such that all the output files are created by just running `snakemake --cores 1`
