# -*- coding: utf-8 -*-
"""
Created on Thu Sep 16 18:27:35 2021

Merges DHS, NTL, roads and AR data by cluster id 

To do:
    -add AR data, aridity and topography
    -add population data 
    -write general function for merging... but need consistent                                              inputt for that?

# - directory
# - column names 
# - main differences between google earth engine stuff and own files 


@author: Rob
"""

import pandas as pd
from sklearn.preprocessing import StandardScaler


# import DHS rural wealth index data 
dhs = pd.read_csv(r"C:\Users\Rob\Dropbox\My PC (DESKTOP-DP7OCOF)\Desktop\GIS_thesis\01_thesis_data\02_temp\05_dhs\ug_dhs_wi.csv")


# dhs + ntl
# make a new DF for merge
dhs_ntl = dhs.copy()

# loops over csv files with ntl observations and merges them with dhs wealth index data 
for i in [*range(3,8,1)]:
    dir = str(r"C:\Users\Rob\Dropbox\My PC (DESKTOP-DP7OCOF)\Desktop\GIS_thesis\01_thesis_data\02_temp\02_ntl\ntl_observations\ntl_" + str(i) + ".csv")
    ntl = pd.read_csv(dir)
    ntl = ntl[["DHSCLUST", "mean"]]
    ntl.rename(columns = {"mean":str("ntl_mean_"+str(i)), }, inplace=True)
    dhs_ntl = dhs_ntl.merge(ntl, left_on = "cluster", right_on = "DHSCLUST")


# dhs + ntl + road
# make new DF for merge 
dhs_ntl_road = dhs_ntl

# loops over csv files with road observations and merges them with dhs wealth index data 
for i in [*range(3,8,1)]:
    dir = str(r"C:\Users\Rob\Dropbox\My PC (DESKTOP-DP7OCOF)\Desktop\GIS_thesis\01_thesis_data\02_temp\03_road\road_aggregate\road_"+ str(i) +".csv")
    road = pd.read_csv(dir)
    road = road[["DHSCLUST","length"]]
    road.rename(columns = {"length":str("road_length_"+str(i))}, inplace=True)
    dhs_ntl_road = dhs_ntl_road.merge(road, left_on = "cluster", right_on = "DHSCLUST")
    
# dhs + ntl + road + aridity 
# make new DF for merge g
dhs_ntl_road_aridity = dhs_ntl_road

#import road for each scale and merge with DHS_NTL DF 
vars_aridity = []
for i in [*range(3,8,1)]:
    dir = str(r"C:\Users\Rob\Dropbox\My PC (DESKTOP-DP7OCOF)\Desktop\GIS_thesis\01_thesis_data\02_temp\04_aridity\02_observations\aridity_" + str(i) +".csv")
    aridity = pd.read_csv(dir)
    aridity = aridity[["DHSCLUST", "_mean"]]
    aridity.rename(columns = {"_mean":str("aridity_mean_" +str(i))}, inplace=True)
    dhs_ntl_road_aridity = dhs_ntl_road_aridity.merge(aridity, left_on = "cluster", right_on = "DHSCLUST")


#clean by dropping all the clustter clutter 
df = dhs_ntl_road_aridity[["cluster", "wi", "ntl_mean_3", "ntl_mean_4", "ntl_mean_5", "ntl_mean_6", "ntl_mean_7", "road_length_3", "road_length_4", "road_length_5", "road_length_6", "road_length_7", "aridity_mean_3", "aridity_mean_4", "aridity_mean_5", "aridity_mean_6", "aridity_mean_7"]]

df.to_csv(r"C:\Users\Rob\Desktop\GIS_thesis\01_thesis_data\03_output\01_analysis1\data_analysis1.csv", index = True)

# standardize the indepndent variables using sklearn function (subtract mean and devide by standard deviation)
# xstandard = (xi – mean(x)) / sd(x) 
df_standard = df.copy()
df_standard.iloc[:,2:] = StandardScaler().fit_transform(df_standard.iloc[:,2:])

df_standard.to_csv(r"C:\Users\Rob\Desktop\GIS_thesis\01_thesis_data\03_output\01_analysis1\data_analysis1_standardized.csv", index = True)


















