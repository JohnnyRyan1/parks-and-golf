#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""

Compute centroids for parks and golf course and export to shapefile.

"""

# Import modules
import geopandas as gpd
import pandas as pd
import glob
import math

# Define path
path = '/home/johnny/Documents/Teaching/490_Geospatial_Data_Science_Applications/Applications/OSM_Parks_and_Golf/data/'

# Import urban areas shapefile
urban = gpd.read_file(path + 'urban_areas/tl_2020_us_uac10.shp')

# Convert urban to 
urban_wgs84 = urban.to_crs('EPSG:4326')

# Define parks and golf courses
park_list = sorted(glob.glob(path + 'parks_and_golf/*_parks.shp'))
golf_list = sorted(glob.glob(path + 'parks_and_golf/*_golf_courses.shp'))

def convert_wgs_to_utm(lon, lat):
    utm_band = str((math.floor((lon + 180) / 6 ) % 60) + 1)
    if len(utm_band) == 1:
        utm_band = '0'+utm_band
    if lat >= 0:
        epsg_code = '326' + utm_band
    else:
        epsg_code = '327' + utm_band
    return epsg_code

def export_centroids(file_list, category):
    
    df_list = []
    for infile in file_list:
        print('Processing... %s' %infile)
        
        # Read data
        data = gpd.read_file(infile)
        
        # Dissolve and explode to remove overlapping polygons
        dissolve = data.dissolve()
        dissolve = dissolve.explode()
        
        # Only get features contained in urban areas
        u_dissolve = gpd.sjoin(dissolve, urban_wgs84, how='inner', op='within')
        
        # Drop some unnecessary columns
        u_dissolve.drop(columns=['index_right', 'UACE10', 'GEOID10', 'NAME10',
       'NAMELSAD10', 'LSAD10', 'MTFCC10', 'UATYP10', 'FUNCSTAT10', 'ALAND10',
       'AWATER10', 'INTPTLAT10', 'INTPTLON10', 'FID'], inplace=True)
        
        # Get UTM zone EPSG code of state
        lon_poly, lat_poly = u_dissolve[(u_dissolve['geometry'].geom_type == 'Polygon')]['geometry'].iloc[0].exterior.coords.xy
        utm_zone = convert_wgs_to_utm(lon_poly[0], lat_poly[0])
        epsg = 'EPSG:' + utm_zone
        
        # Convert coordinates
        u_dissolve = u_dissolve.to_crs(epsg)
        
        # Compute area
        u_dissolve['area'] = u_dissolve['geometry'].area
        
        # Remove anything smaller than a football pitch
        u_dissolve = u_dissolve[u_dissolve['area'] > 7000]
        
        # Reset index
        u_dissolve.reset_index(inplace=True)
        
        # Compute centroids
        u_dissolve['centroid'] = u_dissolve['geometry'].centroid
        
        # Remove geometry column
        u_dissolve.drop(columns=['geometry'], inplace=True)
        u_dissolve.rename(columns={'centroid': 'geometry'}, inplace=True)
        
        # Convert back to WGS84
        u_dissolve = u_dissolve.to_crs('EPSG:4326')
    
        # Store DataFrame in list
        df_list.append(u_dissolve)
        
    df = pd.concat(df_list)
    
    return df
    
# Call function
park_df = export_centroids(park_list)
golf_df = export_centroids(golf_list)
    
# Export to shapefile
park_df.to_file(path + 'parks_and_golf_centroids/park.shp')
golf_df.to_file(path + 'parks_and_golf_centroids/golf.shp')


















    
    
