import geopandas
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import scipy.stats
from data_utils import load_census_block_data
import pickle
import argparse


parser = argparse.ArgumentParser()
parser.add_argument("--FIPS", help="FIPS Code for the state to join", default=11, type=int)
args = parser.parse_args()

FIPS = args.FIPS

# load business data
gdf = pickle.load(open("../data/Business_locations_split/BUSINESS_DATA_GDF_FIPS_{:02d}.pkl".format(FIPS), "rb"))


keys_to_save_business = set(gdf.keys())
keys_to_save_business.add("GEOID10")
keys_to_save_business.remove("geometry")
keys_to_save_business = list(keys_to_save_business)

keys_to_save_census = ["GEOID10", "ALAND10", "POP10"]

# load census data
census_data = load_census_block_data(FIPS)

joined_df = geopandas.sjoin(gdf, census_data, how="inner", op='intersects')
business_df_to_save = joined_df[keys_to_save_business]
census_df_to_save = joined_df[keys_to_save_census]

pickle.dump(business_df_to_save, open("../data/Business_locations_split/GEOCODED_BUSINESS_DATA_GDF_FIPS_{:02d}.pkl".format(FIPS), "wb"))
pickle.dump(census_df_to_save, open("../data/Business_locations_split/SUMMARY_CENSUS_DATA_GDF_FIPS_{:02d}.pkl".format(FIPS), "wb"))

business_df_to_save.to_csv("../data/Business_locations_split/GEOCODED_BUSINESS_DATA_GDF_FIPS_{:02d}.csv".format(FIPS))
census_df_to_save.to_csv("../data/Business_locations_split/SUMMARY_CENSUS_DATA_GDF_FIPS_{:02d}.csv".format(FIPS))

