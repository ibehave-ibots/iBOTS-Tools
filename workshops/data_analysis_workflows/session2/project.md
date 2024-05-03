## Merging multiple files into a single file for downstream analysis

### Steinmetz Dataset

We will be using a subset of the Steinmetz dataset ([Nature 2019](https://www.nature.com/articles/s41586-019-1787-x)) which contains 3 Neuropixels recordings of 400-700 neurons each from across the mouse brain during a visual behavior task. Briefly, the task was a decision-making task where the mouse had to decide whether the contrast of a left stimulus is higher or the contrast of the right stimulus, and reported their decision by turning a wheel such that the stimulus with the higher contrast was moved to the center (e.g. if the right stimulus had a higher contrast, they moved the wheel to the left).

#### Download the data
- Steinmetz data for three recording sessions (~13MB): [https://uni-bonn.sciebo.de/s/2kRLP1Qsj4VXwLk](https://uni-bonn.sciebo.de/s/2kRLP1Qsj4VXwLk)
- Same data but without neural responses (~6MB): [https://uni-bonn.sciebo.de/s/cELWgBIoFCl2ts3](https://uni-bonn.sciebo.de/s/cELWgBIoFCl2ts3)

For a more detailed decsription (maybe while the data is being downloaded?) you can watch this short (~8min) [YouTube video](https://youtu.be/WXn4-FpVaOo?si=0dIgwNUWGajmZ4B6)

---

### Task: Merge single-trial variables into a single CSV file

The goal is to create a CSV file that contains all the variables that have a single value per trial. These variables are basically task-related and performance-related variables that are stored in the `task` and `performance` folder for each session:

- Each column of the CSV file should be single variable and each row is a single trial.
- Additionally we would also want to have the metadata (the info in the `metadata.json`) in this CSV file (info such as `session_date`, `mouse_name`, `stim_onset`, etc.)

**Focusing on a single session**: We will be focusing on a single recording session (e.g. subject "Lederberg" and session "20171205").

Here are the steps for this task:
1. create a CLI/script, called `merge_task_data.py` that given the path to the task data, combines all files into a CSV file called `task_data.csv`
2. create a CLI/script that given the path to the performance data, combines all the files into a CSV file called `performance_data.csv`
3. create a CLI/script, called `merge_single_trial_data.py`, that takes the path to `task_data.csv` and `performance_data.csv` and combines them together into a single CSV file called `single_trial_data.csv`

This is a group project, so let's do it together (while someone shares the screen). And feel free to explore the data as you like (e.g. in a Jupyter Notebook), and use all the tools (Google, ChatGPT, etc.) you have access to.

**Things to keep in mind**
- Let's stay organized: 
    - scripts in `scripts` folder
    - CLIs in `clis` folder
    - processed data (i.e. resulting CSV files) in the `steinmetz/processed` folder
- Let's keep track and document our development by making commits (and pushing to GitHub)