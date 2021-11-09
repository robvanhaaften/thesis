"""
Created on Fri Oct 15

Disaggragates the road network data by road type and merges the results into CSV files 

The script is devided into 4 functions that do the following: 

1. Splits the road shapefile by the different raod types using the "splitvectorlayer" function

2. Calculates the total road length for the different road types and hexagon sizes 

3. Merges these statistics with dhs data into one csv file 


@author: Rob van Haaften
"""

from pathlib import Path
from pathlib import PureWindowsPath
import pandas as pd



# 2. Calculates the total road length for the different road types 
def create_zonal_statistics():
    
    # generate a list of all the road type file paths created in road_split_uganda()
    shp_folder_road = Path(r'C:\Users\Rob\Dropbox\My PC (DESKTOP-DP7OCOF)\Desktop\GIS_thesis\01_thesis_data\02_temp\03_road\roads_split\uganda_total').rglob('*.shp')
    files_road = [x for x in shp_folder_road]
    
    grid = "C:/Users/Rob/Dropbox/My PC (DESKTOP-DP7OCOF)/Desktop/GIS_thesis/01_thesis_data/02_temp/01_observations/04_dhs_mis_grid/dhs_grid_mis.shp"
    for road_type in files_road:
        file = PureWindowsPath(road_type).name.split('.')[0]
        processing.run("native:sumlinelengths", \
        {'POLYGONS':grid,\
        'LINES':str(road_type),\
        'LEN_FIELD':str(str(file) + 'length'),\
        'COUNT_FIELD':str(str(file) + 'count'),\
        'OUTPUT':str(r'C:\Users\Rob\Dropbox\My PC (DESKTOP-DP7OCOF)\Desktop\GIS_thesis\01_thesis_data\02_temp\03_road\roads_split\zonal_stats\dhs_mis\%s.csv' %(file))})


#merge files for each grid size 
#####REPLACE THE ENDLESS DIRECTORIES WITH THIS SHIT!!!!###
base_dir = r'C:\Users\Rob\Dropbox\My PC (DESKTOP-DP7OCOF)\Desktop\GIS_thesis\01_thesis_data\02_temp\03_road\roads_split\zonal_stats'

def merge_zonal_stats(): 

    # generates a list of csv files for each folder (the 30 roadtypes)
    #zonal_stats_csv = Path(str(r'C:\Users\Rob\Dropbox\My PC (DESKTOP-DP7OCOF)\Desktop\GIS_thesis\01_thesis_data\02_temp\03_road\roads_split\zonal_stats\\' + str(folder))).rglob('*.csv')
    zonal_stats_csv = Path(r'C:\Users\Rob\Dropbox\My PC (DESKTOP-DP7OCOF)\Desktop\GIS_thesis\01_thesis_data\02_temp\03_road\roads_split\zonal_stats\dhs_mis\\').rglob('*.csv')
    csv_list = [str(x) for x in zonal_stats_csv]
    #makes a merged csv file of allt the road types 
    processing.run("native:mergevectorlayers", 
    {'LAYERS':csv_list,\
    'CRS':None, \
    'OUTPUT':str(r'C:\Users\Rob\Dropbox\My PC (DESKTOP-DP7OCOF)\Desktop\GIS_thesis\01_thesis_data\02_temp\03_road\roads_split\zonal_stats\mis_merged.csv')})




# un-comment to run the funcitons note that the second function takes a while to run


#2 create zonal statistics for each road type
#create_zonal_statistics()

#3 merge all the excel sheets per grid size 
#merge_zonal_stats()







