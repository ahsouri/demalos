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
                raise TypeError("only folders are allowed!")

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
