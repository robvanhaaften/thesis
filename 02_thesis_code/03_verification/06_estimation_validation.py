# -*- coding: utf-8 -*-
"""
Created on Fri Oct 22 18:55:44 2021

predict 2018-19 dhs mis outcomes using weflare estimation model

@author: Rob
"""


import pandas as pd 
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt
import statsmodels.formula.api as sm
import seaborn as sns
from statsmodels.iolib.summary2 import summary_col


 
sns.set_theme()


# import proxy observations

ntl = pd.read_csv(r"C:\Users\Rob\Dropbox\My PC (DESKTOP-DP7OCOF)\Desktop\GIS_thesis\01_thesis_data\02_temp\02_ntl\ntl_observations\ntl_mis.csv")

road = pd.read_csv(r"C:\Users\Rob\Dropbox\My PC (DESKTOP-DP7OCOF)\Desktop\GIS_thesis\01_thesis_data\02_temp\03_road\roads_split\zonal_stats\mis_merged.csv")

aridity = pd.read_csv(r"C:\Users\Rob\Dropbox\My PC (DESKTOP-DP7OCOF)\Desktop\GIS_thesis\01_thesis_data\02_temp\04_aridity\02_observations\aridity_mis.csv")


# clean roads 
# group by cluster by avaraging the household level observations 
road = road.groupby(by = "DHSCLUST").mean()
# keep all the relevant observations and teh "id"
road = road[road.columns[(road.columns.str.endswith('length')) | (road.columns.str.endswith('id'))]]
# drop unmaintained because it give trouble 
road = road[road.columns[(~road.columns.str.contains("maintained"))]]

# rename columns
road.rename(columns = {
    
    "highway_bridlewaylength"          : "Bridleway", 
    "highway_constructionlength"       : "Construction", 
    "highway_crossinglength"           : "Crossing", 
    "highway_cyclewaylength"           : "Cycleway", 
    "highway_footwaylength"            : "Footway", 
    "highway_living_streetlength"      : "Living_street", 
    "highway_motorwaylength"           : "Motorway", 
    "highway_motorway_linklength"      : "Motorway_link", 
    "highway_pathlength"               : "Path", 
    "highway_pedestrianlength"         : "Pedestrian", 
    "highway_primarylength"            : "Primary", 
    "highway_primary_linklength"       : "Primary_link", 
    "highway_proposedlength"           : "Proposed", 
    "highway_residentiallength"        : "Residential", 
    "highway_roadlength"               : "Road", 
    "highway_secondarylength"          : "Secondary", 
    "highway_secondary_linklength"     : "Secondary_link", 
    "highway_servicelength"            : "Service", 
    "highway_stepslength"              : "Steps",
    "highway_tertiarylength"           : "Tertiary", 
    "highway_tertiary_linklength"      : "Tertiary_link", 
    "highway_trunklength"              : "Trunk", 
    "highway_trunk_linklength"         : "Trunk_link", 
    "highway_unclassifiedlength"       : "Unclassified"
    
    }, inplace=True)

# keep only roads that made it to the reduced model 
road = road[["id", "Path", "Primary", "Residential", "Secondary", "Tertiary", "Trunk", "Unclassified"]]

# merge predictors merge ntl, road and aridity on cluster id 
ntl_road = ntl.merge(road, on = "DHSCLUST")
ntl_road_arididty = ntl_road.merge(aridity, on = "DHSCLUST")

# keep whats relevant (mean is for ntl and _mean is for aridity)
data = ntl_road_arididty[["DHSCLUST", "mean", "_mean", "Path", "Primary", "Residential", "Secondary", "Tertiary", "Trunk", "Unclassified"]]
# rename ntl and aridity 
data.rename(columns = {"mean": "ntl", "_mean": "aridity"}, inplace = True)

# standardize the indepndent variables by subtracting the mean and deviding by the standard deviation)
# xi_standard = (xi – mean(x)) / sd(x) 
data.iloc[:,1:] = StandardScaler().fit_transform(data.iloc[:,1:])

# import coeficients from final model 
coeficients = pd.read_csv(r"C:\Users\Rob\Dropbox\My PC (DESKTOP-DP7OCOF)\Desktop\GIS_thesis\01_thesis_data\03_output\03_analysis3\model_coeficients.csv")

# calculate estimates for individual proxies: observation * coeficient = observation_estimate 
num = 1
for i in list(data)[1:]:
    new_var = i + "_estimate"
    data[new_var] = data[i] * coeficients.iloc[num][1]
    num += 1

# estimate final output by summing observation_estimates with intercept: Intercept + estimate ...
col_list = [x for x in list(data) if 'estimate' in x]
data["estimate"] = data[col_list].sum(axis=1) + coeficients.iloc[0][1]

# import survey outcomes 
dhs_mis = pd.read_csv(r"C:\Users\Rob\Dropbox\My PC (DESKTOP-DP7OCOF)\Desktop\GIS_thesis\01_thesis_data\02_temp\05_dhs\ug_dhs_mis_wi.csv")

# merge survey with estimates 
data = data.merge(dhs_mis, left_on = "DHSCLUST", right_on="cluster")


# plot predictions against outcomes
reg = sm.ols(formula = "wi ~ estimate", data = data).fit()
print("r-squared adjusted = \t" + str(reg.rsquared_adj))
reg_out = summary_col([reg],stars=True,float_format="%0.3f", model_names=["Validation"],info_dict={"N":lambda x: "{0:d}".format(int(x.nobs))})
print(reg_out)

reg_out_table = reg_out.tables
reg_out_table[0].to_csv(r"C:\Users\Rob\Dropbox\My PC (DESKTOP-DP7OCOF)\Desktop\GIS_thesis\01_thesis_data\03_output\tables\regression_validation.csv")
# Note that tables is a list. The table at index 1 is the "core" table. Additionally, read_html puts dfs in a list, so we want index 0


sns.regplot(x='wi', y='estimate', data=data)
plt.ylabel("Obsevartions")
plt.xlabel("Estimates")
plt.savefig(r"C:\Users\Rob\Dropbox\My PC (DESKTOP-DP7OCOF)\Desktop\GIS_thesis\01_thesis_data\03_output\plots\Figure4.png")








