import pandas as pd
import data_utils

from plot_utils import *

df = data_utils.load_dataset()

total_tokens = df.shape[0]

# 1
print("\section{}")

# a
print("\subsection{a}")
print(f"The dataset contains $N = {total_tokens}$ tokens.")

ZIPF_fig_file_name_base = "figs/2021_POCS_Assignment_2_q1_zipf_"
FIG_EXTENSIONS = ["pdf", "png"]


# b + c
print("\subsection{b+c}")
ZIPF_fig_file_name = [ZIPF_fig_file_name_base + "." + ext for ext in FIG_EXTENSIONS]
categories_and_counts = df["fldHeading"].value_counts()
num_unique_categories = categories_and_counts.shape[0]

print(f"The dataset contains $N_{'{types}'}= {num_unique_categories}$ unique categories matching the current selection.")

plot_ZIPF(categories_and_counts.values, xlabel="Category Rank", ylabel="Number of Tokens", title=f"US Business Categories ZIPF", save=ZIPF_fig_file_name)

categories_and_counts_with_index = categories_and_counts.reset_index()
categories_and_counts_with_index.rename(columns={"index":"Category", "fldHeading":"Token Count"}, inplace=True)

print(categories_and_counts_with_index.iloc[:10].to_latex())

# d
print("\subsection{d}")

ZIPF_fig_file_name = [ZIPF_fig_file_name_base + "_CHURCHES." + ext for ext in FIG_EXTENSIONS]

df_subset = df[df["fldHeading"].str.contains("CHURCHES", na=False)]

categories_and_counts = df_subset["fldHeading"].value_counts()
num_unique_categories = categories_and_counts.shape[0]

print(f"The dataset contains $N_{'{types}'}= {num_unique_categories}$ unique categories matching the current selection.")

plot_ZIPF(categories_and_counts.values, xlabel="Category Rank", ylabel="Number of Tokens", title=f"US CHURCH Categories ZIPF", save=ZIPF_fig_file_name)

categories_and_counts_with_index = categories_and_counts.reset_index()
categories_and_counts_with_index.rename(columns={"index":"Category", "fldHeading":"Token Count"}, inplace=True)

print(categories_and_counts_with_index.iloc[:10].to_latex())

# e
print("\subsection{e}")

ZIPF_fig_file_name = [ZIPF_fig_file_name_base + "_COFFEE HOUSES & CAFES." + ext for ext in FIG_EXTENSIONS]

df_subset = df[df["fldHeading"].str.contains("COFFEE HOUSES & CAFES", na=False)]

categories_and_counts = df_subset["fldBusinessName"].value_counts()
num_unique_categories = categories_and_counts.shape[0]

print(f"The dataset contains $N_{'{types}'}= {num_unique_categories}$ unique categories matching the current selection.")

plot_ZIPF(categories_and_counts.values, xlabel="Category Rank", ylabel="Number of Tokens", title=f"US COFFEE HOUSES & CAFES Categories ZIPF", save=ZIPF_fig_file_name)

categories_and_counts_with_index = categories_and_counts.reset_index()
categories_and_counts_with_index.rename(columns={"index":"Category", "fldBusinessName":"Token Count"}, inplace=True)

print(categories_and_counts_with_index.iloc[:10].to_latex())



