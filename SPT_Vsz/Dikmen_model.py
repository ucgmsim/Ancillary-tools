"""
Author: Sirui Wang
Last edit: 1/18/2021
contact email: sirui_wang@outlook.com
"""

import argparse

import matplotlib.pyplot as plt
import pandas as pd

import N60Conversion
import Random_generation as rng
import Vs2Vs30
import Brandenberg_VsCorrelation
import filters
import get_mean
import plotting


def Dikmen_model(N, soiltype="default"):
    if soiltype in ["Sand"]:
        Vs = 73 * N ** 0.33
    elif soiltype in ["Clay"]:
        Vs = 44 * N ** 0.48
    elif soiltype in ["Silt"]:
        Vs = 60 * N ** 0.36
    else:
        Vs = 58*N**0.39
    return Vs


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

for key, spt_df in spt_dict.items():
    N_Values = spt_df["NValue"]
    Vs_list = []
    for N in N_Values:
        Vs = Dikmen_model(N)
        Vs_list.append(Vs)
    spt_df["Vs"] = Vs_list
    print(spt_df)
    fig, ax = plt.subplots()
    sampled_depth = spt_df["Depth"]
    plot_depth = pd.concat([pd.Series(0), sampled_depth])
    special_Vs = spt_df["Vs"]
    special_Vs_list = special_Vs.tolist()
    special_Vs_list.insert(0, special_Vs_list[0])
    plt.step(special_Vs_list, -plot_depth, color="Blue")
    ax.set_title(key)
    ax.set_xlabel("shear wave velocity, randomly filled parameter")
    ax.set_ylabel("Depth of soil")
    ax.set_xlim([90,320])
    filepath = "outputs/processed_spt/{}_Dikmen.csv".format(key)
    spt_df.to_csv(filepath)
plt.show()

