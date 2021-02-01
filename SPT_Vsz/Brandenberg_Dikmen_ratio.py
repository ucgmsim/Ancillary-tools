"""
Author: Sirui Wang
Last edit: 1/18/2021
contact email: sirui_wang@outlook.com
"""

import argparse

import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

import N60Conversion
import Random_generation as rng
import Vs2Vs30
import Brandenberg_VsCorrelation
import filters
import get_mean
import plotting

# Create the parser and add arguments
# Edit test parser by -> run -> Edit Configuration -> Parameters (Pycharm)
parser = argparse.ArgumentParser()
parser.add_argument("--spt_file_path", "-s", help="Input spt file path into this argument")
parser.add_argument("--location_file_path", "-l", help="Input spt location path into this argument")
parser.add_argument("--output_path", "-o", default="outputs/output.csv", help="Input path to save the output csv file")
parser.add_argument("--plot_Vs_depth", "-p", action="store_true", help="Plot Vs vs Depth, True or False, default False")
parser.add_argument("--NumberOfPlots", "-N", default=10, help="Only Input this parameter if plot_Vs_depth is also "
                                                              "inputted, default value for this parameter is 10")
parser.add_argument("--model", "-m", default="Brandenberg 2010", help="Input the model you want to run, currently "
                                                                      "supported 'Brandenberg 2010' 'Dikmen empirical'")

# args variables
args = parser.parse_args()
spt_file = args.spt_file_path
location_file = args.location_file_path
output_path = args.output_path
do_plot = args.plot_Vs_depth
max_plot = args.NumberOfPlots
correlation_model = args.model
print("Stage 1 complete")

# the following line acquires the data of interests and stores in Pandas dataframe
# use index_col=1 to achieve that both spt and location has CombinedName as their index
public_spt_data = pd.read_csv(spt_file, header=0, index_col=0)
spt_locations_data = pd.read_csv(location_file, header=0, index_col=1)

# Determines all site CombinedName and compile them into a unique list
# All CombinedNames, Include data entries that maybe invalid.
pd_index = public_spt_data.index.values.tolist()
location_ids = list(set(pd_index))
print("Stage 2 complete")

# remove or edit any data that is invalid.
# log all CombinedName and reason for removal as txt file in default output folder
spt_dict = {}
location_dict = {}
with open('outputs/invalid_locations.txt', 'w') as log:
    for i in location_ids:
        spt_df = public_spt_data.loc[i].copy(deep=True)
        valid_spt_df = filters.remove_invalid_data(log, i, spt_locations_data, spt_df)
        if valid_spt_df is not None:
            spt_dict[i] = valid_spt_df
            location_dict[i] = spt_locations_data.loc[i]
        else:
            continue
print("Stage 3 complete")

for location in list(spt_dict.keys()):
    Dikmen_fp = "outputs/processed_spt/{}_Dikmen.csv".format(location)
    Dikmen_pd = pd.read_csv(Dikmen_fp, header=0, index_col=0)
    Brandenberg_fp = "outputs/processed_spt/{}_Brandenberg.csv".format(location)
    Brandenberg_pd = pd.read_csv(Brandenberg_fp, header=0, index_col=0)
    Peerc_fp = "outputs/processed_spt/{}_Peerc.csv".format(location)
    Peerc_pd = pd.read_csv(Peerc_fp, header=0, index_col=0)
    depth = Brandenberg_pd["Depth"]
    Brandenberg_Vs = Brandenberg_pd["Vs"]
    Dikmen_Vs = Dikmen_pd["Vs"]
    Peerc_Vs = Peerc_pd["Vs"]
    Brandenberg_Dikmen_ratio = []
    Brandenberg_Peerc_ratio = []
    Dikmen_Peerc_ratio = []
    for i in range(0,len(Brandenberg_Vs)):
        BD_ratio = Brandenberg_Vs.iloc[i]/Dikmen_Vs.iloc[i]
        BD_ratio = np.log(BD_ratio)
        Brandenberg_Dikmen_ratio.append(BD_ratio)
        BP_ratio = Brandenberg_Vs.iloc[i] / Peerc_Vs.iloc[i]
        BP_ratio = np.log(BP_ratio)
        Brandenberg_Peerc_ratio.append(BP_ratio)
        DP_ratio = Dikmen_Vs.iloc[i] / Peerc_Vs.iloc[i]
        DP_ratio = np.log(DP_ratio)
        Dikmen_Peerc_ratio.append(DP_ratio)
    fig, ax = plt.subplots()
    ax.plot(Brandenberg_Dikmen_ratio, -depth, label="BD Match")
    ax.plot(Brandenberg_Peerc_ratio, -depth, label="BP Match")
    ax.plot(Dikmen_Peerc_ratio, -depth, label="DP Match")
    ax.plot(np.zeros(len(depth)), -depth, label="Perfect match")
    ax.set_title("Brandenberg to Dikmen to Peerc model ratio for {}".format(location))
    ax.set_xlabel("Ratio")
    ax.set_ylabel("Depth of soil")
    ax.legend()

plt.show()
