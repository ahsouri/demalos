# UTF-8
# Catch and subset/output ALOS 30[m] DEM 
# Amir Souri (ahsouri@cfa.harvard.edu;ahsouri@gmail.com)


from typing import Type


class demalos(object):

    def __init__(self,lat0,lon0,dlat,dlon,alos_folder_in = None, alos_folder_out = None):

            import os.path
            '''
            Initializing alos with the primary inputs
            ARGS:
                lat0 (float): the lowest left latitude of our domain
                lon0 (float): the lowest left longitude of our domain
                dlat (float): the width of our domain
                dlon (float): the length of our domain
                alos_folder_in (str): the folder where alos data are (or will be) downloaded
                alos_folder_out (str): the folder of the output
            ''' 

            self.lat0 = lat0
            self.lon0 = lon0
            self.dlat = dlat
            self.dlon = dlon
            

            if (os.path.isdir(os.path.abspath(alos_folder_in))) and \
                (os.path.isdir(os.path.abspath(alos_folder_out))):
                  self.alos_folder_in = alos_folder_in
                  self.alos_folder_out = alos_folder_out
            else:
                raise TypeError("paths are either not a folder or non-existent")

    def download_alos(self,dem_file = None):
        
        import wget
        '''
           Download ALOS DEM for 5 by 5 deg globally
           currently thhe package doesn't download a subset 
           based on lat/lon, unless you specify exactly the 
           name of DEM file
        '''
        jaxa_url = 'https://www.eorc.jaxa.jp/ALOS/aw3d30/data/release_v2012/'



        if (dem_file is not None):
            wget.download(jaxa_url + dem_file + '.zip', self.alos_folder_in, bar=self.bar_progress)
            return

        hemisphere_1 = ['N','S']
        hemisphere_2 = ['W','E']

        files = []      
        for h1 in hemisphere_1:
            for h2 in hemisphere_2:
                for lat in range(0,95,5):
                    for lon in range(0,185,5):
                        if ((h1 == 'N') and (h2 == 'E')):
                           file = h1 + f"{lat:03}" + h2 + f"{lon:03}" + '_' +\
                                  h1 + f"{lat+5:03}" + h2 + f"{lon+5:03}" + '.zip'
                        if ((h1 == 'N') and (h2 == 'W')):
                           file = h1 + f"{lat:03}" + h2 + f"{lon:03}" + '_' +\
                                  h1 + f"{lat+5:03}" + h2 + f"{lon-5:03}" + '.zip' 
                        if ((h1 == 'S') and (h2 == 'W')):
                           file = h1 + f"{lat:03}" + h2 + f"{lon:03}" + '_' +\
                                  h1 + f"{lat-5:03}" + h2 + f"{lon-5:03}" + '.zip' 
                        if ((h1 == 'S') and (h2 == 'E')):
                           file = h1 + f"{lat:03}" + h2 + f"{lon:03}" + '_' +\
                                  h1 + f"{lat-5:03}" + h2 + f"{lon+5:03}" + '.zip' 
                        
                        files.append(jaxa_url + file)
        
        for f in files:
            wget.download(f, self.alos_folder_in, bar=self.bar_progress)

    def bar_progress(self,current, total, width=80):
        import sys
        progress_message = "Downloading: %d%% [%d / %d] bytes" % (current / total * 100, current, total)
        # Don't use print() as it will print in new line every time.
        sys.stdout.write("\r" + progress_message)
        sys.stdout.flush()

    def subset_alos(self):
        
        '''
           subset/merge alos geotiff files based on lat0/lon0
        '''

        import rasterio
        import glob
        from rasterio.merge import merge
        from shapely.geometry import Polygon
        import numpy as np
        import matplotlib.pyplot as plt
        
        within_box = []
        intersect_box = []
        # sort tiff files
        alos_fname = sorted(glob.glob(self.alos_folder_in + '/*DSM.tif'))

        for fname in alos_fname:
            try:
                src = rasterio.open(fname)
            except:
                continue
        
            out_trans = src.transform
            # check the boundaries and make polygons
            width = src.width
            height = src.height

            corner1 =  out_trans * (0,0)     
            corner4 =  out_trans * (height,width)

            pol_alos = Polygon([(corner1[0],corner4[1]), (corner4[0],corner4[1]), (corner4[0],corner1[1]), 
                             (corner1[0],corner1[1]), (corner1[0],corner4[1])])

            pol_target = Polygon([(self.lon0,self.lat0), 
                          (self.lon0+self.dlon,self.lat0),
                          (self.lon0+self.dlon,self.lat0+self.dlat), 
                          (self.lon0,self.lat0+self.dlat),
                          (self.lon0,self.lat0)])

            #x,y = pol_alos.exterior.xy
            #plt.plot(x, y, c = "blue")
            #print(x,y)
            #x,y = pol_target.exterior.xy
            #print(x,y)
            #plt.plot(x, y, c = "red")
            #plt.show()
           
            if (pol_alos.contains(pol_target)):
               within_box.append(fname)
            elif (pol_alos.intersects(pol_target)) and (pol_alos.intersection(pol_target).area>0.0):
               intersect_box.append(fname)
        
        if ((not within_box) and (not intersect_box)):
            raise TypeError("the pool data do not cover this area; download more!")
            
        if (not within_box) and (intersect_box):
            src_appended = []
            for int_box in range(len(intersect_box)):
                src = rasterio.open(intersect_box[int_box])
                src_appended.append(src)
                
            alos_dem, out_trans = merge(src_appended)
            print('Several tiles are chosen from the pool')
            # if there is at least one master to fully enclose the slave
        elif within_box:           
            print('The chosen ALOS file is ' +  within_box[0])
            src = rasterio.open(within_box[0])
            out_trans = src.transform
            alos_dem = src.read(1)

        # getting lat and lons based on the transformation
        lat_alos = np.zeros_like(alos_dem)*np.nan
        lon_alos = np.zeros_like(alos_dem)*np.nan
        for i in range(np.shape(alos_dem)[0]):
            for j in range(np.shape(alos_dem)[1]):
                temp = out_trans * (j,i)
                lat_alos[i,j] = temp[0] 
                lon_alos[i,j] = temp[1]

        self.lat_alos = np.float32(lat_alos)
        self.lon_alos = np.float32(lon_alos)
        self.alos_dem = np.array(alos_dem).squeeze()
        self.crs = src.crs
        self.transform = out_trans

    def save_to_tiff(self,filename):
         
        '''
           save the outputs to a geotiff file (filename) 
           in alos_folder_out folder
        '''

        import rasterio
        import numpy as np  
            
        new_tiff = rasterio.open(
            self.alos_folder_out + str(filename),
            'w',
            driver='GTiff',
            height=self.alos_dem.shape[0],
            width=self.alos_dem.shape[1],
            count=1,
            dtype=np.float32,
            crs=self.crs,
            transform=self.transform,
            )

        new_tiff.write(self.alos_dem,1)
        new_tiff.close()
    
    def save_to_nc(self,filename):
         
        '''
           save the outputs to a ncfile (filename) 
           in alos_folder_out folder
        '''

        from netCDF4 import Dataset
        import numpy as np
        from numpy import dtype
        import numpy as np  
            
        ncfile = Dataset(filename,'w')
        # create the x and y dimensions.
        ncfile.createDimension('x',np.shape(self.alos_dem)[0])
        ncfile.createDimension('y',np.shape(self.alos_dem)[1])

        data1 = ncfile.createVariable('ALOS_DEM',dtype('float64').char,('x','y'))
        data1[:,:] = self.alos_dem
        
        data2 = ncfile.createVariable('lat',dtype('float64').char,('x','y'))
        data2[:,:] = self.lat_alos
        
        data3 = ncfile.createVariable('lon',dtype('float64').char,('x','y'))
        data3[:,:] = self.lon_alos