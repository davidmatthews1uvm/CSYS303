import geopandas
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import scipy.stats
import data_utils
from data_utils import  load_business_data_geo, load_census_data_joined, load_census_tracts_data, load_census_counties_data
import pickle

#
fips2state = {
        "01": "AL", "02": "AK", "04": "AZ", "05": "AR", "06": "CA",
        "08": "CO", "09": "CT", "10": "DE", "11": "DC", "12": "FL",
        "13": "GA", "15": "HI", "16": "ID", "17": "IL", "18": "IN",
        "19": "IA", "20": "KS", "21": "KY", "22": "LA", "23": "ME",
        "24": "MD", "25": "MA", "26": "MI", "27": "MN", "28": "MS",
        "29": "MO", "30": "MT", "31": "NE", "32": "NV", "33": "NH",
        "34": "NJ", "35": "NM", "36": "NY", "37": "NC", "38": "ND",
        "39": "OH", "40": "OK", "41": "OR", "42": "PA", "44": "RI",
        "45": "SC", "46": "SD", "47": "TN", "48": "TX", "49": "UT",
        "50": "VT", "51": "VA", "53": "WA", "54": "WV", "55": "WI",
        "56": "WY",  # dictionary mapping FIPS code to state abbreviation
    }

state2fips = dict([(v,k) for (k,v) in fips2state.items()])



# geocode the data.

business_gdf = load_business_data_geo()

# 1. Seperate business gdf into sub dataframes + Save to file.
states = list(business_gdf["fldState"].unique())
state_dfs = [business_gdf[business_gdf["fldState"] == state] for state in states]

for state_abv, state_df in zip(states, state_dfs):
   pickle.dump(state_df, open(f"../data/BUSINESS_DATA_GDF_FIPS_{state2fips[state_abv]}.pkl", "wb"))

