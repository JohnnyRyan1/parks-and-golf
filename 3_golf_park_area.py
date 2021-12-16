#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""

Compute number and area of greenspaces and golf courses for each urban area.

"""

# Import modules
import geopandas as gpd
import pandas as pd
import numpy as np
import glob 
import math
from shapely.geometry import Point

# Define path
path = '/home/johnny/Documents/Teaching/490_Geospatial_Data_Science_Applications/Applications/OSM_Parks_and_Golf/data/'

# Import states
states = gpd.read_file(path + 'states/tl_2020_us_state.shp')

# Define parks and golf courses
park_list = sorted(glob.glob(path + 'parks_and_golf/*_parks.shp'))
golf_list = sorted(glob.glob(path + 'parks_and_golf/*_golf_courses.shp'))
golf_stat_list = sorted(glob.glob(path + 'golf_with_stats/*_golf_courses.shp'))

# Define urban areas
urban = gpd.read_file(path + 'urban_areas/tl_2020_us_uac10.shp')
urban = urban.to_crs('EPSG:4326')

def convert_wgs_to_utm(lon, lat):
    utm_band = str((math.floor((lon + 180) / 6 ) % 60) + 1)
    if len(utm_band) == 1:
        utm_band = '0'+utm_band
    if lat >= 0:
        epsg_code = '326' + utm_band
    else:
        epsg_code = '327' + utm_band
    return epsg_code

def state_to_country_append(file_list):
    
    df_list = []
    for infile in file_list:
        
        # Read file
        data = gpd.read_file(infile)
        
        # Store DataFrame in list
        df_list.append(data)
        
    return pd.concat(df_list)

park_df = state_to_country_append(park_list)
golf_df = state_to_country_append(golf_list)
golf_stats_df = state_to_country_append(golf_stat_list)

# Dissolve and explode to remove overlapping polygons    
park_dissolve = park_df.dissolve()
park_dissolve = park_dissolve.explode()
# =============================================================================
# golf_dissolve = golf_df.dissolve()
# golf_dissolve = golf_dissolve.explode()
# golf_stats_dissolve = golf_stats_df.dissolve()
# golf_stats_dissolve = golf_stats_dissolve.explode()
# =============================================================================

# Intersect
urban_park = gpd.sjoin(park_dissolve, urban, how='inner', op='within')
urban_golf = gpd.sjoin(golf_df, urban, how='inner', op='within')
urban_golf_stats = gpd.sjoin(golf_stats_df, urban, how='inner', op='within')

# Loop through every city and get greenspace and golf area and number
cities = np.unique(urban_park['NAME10'].values)

city_name = []
state_id = []
region_id = []
city_area = []
park_area = []
golf_area = []
park_num = []
golf_num = []
golf_private_area = []
golf_public_area = []
golf_private_num = []
golf_public_num = []
lat = []
lon = []

for i in range(len(cities)):
    print('Processing... %.0f out of %.0f' %(i+1, len(cities)))

    # Get lat/lon of city
    city_lat = float(urban_park[urban_park['NAME10'] == cities[i]].iloc[0]['INTPTLAT10'])
    city_lon = float(urban_park[urban_park['NAME10'] == cities[i]].iloc[0]['INTPTLON10'])
    
    # Get state and region
    p1 = Point(city_lon, city_lat)
    
    region = []
    state = []
    for j in range(states.shape[0]):
        if p1.within(states.loc[j, 'geometry']) == True:
            region.append(int(states.loc[j]['REGION']))
            state.append(int(states.loc[j]['STATEFP']))
        else:
            pass
    
    # Get parks
    park = urban_park[urban_park['NAME10'] == cities[i]]
    golf = urban_golf[urban_golf['NAME10'] == cities[i]]
    golf_stats = urban_golf_stats[urban_golf_stats['NAME10'] == cities[i]]
    
    # Get UTM zone EPSG code of city
    lon_poly, lat_poly = park[(park['geometry'].geom_type == 'Polygon')]['geometry'].iloc[0].exterior.coords.xy
    utm_zone = convert_wgs_to_utm(lon_poly[0], lat_poly[0])
    epsg = 'EPSG:' + utm_zone
    
    # Convert coordinates
    park = park.to_crs(epsg)
    golf = golf.to_crs(epsg)
    golf_stats = golf_stats.to_crs(epsg)
    
    # Add area columns
    park['area'] = park.area
    golf['area'] = golf.area
    golf_stats['area'] = golf_stats.area
    
    # Remove any park smaller than a football pitch
    park = park[park['area'] > 7000]
    
    # Number and area of private golf courses
    private_golf_no = np.sum((golf_stats['ownership'] == 'Private') | \
                             (golf_stats['ownership'] == 'Resort') | \
                             (golf_stats['ownership'] == 'Military'))
    private_golf_area = np.sum(golf_stats['area'][(golf_stats['ownership'] == 'Private') | \
                             (golf_stats['ownership'] == 'Resort') | \
                             (golf_stats['ownership'] == 'Military')])
    
    # Number and area of public golf courses
    public_golf_no = np.sum((golf_stats['ownership'] == 'Public') | \
                         (golf_stats['ownership'] == 'Semi-Private'))
    public_golf_area = np.sum(golf_stats['area'][(golf_stats['ownership'] == 'Public') | \
                         (golf_stats['ownership'] == 'Semi-Private')])
        
    # Check
    if int(public_golf_area + private_golf_area) == int(np.sum(golf_stats['area'])):
        pass
    else:
        print('Hold up now...')
        
    if park.shape[0] > 0:
        
        # Append to list
        city_name.append(cities[i])
        state_id.append(state[0])
        region_id.append(region[0])
        city_area.append(park['ALAND10'].iloc[0])
        park_area.append(park.area.sum())
        golf_area.append(golf.area.sum())
        park_num.append((park.shape[0]))
        golf_num.append((golf.shape[0]))
        golf_private_area.append(private_golf_area)
        golf_public_area.append(public_golf_area)
        golf_private_num.append(private_golf_no)
        golf_public_num.append(public_golf_no)
        lat.append(city_lat)
        lon.append(city_lon)
    else:
        pass

# Put back into DataFrame
df = pd.DataFrame(list(zip(city_name, lon, lat, state_id, region_id, city_area, 
                           park_area, golf_area,
                           park_num, golf_num, golf_private_area, 
                           golf_public_area, golf_private_num, golf_public_num)))
df.columns = ['city_name', 'city_lon', 'city_lat', 'state', 'region', 'city_area', 
              'park_area', 'golf_area', 'park_num', 'golf_num', 
              'private_golf_area', 'public_golf_area', 'private_golf_num',
              'public_golf_num']

# Compute some new columns
df['park_fraction'] = df['park_area'] / df['city_area']
df['golf_fraction'] = df['golf_area'] / df['city_area']
df['private_golf_fraction'] = df['private_golf_area'] / df['city_area']
df['public_golf_fraction'] = df['public_golf_area'] / df['city_area']

# Save to csv
df.to_csv(path + 'golf_course_states_usa.csv', index=False)















        
