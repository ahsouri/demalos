[![DOI](https://zenodo.org/badge/485365918.svg)](https://zenodo.org/badge/latestdoi/485365918)

# demalos
Downloading and subsetting ALOS 30m DEM

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install demalos

```bash
pip install demalos
```

## Usage

see example.py

or 

```bash
from demalos import demalos

lat0 = 41
lon0 = -113
dlat = 0.1
dlon = 0.1

alos_obj = demalos(lat0,lon0,dlat,dlon,alos_folder_in='/Volumes/Amir_5TB/SAO/ALOS_DEM/in/N040W115_N045W110',
                   alos_folder_out='/Volumes/Amir_5TB/SAO/ALOS_DEM/out/')

alos_obj.subset_alos()
alos_obj.save_to_tiff("output_test3.tif")
alos_obj.save_to_nc("output_test3.nc")
```

to download alos files use

```bash
alos_obj.download_alos(dem_file = "N040W115_N045W110")
```

Warning! not specifying dem_file will make the code want to download the whole dataset

## License
[MIT](https://choosealicense.com/licenses/mit/)
