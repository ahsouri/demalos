from demalos import demalos

alos_obj = demalos(50,50,10,10,alos_folder_in='/Volumes/Amir_5TB/SAO/ALOS_DEM/in',
                   alos_folder_out='/Volumes/Amir_5TB/SAO/ALOS_DEM/out')

alos_obj.download_alos()
