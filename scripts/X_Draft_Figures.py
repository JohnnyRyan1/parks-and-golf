#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Draft figures

"""


###############################################################################
# Figure 2: Area of urban greenspace statistics for 216 largest cities in US
###############################################################################

slope1, intercept1, r_value1, p_value1, std_err1 = stats.linregress(city_pop_area['Population'], city_pop_area['park_area'])
slope3, intercept3, r_value3, p_value3, std_err3 = stats.linregress(city_pop_area['park_per_capita'], city_pop_area['golf_per_capita'])
slope4, intercept4, r_value4, p_value4, std_err4 = stats.linregress(urban_large['park_fraction'], urban_large['golf_fraction'])

x1 = np.arange(0,17900000, 10000)
x3 = np.arange(0,150, 10)
x4 = np.arange(0,0.11, 0.05)

fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(nrows=2, ncols=2, figsize=(8, 6))

ax1.scatter(city_pop_area['Population'], city_pop_area['park_area'], zorder=2)
ax1.plot(x1, (x1*slope1) + intercept1, color='k', lw=1, zorder=3)
ax1.grid(ls='dashed', lw=1, zorder=1)
ax1.set_xlabel('Population')
ax1.set_ylabel('Park area (km$^2$)')
ax1.set_xlim(0,17900000)
ax1.set_ylim(0,510000000)

ax1.annotate('Greater Boston, MA', 
            (city_pop_area['Population'].iloc[22],
             city_pop_area['park_area'].iloc[22]))
ax1.annotate('Chicago, IL', 
            (city_pop_area['Population'].iloc[34],
             city_pop_area['park_area'].iloc[34]))
# =============================================================================
# ax1.annotate('New York-Newark', 
#             (city_pop_area['Population'].iloc[131],
#              city_pop_area['park_area'].iloc[131]))
# =============================================================================
ax1.annotate('Greater LA, CA', 
            (city_pop_area['Population'].iloc[108],
             city_pop_area['park_area'].iloc[108]))
ax1.annotate('Minneapolis-St. Paul, MN', 
            (city_pop_area['Population'].iloc[119],
             city_pop_area['park_area'].iloc[119]))
ax1.annotate('Washington, DC', 
            (city_pop_area['Population'].iloc[207],
             city_pop_area['park_area'].iloc[207]))
ax1.annotate('Miami, FL', 
            (city_pop_area['Population'].iloc[116],
             city_pop_area['park_area'].iloc[116]))

ax2.scatter(city_pop_area['Population'], city_pop_area['golf_area'], zorder=2)
ax2.plot(x1, (x1*slope2) + intercept2, color='k', lw=1, zorder=3)
ax2.grid(ls='dashed', lw=1, zorder=1)
ax2.set_xlabel('Population')
ax2.set_ylabel('Golf area (km$^2$)')
ax2.set_xlim(0,17900000)
ax2.set_ylim(0,154000000)

ax2.annotate('Miami, FL', 
            (city_pop_area['Population'].iloc[116],
             city_pop_area['golf_area'].iloc[116]))
ax2.annotate('Chicago, IL', 
            (city_pop_area['Population'].iloc[34],
             city_pop_area['golf_area'].iloc[34]))
# =============================================================================
# ax2.annotate('New York-Newark', 
#             (city_pop_area['Population'].iloc[131],
#              city_pop_area['golf_area'].iloc[131]))
# =============================================================================
ax2.annotate('Greater LA, CA', 
            (city_pop_area['Population'].iloc[108],
             city_pop_area['golf_area'].iloc[108]))
ax2.annotate('Atlanta, GA', 
            (city_pop_area['Population'].iloc[10],
             city_pop_area['golf_area'].iloc[10]))
ax2.annotate('Phoenix, AZ', 
            (city_pop_area['Population'].iloc[145],
             city_pop_area['golf_area'].iloc[145]))

ax3.scatter(city_pop_area['park_per_capita'], city_pop_area['golf_per_capita'], zorder=2)
#ax3.plot(x3, (x3*slope3) + intercept3, color='k', lw=1, zorder=2)
ax3.grid(ls='dashed', lw=1, zorder=1)
ax3.set_xlabel('Park area per capita (km$^2$)')
ax3.set_ylabel('Golf area per capita (km$^2$)')
ax3.set_xlim(0,140)
ax3.set_ylim(0,212)

ax3.annotate('Bonita Springs, FL', 
            (city_pop_area['park_per_capita'].iloc[21],
             city_pop_area['golf_per_capita'].iloc[21]))
ax3.annotate('Myrtle Beach, SC', 
            (city_pop_area['park_per_capita'].iloc[125],
             city_pop_area['golf_per_capita'].iloc[125]))
ax3.annotate('Indio--Cathedral City, CA', 
            (city_pop_area['park_per_capita'].iloc[87],
             city_pop_area['golf_per_capita'].iloc[87]))
ax3.annotate('Port St. Lucie, FL', 
            (city_pop_area['park_per_capita'].iloc[148],
             city_pop_area['golf_per_capita'].iloc[148]))

ax4.scatter(urban_large['park_fraction'], urban_large['golf_fraction'], zorder=2)
#ax4.plot(x4, (x4*slope4) + intercept4, color='k', lw=1, zorder=2)
ax4.grid(ls='dashed', lw=1, zorder=1)
ax4.set_xlabel('Park fraction (%)')
ax4.set_ylabel('Golf course fraction (%)')
ax4.set_xlim(0,0.106)
ax4.set_ylim(0,0.11)

ax4.annotate('Bonita Springs, FL', 
            (city_pop_area['park_fraction'].iloc[21],
             city_pop_area['golf_fraction'].iloc[21]))
ax4.annotate('Miami, FL', 
            (city_pop_area['park_fraction'].iloc[116],
             city_pop_area['golf_fraction'].iloc[116]))
ax4.annotate('Indio--Cathedral City, CA', 
            (city_pop_area['park_fraction'].iloc[87],
             city_pop_area['golf_fraction'].iloc[87]))
ax4.annotate('Port St. Lucie, FL', 
            (city_pop_area['park_fraction'].iloc[148],
             city_pop_area['golf_fraction'].iloc[148]))

fig.tight_layout()
plt.savefig(savepath + 'park_golf_scatterplots.svg', dpi=200)


###############################################################################
# Number of people closer/further than 1 km from green space and that would benefit 
# from conversion of golf course
###############################################################################
green_close_1km = df_large[(df_large['golf_dist'] <= 1000) | (df_large['park_dist'] <= 1000)]
green_not_close_1km = df_large[(df_large['golf_dist'] > 1000) & (df_large['park_dist'] > 1000)]

park_close_1km = df_large[df_large['park_dist'] <= 1000]

park_but_not_golf_1km = df_large[(df_large['golf_dist'] <= 1000) & (df_large['park_dist'] > 1000)] 
golf_but_not_park_1km = df_large[(df_large['golf_dist'] <= 1000) & (df_large['park_dist'] > 1000)]


###############################################################################
# Which cities have best/worst as a percentage of population park access?
###############################################################################
cities_park_close = df_large[df_large['park_dist'] <= 1000].groupby(by=['NAME10'])['Population'].sum()
cities_park_far = df_large[df_large['park_dist'] > 1000].groupby(by=['NAME10'])['Population'].sum()
cities_park_fraction = cities_park_close / (cities_park_far + cities_park_close)

x_pos = [i for i, _ in enumerate(cities_park_fraction[::5])]

fig, ax = plt.subplots(figsize=(15, 4))
ax.grid(ls='dashed', lw=1, zorder=1)
ax.bar(x_pos, cities_park_fraction.sort_values()[::5], zorder=2)
ax.set_ylabel('Population < 1 km from park (%)')
ax.set_xticks(x_pos)
ax.set_xticklabels(cities_park_fraction.sort_values().index.values[::5], 
                   rotation=90)

###############################################################################
# Greenspace and golf course access by state
###############################################################################
states = gpd.read_file(path + 'states/cb_2018_us_state_20m.shp')
states['state'] = states['STATEFP'].astype(int)
urban_pop_by_state = df.groupby(by='state')['Population'].sum().reset_index()

park_close_1km = df[df['park_dist'] <= 1000]
park_not_close_1km = df[df['park_dist'] > 1000]
golf_but_not_park_1km = df[(df['golf_dist'] <= 1000) & (df['park_dist'] > 1000)]

parks_close_by_state = park_close_1km.groupby(by='state')['Population'].sum().reset_index()
parks_far_by_state = park_not_close_1km.groupby(by='state')['Population'].sum().reset_index()
golf_close_by_state = golf_but_not_park_1km.groupby(by='state')['Population'].sum().reset_index()
urban_pop_by_state['parks_close'] = parks_close_by_state['Population'] / urban_pop_by_state['Population'] 
urban_pop_by_state['parks_far'] = parks_far_by_state['Population'] / urban_pop_by_state['Population'] 
urban_pop_by_state['golf_close'] = golf_close_by_state['Population'] / urban_pop_by_state['Population'] 
states_stats = pd.merge(left=states, right=urban_pop_by_state, how='inner', on='state')

""" change edgecolor to white """
ax1 = states_stats.plot(column='parks_close', scheme='equal_interval', k=6, \
             cmap='magma', legend=True, edgecolor='black', lw=0.5,
             legend_kwds={'loc': 'center left', 'bbox_to_anchor':(1,0.5),  'fmt':"{:.2f}"})
plt.savefig(savepath + 'parks_close_1km.svg', dpi=200)

ax2 = states_stats.plot(column='parks_far', scheme='equal_interval', k=6, \
             cmap='magma_r', legend=True, edgecolor='grey', lw=0.5,
             legend_kwds={'loc': 'center left', 'bbox_to_anchor':(1,0.5),  'fmt':"{:.2f}"})
plt.savefig(savepath + 'parks_far_1km.svg', dpi=200)
    
ax3 = states_stats.plot(column='golf_close', scheme='equal_interval', k=6, \
         cmap='magma_r', legend=True, edgecolor='black', lw=0.5,
         legend_kwds={'loc': 'center left', 'bbox_to_anchor':(1,0.5),  'fmt':"{:.3f}"})
plt.savefig(savepath + 'golf_close_1km.svg', dpi=200)
    
###############################################################################
# Which cities (people + proportion) would benefit most from golf course conversions?
###############################################################################
cities_park_far = green_not_close_1km.groupby(by=['NAME10'])['Population'].sum()
cities_park_far = cities_park_far.reset_index()
cities_df = df_large.groupby(by=['NAME10'])['Population'].sum().reset_index()
cities_park_fraction = pd.merge(left=cities_park_far, 
                                 right=cities_df, how='inner', on='NAME10')
cities_park_fraction['benefit'] = cities_park_fraction['Population_x'] / cities_park_fraction['Population_y']


cities_golf_close = golf_but_not_park_1km.groupby(by=['NAME10'])['Population'].sum()
cities_golf_close = cities_golf_close.reset_index()
cities_df = df_large.groupby(by=['NAME10'])['Population'].sum().reset_index()
cities_golf_fraction = pd.merge(left=cities_golf_close, 
                                 right=cities_df, how='inner', on='NAME10')
cities_golf_fraction['benefit'] = cities_golf_fraction['Population_x'] / cities_golf_fraction['Population_y']

fig, (ax2, ax1) = plt.subplots(nrows=1, ncols=2, figsize=(8, 3))
ax1.grid(ls='dashed', lw=1, zorder=1)
ax1.scatter(cities_golf_fraction['Population_x'], cities_golf_fraction['benefit'], 
           zorder=2)
#ax.set_xticklabels(['{:,}'.format(int(x)) for x in ax.get_xticks().tolist()])
ax1.set_xlabel('Number of people')
ax1.set_ylabel('Fraction of city (%)')
ax1.set_xlim(0, 600000)
ax1.set_ylim(0, 0.38)

ax1.annotate('Myrtle Beach, SC', 
            (cities_golf_fraction['Population_x'].iloc[116],
             cities_golf_fraction['benefit'].iloc[116]))
ax1.annotate('Indio-Cathedral City, CA', 
            (cities_golf_fraction['Population_x'].iloc[80],
             cities_golf_fraction['benefit'].iloc[80]))
ax1.annotate('Bonita Springs, FL', 
            (cities_golf_fraction['Population_x'].iloc[18],
             cities_golf_fraction['benefit'].iloc[18]))
ax1.annotate('Spring Hill, FL', 
            (cities_golf_fraction['Population_x'].iloc[170],
             cities_golf_fraction['benefit'].iloc[170]))
ax1.annotate('Cape Coral, FL', 
            (cities_golf_fraction['Population_x'].iloc[25],
             cities_golf_fraction['benefit'].iloc[25]))
ax1.annotate('Miami, FL', 
            (cities_golf_fraction['Population_x'].iloc[107],
             cities_golf_fraction['benefit'].iloc[107]))
ax1.annotate('New York-Newark, NY', 
            (cities_golf_fraction['Population_x'].iloc[121],
             cities_golf_fraction['benefit'].iloc[121]))
ax1.annotate('Atlanta, GA', 
            (cities_golf_fraction['Population_x'].iloc[8],
             cities_golf_fraction['benefit'].iloc[8]))
ax1.annotate('Greater LA, CA', 
            (cities_golf_fraction['Population_x'].iloc[100],
             cities_golf_fraction['benefit'].iloc[100]))
ax1.annotate('Phoenix, AZ', 
            (cities_golf_fraction['Population_x'].iloc[134],
             cities_golf_fraction['benefit'].iloc[134]))

ax2.grid(ls='dashed', lw=1, zorder=1)
ax2.scatter(cities_park_fraction['Population_x'], cities_park_fraction['benefit'], 
           zorder=2)

""" Chane to scientific notation"""
ax2.set_xlabel('Number of people')
ax2.set_ylabel('Fraction of city (%)')
#ax2.set_xlim(0, 600000)
#ax2.set_ylim(0, 0.38)

ax2.annotate('Jackson, MS', 
            (cities_park_fraction['Population_x'].iloc[88],
             cities_park_fraction['benefit'].iloc[88]))
ax2.annotate('Columbus, GA-AL', 
            (cities_park_fraction['Population_x'].iloc[41],
             cities_park_fraction['benefit'].iloc[41]))
ax2.annotate('Winter Haven, FL', 
            (cities_park_fraction['Population_x'].iloc[211],
             cities_park_fraction['benefit'].iloc[211]))
ax2.annotate('Fredericksburg, VA', 
            (cities_park_fraction['Population_x'].iloc[68],
             cities_park_fraction['benefit'].iloc[68]))
ax2.annotate('Port Arthur, TX', 
            (cities_park_fraction['Population_x'].iloc[146],
             cities_park_fraction['benefit'].iloc[146]))
ax2.annotate('Miami, FL', 
            (cities_park_fraction['Population_x'].iloc[116],
             cities_park_fraction['benefit'].iloc[116]))
ax2.annotate('New York-Newark, NY', 
            (cities_park_fraction['Population_x'].iloc[130],
             cities_park_fraction['benefit'].iloc[130]))
ax2.annotate('Atlanta, GA', 
            (cities_park_fraction['Population_x'].iloc[10],
             cities_park_fraction['benefit'].iloc[10]))
ax2.annotate('Greater LA, CA', 
            (cities_park_fraction['Population_x'].iloc[108],
             cities_park_fraction['benefit'].iloc[108]))
ax2.annotate('Houston, TX', 
            (cities_park_fraction['Population_x'].iloc[83],
             cities_park_fraction['benefit'].iloc[83]))
fig.tight_layout()
plt.savefig(savepath + 'city_benefit_golf_course_conversion.svg', dpi=200)

###############################################################################
# Who are these people that live far from parks AND golf courses?
###############################################################################
not_close_1km = df_large[(df_large['park_dist'] > 1000) & (df_large['golf_dist'] > 1000)]
income_avg_block = df_large['Income'].mean()
white_avg_block = df_large['White'].mean()
not_close_1km['IncomeDiff'] = not_close_1km['Income'] - income_avg_block
not_close_1km['RacialDiff'] = not_close_1km['White'] - white_avg_block
not_close_1km = not_close_1km[not_close_1km['IncomeDiff'].notnull()]
not_close_1km.reset_index(inplace=True)

# Plot block groups that are not close to greenspace by income and ethnicity
fig, ax = plt.subplots()
ax.hist2d(not_close_1km['RacialDiff'], not_close_1km['IncomeDiff'], bins=50,
          cmap='Purples')
ax.axhline(y=0, ls='dashed', lw=1, zorder=2, color='k')
ax.axvline(x=0, ls='dashed', lw=1, zorder=2, color='k')
ax.set_yticklabels(['{:,}'.format(int(x)) for x in ax.get_yticks().tolist()])
ax.set_xlabel('Ethnicity relative to US average')
ax.set_ylabel('Income relative to US average ($)')
fig.tight_layout()
plt.savefig(savepath + 'neighborhoods_far_from_parks.png', dpi=200)

# Upper right quadrant means that people who would benefit from golf course conversion
# are richer/whiter than the average in the city
# Lower right quadrant means that people who would benefit from golf course conversion
# are poorer/whiter than the average in the city
# Upper left quadrant means that people who would benefit from golf course conversion
# are richer/minority than the average in the city
# Lower right quadrant means that people who would benefit from golf course conversion
# are poorer/minority than the average in the city

golf_close_1km = df_large[(df_large['park_dist'] > 1000) & (df_large['golf_dist'] <= 1000)]
income_avg_block = df_large['Income'].mean()
white_avg_block = df_large['White'].mean()
golf_close_1km['IncomeDiff'] = golf_close_1km['Income'] - income_avg_block
golf_close_1km['RacialDiff'] = golf_close_1km['White'] - white_avg_block
golf_close_1km = golf_close_1km[golf_close_1km['IncomeDiff'].notnull()]
golf_close_1km.reset_index(inplace=True)

# Plot block groups that are close to golf course but not park by income and ethnicity
fig, ax = plt.subplots()
ax.hist2d(golf_close_1km['RacialDiff'], golf_close_1km['IncomeDiff'], bins=50,
          cmap='Purples')
ax.axhline(y=0, ls='dashed', lw=1, zorder=2, color='k')
ax.axvline(x=0, ls='dashed', lw=1, zorder=2, color='k')
ax.set_yticklabels(['{:,}'.format(int(x)) for x in ax.get_yticks().tolist()])
ax.set_xlabel('Ethnicity relative to US average')
ax.set_ylabel('Income relative to US average ($)')
fig.tight_layout()
plt.savefig(savepath + 'neighborhoods_close_to_golf.png', dpi=200)


""" Add another figure showing age vs. population density of block groups,
this should demonstrate whether it is surburban neighborhoods or not. """













