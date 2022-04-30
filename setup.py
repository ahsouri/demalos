from setuptools import setup,find_packages
from os.path import splitext
from os.path import basename
from glob import glob


with open('README.md') as f:
    readme = f.read()

setup(name='demalos',
      version='0.0.1',
      description='ALOS 30 m downloader/subsetter',
      long_description=readme,
      long_description_content_type='text/markdown',
      author='Amir Souri',
      author_email='ahsouri@gmail.com',
      license='MIT',
      packages=['demalos'],
      install_requires=[
          'wget','matplotlib','rasterio','netCDF4','rasterio','shapely'
      ],
      zip_safe=False)
