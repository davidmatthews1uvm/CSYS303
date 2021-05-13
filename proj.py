import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import geopandas as gpd
import re

import scipy
from scipy.spatial import KDTree

from data_utils import *
from haversine import dist
import mapclassify

df = load_business_data()
census_df = pd.read_csv("merged_census_with_centroid.csv")

census_tracts_df = gpd.read_file("zip://../tmp/census/2010/Tract_2010Census_DP1.zip")
census_tracts_df["Centroid_Lng"] = census_tracts_df["geometry"].apply(lambda x: x.centroid.x)
census_tracts_df["Centroid_Lat"] = census_tracts_df["geometry"].apply(lambda x: x.centroid.y)
# census_tracts_df = census_tracts_df[["GEOID10", "ALAND10", "Centroid_Lat", "Centroid_Lng", "DP0010001"]]
census_tracts_df.rename(columns={"DP0010001":"POP10"}, inplace=True)

# census_df_poverty = pd.read_csv("../tmp/nhgis0001_csv/nhgis0001_ds177_20105_2010_tract.csv")
census_df_income = pd.read_csv("../tmp/nhgis0001_csv/nhgis0001_ds176_20105_2010_tract.csv")

categories = np.array(sorted([s.lower() for s in df["fldHeading"].unique()]))

def match_partial(search, categories):
    for category in categories:
        if search in category:
            print(category)

match_partial("organic products", categories)
match_partial("grocer", categories)
match_partial("supermarket", categories)
match_partial("deli", categories)
match_partial("convenience", categories)

# The following is too board. Visual inspection indicates that
# most fresh food stores are not included in in this set of categories.
# match_partial("food", categories)


organic_products_mask = df["fldHeading"].str.contains("organic products", na=False, flags=re.IGNORECASE)
grocer_mask = df["fldHeading"].str.contains("grocer", na=False, flags=re.IGNORECASE)
supermarket_mask = df["fldHeading"].str.contains("supermarket", na=False, flags=re.IGNORECASE)

df_fresh_food_stores = df[organic_products_mask | grocer_mask | supermarket_mask]

df_restaurants = df[df["fldHeading"].str.contains("restaurants", na=False, flags=re.IGNORECASE)]
df_restaurants

df_convenience_stores =  df[(df["fldHeading"] == "CONVENIENCE STORES" )|( df["fldHeading"] == "GAS CONVENIENCE STORE")]



for category, df_category in [("fresh_food", df_fresh_food_stores),
                                ("restaurants", df_restaurants),
                                ("convenience_store", df_convenience_stores)]:

    store_locations = df_category[["fldLng", "fldLat"]].values

    # 10k lookups in 2 seconds
    # 10M lookups in 2000 seconds = 20 mins.
    kdtree = KDTree(store_locations)

    census_block_locations = census_df[["Centroid_Lng", "Centroid_Lat"]].values
    %time i = kdtree.query(census_block_locations, workers=-1)[1]
    d = dist(store_locations[i].T, census_block_locations.T)/1000

    census_df[f"{category}"] = d
    census_df[f"{category}_idx"] = i


    census_tract_locations = census_tracts_df[["Centroid_Lng", "Centroid_Lat"]].values
    %time i = kdtree.query(census_tract_locations, workers=-1)[1]
    d = dist(store_locations[i].T, census_tract_locations.T)/1000

    census_tracts_df[f"{category}"] = d
    census_tracts_df[f"{category}_idx"] = i

census_df_with_people = census_df[census_df["POP10"] > 0]
census_df_with_people_tract = census_tracts_df[census_tracts_df["POP10"] > 0]
for category, df_category in [("fresh_food", df_fresh_food_stores),
                                ("restaurants", df_restaurants),
                                ("convenience_store", df_convenience_stores)]:
    census_df_with_people = census_df_with_people[census_df_with_people[f"{category}"] < 1000] # bug with 2 census tracks in far west alaska which have 174, 173 longitude! need to modify to be -187 or something
    census_df_with_people_tract = census_df_with_people_tract[census_df_with_people_tract[f"{category}"] < 1000] # bug with 2 census tracks in far west alaska which have 174, 173 longitude! need to modify to be -187 or something

census_df_with_people["PopDensity"] = census_df_with_people["POP10"] / (census_df_with_people["ALAND10"]/(1000000) + 1e-3) # min ALAND > 0 is 1. convert to people / km^2
census_df_with_people_tract["PopDensity"] = census_df_with_people_tract["POP10"] / (census_df_with_people_tract["ALAND10"]/(1000000) + 1e-3) # min ALAND > 0 is 1. convert to people / km^2

# VT: 50
# CA: 08
census_df_with_people_tract[census_df_with_people_tract["GEOID10"].str.startswith("50")].plot(column='fresh_food', scheme='quantiles', k=5, figsize=(16, 9), legend=True)
census_df_with_people_tract[census_df_with_people_tract["GEOID10"].str.startswith("50")].plot(column='restaurants', scheme='quantiles', k=5, figsize=(16, 9), legend=True)
census_df_with_people_tract[census_df_with_people_tract["GEOID10"].str.startswith("50")].plot(column='convenience_store', scheme='quantiles', k=5, figsize=(16, 9), legend=True)
census_df_with_people_tract[census_df_with_people_tract["GEOID10"].str.startswith("50")].plot(column='PopDensity', scheme='quantiles', k=5, figsize=(16, 9), legend=True)

census_df_with_people_tract[census_df_with_people_tract["GEOID10"].str.startswith("25")].plot(column='fresh_food', scheme='quantiles', k=5, figsize=(16, 9), legend=True)
census_df_with_people_tract[census_df_with_people_tract["GEOID10"].str.startswith("25")].plot(column='restaurants', scheme='quantiles', k=5, figsize=(16, 9), legend=True)
census_df_with_people_tract[census_df_with_people_tract["GEOID10"].str.startswith("25")].plot(column='convenience_store', scheme='quantiles', k=5, figsize=(16, 9), legend=True)
census_df_with_people_tract[census_df_with_people_tract["GEOID10"].str.startswith("25")].plot(column='PopDensity', scheme='quantiles', k=5, figsize=(16, 9), legend=True)

census_df_with_people_tract[census_df_with_people_tract["GEOID10"].str.startswith("36")].plot(column='fresh_food', scheme='quantiles', k=5, figsize=(16, 9), legend=True)
census_df_with_people_tract[census_df_with_people_tract["GEOID10"].str.startswith("36")].plot(column='restaurants', scheme='quantiles', k=5, figsize=(16, 9), legend=True)
census_df_with_people_tract[census_df_with_people_tract["GEOID10"].str.startswith("36")].plot(column='convenience_store', scheme='quantiles', k=5, figsize=(16, 9), legend=True)
census_df_with_people_tract[census_df_with_people_tract["GEOID10"].str.startswith("36")].plot(column='PopDensity', scheme='quantiles', k=5, figsize=(16, 9), legend=True)

for category in ["fresh_food", "restaurants", "convenience_store"]:
    plt.scatter(census_df_with_people_tract[f"{category}"].values,
                census_df_with_people_tract["PopDensity"].values)
    plt.xlabel(f"avg dist to {category}")
    plt.ylabel(r"pop density $\frac{ppl }{km^2}$")
    plt.loglog()
    plt.show()

import seaborn as sns
data = np.random.rand(8, 8)
ax = sns.heatmap(data, linewidth=0.3)
plt.show()

log_pop_density = np.log10(census_df_with_people_tract["PopDensity"].values)
log_food_dist = np.log10(census_df_with_people_tract["fresh_food"].values)
slope, intercept, rval, pval, stderr = scipy.stats.linregress(log_food_dist, log_pop_density)
slope, rval

log_restaurants_dist = np.log10(census_df_with_people_tract["restaurants"].values)
slope, intercept, rval, pval, stderr = scipy.stats.linregress(log_restaurants_dist, log_pop_density)
slope, rval

log_convenience_store_dist = np.log10(census_df_with_people_tract["convenience_store"].values)
slope, intercept, rval, pval, stderr = scipy.stats.linregress(log_convenience_store_dist, log_pop_density)
slope, rval

log_pop_density = np.log10(census_df_with_people_tract["restaurants"].values)
log_food_dist = np.log10(census_df_with_people_tract["fresh_food"].values)
slope, intercept, rval, pval, stderr = scipy.stats.linregress(log_food_dist, log_pop_density)
slope, rval

log_pop_density = np.log10(census_df_with_people_tract["convenience_store"].values)
log_food_dist = np.log10(census_df_with_people_tract["fresh_food"].values)
slope, intercept, rval, pval, stderr = scipy.stats.linregress(log_food_dist, log_pop_density)
slope, rval

log_pop_density = np.log10(census_df_with_people_tract["convenience_store"].values)
log_food_dist = np.log10(census_df_with_people_tract["restaurants"].values)
slope, intercept, rval, pval, stderr = scipy.stats.linregress(log_food_dist, log_pop_density)
slope, rval
