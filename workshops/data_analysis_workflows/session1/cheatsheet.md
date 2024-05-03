Here are some functions that might come handy going through the exercises.

<br>

**Sys Module Functions**

| Function               | Code Example                           | Description                                                   |
|------------------------|----------------------------------------|---------------------------------------------------------------|
| Get the first argument | `args = sys.argv[1]`                   | Access the first arguments passed to the script.              |
| Get the first argument | `args = sys.argv[2]`                   | Access the second arguments passed to the script.             |
| Get the first argument | `args = sys.argv[3]`                   | Access the third arguments passed to the script.              |

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