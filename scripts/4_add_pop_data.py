#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""

Add census data to block group shapefile.

"""

# Import modules
import geopandas as gpd
import pandas as pd
import numpy as np
import glob

# Define path
path = '/home/johnny/Documents/Teaching/490_Geospatial_Data_Science_Applications/Applications/OSM_Parks_and_Golf/data/'

# Import state codes
codes = pd.read_csv(path + 'state_codes.csv')

# Define block group files
bg_list = sorted(glob.glob(path + 'state_stats/data*.shp'))
pop_list = sorted(glob.glob(path + 'pop_by_block_group/*.csv'))

# Define urban areas
urban = gpd.read_file(path + 'urban_areas/tl_2020_us_uac10.shp')

for j in range(codes.shape[0]):
    # Get FIPS code
    fips = str(codes['FIPS'].iloc[j]).zfill(2)
    
    # Get state name
    state_name = codes['Name'].iloc[j].replace(' ', '_')
    
    print('Processing... %.0f out of %.0f' %(j+1, codes.shape[0]))
    
    #######################################################################
    # Get corresponding files
    #######################################################################
    
    # Get block groups shapefile
    matching_bg = [s for s in bg_list if fips + '_' + state_name + '.shp' in s]
    
    # Get block group population table
    matching_pop = [s for s in pop_list if '_' + fips in s]
    
    #######################################################################
    # Read all files
    #######################################################################
    bg_gdf = gpd.read_file(matching_bg[0])
    pop_df = pd.read_csv(matching_pop[0])

    #######################################################################
    # Add population column to block group shapefile
    #######################################################################
    # Edit some columns so they match
    pop_df['COUNTYFP'] = np.char.zfill(pop_df['county'].values.astype(str), 3)
    pop_df['TRACTCE'] = np.char.zfill(pop_df['tract'].values.astype(str), 6)
    pop_df['BLKGRPCE'] = pop_df['block group'].astype(str)
    
    # Merge
    bg_pop_gdf = pd.merge(left=bg_gdf, right=pop_df, on=(['COUNTYFP', 'TRACTCE', 'BLKGRPCE']))
    
    # Drop some unnecessary columns
    bg_pop_gdf.drop(columns=['county', 'tract', 'block group'], inplace=True)
    
    ###########################################################################
    # Also add urban area name for analysis
    ###########################################################################
    # First convert to WGS84
    bg_pop_gdf = bg_pop_gdf.to_crs('EPSG:4326')
    urban = urban.to_crs('EPSG:4326')
    
    # Intersect
    urban_bg_pop = gpd.overlay(bg_pop_gdf, urban, how='intersection')
    
    # Drop some unnecessary columns
    urban_bg_pop.drop(columns=['UACE10', 'GEOID10', 'NAMELSAD10', 'LSAD10',
       'MTFCC10', 'UATYP10', 'FUNCSTAT10', 'ALAND10', 'AWATER10', 'INTPTLAT10',
       'INTPTLON10', 'NAME'], inplace=True)
    
    # Rename and format some columns
    urban_bg_pop.rename(columns={'B01001_001E': 'Population', 
                                 'B25077_001E': 'HousePrice',
                                 'B19013_001E': 'Income'}, inplace=True)
    
    urban_bg_pop['White'] = urban_bg_pop['B03002_003E']
    urban_bg_pop['Black'] = urban_bg_pop['B03002_004E']
    urban_bg_pop['Asian'] = urban_bg_pop['B03002_006E']
    urban_bg_pop['Hispanic'] = urban_bg_pop['B03003_003E']
    urban_bg_pop['Other'] = (urban_bg_pop['B03002_005E'] + urban_bg_pop['B03002_007E']\
                             +  urban_bg_pop['B03002_008E'] +  urban_bg_pop['B03002_009E'])

    
    urban_bg_pop['SumAge'] = (urban_bg_pop.iloc[:, 30] * 2.5) +\
                              (urban_bg_pop.iloc[:, 31] * 7) +\
                              (urban_bg_pop.iloc[:, 32] * 12) +\
                              (urban_bg_pop.iloc[:, 33] * 16) +\
                              (urban_bg_pop.iloc[:, 34] * 18.5) +\
                              (urban_bg_pop.iloc[:, 35] * 20) +\
                              (urban_bg_pop.iloc[:, 36] * 21) +\
                              (urban_bg_pop.iloc[:, 37] * 23) +\
                              (urban_bg_pop.iloc[:, 38] * 27) +\
                              (urban_bg_pop.iloc[:, 39] * 32) +\
                              (urban_bg_pop.iloc[:, 40] * 37) +\
                              (urban_bg_pop.iloc[:, 41] * 42) +\
                              (urban_bg_pop.iloc[:, 42] * 47) +\
                              (urban_bg_pop.iloc[:, 43] * 52) +\
                              (urban_bg_pop.iloc[:, 44] * 57) +\
                              (urban_bg_pop.iloc[:, 45] * 60.5) +\
                              (urban_bg_pop.iloc[:, 46] * 63) +\
                              (urban_bg_pop.iloc[:, 47] * 65.5) +\
                              (urban_bg_pop.iloc[:, 48] * 68) +\
                              (urban_bg_pop.iloc[:, 49] * 72) +\
                              (urban_bg_pop.iloc[:, 50] * 77) +\
                              (urban_bg_pop.iloc[:, 51] * 82) +\
                              (urban_bg_pop.iloc[:, 52] * 85) +\
                              (urban_bg_pop.iloc[:, 53] * 2.5) +\
                              (urban_bg_pop.iloc[:, 54] * 7) +\
                              (urban_bg_pop.iloc[:, 55] * 12) +\
                              (urban_bg_pop.iloc[:, 56] * 16) +\
                              (urban_bg_pop.iloc[:, 57] * 18.5) +\
                              (urban_bg_pop.iloc[:, 58] * 20) +\
                              (urban_bg_pop.iloc[:, 59] * 21) +\
                              (urban_bg_pop.iloc[:, 60] * 23) +\
                              (urban_bg_pop.iloc[:, 61] * 27) +\
                              (urban_bg_pop.iloc[:, 62] * 32) +\
                              (urban_bg_pop.iloc[:, 63] * 37) +\
                              (urban_bg_pop.iloc[:, 64] * 42) +\
                              (urban_bg_pop.iloc[:, 65] * 47) +\
                              (urban_bg_pop.iloc[:, 66] * 52) +\
                              (urban_bg_pop.iloc[:, 67] * 57) +\
                              (urban_bg_pop.iloc[:, 68] * 60.5) +\
                              (urban_bg_pop.iloc[:, 69] * 63) +\
                              (urban_bg_pop.iloc[:, 70] * 65.5) +\
                              (urban_bg_pop.iloc[:, 71] * 68) +\
                              (urban_bg_pop.iloc[:, 72] * 72) +\
                              (urban_bg_pop.iloc[:, 73] * 77) +\
                              (urban_bg_pop.iloc[:, 74] * 82) +\
                              (urban_bg_pop.iloc[:, 75] * 85)
    
    urban_bg_pop['MeanAge'] = urban_bg_pop['SumAge'] / urban_bg_pop['Population']
    urban_bg_pop['NumChildren'] = urban_bg_pop.iloc[:, 30:34].sum(axis=1) +\
                               urban_bg_pop.iloc[:, 53:57].sum(axis=1)
                    

    # Drop some unnecessary columns
    urban_bg_pop.drop(columns=['B03002_001E', 'B03002_003E', 'B03002_004E', 
                               'B03002_005E', 'B03002_006E', 'B03002_007E',
                               'B03002_008E', 'B03002_009E', 'B03002_010E', 
                               'B03002_011E', 'B03002_012E',
                               'B01001_003E', 'B01001_004E', 'B01001_005E', 'B01001_006E',
                               'B01001_007E', 'B01001_008E', 'B01001_009E', 'B01001_010E',
                               'B01001_011E', 'B01001_012E', 'B01001_013E', 'B01001_014E',
                               'B01001_015E', 'B01001_016E', 'B01001_017E', 'B01001_018E',
                               'B01001_019E', 'B01001_020E', 'B01001_021E', 'B01001_022E',
                               'B01001_023E', 'B01001_024E', 'B01001_025E', 
                               'B01001_027E', 'B01001_028E', 'B01001_029E', 'B01001_030E', 
                               'B01001_031E', 'B01001_032E', 'B01001_033E', 'B01001_034E', 
                               'B01001_035E', 'B01001_036E', 'B01001_037E', 'B01001_038E', 
                               'B01001_039E', 'B01001_040E', 'B01001_041E', 'B01001_042E', 
                               'B01001_043E', 'B01001_044E', 'B01001_045E', 'B01001_046E', 
                               'B01001_047E', 'B01001_048E', 'B01001_049E',
                               'B03002_002E','B03003_001E', 'B03003_002E', 'B03003_003E',
                               'SumAge'], inplace=True)
    
    # Save to shapefile
    urban_bg_pop.to_file(path + 'state_stats_with_census/data_' + fips + '_' + state_name + '.shp')
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    