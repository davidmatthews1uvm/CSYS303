import pandas as pd
import numpy as np
from data_utils import *
import re
from scipy.spatial import KDTree
from haversine import dist

import matplotlib.pyplot as plt



df = load_business_data()
census_df = pd.read_csv("merged_census_with_centroid.csv")


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


store_locations = df_fresh_food_stores[["fldLng", "fldLat"]].values

# 10k lookups in 2 seconds
# 10M lookups in 2000 seconds = 20 mins.
kdtree = KDTree(store_locations)

census_block_locations = census_df[["Centroid_Lng", "Centroid_Lat"]].values
%time i = kdtree.query(census_block_locations, workers=-1)[1]
d = dist(store_locations[i].T, census_block_locations.T)/1000

census_df["Nearest_Fresh_Food"] = d
census_df["Nearest_Fresh_Food_idx"] = i


census_df_with_people = census_df[census_df["POP10"] > 0]
census_df_with_people = census_df_with_people[census_df_with_people["Nearest_Fresh_Food"] < 1000] # bug with 2 census tracks in far west alaska which have 174, 173 longitude! need to modify to be -187 or something

census_df_with_people["PopDensity"] = census_df_with_people["POP10"] / (census_df_with_people["ALAND10"]/(1000000) + 1e-3) # min ALAND > 0 is 1. convert to people / km^2
census_df_with_people["Nearest_Fresh_Food"]



plt.scatter(census_df_with_people["Nearest_Fresh_Food"].values[:100000], census_df_with_people["PopDensity"].values[:100000])
plt.xlabel("avg dist to fresh food")
plt.ylabel(r"pop density $\frac{ppl }{km^2}$")
plt.loglog()


import seaborn as sns
data = np.random.rand(8, 8)
ax = sns.heatmap(data, linewidth=0.3)
plt.show()