General introduction 
-folders 
-files and suffixes 
-annotation explained 
-data sourcing 
	ntl:		Google Earth Engine API
	road network: 	humantiarian data exchange (URL: ...)
	aridity index:	Calculated from CGIAR and sentinel 2 data (URL1: ..., URL2:...)


01_observations
This folder contains all the scripts used to generate, clean and merge the observations. When the filename ends with QGIS it has to be run in the QGIS python console. When the filename ends with python it can be run in python. 

In the following a short description is given for each script. For more details see the comments in the scripts.

01_create_gridcells_QGIS
Makes the hexagonal grids which are used to extract the observations

02_ntl_QGIS
Generates the ntl observations using the Google Earth Engine 

03_road_aggragated_QGIS
Calculates the sum of all the road lengths within each hexagon

04_aridity_QGIS
Calculates the average adjusted aridity index for each hexagon 

05_dhs_clean_python
Cleans dhs data 

06_merge_analysis1_python
Merges dhs, ntl, roads and aridity data by cluster id for analysis part 1 

07_road_disaggragated_QGIS

Disaggragates the road network data by road type and merges the results into CSV files 

	02_analysis


01_analysis_1

02_analysis_2

03_analysis_3
