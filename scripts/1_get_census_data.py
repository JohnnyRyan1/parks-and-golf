#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""

Download census data.

Cloned from: 
    https://github.com/jtleider/censusdata

Note that I was having no luck getting it to download at the block group level.

The solution:
    (1) it was a variable name problem, needed "B01001_001E" instead.
    (2) also had to change tabletype to "detail", don't know why this makes a difference.

Variables for block groups here:
    https://api.census.gov/data/2019/acs/acs5/variables.html
    
Excellent guide can be found here:
    https://api.census.gov/data.html

"""

# Import modules
import censusdata

# Define path to save
path = '/home/johnny/Documents/Teaching/490_Geospatial_Data_Science_Applications/Applications/OSM_Parks_and_Golf/data/'

# Print list of census data attributes
#censusdata.printtable(censusdata.censustable('acs5', 2015, 'DP05'))

# Get list of state IDs
state_dict = censusdata.geographies(censusdata.censusgeo([('state', '*')]), 'acs5', 2019)

# Define list of variables
variables = ['B01001_001E', # Total population 
             'B03002_001E', # Also total population
             'B03002_002E', # Not Hispanic or Latino
             'B03002_003E', # White
             'B03002_004E', # Black or African American
             'B03002_005E', # American Indian or Alaska Native
             'B03002_006E', # Asian
             'B03002_007E', # Native Hawaiian or Pacific Islander
             'B03002_008E', # Some other race
             'B03002_009E', # Two or more races
             'B03002_010E', # Two or more races including some other race
             'B03002_011E', # Two races excluding some other race, and three or more races
             'B03002_012E', # Hispanic or Latino
             'B03003_001E', # Also total population
             'B03003_002E', # Not Hispanic or Latino
             'B03003_003E', # Hispanic or Latino
             'B19013_001E', # Median household income in the past 12 months
             'B25077_001E', # Median house value
             'B01001_003E', # Male: under 5 years
             'B01001_004E', 'B01001_005E', 'B01001_006E',
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
             'B01001_047E', 'B01001_048E', 'B01001_049E']

# =============================================================================
# # Download population by tract
# for key1, value1 in state_dict.items():
#     state_id = str(value1)[-2:]
# 
#     # Download population by tract
#     pop_tract = censusdata.download('acs5', 2019, 
#                                            censusdata.censusgeo([('state', state_id), 
#                                                                  ('county', '*'),
#                                                                  ('tract', '*')]),
#                                            ['DP05_0001E'], 
#                                            key = 'cf7bfd71f6e64ddabdc65b3c7e00ebe11de9eea2',
#                                            tabletype='profile')
# 
#     censusdata.exportcsv(path + 'pop_by_tract/' + key1 + '_' + state_id + '.csv', pop_tract)
# =============================================================================
    
# Download population data by block group
for key1, value1 in state_dict.items():
    state_id = str(value1)[-2:]
    print('Processing... %s' % key1)
           
    # Download population by block group
    pop_block_group = censusdata.download('acs5', 2019, 
                                       censusdata.censusgeo([('state', state_id), 
                                                             ('county', '*'),
                                                             ('tract', '*'),
                                                             ('block group', '*')]),
                                       variables, 
                                       key = 'cf7bfd71f6e64ddabdc65b3c7e00ebe11de9eea2',
                                       tabletype='detail')
    
    key1.replace(' ', '_')

    censusdata.exportcsv(path + 'pop_by_block_group/' + key1.replace(' ', '_') + '_' + state_id + '.csv', pop_block_group)








