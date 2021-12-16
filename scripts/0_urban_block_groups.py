#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""

Produce shapefile for block groups that are contained in urban areas.

Data can be downloaded here:
    https://www.census.gov/cgi-bin/geo/shapefiles/index.php?year=2015&layergroup=Block+Groups
    

"""

# Import modules
import geopandas as gpd
import os
import glob

# Define global filepath
path = '/home/johnny/Documents/Teaching/490_Geospatial_Data_Science_Applications/Applications/OSM_Parks_and_Golf/data/'

# Import urban areas shapefile
urban = gpd.read_file(path + 'urban_areas/tl_2020_us_uac10.shp')

# Import state codes
codes = gpd.read_file(path + 'state_codes.csv')

# Define list of block group shapefiles
bg_list = sorted(glob.glob(path + 'census_block_groups_2015/*/*.shp'))

for i in range(len(bg_list)):
    
    # Get path and filename seperately 
    infilepath, infilename = os.path.split(bg_list[i])
    # Get file name without extension            
    infilehortname, extension = os.path.splitext(infilename)
    print('Processing number %.0f out of %.0f' %(i+1, len(bg_list)))
    
    # Read file
    bg = gpd.read_file(bg_list[i])
    
    # Intersect
    urban_bg = gpd.sjoin(bg, urban, how='inner', op='within')
    
    # Drop some unnecessary columns
    urban_bg.drop(columns=['UACE10', 'GEOID10', 'NAME10', 'NAMELSAD10', 'LSAD10', 'MTFCC10',
       'UATYP10', 'FUNCSTAT10', 'ALAND10', 'AWATER10', 'INTPTLAT10',
       'INTPTLON10', 'index_right'], inplace=True)
    
    # Get state abbreviation
    abv = codes['Postal Code'][codes['FIPS'].astype(int) == int(infilehortname[8:10])].values[0]
    
    # Define new id column
    urban_bg['code'] = abv
    urban_bg['idx'] = urban_bg.index.values.astype(str)
    urban_bg['id'] = urban_bg['code'] + urban_bg['idx']
    
    # Drop some unnecessary columns
    urban_bg.drop(columns=['code', 'idx'], inplace=True)
               
    # Save to file
    urban_bg.to_file(path + 'urban_block_groups/' + infilehortname + '_urban.shp')
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
