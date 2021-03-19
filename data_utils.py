import pickle
import numpy as np

import pandas as pd
import geopandas
from joblib import Parallel, delayed

def load_dataset():
    print("Deprecated. Use load_business_data instead!")
    return load_business_data()

def load_business_data():
    try:
        df = pd.read_pickle("../data/business_locations_df_cache.pkl")
    except Exception as e:
        print("Error loading from cache:", e)
        print("Falling back to loading from source csv")
        df = pd.read_csv("../data/business-locations-us.txt", sep="\t")
        df["fldHeading"] = df["fldHeading"].replace(np.nan, 'NAN_CATEGORY_MISSING', regex=True)
        df.to_pickle("../data/business_locations_df_cache.pkl")
    return df

def load_dataset_geo():
    print("Deprecated. Use load_business_data_geo instead!")
    return load_business_data_geo()

def load_business_data_geo():
    try:
        gdf =  pickle.load(open("../data/business_locations_gdf_cache.pkl", "rb"))
    except Exception as e:
        print("Error loading from cache:", e)
        print("Falling back to loading from source df")
        df = load_dataset()
        gdf = geopandas.GeoDataFrame(df, geometry=geopandas.points_from_xy(df.fldLng, df.fldLat))
        gdf.crs = "EPSG:4269"

        pickle.dump(gdf, open("../data/business_locations_gdf_cache.pkl", "wb"))
    return gdf

def load_census_block_data(block_id):
    try:
        census_blocks_df = geopandas.read_file("zip://../tmp/census/2010/tabblock/tl_2020_{:02d}_tabblock10.zip".format(block_id))

        census_blocks_df_pop = geopandas.read_file("zip://../tmp/census/2010/tabblockpop/tabblock2010_{:02d}_pophu.zip".format(block_id))

        census_blocks_df = census_blocks_df[["GEOID10", "ALAND10", "geometry"]]
        census_blocks_df_pop = census_blocks_df_pop[["BLOCKID10", "POP10"]]
        census_blocks_df_pop.rename(columns={"BLOCKID10":"GEOID10"}, inplace=True)
        census_blocks = census_blocks_df.merge(census_blocks_df_pop)
        del census_blocks_df_pop, census_blocks_df

        return census_blocks
    except Exception as e:
        print(e)
        return None

def load_census_blocks_data():
    return Parallel(n_jobs=-1)(delayed(load_census_block_data)(i) for i in range(10))

    
def load_census_tracts_data():
    try:
        gdf = pickle.load(open("../data/census_tracts_gdf_cache.pkl", "rb"))
    except Exception as e:
        print("Failed to load from cache:", e)
        print("Falling back to loading from source")
        gdf = geopandas.read_file("zip://../data/Tract_2010Census_DP1.zip")
        pickle.dump(gdf, open("../data/census_tracts_gdf_cache.pkl", "wb"))
    return gdf

def load_census_counties_data():
    try:
        gdf = pickle.load(open("../data/census_counties_gdf_cache.pkl", "rb"))
    except Exception as e:
        print("Failed to load from cache:", e)
        print("Falling back to loading from source")
        gdf = geopandas.read_file("zip://../data/County_2010Census_DP1.zip")
        pickle.dump(gdf, open("../data/census_counties_gdf_cache.pkl", "wb"))
    return gdf


def load_census_data_joined():
    try:
        gdf = pickle.load(open("../data/joined_data_cache.pkl", "rb"))
    except Exception as e:
        print("Failed to load from cache:", e)
        print("Falling back to loading from source. This may take a while.")
        census_gdf = load_census_tracts_data()
        business_gdf = load_business_data_geo()
        census_gdf_sub = census_gdf[["GEOID10", "geometry"]]
        
        gdf =  geopandas.sjoin(business_gdf, census_gdf_sub, how="inner", op='intersects')
        pickle.dump(gdf, open("../data/joined_data_cache.pkl", "wb"))
    return gdf



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

