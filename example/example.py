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
