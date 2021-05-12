import geopandas as gpd
import pandas as pd
import pickle
from tqdm import tqdm
from data_utils import fips2state
from joblib import Parallel, delayed

def merge_census_data(fips):
    if "{:02d}".format(fips) not in fips2state:
        return None

    state = fips2state["{:02d}".format(fips)]
    print(f"beginning reading for {state}")

    census_blocks_df = gpd.read_file("zip://../tmp/census/2010/tabblock/tl_2020_{:02d}_tabblock10.zip".format(fips))
    census_blocks_df["Centroid_Lng"] = census_blocks_df["geometry"].apply(lambda x: x.centroid.x)
    census_blocks_df["Centroid_Lat"] = census_blocks_df["geometry"].apply(lambda x: x.centroid.y)

    census_blocks_df = census_blocks_df[["GEOID10", "ALAND10", "Centroid_Lat", "Centroid_Lng"]]
    print(f"Land area for {state} read in.")

    # POPULATION DATA!
    census_blocks_df_pop = gpd.read_file("zip://../tmp/census/2010/tabblockpop/tabblock2010_{:02d}_pophu.zip".format(fips))
    census_blocks_df_pop = census_blocks_df_pop[["BLOCKID10", "POP10"]]
    census_blocks_df_pop.rename(columns={"BLOCKID10":"GEOID10"}, inplace=True)
    print(f"Pop data for {state} read in.")
    return census_blocks_df.merge(census_blocks_df_pop)


merged_data = Parallel(n_jobs=4)(delayed(merge_census_data)(i) for i in tqdm(range(56)))

merged_data_df = pd.concat(md for md in merged_data if md is not None)
merged_data_df.to_csv("merged_census_with_centroid.csv")
