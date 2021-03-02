import geopandas
from data_utils import load_business_data_geo, load_census_data_joined

business_gdf = load_business_data_geo()

business_census_gdf = load_census_data_joined()

print(business_census_gdf["GEOID10"].value_counts())
