import geopandas
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import scipy.stats
from data_utils import  load_business_data_geo, load_census_data_joined, load_census_tracts_data, load_census_counties_data


business_gdf = load_business_data_geo()

# business_census_gdf = load_census_data_joined()

census_tracts_gdf = load_census_tracts_data()
census_counties_gdf = load_census_counties_data()
census_blocks_joined = pd.read_csv("census_data.csv")
business_blocks_joined = pd.read_csv("business_data.csv")

def join_blocks(gdf):
    businesses_of_interest = business_blocks_joined[business_blocks_joined["pkRecordId"].isin(sub_df["pkRecordId"])]
    block_value_counts = businesses_of_interest["GEOID10"].value_counts()
    block_value_counts = block_value_counts.reset_index().rename(columns={"index":"GEOID10", "GEOID10": "Count"})

    census_df_sub = census_blocks_joined[census_blocks_joined["GEOID10"].isin(businesses_of_interest["GEOID10"])][["GEOID10", "ALAND10", "POP10"]]

    joined_sub = pd.merge(block_value_counts, census_df_sub)
    joined_sub["ALAND10_KM2"] = joined_sub["ALAND10"]/1e6
    joined_sub["POP_DENSITY"] = joined_sub["POP10"] / joined_sub["ALAND10_KM2"]
    joined_sub["COUNT_DENSITY"] = joined_sub["Count"] / joined_sub["ALAND10_KM2"]
    return joined_sub

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


def plot(joined_gdf, title="", scaling_break=None):
    joined_gdf = joined_gdf.replace([np.inf, -np.inf], np.nan).dropna() # census tracts can have 0 land area! This causes INFs to appear.
    joined_sub_valid = joined_gdf[joined_gdf["POP_DENSITY"] !=0 ]
    

    x = joined_sub_valid["POP_DENSITY"]
    x_log = np.log10(x)

    y = joined_sub_valid["COUNT_DENSITY"]
    y_log = np.log10(y)


    # print(x.min(), x.max())
    # print(y.min(), y.max())
    plt.clf()
    plt.cla()
    plt.scatter(x, y)

    if scaling_break is not None:
        x_log_low = x_log[joined_sub_valid["POP_DENSITY"] < scaling_break]
        y_log_low = y_log[joined_sub_valid["POP_DENSITY"] < scaling_break]

        slope, intercept, rval, pval, stderr = scipy.stats.linregress(x_log_low, y_log_low)

        RMA_slope_direct = np.std(y_log_low) / np.std(x_log_low)
        RMA_slope_secondary = slope * 1/rval

        f_ols = lambda x:  np.power(10, np.log10(x) * slope + intercept)
        f_rma = lambda x:  np.power(10, np.log10(x) * RMA_slope_direct + intercept)

        x_nought = np.power(10, x_log_low.min())
        plt.plot([x_nought, scaling_break], [f_ols(x_nought), f_ols(scaling_break)], c="C1", label=r"$x<{}$ OSL Slope = {:.2f} $R = {:.3E}$".format(scaling_break, slope, rval), linestyle="dashed")
        plt.plot([x_nought, scaling_break], [f_rma(x_nought), f_rma(scaling_break)], c="C2", label=r"$x<{}$ RMA Slope = {:.2f}".format(scaling_break, RMA_slope_direct), linestyle="dashed")
        
        print("Running with Scaling break! at", scaling_break)
        print(f"x < {scaling_break}")
        print("OSL", slope, rval, pval)
        print("RMA", RMA_slope_direct, RMA_slope_secondary)

        x_log_high = x_log[joined_sub_valid["POP_DENSITY"] >= scaling_break]
        y_log_high  = y_log[joined_sub_valid["POP_DENSITY"] >= scaling_break]

        slope, intercept, rval, pval, stderr = scipy.stats.linregress(x_log_high, y_log_high)

        RMA_slope_direct = np.std(y_log_high) / np.std(x_log_high)
        RMA_slope_secondary = slope * 1/rval

        f_ols = lambda x:  np.power(10, np.log10(x) * slope + intercept)
        f_rma = lambda x:  np.power(10, np.log10(x) * RMA_slope_direct + intercept)

        x_nought = np.power(10, x_log_high.max())
        plt.plot([scaling_break, x_nought], [f_ols(scaling_break), f_ols(x_nought)], c="C3", label=r"$x >= {}$ OSL Slope = {:.2f} $R = {:.3E}$ ".format(scaling_break, slope, rval), linestyle="dashed")
        plt.plot([scaling_break, x_nought], [f_rma(scaling_break), f_rma(x_nought)], c="C4", label=r"$x >= {}$ RMA Slope = {:.2f}".format(scaling_break, RMA_slope_direct), linestyle="dashed")


        print(f"x >= {scaling_break}")
        print("OSL", slope, rval, pval)
        print("RMA", RMA_slope_direct, RMA_slope_secondary)

    else:

        slope, intercept, rval, pval, stderr = scipy.stats.linregress(x_log, y_log)

        RMA_slope_direct = np.std(y_log) / np.std(x_log)
        RMA_slope_secondary = slope * 1/rval

        f_ols = lambda x:  np.power(10, np.log10(x) * slope + intercept)
        f_rma = lambda x:  np.power(10, np.log10(x) * RMA_slope_direct + intercept)

        x_nought = np.power(10, x_log.min())
        x_prime = np.power(10, x_log.max())
        plt.plot([x_nought, x_prime], [f_ols(x_nought), f_ols(x_prime)], c="C1", label="OSL Slope = {:.2f} $R = {:.3E}$".format(slope, rval), linestyle="dashed")
        plt.plot([x_nought, x_prime], [f_rma(x_nought), f_rma(x_prime)], c="C2", label="RMA Slope = {:.2f}".format(RMA_slope_direct), linestyle="dashed")

        print("OSL", slope, rval, pval)
        print("RMA", RMA_slope_direct, RMA_slope_secondary)



    plt.yscale("log")
    plt.xscale("log")
    plt.xlim((x.min() * 0.5, x.max()*2))
    plt.xlabel("Population Density")
    plt.ylabel("{} Density".format(category))
    plt.title(title)
    plt.legend()
    plt.savefig(f"figs/A6_Q5_{title}.pdf", bbox_inches="tight")
    plt.savefig(f"figs/A6_Q5_{title}.png", bbox_inches="tight", dpi=300)
    plt.show()




for category in [ "COFFEE HOUSES & CAFES", "SCHOOL", "CHURCHES" ]:
    print("\n\n", category)
    sub_df = business_gdf[business_gdf["fldHeading"].str.contains(category)]
    joined_blocks = join_blocks(sub_df)
    joined_tracts = join_tracts(sub_df)
    joined_counties = join_counties(sub_df)

    print("Blocks...")
    plot(joined_blocks, title=f"{category} BLOCKS", scaling_break=None)
    print("Tracts...")
    plot(joined_tracts, title=f"{category} TRACTS", scaling_break = 100 if category == "COFFEE HOUSES & CAFES" else None)
    print("Counties...")
    plot(joined_counties, title=f"{category} COUNTIES", scaling_break = 100 if category == "COFFEE HOUSES & CAFES" else None)


# category = "COFFEE HOUSES & CAFES"
# sub_df = business_gdf[business_gdf["fldHeading"].str.contains(category)]
# joined_counties = join_counties(sub_df)
# plot(joined_counties, title=f"{category} COUNTIES", scaling_break = 100 if category == "COFFEE HOUSES & CAFES" else None)
