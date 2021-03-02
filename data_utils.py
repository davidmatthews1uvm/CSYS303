import pickle
import numpy as np

import pandas as pd
import geopandas

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

def load_census_data():
    try:
        gdf = pickle.load(open("../data/census_gdf_cache.pkl", "rb"))
    except Exception as e:
        print("Failed to load from cache:", e)
        print("Falling back to loading from source")
        gdf = geopandas.read_file("zip://../data/Tract_2010Census_DP1.zip")
        pickle.dump(gdf, open("../data/census_gdf_cache.pkl", "wb"))
    return gdf

def load_census_data_joined():
    try:
        gdf = pickle.load(open("../data/joined_data_cache.pkl", "rb"))
    except Exception as e:
        print("Failed to load from cache:", e)
        print("Falling back to loading from source. This may take a while.")
        census_gdf = load_census_data()
        business_gdf = load_business_data_geo()
        census_gdf_sub = census_gdf[["GEOID10", "geometry"]]
        
        gdf =  geopandas.sjoin(business_gdf, census_gdf_sub, how="inner", op='intersects')
        pickle.dump(gdf, open("../data/joined_data_cache.pkl", "wb"))
    return gdf