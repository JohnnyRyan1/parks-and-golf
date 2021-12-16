#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""

Data analysis for golf courses.

"""

# Import modules
import geopandas as gpd
import pandas as pd
import numpy as np
import glob
import matplotlib.pyplot as plt
from scipy import stats

# Define path to data 
path = '/Users/jryan4/Dropbox (University of Oregon)/Parks_and_Golf/data/'

# Define save path
savepath = '/Users/jryan4/Dropbox (University of Oregon)/Parks_and_Golf/figures/'

# Define save data path
datapath = '/Users/jryan4/Dropbox (University of Oregon)/Parks_and_Golf/repo/'

###############################################################################
# Number of golf courses in GolfNationwide.com directory
###############################################################################
database_list = glob.glob(path + 'golfnationwide/*.csv')

df_list = []
for infile in database_list:
    
    # Read file
    data = pd.read_csv(infile)
    
    # Store DataFrame in list
    df_list.append(data)
    
database_df = pd.concat(df_list)

print('Number of golf courses in GolfNationwide.com = %.0f' %database_df.shape[0])

###############################################################################
# Urban golf course statistics
###############################################################################
urban_golf = pd.read_csv(path + 'golf_course_states_usa.csv')
urban_golf['greenspace_area'] = urban_golf['park_area'] + urban_golf['golf_area']

print('Number of urban golf courses in OSM = %.0f' %np.sum(urban_golf['golf_num']))
print('Number of matched urban golf courses = %.0f'\
      %((np.sum(urban_golf['private_golf_num']) + np.sum(urban_golf['public_golf_num']))))
print('Area of urban golf courses in OSM = %.0f' %np.sum(urban_golf['golf_area']))

print('Area of urban greenspace that is golf course = %.3f' %(
    np.sum(urban_golf['golf_area']) / np.sum(urban_golf['greenspace_area'])))


###############################################################################
# Area of golf courses relative to greenspace for US urban areas by region
###############################################################################
region_stats = urban_golf.groupby(by=['region'])[['greenspace_area', 'golf_area']].sum()
region_stats['golf_fraction'] = region_stats['golf_area'] / region_stats['greenspace_area']

###############################################################################
# Area of golf courses for US urban areas by for fifty largest cities
###############################################################################

# Define file list
file_list = sorted(glob.glob(path + 'state_stats_with_census/*.shp'))
df_list = []
for infile in file_list:
    
    data = gpd.read_file(infile)
    
    # store DataFrame in list
    df_list.append(data)
    
df = pd.concat(df_list)
df[df == -666666666] = np.nan

# Add region column
df['region'] = 0

# Northeast
df.loc[df['STATEFP'] == '09', 'region'] = 1
df.loc[df['STATEFP'] == '23', 'region'] = 1
df.loc[df['STATEFP'] == '25', 'region'] = 1
df.loc[df['STATEFP'] == '33', 'region'] = 1
df.loc[df['STATEFP'] == '44', 'region'] = 1
df.loc[df['STATEFP'] == '50', 'region'] = 1
df.loc[df['STATEFP'] == '34', 'region'] = 1
df.loc[df['STATEFP'] == '36', 'region'] = 1
df.loc[df['STATEFP'] == '42', 'region'] = 1

# Midwest
df.loc[df['STATEFP'] == '17', 'region'] = 2
df.loc[df['STATEFP'] == '18', 'region'] = 2
df.loc[df['STATEFP'] == '26', 'region'] = 2
df.loc[df['STATEFP'] == '39', 'region'] = 2
df.loc[df['STATEFP'] == '55', 'region'] = 2
df.loc[df['STATEFP'] == '19', 'region'] = 2
df.loc[df['STATEFP'] == '20', 'region'] = 2
df.loc[df['STATEFP'] == '27', 'region'] = 2
df.loc[df['STATEFP'] == '29', 'region'] = 2
df.loc[df['STATEFP'] == '31', 'region'] = 2
df.loc[df['STATEFP'] == '38', 'region'] = 2
df.loc[df['STATEFP'] == '46', 'region'] = 2

# South
df.loc[df['STATEFP'] == '10', 'region'] = 3
df.loc[df['STATEFP'] == '11', 'region'] = 3
df.loc[df['STATEFP'] == '12', 'region'] = 3
df.loc[df['STATEFP'] == '13', 'region'] = 3
df.loc[df['STATEFP'] == '24', 'region'] = 3
df.loc[df['STATEFP'] == '37', 'region'] = 3
df.loc[df['STATEFP'] == '45', 'region'] = 3
df.loc[df['STATEFP'] == '51', 'region'] = 3
df.loc[df['STATEFP'] == '54', 'region'] = 3
df.loc[df['STATEFP'] == '01', 'region'] = 3
df.loc[df['STATEFP'] == '21', 'region'] = 3
df.loc[df['STATEFP'] == '28', 'region'] = 3
df.loc[df['STATEFP'] == '47', 'region'] = 3
df.loc[df['STATEFP'] == '05', 'region'] = 3
df.loc[df['STATEFP'] == '22', 'region'] = 3
df.loc[df['STATEFP'] == '40', 'region'] = 3
df.loc[df['STATEFP'] == '48', 'region'] = 3

# West
df.loc[df['STATEFP'] == '04', 'region'] = 4
df.loc[df['STATEFP'] == '08', 'region'] = 4
df.loc[df['STATEFP'] == '16', 'region'] = 4
df.loc[df['STATEFP'] == '30', 'region'] = 4
df.loc[df['STATEFP'] == '32', 'region'] = 4
df.loc[df['STATEFP'] == '35', 'region'] = 4
df.loc[df['STATEFP'] == '49', 'region'] = 4
df.loc[df['STATEFP'] == '56', 'region'] = 4
df.loc[df['STATEFP'] == '06', 'region'] = 4
df.loc[df['STATEFP'] == '15', 'region'] = 4
df.loc[df['STATEFP'] == '41', 'region'] = 4
df.loc[df['STATEFP'] == '53', 'region'] = 4

city_pop = df.groupby(by=['NAME10'])['Population'].sum()

# Get 50 largest cities in US
big_fifty = city_pop.sort_values().tail(50).index.values

# Filter DataFrame
df_big = df[df['NAME10'].isin(big_fifty)]
df_big.reset_index(inplace=True)

# Do some filtering
df_big[df_big == -666666666] = np.nan

# Filter DataFrame
urban_large = urban_golf[urban_golf['city_name'].isin(big_fifty)]
urban_large.reset_index(inplace=True)

# Merge greenspace area and city population data
urban_large['NAME10']= urban_large['city_name']
city_pop_area = pd.merge(left=urban_large, right=city_pop, how='inner', on='NAME10')
city_pop_area['golf_per_capita'] = city_pop_area['golf_area'] / city_pop_area['Population']
city_pop_area['green_per_capita'] = city_pop_area['greenspace_area'] / city_pop_area['Population']

city_pop_area['golf_vs_greenspace'] = city_pop_area['golf_area'] / city_pop_area['greenspace_area']

print(city_pop_area.sort_values(by=['golf_fraction'])[['NAME10','golf_fraction']].tail(10))
print(city_pop_area.sort_values(by=['golf_fraction'])[['NAME10','golf_fraction']].head(10))

print(city_pop_area.sort_values(by=['golf_vs_greenspace'])[['NAME10','golf_vs_greenspace']].tail(10))
print(city_pop_area.sort_values(by=['golf_vs_greenspace'])[['NAME10','golf_vs_greenspace']].head(10))

print(city_pop_area.sort_values(by=['golf_per_capita'])[['NAME10','golf_per_capita']].tail(10))
print(city_pop_area.sort_values(by=['golf_per_capita'])[['NAME10','golf_per_capita']].head(10))

# Save to csv
city_pop_area = city_pop_area.drop(labels='NAME10', axis=1)
city_pop_area = city_pop_area.drop(labels='index', axis=1)
city_pop_area.to_csv(datapath + 'data/city_stats.csv')
df.to_csv(datapath + 'data/block_group_stats.csv')

###############################################################################
# Area of golf courses for US urban areas by for cities > 100,000 people
###############################################################################

# =============================================================================
# # Get cities with populations larger than 100K
# large_cities = city_pop[city_pop > 100000].index.values
# 
# # Filter DataFrame
# df_large = df[df['NAME10'].isin(large_cities)]
# df_large.reset_index(inplace=True)
# 
# # Do some filtering
# df_large[df_large == -666666666] = np.nan
# 
# # Filter DataFrame
# urban_large = urban_golf[urban_golf['city_name'].isin(large_cities)]
# urban_large.reset_index(inplace=True)
# 
# # Merge greenspace area and city population data
# urban_large['NAME10']= urban_large['city_name']
# city_pop_area = pd.merge(left=urban_large, right=city_pop, how='inner', on='NAME10')
# city_pop_area['golf_per_capita'] = city_pop_area['golf_area'] / city_pop_area['Population']
# city_pop_area['green_per_capita'] = city_pop_area['greenspace_area'] / city_pop_area['Population']
# 
# city_pop_area['golf_vs_greenspace'] = city_pop_area['golf_area'] / city_pop_area['greenspace_area']
# 
# 
# print(city_pop_area.sort_values(by=['golf_fraction'])[['NAME10','golf_fraction']].tail(10))
# print(city_pop_area.sort_values(by=['golf_fraction'])[['NAME10','golf_fraction']].head(10))
# 
# print(city_pop_area.sort_values(by=['golf_vs_greenspace'])[['NAME10','golf_vs_greenspace']].tail(10))
# print(city_pop_area.sort_values(by=['golf_vs_greenspace'])[['NAME10','golf_vs_greenspace']].head(10))
# 
# print(city_pop_area.sort_values(by=['golf_per_capita'])[['NAME10','golf_per_capita']].tail(10))
# print(city_pop_area.sort_values(by=['golf_per_capita'])[['NAME10','golf_per_capita']].head(10))
# =============================================================================


###############################################################################
# Bubble map showing golf course statistics
###############################################################################

""" Some examples:
    https://stackoverflow.com/questions/54541081/how-to-plot-a-donut-chart-around-a-point-on-a-scatterplot
    https://stackoverflow.com/questions/51409257/exploding-wedges-of-pie-chart-when-plotting-them-on-a-map-python-matplotlib
    https://stackoverflow.com/questions/56337732/how-to-plot-scatter-pie-chart-using-matplotlib
    
"""
# Import USA shapefile
usa = gpd.read_file(path + 'states/cb_2018_us_state_5m_conterminous.shp')
gdf = gpd.GeoDataFrame(city_pop_area, geometry=gpd.points_from_xy(city_pop_area['city_lon'], city_pop_area['city_lat']))
#gdf = gpd.GeoDataFrame(urban_golf, geometry=gpd.points_from_xy(urban_golf['city_lon'], urban_golf['city_lat']))

# Convert to USA projection
usa = usa.to_crs('EPSG:2163')
gdf.crs = 'EPSG:4326'
gdf = gdf.to_crs('EPSG:2163')

#function to draw pie charts on map    
def drawPieMarker(xs, ys, ratios, sizes, colors):
    assert sum(ratios) <= 1, 'sum of ratios needs to be < 1'

    markers = []
    previous = 0
    # calculate the points of the pie pieces
    for color, ratio in zip(colors, ratios):
        this = 2 * np.pi * ratio + previous
        x  = [0] + np.cos(np.linspace(previous, this, 20)).tolist() + [0]
        y  = [0] + np.sin(np.linspace(previous, this, 20)).tolist() + [0]
        xy = np.column_stack([x, y])
        previous = this
        markers.append({'marker':xy, 's':np.abs(xy).max()**2*np.array(sizes), 'facecolor':color})

    # scatter each of the pie pieces to create pies
    for marker in markers:
        ax.scatter(xs, ys, **marker, edgecolor='k', alpha=0.7, linewidth=0.7)


# Plot figure
fig, ax = plt.subplots(figsize=(16,16))
usa.plot(ax=ax, color='lightgray', edgecolor='grey', linewidth=0.6)
for i in range(gdf.shape[0]):
    drawPieMarker(xs=gdf['geometry'].x[i],
                  ys=gdf['geometry'].y[i],
                  ratios=[gdf['golf_vs_greenspace'][i], 1 - gdf['golf_vs_greenspace'][i]],
                  sizes=[gdf['green_per_capita'][i]*30],
                  colors=['#f7fcb9', '#31a354'])
ax.axis('off')
plt.savefig(savepath + 'golf_stats_map.svg')

###############################################################################
# Number of people closer/further than 1 km from greenspace by region
###############################################################################
park_close_1km = df[(df['park_dist'] <= 1000)]
golf_close_park_far = df[(df['golf_dist'] <= 1000) & (df['park_dist'] > 1000)]
golf_far_park_far = df[(df['golf_dist'] > 1000) & (df['park_dist'] > 1000)]

print(park_close_1km['Population'].sum() / df['Population'].sum())
print(golf_close_park_far['Population'].sum() / df['Population'].sum())


park_close_1km = park_close_1km.groupby(by=['region'])[['Population']].sum()
golf_close_park_far = golf_close_park_far.groupby(by=['region'])[['Population']].sum()

print(golf_close_park_far / (park_close_1km + golf_close_park_far))

###############################################################################
# Number of people closer/further than 1 km from golf course by city
###############################################################################

# Get people who live in big cities
big_cities = df[df['NAME10'].isin(big_fifty)]

golf_close_park_far = big_cities[(big_cities['golf_dist'] <= 1000) & (big_cities['park_dist'] > 1000)]
golf_close_park_far_city = golf_close_park_far.groupby(by=['NAME10'])['Population'].sum()
golf_close_park_far_city = golf_close_park_far_city.reset_index()
golf_close_park_far_city['fraction'] = golf_close_park_far_city['Population'] / city_pop_area['Population']

###############################################################################
# Who lives far from greenspace? Nationally
###############################################################################
big_cities['White_Fraction'] = big_cities['White'] / big_cities['Population']
big_cities['Asian_Fraction'] = big_cities['Asian'] / big_cities['Population']
big_cities['Black_Fraction'] = big_cities['Black'] / big_cities['Population']
big_cities['Hispanic_Fraction'] = big_cities['Hispanic'] / big_cities['Population']

# Get neighborhoods
golf_close_green_far = big_cities[(big_cities['golf_dist'] <= 1000) & (big_cities['park_dist'] > 1000)]

# Remove NaNs
golf_close_green_far = golf_close_green_far[golf_close_green_far['White'].notnull()]
golf_close_green_far = golf_close_green_far[golf_close_green_far['HousePrice'].notnull()]
golf_close_green_far = golf_close_green_far[golf_close_green_far['Income'].notnull()]

stats.ttest_ind(golf_close_green_far['White_Fraction'].values, big_cities['White_Fraction'].values)
stats.ttest_ind(golf_close_green_far['Black_Fraction'].values, big_cities['Black_Fraction'].values)
stats.ttest_ind(golf_close_green_far['Hispanic_Fraction'].values, big_cities['Hispanic_Fraction'].values)
stats.ttest_ind(golf_close_green_far['Asian_Fraction'].values, big_cities['Asian_Fraction'].values)

stats.ttest_ind(golf_close_green_far['HousePrice'].values, big_cities['HousePrice'].values)
stats.ttest_ind(golf_close_green_far['Income'].values, big_cities['Income'].values)

print(golf_close_green_far['White_Fraction'].mean())
print(big_cities['White_Fraction'].mean())

print(golf_close_green_far['Black_Fraction'].mean())
print(big_cities['Black_Fraction'].mean())

print(golf_close_green_far['Hispanic_Fraction'].mean())
print(big_cities['Hispanic_Fraction'].mean())

print(golf_close_green_far['Asian_Fraction'].mean())
print(big_cities['Asian_Fraction'].mean())

print(golf_close_green_far['HousePrice'].mean())
print(big_cities['HousePrice'].mean())

print(golf_close_green_far['Income'].mean())
print(big_cities['Income'].mean())

###############################################################################
# Who lives far from greenspace? Regionally
###############################################################################
region_golf_close = golf_close_green_far.groupby(by='region')['White', 'Black', 
                                                                      'Hispanic', 'Asian', 
                                                                      'Population'].sum()
region_all = big_cities.groupby(by='region')['White', 'Black', 'Hispanic', 'Asian', 
                                                                      'Population'].sum()

# Probability of a single resident having poor greenspace access by region
print((region_golf_close['Population'] / region_all['Population']))

# Probability of a Black resident with poor greenspace access by region
print((region_golf_close['Black'] / region_all['Black']) /\
      (region_golf_close['Population'] / region_all['Population']))

# Probability of a Hispanic resident with poor greenspace access by region
print((region_golf_close['Hispanic'] / region_all['Hispanic']) /\
      (region_golf_close['Population'] / region_all['Population']))

# Probability of a Asian resident with poor greenspace access by region
print((region_golf_close['Asian'] / region_all['Asian']) /\
      (region_golf_close['Population'] / region_all['Population']))
    
# Probability of a White resident with poor greenspace access by region
print((region_golf_close['White'] / region_all['White']) /\
      (region_golf_close['Population'] / region_all['Population']))

###############################################################################
# Who lives far from greenspace? By city
###############################################################################
city_golf_close = golf_close_green_far.groupby(by='NAME10')['White', 'Black', 
                                                            'Hispanic', 'Asian', 
                                                            'Population','NumChildre'].sum()

city_all = big_cities.groupby(by='NAME10')['White', 'Black', 'Hispanic', 'Asian', 
                                           'Population', 'NumChildre'].sum()
   
# Average income of people in city
all_income = big_cities.groupby(by='NAME10')['Income'].mean()

# Average income of people who would benefit most from golf course access
city_golf_close_income = golf_close_green_far.groupby(by='NAME10')['Income'].mean()

# Relative income
relative_income = (city_golf_close_income / all_income) - 1

# Average white fraction in city
city_all['White_Fraction'] = city_all['White'] / city_all['Population']
city_golf_close['White_Fraction'] = city_golf_close['White'] / city_golf_close['Population']
relative_white = (city_golf_close['White_Fraction'] / city_all['White_Fraction'])

# Plot
fig, ax1 = plt.subplots(nrows=1, ncols=1, figsize=(5, 5))
ax1.grid(ls='dashed', lw=1, zorder=1)
ax1.scatter(relative_income, relative_white,
            zorder=3, edgecolor='k', s=list(city_golf_close['Population']/500), alpha=0.7)

ax1.set_ylabel('Proportion of White residents relative \n to city average', fontsize=12)
ax1.set_xlabel('Income relative to city average', fontsize=12)
ax1.tick_params(axis='x', labelsize=12)
ax1.tick_params(axis='y', labelsize=12)
ax1.axhline(y=1, ls='dashed', lw=1, zorder=2, color='k')
ax1.axvline(x=0, ls='dashed', lw=1, zorder=2, color='k')

ax1.annotate('Los Angeles, CA', (relative_income.iloc[20], relative_white.iloc[20]))
ax1.annotate('Miami, FL', (relative_income.iloc[23], relative_white.iloc[23]))
ax1.annotate('Riverside, CA', (relative_income.iloc[37], relative_white.iloc[37]))

plt.savefig(savepath + 'who_lives_near_golf_courses.svg')

###############################################################################
# Map showing where most people who only have access to golf courses
###############################################################################
city_golf_close['White_Fraction'] = city_golf_close['White'] / city_golf_close['Population']
city_golf_close['Black_Fraction'] = city_golf_close['Black'] / city_golf_close['Population']
city_golf_close['Hispanic_Fraction'] = city_golf_close['Hispanic'] / city_golf_close['Population']
city_golf_close['Asian_Fraction'] = city_golf_close['Asian'] / city_golf_close['Population']
city_golf_close['Other_Fraction'] = 1 - (city_golf_close['White_Fraction'] + city_golf_close['Black_Fraction'] +\
                                         city_golf_close['Hispanic_Fraction'] + \
                                         city_golf_close['Asian_Fraction'])

# Plot figure
fig, ax = plt.subplots(figsize=(16,16))
usa.plot(ax=ax, color='lightgray', edgecolor='grey', linewidth=0.6)
for i in range(gdf.shape[0]):
    drawPieMarker(xs=gdf['geometry'].x[i],
                  ys=gdf['geometry'].y[i],
                  ratios=[city_golf_close['White_Fraction'][i], 
                          city_golf_close['Black_Fraction'][i],
                          city_golf_close['Hispanic_Fraction'][i], 
                          city_golf_close['Asian_Fraction'][i],
                          city_golf_close['Other_Fraction'][i]],
                  sizes=[city_golf_close['Population'][i]/50],
                  colors=['#ffa600', '#ff6361', '#bc5090', '#58508d', '#003f5c'])
ax.axis('off')
plt.savefig(savepath + 'golf_access_equity_map.svg')

###############################################################################
# Private vs. Public golf course stats
###############################################################################
gdf['private_fraction'] = gdf['private_golf_num'] / (gdf['private_golf_num'] + gdf['public_golf_num'])
print(gdf['private_fraction'].mean())
region_ownership = gdf.groupby(by='region')['private_fraction'].mean()
print(gdf[['NAME10', 'private_fraction', 'private_golf_num']].sort_values(by='private_fraction'))

###############################################################################
# Private vs. Public golf course map
###############################################################################
gdf['private_golf'] = gdf['private_golf_num'] / (gdf['public_golf_num'] + gdf['private_golf_num'])
gdf['public_golf'] = gdf['public_golf_num'] / (gdf['public_golf_num'] + gdf['private_golf_num'])

# Plot figure
fig, ax = plt.subplots(figsize=(16,16))
usa.plot(ax=ax, color='lightgray', edgecolor='grey', linewidth=0.6)
for i in range(gdf.shape[0]):
    drawPieMarker(xs=gdf['geometry'].x[i],
                  ys=gdf['geometry'].y[i],
                  ratios=[gdf['private_golf'][i], gdf['public_golf'][i]],
                  sizes=[gdf['golf_per_capita'][i]*100],
                  colors=['#fc8d59', '#91bfdb'])
ax.axis('off')
plt.savefig(savepath + 'golf_ownership_map.svg')

print(gdf['public_golf'].mean())
print(gdf['private_golf'].mean())














