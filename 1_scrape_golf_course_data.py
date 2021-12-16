#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""

Match OSM golf courses to GolfNationwide.com database.

USA golf course directory:
    http://www.golfnationwide.com/US-Golf-Course-List-And-Directory.aspx

"""

# Import modules
import numpy as np
import pandas as pd
import geopandas as gpd
import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

# Define filepath to data
filepath = '/home/johnny/Documents/Teaching/490_Geospatial_Data_Science_Applications/Applications/OSM_Parks_and_Golf/'

# Define savepath
savepath = '/home/johnny/Documents/Teaching/490_Geospatial_Data_Science_Applications/Applications/OSM_Parks_and_Golf/data/golfnationwide/'

# Set options for headless Chrome
chrome_driver = filepath + '/chromedriver'
chrome_options = Options()
chrome_options.add_argument('--headless')

# Speed things up by not loading images
prefs = {"profile.managed_default_content_settings.images": 2}
chrome_options.add_experimental_option("prefs", prefs)

# Import states data
states = gpd.read_file(filepath + 'data/states/tl_2020_us_state.shp')

# Define base url
base_url = 'http://www.golfnationwide.com/Golf-Courses-By-State/'

for j in range(states.shape[0]):
    print('Processing %.0f out of %.0f' %(j+1, states.shape[0]))

    
    # State string
    state_str = states.iloc[j]['NAME'].replace(' ','-')
        
    if os.path.exists(savepath + state_str + '_' + states.iloc[j]['STATEFP'].zfill(2) + '.csv'):
        pass
    else:
        # Concatenate strings
        url = base_url + state_str + '-Golf-Courses__' + states.iloc[j]['STUSPS'] + '.aspx'
        
        # Define location of WebDriver
        driver = webdriver.Chrome(options=chrome_options, executable_path=chrome_driver)
        driver.get(url)
        
        # Get table
        table = driver.find_elements_by_xpath('//*[@id="ctl00_MainContentPlaceholder_GridView1"]')
        rows = table[0].find_elements_by_tag_name('tr')
        
        # Get a list of golf course names
        course_list = []
        for row in np.arange(2, len(rows)+1, 1):
            path = driver.find_elements_by_xpath('//*[@id="ctl00_MainContentPlaceholder_GridView1"]/tbody/tr[' + str(row) + ']/td[1]')[0]
            course_list.append(path.text)
         
        street = []
        town = []
        state = []
        zipcode = []
        annual_rounds = []
        classification = []
        year_built = []
        green_fees_weekend = []
        
        # Click on each golf course
        for row in np.arange(2, len(rows)+1, 1):
            print('Processing %.0f out of %.0f' %(row, len(rows)+1))
    
            # Go back to original page
            driver.get(url)
            
            # Find golf course to click on
            course = driver.find_element_by_xpath('//*[@id="ctl00_MainContentPlaceholder_GridView1"]/tbody/tr[' + str(row) + ']/td[1]/a')
            course.click()
    
            # Identify parameters
            street.append(driver.find_element_by_xpath('//*[@id="ctl00_MainContentPlaceholder_AddressLabel"]').text)
            town.append(driver.find_element_by_xpath('//*[@id="ctl00_MainContentPlaceholder_CityLabel"]').text)
            state.append(states.iloc[j]['STUSPS'])
            zipcode.append(driver.find_element_by_xpath('//*[@id="ctl00_MainContentPlaceholder_ZipLabel"]').text)
            annual_rounds.append(driver.find_element_by_xpath('//*[@id="ctl00_MainContentPlaceholder_AnnualRoundsLabel"]').text)
            classification.append(driver.find_element_by_xpath('//*[@id="ctl00_MainContentPlaceholder_ClassificationLabel"]').text)
            year_built.append(driver.find_element_by_xpath('//*[@id="ctl00_MainContentPlaceholder_YearBuiltLabel"]').text)
            green_fees_weekend.append(driver.find_element_by_xpath('//*[@id="ctl00_MainContentPlaceholder_GreensFeesWeekendLabel"]').text)
        
        # Put into DataFrame
        df = pd.DataFrame(list(zip(course_list, street, town, state, zipcode,
                               annual_rounds, classification, year_built, green_fees_weekend)))
    
        df.columns = ['name', 'street', 'town', 'state', 'zipcode', 'annual_rounds',
                      'ownership', 'year_built', 'green_fees']
        
        # Save to csv
        df.to_csv(savepath + state_str + '_' + states.iloc[j]['STATEFP'].zfill(2) + '.csv')
























