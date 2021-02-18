import pandas as pd
import data_utils
from plot_utils import *

df = data_utils.load_dataset()

ZIPF_fig_file_name_base = "figs/2021_POCS_Assignment_3_q1_zipf_"
FIG_EXTENSIONS = ["pdf", "png"]

# 1
print("\section{Data Wrangling}")

# a
print("\subsection{a}")
category = "SCHOOL"

ZIPF_fig_file_name = [ZIPF_fig_file_name_base + category + "." + ext for ext in FIG_EXTENSIONS]

df_subset = df[(df["fldHeading"].str.contains(category, na=False))]

categories_and_counts = df_subset["fldHeading"].value_counts()
num_unique_categories = categories_and_counts.shape[0]

print(f"The dataset contains $N_{'{types}'}= {num_unique_categories}$ unique categories containing the string: '{category}'.")

plot_ZIPF(categories_and_counts.values, xlabel="Category Rank", ylabel="Number of Tokens", title=f"US {category} Categories ZIPF", save=ZIPF_fig_file_name)

categories_and_counts_with_index = categories_and_counts.reset_index()
categories_and_counts_with_index.rename(columns={"index":"Category", "fldHeading":"Token Count"}, inplace=True)

print()
print(categories_and_counts_with_index.iloc[:10].to_latex())
