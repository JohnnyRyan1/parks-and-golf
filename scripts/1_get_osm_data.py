#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""

Get parks and golf courses for each state from OSM.

"""

# Import modules
import osmnx as ox
import geopandas as gpd
import os

# Define filepath
path = '/home/johnny/Documents/Teaching/490_Geospatial_Data_Science_Applications/Applications/OSM_Parks_and_Golf/data/'

# Import state boundary data
states = gpd.read_file(path + 'states/tl_2020_us_state.shp')

# Define tags
park_tags = {'leisure':['park', 'nature_reserve', 'dog_park', 'playground'], 
        'landuse':['recreation_ground'], 'boundary':['protected_area']}

""" might be other categories e.g. greenways? grassland? """

golf_tags = {'leisure':'golf_course'}

for i in states['NAME'].values:
    
    # Define state name for osmnx
    place_name = i + ', USA' 
    if os.path.exists(path + 'parks_and_golf/' + i.replace(' ', '_') + '_golf_courses.shp'):
        print('Skipping... %s' %(i))
    
    else:
        print('Downloading... %s' %(i))
         # Get areas labelled as parks or green spaces        
        parks = ox.geometries_from_place(place_name, park_tags)
        
        # Get areas labeled as golf course
        golf_courses = ox.geometries_from_place(place_name, golf_tags)
              
        # Get just polygons
        golf_courses = golf_courses[(golf_courses['geometry'].geom_type == 'Polygon') | (golf_courses['geometry'].geom_type == 'MultiPolygon')]
        parks = parks[(parks['geometry'].geom_type == 'Polygon') | (parks['geometry'].geom_type == 'MultiPolygon')]
        
        # Export to file
        golf_gdf = gpd.GeoDataFrame(geometry=list(golf_courses['geometry']), crs=4326)
        golf_gdf.to_file(path + 'parks_and_golf/' + i.replace(' ', '_') + '_golf_courses.shp')
        
        park_gdf = gpd.GeoDataFrame(geometry=list(parks['geometry']), crs=4326)
        park_gdf.to_file(path + 'parks_and_golf/' + i.replace(' ', '_') + '_parks.shp')


###############################################################################
# Download Washington State separately
###############################################################################
i = 'Washington'

# Define state name for osmnx
place_name = i + ', USA' 

# Get areas labeled as parks and green spaces
parks = ox.geometries_from_place(place_name, park_tags, which_result=2)

# Get areas labeled as golf course
tags = {'leisure':'golf_course'}
golf_courses = ox.geometries_from_place(place_name, golf_tags, which_result=2)

# Get just polygons
golf_courses = golf_courses[(golf_courses['geometry'].geom_type == 'Polygon') | (golf_courses['geometry'].geom_type == 'MultiPolygon')]
parks = parks[(parks['geometry'].geom_type == 'Polygon') | (parks['geometry'].geom_type == 'MultiPolygon')]

# Export to file
golf_gdf = gpd.GeoDataFrame(geometry=list(golf_courses['geometry']), crs=4326)
golf_gdf.to_file(path + 'parks_and_golf/' + i.replace(' ', '_') + '_golf_courses.shp')

park_gdf = gpd.GeoDataFrame(geometry=list(parks['geometry']), crs=4326)
park_gdf.to_file(path + 'parks_and_golf/' + i.replace(' ', '_') + '_parks.shp')

###############################################################################
# Download New York State separately
###############################################################################
i = 'New York'

# Define state name for osmnx
place_name = i + ', USA' 

# Get areas labeled as parks and green spaces
parks = ox.geometries_from_place(place_name, park_tags, which_result=2)

# Get areas labeled as golf course
tags = {'leisure':'golf_course'}
golf_courses = ox.geometries_from_place(place_name, golf_tags, which_result=2)

# Get just polygons
golf_courses = golf_courses[(golf_courses['geometry'].geom_type == 'Polygon') | (golf_courses['geometry'].geom_type == 'MultiPolygon')]
parks = parks[(parks['geometry'].geom_type == 'Polygon') | (parks['geometry'].geom_type == 'MultiPolygon')]

# Export to file
golf_gdf = gpd.GeoDataFrame(geometry=list(golf_courses['geometry']), crs=4326)
golf_gdf.to_file(path + 'parks_and_golf/' + i.replace(' ', '_') + '_golf_courses.shp')

park_gdf = gpd.GeoDataFrame(geometry=list(parks['geometry']), crs=4326)
park_gdf.to_file(path + 'parks_and_golf/' + i.replace(' ', '_') + '_parks.shp')









