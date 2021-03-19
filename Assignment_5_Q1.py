import geopandas
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import scipy.stats
from data_utils import  load_business_data_geo, load_census_data_joined, load_census_blocks_data, load_census_tracts_data, load_census_counties_data


business_gdf = load_business_data_geo()

# business_census_gdf = load_census_data_joined()

census_block_gdfs = load_census_blocks_data()
census_tracts_gdf = load_census_tracts_data()
census_counties_gdf = load_census_counties_data()

def join_blocks(gdf):
    print("BLOCKS NOT JOINED! IMPLEMENT ME!")
    return None

def join_tracts(gdf):
    joined_df = geopandas.sjoin(gdf, census_tracts_gdf, how="inner", op='intersects')

    value_counts = joined_df["GEOID10"].value_counts().reset_index().rename(columns={"index":"GEOID10", "GEOID10": "Count"})
    census_df_sub = census_tracts_gdf[census_tracts_gdf["GEOID10"].isin(joined_df["GEOID10"])][["GEOID10", "ALAND10", "DP0010001"]]
    joined_sub = pd.merge(value_counts, census_df_sub)
    joined_sub["ALAND10_KM2"] = joined_sub["ALAND10"]/1e6
    joined_sub["POP_DENSITY"] = joined_sub["DP0010001"] / joined_sub["ALAND10_KM2"]
    joined_sub["COUNT_DENSITY"] = joined_sub["Count"] / joined_sub["ALAND10_KM2"]
    return joined_sub

def join_counties(gdf):
    joined_df = geopandas.sjoin(gdf, census_counties_gdf, how="inner", op='intersects')
    
    value_counts = joined_df["GEOID10"].value_counts().reset_index().rename(columns={"index":"GEOID10", "GEOID10": "Count"})
    census_df_sub = census_counties_gdf[census_counties_gdf["GEOID10"].isin(joined_df["GEOID10"])][["GEOID10", "ALAND10", "DP0010001"]]
    joined_sub = pd.merge(value_counts, census_df_sub)
    joined_sub["ALAND10_KM2"] = joined_sub["ALAND10"]/1e6
    joined_sub["POP_DENSITY"] = joined_sub["DP0010001"] / joined_sub["ALAND10_KM2"]
    joined_sub["COUNT_DENSITY"] = joined_sub["Count"] / joined_sub["ALAND10_KM2"]
    return joined_sub


def plot(joined_gdf, title=""):
    joined_sub_valid = joined_gdf[joined_gdf["POP_DENSITY"] !=0 ]

    x = joined_sub_valid["POP_DENSITY"]
    x_log = np.log10(x)

    y = joined_sub_valid["COUNT_DENSITY"]
    y_log = np.log10(y)


    print(x.min(), x.max())
    print(y.min(), y.max())

    slope, intercept, rval, pval, stderr = scipy.stats.linregress(x_log, y_log)
    f = lambda x:  np.power(10, np.log10(x) * slope + intercept)

    RMA_slope_direct = np.std(y_log) / np.std(x_log)
    RMA_slope_secondary = slope * 1/rval

    print("OSL", slope, rval, pval)
    print("RMA", RMA_slope_direct, RMA_slope_secondary)


    plt.scatter(x, y)
    plt.yscale("log")
    plt.xscale("log")
    plt.xlim((x.min() * 0.5, x.max()*2))
    plt.xlabel("Population Density")
    plt.ylabel("{} Density".format(category))
    plt.title(title)
    plt.show()




for category in [ "COFFEE HOUSES & CAFES"]: # ,"SCHOOL", "CHURCHES" ]:
    print(category)
    sub_df = business_gdf[business_gdf["fldHeading"].str.contains(category)]
    joined_blocks = join_blocks(sub_df)
    joined_tracts = join_tracts(sub_df)
    joined_counties = join_counties(sub_df)

    # plot(joined_blocks)
    plot(joined_tracts, title="TRACTS")
    plot(joined_counties, title="COUNTIES")



