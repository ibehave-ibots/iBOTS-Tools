Here are some functions/commands that might come handy going through the exercises.

### Argparse CLI Functions

**Argparse**

| Function      | Code Example                                                                                    | Description                                                      |
|--------------|---------------------------------------------------------                                        |------------------------------------------------------------------|
| Create Parser| `parser = argparse.ArgumentParser(description='CLI Tool')`                                      | Initialize a new argument parser for CLI.                        |
| Add Argument | `parser.add_argument('name', type=str, help='user name')`                                       | Define a positional argument for the CLI.                        |
| Parse Args   | `args = parser.parse_args()`                                                                    | Parse the arguments given at the command line.                   |
| Numeric Arg  | `parser.add_argument('number', type=int, help='a number')`                                      | Accept a numeric input and ensure it's of type `int`.            |
| Optional Arg | `parser.add_argument('--sum', dest='accumulate', action='store_const', const=sum, default=max)` | Add an optional argument with a default value.                   |

<br>

**Terminal Commands for CLIs**

| Command      | Example                                               | Description                                                      |
|--------------|------------------------------------------------------------|------------------------------------------------------------------|
| Help Flag    | `python cli_name.py -h`                                    | Display the help message for the CLI.                            |

<br>

**Numpy Functions**

| Function       | Code                             | Description                                     |
|----------------|----------------------------------|-------------------------------------------------|
| Load array     | `array = np.load('file.npy')`    | Load a numpy array from a .npy file.            |
| Save array     | `np.save('file.npy', array)`     | Save a numpy array to a .npy file.              |
| Array mean     | `np.mean(array)`                 | Compute the mean of an array.                   |
| Array std dev  | `np.std(array)`                  | Compute the standard deviation of an array.     |
| Array minimum  | `np.min(array)`                  | Find the minimum value in an array.             |
| Array maximum  | `np.max(array)`                  | Find the maximum value in an array.             |

<br>

**Pandas Functions**

| Function          | Code                                     | Description                                                      |
|-------------------|------------------------------------------|------------------------------------------------------------------|
| Read CSV          | `df = pd.read_csv('file.csv')`           | Read data from a CSV file into a DataFrame.                      |
| Write CSV         | `df.to_csv('file.csv', index=False)`     | Write a DataFrame to a CSV file.                                 |
| Column mean       | `df.mean()`                              | Compute the mean of each column in a DataFrame.                  |
| Column std dev    | `df.std()`                               | Compute the standard deviation of each column in a DataFrame.    |
| Column minimum    | `df.min()`                               | Compute the minimum of each column in a DataFrame.               |
| Column maximum    | `df.max()`                               | Compute the maximum of each column in a DataFrame.               |
| Conditional select| `df.loc[df['column'] > value]`           | Access rows and columns by labels or a boolean array based on a condition. |
