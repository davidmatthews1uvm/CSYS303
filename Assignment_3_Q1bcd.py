import pandas as pd

import data_utils
from plot_utils import *
import matplotlib.pyplot as plt
import geopandas
import contextily as ctx


ZIPF_fig_file_name_base = "figs/2021_POCS_Assignment_3_q1_GPS_"
FIG_EXTENSIONS = ["pdf", "png"]


# print("loading dataset to pandas")
# df = data_utils.load_dataset()

print("loading dataset")
gdf_all  = data_utils.load_dataset_geo()
minx, miny, maxx, maxy = gdf_all.total_bounds

for category in ["COFFEE HOUSES & CAFES", "CHURCHES", "SCHOOL"]:
    print("Plotting for:", category)
    ZIPF_fig_file_name = [ZIPF_fig_file_name_base + category + "." + ext for ext in FIG_EXTENSIONS]

    gdf = gdf_all[gdf_all["fldHeading"].str.contains(category, na=False)]
    gdf.crs = "EPSG:4269"
    gdf = gdf.to_crs(epsg=3857)
    ax = gdf.plot(figsize=(10, 5), alpha=0.5, edgecolor='k', markersize=1 if category == "COFFEE HOUSES & CAFES" else 0.1)
    # ax.set_xlim(minx, maxx)
    # ax.set_ylim(miny, maxy)
    ctx.add_basemap(ax)
    for ext in FIG_EXTENSIONS:
        plt.savefig(ZIPF_fig_file_name_base  + category + "." + ext, padding="tight")