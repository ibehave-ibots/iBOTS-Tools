Understood. I'll revise the README file to emphasize these specific features—automatic loading of associated dimensions and reshaping data into long tables, inspired by xarray's `load_dataset().to_dataframe()` feature in Python. Here's the updated README:

---

# NetCDF MATLAB Class

## Overview

The NetCDF MATLAB Class is an efficient tool designed to emulate the functionality of xarray's `load_dataset().to_dataframe()` feature in Python, tailored for MATLAB users. It is particularly useful for handling NetCDF files, a prevalent format for storing multi-dimensional scientific data. This class excels in automatically loading associated dimensions and seamlessly reshaping data into long table formats, making it invaluable for environmental, climate, and oceanographic data analysis.

## Key Features

- **Automatic Dimension Loading**: Associated dimensions of data variables are automatically loaded, simplifying the handling of multi-dimensional data.
- **Data Reshaping**: Converts complex multi-dimensional data into user-friendly long table formats, mirroring xarray's ease of converting datasets to dataframes.
- **Read NetCDF Data**: Effortlessly read data from NetCDF files into MATLAB structures or tables with associated dimensions.
- **Autocompletion Support**: After creating the `NetCDF` object, variable names are auto-suggested.

## Usage

### Instantiating the NetCDF Class

Create an object to interact with a specific NetCDF file:

```matlab
ncObj = netcdf.NetCDF('path_to_your_file.nc');
```

### Reading Data with Dimensions

Automatically load data along with its associated dimensions:

```matlab
dataWithDims = ncObj.read2struct();
% Optionally specify particular variables
dataWithDims = ncObj.read2struct({'temperature', 'humidity'});
```

### Reshaping Data into Long Tables

Convert multi-dimensional arrays into long format tables, suitable for analysis:

```matlab
longFormatTable = ncObj.read2table({'temperature', 'pressure'});
```

### Retrieving Variable and Dimension Names

Get names of variables and their associated dimensions:

```matlab
varNames = ncObj.getLoadableVariables();
dimNames = ncObj.getDimensionNames();
```

### Displaying and Retrieving File Information

```matlab
% To display detailed info
ncObj.print_info();

% To get info as a structure
fileInfo = ncObj.info();
```

## Getting Started

2. **Add to MATLAB Path**: Ensure the `netcdf_reader` directory is in your MATLAB path.
3. **Begin Using**: Utilize the examples to start working with your NetCDF files.

## Dependencies

- MATLAB (version XYZ or later)
- NetCDF library for MATLAB

## Inspiration

This project is inspired by xarray's `load_dataset().to_dataframe()` feature in Python, aiming to bring similar functionality and ease of use to MATLAB users handling NetCDF data.

