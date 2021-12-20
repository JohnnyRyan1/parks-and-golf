# Assessing the impacts of urban golf courses on access to greenspace in the United States

This repository all the code and data required to reproduce the data analysis and figures for this paper. Additional data can be found here: https://zenodo.org/record/5787031. The boundaries of US urban areas can be downloaded from: https://www.census.gov/cgi-bin/geo/shapefiles/index.php. Map data from OpenStreetMap is available from: https://www.openstreetmap.org. In this study we downloaded OSM data using `osmnx` which is available to install at: https://github.com/gboeing/osmnx. Golf course ownership status can be downloaded from GolfNationwide: http://www.golfnationwide.com/. Census Bureau data at the block group level can be downloaded from U.S. Census Bureau’s API: https://www.census.gov/data/developers.html. In this study we downloaded Census Bureau data using `censusdata` which is available at: https://github.com/jtleider/censusdata.

### Figures

![flow chart](./figures/flow_chart.png)
**Fig. 1** Schematic of data analysis framework for investigating the extent to which urban golf courses hinder accessibility to greenspace in the US.
<br/><br/>

![golf stats](./figures/golf_stats_map.png)
**Fig. 2** Map showing area of urban greenspace per capita for the fifty largest cities in the US by population. The size of the circles represents the greenspace area per capita for all types of greenspace (including golf courses). The green wedges represent the area of publicly accessible greenspace while the yellow wedges represent the area of golf course per capita.
<br/><br/>

![golf ownership](./figures/golf_ownership_map.png)
**Fig. 3** Map showing area of urban golf courses per capita for the fifty largest cities in the US by population. The size of the circles represents the golf course area per capita for all types of golf courses. The blue wedges represent the area of **public** golf courses per capita while the red wedges represent the area of **private** golf course per capita.
<br/><br/>

![golf access](./figures/golf_access_equity_map.png)
**Fig. 4** Map showing number of people who live within 1 km of a golf course, but further than 1 km from other types of greenspace for the fifty largest cities in the US by population. The size of the circles represents the number of people. The colored wedges represent different ethno-racial groups.
<br/><br/>

<img src="./figures/who_lives_near_golf_courses.png" width="400">

**Fig. 5** Characteristics of people who live within 1 km of a golf course, but further than 1 km from other types of greenspace for the fifty largest cities in the US by population. The size of the circles represents the number of people. Overall, people who live near golf courses but far from other types of greenspace tend to be wealthier and whiter than the city average. 
<br/><br/>
