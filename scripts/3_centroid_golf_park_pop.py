#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""

Compute distance to nearest greenspace and golf course for all block groups.

"""

# Import modules
import geopandas as gpd
import pandas as pd
import numpy as np
import glob
import os
import math
import scipy.spatial as spatial
from shapely.ops import nearest_points

# Define path
path = '/home/johnny/Documents/Teaching/490_Geospatial_Data_Science_Applications/Applications/OSM_Parks_and_Golf/data/'

# Import state codes
codes = pd.read_csv(path + 'state_codes.csv')

# Define parks and golf courses
parks_list = sorted(glob.glob(path + 'parks_and_golf/*_parks.shp'))
golf_list = sorted(glob.glob(path + 'golf_with_name/*_golf_courses.shp'))

# Define urban areas
bg_list = sorted(glob.glob(path + 'urban_block_groups/*.shp'))

# Define population data
pop_list = sorted(glob.glob(path + 'pop_by_block_group/*.csv'))

def convert_wgs_to_utm(lon, lat):
    utm_band = str((math.floor((lon + 180) / 6 ) % 60) + 1)
    if len(utm_band) == 1:
        utm_band = '0'+utm_band
    if lat >= 0:
        epsg_code = '326' + utm_band
    else:
        epsg_code = '327' + utm_band
    return epsg_code

for j in range(codes.shape[0]):
    
    # Get FIPS code
    fips = str(codes['FIPS'].iloc[j]).zfill(2)
    
    # Get state name
    state_name = codes['Name'].iloc[j].replace(' ', '_')
    
    if os.path.exists(path + 'state_stats/data_' + fips + '_' + state_name + '.shp'):
        print('Skipping... %.0f out of %.0f' %(j+1, codes.shape[0]))
    else:
        print('Processing... %.0f out of %.0f' %(j+1, codes.shape[0]))
        
        #######################################################################
        # Get corresponding files
        #######################################################################
        # Get park and golf course shapefiles
        matching_park = [s for s in parks_list if state_name + '_parks.shp' in s]
        matching_golf = [s for s in golf_list if state_name + '_golf_courses.shp' in s]
        
        # Get urban block groups shapefile
        matching_bg = [s for s in bg_list if fips + '_bg_urban.shp' in s]
        
        # Get block group population table
        matching_pop = [s for s in pop_list if '_' + fips in s]
        
        #######################################################################
        # Read all files
        #######################################################################
        park_gdf = gpd.read_file(matching_park[0])
        golf_gdf = gpd.read_file(matching_golf[0])
        bg_gdf = gpd.read_file(matching_bg[0])
        pop_df = pd.read_csv(matching_pop[0])
        
        # Dissolve and explode to remove overlapping polygons
        park_dissolve = park_gdf.dissolve()
        park_dissolve = park_dissolve.explode()
    
# =============================================================================
#         golf_dissolve = golf_gdf.dissolve()
#         golf_dissolve = golf_dissolve.explode()
# =============================================================================
        golf_dissolve = golf_gdf
        
        #######################################################################
        # Convert everything to UTM coordinates
        #######################################################################
        
        # Get UTM zone EPSG code of state
        lon_poly, lat_poly = park_dissolve[(park_dissolve['geometry'].geom_type == 'Polygon')]['geometry'].iloc[0].exterior.coords.xy
        utm_zone = convert_wgs_to_utm(lon_poly[0], lat_poly[0])
        epsg = 'EPSG:' + utm_zone
        
        # Convert
        bg_gdf = bg_gdf.to_crs(epsg)
        park_dissolve = park_dissolve.to_crs(epsg)
        golf_dissolve = golf_dissolve.to_crs(epsg)
        
        # Compute area
        park_dissolve['area'] = park_dissolve['geometry'].area
        golf_dissolve['area'] = golf_dissolve['geometry'].area
        
        # Remove anything smaller than a football pitch
        park_dissolve = park_dissolve[park_dissolve['area'] > 7000]
        golf_dissolve = golf_dissolve[golf_dissolve['area'] > 7000]
        
        park_dissolve.reset_index(inplace=True)
        golf_dissolve.reset_index(inplace=True)
        
        # Compute centroids
        bg_gdf['centroid'] = bg_gdf['geometry'].centroid
        park_dissolve['centroid'] = park_dissolve['geometry'].centroid
        golf_dissolve['centroid'] = golf_dissolve['geometry'].centroid
        
        # Construct kd tree
        park_point_tree = spatial.cKDTree(np.vstack((park_dissolve['centroid'].x.values, 
                                        park_dissolve['centroid'].y.values)).T)
        golf_point_tree = spatial.cKDTree(np.vstack((golf_dissolve['centroid'].x.values, 
                                        golf_dissolve['centroid'].y.values)).T)
        
        # Calculate distance to parks and golf courses
        distance_park = []
        distance_golf = []
        name_golf = []
        
        for i in range(bg_gdf.shape[0]):
            #print('%s... %.0f out of % .0f' %(state_name, i+1, bg_gdf.shape[0]))
            
            # Find nearest park to block group centroid
            dist1, idx1 = park_point_tree.query((bg_gdf['centroid'].x.iloc[i],
                                               bg_gdf['centroid'].y.iloc[i]),
                                               k=4)
            
            # Compute distance from block group centroid to park edge
            distances = []
            for idx in range(len(idx1)):
                p1, p2 = nearest_points(park_dissolve.iloc[idx1[idx]]['geometry'], bg_gdf['centroid'].iloc[i])
                distances.append(p1.distance(p2))
                
            # Append to list
            distance_park.append(np.array(distances).min())
            
            # Find nearest golf course to block group centroid
            dist2, idx2 = golf_point_tree.query((bg_gdf['centroid'].x.iloc[i],
                                               bg_gdf['centroid'].y.iloc[i]),
                                               k=1)
            
            # Compute distance from block group centroid to park edge
            p3, p4 = nearest_points(golf_dissolve.iloc[idx2]['geometry'], bg_gdf['centroid'].iloc[i])
            
            # Append to list
            distance_golf.append(p3.distance(p4))
            name_golf.append(golf_dissolve.iloc[idx2]['name'])
        
        """ note that it is possible that some parks and golf courses overlap.
        Right now they would both be counted. """
                
        bg_gdf['park_dist'] = distance_park
        bg_gdf['golf_dist'] = distance_golf
        bg_gdf['golf_name'] = name_golf
        
        # Drop some columns so can export
        bg_gdf.drop(columns=['centroid'], inplace=True)
        
        # Export to shapefile
        bg_gdf.to_file(path + 'state_stats/data_' + fips + '_' + state_name + '.shp')

    

















    
    
