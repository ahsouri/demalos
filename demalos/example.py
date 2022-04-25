from demalos import demalos

alos_obj = demalos(41,-112,0.2,0.2,alos_folder_in='/Volumes/Amir_5TB/SAO/ALOS_DEM/in/N040W115_N045W110',
                   alos_folder_out='/Volumes/Amir_5TB/SAO/ALOS_DEM/out/')

alos_obj.subset_alos()
alos_obj.save_to_tiff("output_test.tif")
