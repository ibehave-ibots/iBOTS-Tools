## iBOTS Workshop: Developing Neuroscience Data Analysis Projects with Python, Git, and Snakemake

As neuroscience evolves with increasingly large data sets, complex analyses, and bigger teams, building robust, reproducible, and scalable analysis workflows becomes essential in order to develop large computational science projects and keep them sustainable over time. 

In this workshop, you will gain hands-on experience in crafting modular code scripts and command-line tools for efficient data processing, and how to cleanly combine them into a complete analysis pipeline, using Python’s snakemake package. We will explore tools such as Conda package manager to ensure consistent computational environments, vital for sharing code and ensuring computational reproducibility, and Git and GitHub for collaborating and sharing code across teams.

By the end of this workshop, you'll be able to develop and manage data analysis pipelines, ensuring that your projects are not only advanced in their execution but also sustainable in the long term - your future self will thank you for it!

---

### Session 1: Git, GitHub, and Python Scripts
- [**Git Slides**](https://docs.google.com/presentation/d/1E9Ap5-I2Z5R7aGThrE6gF_eFwFvvOseedldnha76V6w/edit?usp=sharing): The basics of git and GitHub
- [**Exercises**](session1/exercises.md): The basics of creating Python scripts

### Session 2: Command-Line Interfaces (CLIs) with Python
- [**Exercises**](session2/exercises.md): The basics of creating CLIs
- [**Project**](session2/project.md): Using scripts and CLIs to collect per-trial data into a single file

### Session 3: Python Modules and Functions
- [**Exercises - part 1**](session3/notebooks/1_python_functions.ipynb): Creating python functions
- [**Exercises - part 2**](session3/notebooks/2_functions_from_modules.ipynb): Organizing functions into Python modules
- [**Project**](session3/notebooks/3_identifying_repetitive_patterns.ipynb): Extracting functions from existing project code and storing them into modules 

### Session 4: Workflows with Snakemake [![Generic badge](https://img.shields.io/badge/Open_in_Gitpod-FF8F0E.svg)](https://gitpod.io/#https://github.com/ibehave-ibots/iBOTS-Developing-Data-Analysis-Projects)
- [**Exercises - part 1**](session4/1_intro_to_snakemake.md): Intro to Snakemake and creating single rules
- [**Exercises - part 2**](session4/2_workflows_with_snakemake.md): Creating workflows with Snakemake

### Session 5: Scaling up Snakemake Workflows [![Generic badge](https://img.shields.io/badge/Open_in_Gitpod-FF8F0E.svg)](https://gitpod.io/#https://github.com/ibehave-ibots/iBOTS-Developing-Data-Analysis-Projects)
- [**Exercises**](session5/scaling_up_workflows_with_wildcards.md): Scaling up Snakemake workflows with wildcards
- [**Project**](session5/scaling_up_workflows_with_wildcards.md#workflow-for-the-steinmetz-dataset): Creating a Snakemake workflow for Steinmetz dataset
