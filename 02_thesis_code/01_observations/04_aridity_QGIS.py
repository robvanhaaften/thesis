"""
Created on Fri Oct 15

Calculates the average adjusted aridity index for each hexagon 

@author: Rob van Haaften
"""

for i in [*range(3,8,1)]:
    #grid cells with observations 
    inp = str("C:/Users/Rob/Desktop/GIS_thesis/01_thesis_data/02_temp/01_observations/03_dhs_grid/dhs_grid_" + str(i) + ".shp")
    #visible lights
    out = str("C:/Users/Rob/Dropbox/My PC (DESKTOP-DP7OCOF)/Desktop/GIS_thesis/01_thesis_data/02_temp/04_aridity/02_observations/aridity_" + str(i) + ".csv")
    pref = None 
    processing.run("native:zonalstatisticsfb", \
    {'INPUT':inp,\
    'INPUT_RASTER':'C:/Users/Rob/Desktop/GIS_thesis/01_thesis_data/02_temp/04_aridity/01_input/aridity_index_adj.tif', \
    'RASTER_BAND':1,\
    'COLUMN_PREFIX': None,'STATISTICS':[2],\
    'OUTPUT': out})
    
    
