import pickle
import numpy as np

import pandas as pd
import geopandas

def load_dataset():
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