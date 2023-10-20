# Convert Steinmetz NPZ Dataset to NetCDF

This data pipeline is used to make `.nc` files from the Steinmetz example neurophysiology data used in the Neuromatch Academy courses.

## Running the Pipeline

```bash
python scripts/1_download_data.py 
python scripts/2_convert_to_netcdf.py
```

## Data Source:

  - [Steinmetz Neuropixels Data](https://github.com/NeuromatchAcademy/course-content/blob/main/projects/neurons/load_steinmetz_extra.ipynb)
  - [Steinmetz LFP Data](https://github.com/NeuromatchAcademy/course-content/blob/main/projects/neurons/load_steinmetz_extra.ipynb)