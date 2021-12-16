#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""

Match golf course addresses from Golfnationwide.com to OSM golf courses. 

"""

# Import modules
import numpy as np
import pandas as pd
import geopandas as gpd
import os
from geopy.geocoders import GoogleV3
import scipy.spatial as spatial
import math
from pyproj import Transformer
from shapely.ops import nearest_points
from shapely.geometry import Point
#from geopy.extra.rate_limiter import RateLimiter

def convert_wgs_to_utm(lon, lat):
    utm_band = str((math.floor((lon + 180) / 6 ) % 60) + 1)
    if len(utm_band) == 1:
        utm_band = '0'+utm_band
    if lat >= 0:
        epsg_code = '326' + utm_band
    else:
        epsg_code = '327' + utm_band
    return epsg_code

# Define filepath to data
filepath = '/Users/jryan4/Dropbox (University of Oregon)/Parks_and_Golf/'

# Define API key
key_path = '/Users/jryan4/Dropbox (University of Oregon)/Parks_and_Golf/google-api-key.txt'
with open(key_path) as f:
    key = f.readlines()

# Define GeoCoder
geolocator = GoogleV3(api_key=key[0])

# Import states data
states = gpd.read_file(filepath + 'data/states/tl_2020_us_state.shp')

for j in range(states.shape[0]):

    # Get FIPS code
    fips = states['STATEFP'].iloc[j]
    state_name1 = states['NAME'].iloc[j].replace(' ', '_')
    state_name2 = states['NAME'].iloc[j].replace(' ', '-')
        
    if os.path.exists(filepath + 'data/golf_with_stats/' + state_name1 + '_golf_courses.shp'):
        print('Skipping... %s' %state_name1)
    else:
        print('Processing... %s' %state_name1)
    
        # Read golf course datasets
        osm_golf_courses = gpd.read_file(filepath + 'data/golf_with_name/' + state_name1 + '_golf_courses.shp')
        database_golf_courses = pd.read_csv(filepath + 'data/golfnationwide/' + state_name2 + '_' + fips + '.csv')
        
        # Get UTM zone EPSG code of state
        lon_poly, lat_poly = osm_golf_courses[(osm_golf_courses['geometry'].geom_type == 'Polygon')]['geometry'].iloc[0].exterior.coords.xy
        utm_zone = convert_wgs_to_utm(lon_poly[0], lat_poly[0])
        epsg = 'EPSG:' + utm_zone
        
        # Convert golf course shapefile to UTM
        osm_golf_courses_utm = osm_golf_courses.to_crs(epsg)
        
        idx_list = []
        geometry_list = []
        name_list = []
        address_lon = []
        address_lat = []
        distance_golf = []
        
        for i in range(database_golf_courses.shape[0]):
            print('Processing %.0f out of %.0f' %(i+1, database_golf_courses.shape[0]))
            # Get first address
            inputAddress = database_golf_courses.iloc[i]['name'] + ', ' +\
                           database_golf_courses.iloc[i]['town'] + ', ' +\
                           database_golf_courses.iloc[i]['state']
            
            # Find the address location
            try:
                location = geolocator.geocode(inputAddress, timeout=10)
            
                # Get lat/lon of address
                lon, lat = location.longitude, location.latitude
                
                transformer = Transformer.from_crs(4326, int(utm_zone), always_xy=True)
                x, y = transformer.transform(lon, lat)
                
                # Construct kd tree
                osm_golf_courses_utm['centroid'] = osm_golf_courses_utm['geometry'].centroid
                golf_point_tree = spatial.cKDTree(np.vstack((osm_golf_courses_utm['centroid'].x.values, 
                                                osm_golf_courses_utm['centroid'].y.values)).T)
                        
                # Find nearest park to block group centroid
                dist, idx = golf_point_tree.query((x, y), k=3)
                
                # Compute distance from block group centroid to park edge
                distances = []
                for k in range(len(idx)):
                    p1, p2 = nearest_points(osm_golf_courses_utm.iloc[idx[k]]['geometry'], Point(x, y))
                    distances.append(p1.distance(p2))
                
                # Get index of nearest golf course
                nearest_golf_idx = idx[np.array(distances).argmin()]
                
                if np.array(distances).min() < 2000:
                
                    # Append to list
                    distance_golf.append(np.array(distances).min())
                    address_lon.append(lon)
                    address_lat.append(lat)
                    idx_list.append(nearest_golf_idx)
                    geometry_list.append(osm_golf_courses['geometry'].iloc[nearest_golf_idx])
                    name_list.append(osm_golf_courses['name'].iloc[nearest_golf_idx])
                
                else:
                    distance_golf.append('N/A')
                    address_lon.append(lon)
                    address_lat.append(lat)
                    idx_list.append('N/A')
                    geometry_list.append('N/A')
                    name_list.append('N/A')
            
            except AttributeError:
                print("No coordinates found for this address...")
                distance_golf.append('N/A')
                address_lon.append(lon)
                address_lat.append(lat)
                idx_list.append('N/A')
                geometry_list.append('N/A')
                name_list.append('N/A')
        
        # Put back into DataFrame
        database_golf_courses['geometry'] = geometry_list
        database_golf_courses['osm_name'] = name_list
        database_golf_courses['osm_index'] = idx_list
        database_golf_courses['distance'] = distance_golf
        database_golf_courses.index = database_golf_courses['osm_index']
        
        # Combine with OSM golf course database
        df = osm_golf_courses.join(database_golf_courses, how='inner', rsuffix='_1')
        
        # Drop duplicates based on minimum distance
        df = df.sort_values('distance', ascending=True).drop_duplicates('name').sort_index()
        
        # Drop some more columns
        del df['name']
        del df['geometry_1']
        del df['distance']
        del df['osm_index']
        df.rename(columns={'name_1': 'database_name'}, inplace=True)
        
        # Convert back to GeoPandas DataFrame
        gdf = gpd.GeoDataFrame(df, geometry='geometry')
        
        # Save to shapefile
        gdf.to_file(filepath + 'data/golf_with_stats/' + state_name1 + '_golf_courses.shp')











