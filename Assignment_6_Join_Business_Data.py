import geopandas
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import scipy.stats
import data_utils
from data_utils import  load_business_data_geo, load_census_data_joined, load_census_tracts_data, load_census_counties_data, load_census_block_data
import pickle
import argparse


parser = argparse.ArgumentParser()
parser.add_argument("--FIPS", help="FIPS Code for the state to join", default=0, type=int)
args = parser.parse_args()


# load business data

# load census data
census_data = load_census_block_data(args.FIPS)


# geocode the data.

business_gdf = load_business_data_geo()

# 1. Seperate business gdf into sub dataframes + Save to file.
states = list(business_gdf["fldState"].unique())
state_dfs = [business_gdf[business_gdf["fldState"] == state] for state in states]

for state_abv, state_df in zip(states, state_dfs):
   pickle.dump(state_df, open(f"../data/BUSINESS_DATA_GDF_FIPS_{state2fips[state_abv]}.pkl", "wb"))

