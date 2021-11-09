# -*- coding: utf-8 -*-
"""
Created on Fri Sep 24 16:14:39 2021

merge output from analysis 1 and 2 

make 3 regressions on wealth index: 
    -ntl
    -combined model with total road length
    -combined model with road types 

combine output into single table and export to csv

export coeficients to csv for making final poverty map

@author: Rob


"""

import pandas as pd
import statsmodels.formula.api as sm
from statsmodels.iolib.summary2 import summary_col

# data
# import data from previous analyses 
data_analysis1 = pd.read_csv(r"C:\Users\Rob\Dropbox\My PC (DESKTOP-DP7OCOF)\Desktop\GIS_thesis\01_thesis_data\03_output\01_analysis1\dhs_ntl_road_aridity_3km.csv")

data_analysis2 = pd.read_csv(r"C:\Users\Rob\Dropbox\My PC (DESKTOP-DP7OCOF)\Desktop\GIS_thesis\01_thesis_data\03_output\02_analysis2\dhs_road_split_3km.csv")

# merge data analysis 1 and analysis 2 and clean after merge 
data = data_analysis1.merge(data_analysis2, left_on="cluster", right_on="cluster")
data.rename(columns ={"Wealth_index_x": "Wealth_index"}, inplace=True)

# regressions 
# model 1: ntl
formula =  "Wealth_index ~ Nighttime_light"
reg1 = sm.ols(formula = formula, data = data).fit()

# model 2: combined simple model 
formula =  "Wealth_index ~ Nighttime_light + Road_length + Adjusted_aridity_index"
reg2 = sm.ols(formula = formula, data = data).fit()

# model 3 
formula =  "Wealth_index ~ Nighttime_light + Adjusted_aridity_index + Path + Primary + Residential + Secondary + Tertiary + Trunk + Unclassified"
reg3 = sm.ols(formula = formula, data = data).fit()

# print regression results  
print(reg1.summary(), reg2.summary(), reg3.summary())

# make output summary for ntl, combined model analysis 1 and combined model analysis 2 
regressor_order = ["Intercept", "Nighttime_light", "Road_length", "Adjusted_aridity_index"]
output = summary_col([reg1, reg2,reg3],stars=True,float_format='%0.3f', model_names=["nighttime light", 'combined model 1','combined model 2'],info_dict={'N':lambda x: "{0:d}".format(int(x.nobs))}, regressor_order= regressor_order )
print(output)

# convert regression summaries to table and save that table to csv
reg_out_table = output.tables
reg_out_table[0].to_csv(r"C:\Users\Rob\Dropbox\My PC (DESKTOP-DP7OCOF)\Desktop\GIS_thesis\01_thesis_data\03_output\tables\regression_analysis3.csv")

# export coeficients of final model to make map in QGIS
coeficients = pd.DataFrame(reg3.params)
coeficients.to_csv(r"C:\Users\Rob\Dropbox\My PC (DESKTOP-DP7OCOF)\Desktop\GIS_thesis\01_thesis_data\03_output\03_analysis3\model_coeficients.csv")


