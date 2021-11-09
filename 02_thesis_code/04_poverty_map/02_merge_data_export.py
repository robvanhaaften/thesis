# -*- coding: utf-8 -*-
"""
Created on Thu Sep 23 12:27:29 2021

making the final map 
- get data for all of Uganda for the 3 kilometer grid and merge on grid id 
- get estiamte and coeficients from final model
- calculate the estimates for complete grid
- export output 



@author: Rob
"""
import pandas as pd
from pathlib import Path
from pathlib import PureWindowsPath

# merge data for compelte uganda extract for NTL, roads and AR
# import data
# ntl 
ntl = pd.read_csv(r"C:\Users\Rob\Dropbox\My PC (DESKTOP-DP7OCOF)\Desktop\GIS_thesis\01_thesis_data\02_temp\02_NTL\NTL_VIIRS_uganda_3.csv")
ntl = ntl[["id", "mean"]]

# aridity 
aridity = pd.read_csv(r"C:\Users\Rob\Dropbox\My PC (DESKTOP-DP7OCOF)\Desktop\GIS_thesis\01_thesis_data\02_temp\04_aridity\02_observations\aridity_index_uganda_3.csv")
aridity = aridity[["id", "_mean"]]

# road types
# setting up a dataframe for road types wiht the id's
road_data = pd.read_csv(r"C:\Users\Rob\Dropbox\My PC (DESKTOP-DP7OCOF)\Desktop\GIS_thesis\01_thesis_data\02_temp\03_road\roads_split\zonal_stats_uganda_3\highway_bridleway.csv")
ids = road_data[["id"]]
road_data = ids.copy()

# list of road types for model see output from analysis_3
road_vars = ['highway_path', 'highway_primary', 'highway_residential', 'highway_tertiary', 'highway_trunk', 'highway_unclassified']

# get road types and merge 
for i in road_vars:
    direct = str(r"C:\Users\Rob\Dropbox\My PC (DESKTOP-DP7OCOF)\Desktop\GIS_thesis\01_thesis_data\02_temp\03_road\roads_split\zonal_stats_uganda_3\\" + str(i) +'.csv')
    road_type = pd.read_csv(direct)
    road_data = pd.merge(road_data,road_type, on = "id")

# clean the QGIS mess 
road_data = road_data[["id", "highway_path3length", "highway_primary3length", "highway_residential3length", "highway_tertiary3length", "highway_trunk3length", "highway_unclassified3length"]]


# coefficients from final model 
coeficients = pd.read_csv(r"C:\Users\Rob\Dropbox\My PC (DESKTOP-DP7OCOF)\Desktop\GIS_thesis\01_thesis_data\03_output\03_analysis3\model_coeficients.csv", index_col=0)

# create new column for each variable multiplied by its coeficient 
# ntl 
ntl["ntl_value"] = ntl["mean"].apply(lambda x: x * coeficients.iloc[1]) # can be waay easier see estimation_verification code
aridity["aridity_value"] = aridity["_mean"].apply(lambda x: x * coeficients.iloc[2])

# loop over columns and multiply them their coeficients
count = 1
for i in road_vars:
    road_data[str(i+"_value")] = road_data.iloc[:,count].apply(lambda x: x * coeficients.iloc[count+2])
    count += 1

# dataframe to merge results 
output = ids.copy()

for i in [ntl, aridity, road_data]:
    output = pd.merge(left = output, right = i, on = "id")

# add intercept 
output["intercept"] =  pd.Series([int(coeficients.iloc[0]) for x in range(len(output.index))])

# clean everything 
output = output[["id", "intercept", "ntl_value", "aridity_value", "highway_path_value", "highway_primary_value", "highway_residential_value", "highway_tertiary_value", "highway_trunk_value", "highway_unclassified_value"]]

# make result column, sum up everything but the "id" column
output["result"] = output[list(output)[1:len(list(output))]].sum(axis=1)

# export to csv 
output.to_csv(r"C:\Users\Rob\Dropbox\My PC (DESKTOP-DP7OCOF)\Desktop\GIS_thesis\01_thesis_data\03_output\04_verification\dhs_2018-19_estimates.csv")
