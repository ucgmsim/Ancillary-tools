"""
Author: Sirui Wang
Last edit: 1/18/2021
contact email: sirui_wang@outlook.com
"""

import argparse

import matplotlib.pyplot as plt
import pandas as pd
import random
import Brandenberg_VsCorrelation
import N60Conversion
import Random_generation as rng
import Vs2Vs30
import filters
import get_mean
import plotting


def effective_stress(depth, soiltype="Clay",Geo_age = "Quaternary", water_table_depth=2):
    """
    :param depth: integer
    :param Soil type: string, Default is "Clay"
    :param water_table_depth: integer, default set to 2 m below ground surface
    :return: equation common factors: (A*N60^B*effective_stress^C)*factor
    """
    if soiltype in ["Sand"]:
        if Geo_age in ["Holocene"]:
            factor = 0.90
        elif Geo_age in ["Pleistocene"]:
            factor = 1.17
        else:
            factor = 1
        # (Brandendberg et al, 2010)
        if depth > water_table_depth:
            stress = water_table_depth * 18 + (depth - water_table_depth) * (20-9.81)
        else:
            stress = depth * 18
        A = 30
        B = 0.23
        C = 0.23
        return stress,factor, A, B, C
    elif soiltype in ["Clay", "Silt"]:
        if Geo_age in ["Holocene"]:
            factor = 0.88
        elif Geo_age in ["Pleistocene"]:
            factor = 1.12
        else:
            factor = 1
        # (Brandendberg et al, 2010)
        if depth > water_table_depth:
            stress = water_table_depth * 18 + (depth - water_table_depth) * (20-9.81)
        else:
            stress = depth * 18
        A = 26
        B = 0.17
        C = 0.32
        return stress,factor, A, B, C
    elif soiltype in ["Gravels"]:
        if Geo_age in ["Holocene"]:
            A = 53
            B = 0.19
            C = 0.18
        elif Geo_age in ["Pleistocene"]:
            A = 115
            B = 0.17
            C = 0.12
        else:
            A = 30
            B = 0.215
            C = 0.275
        if depth > water_table_depth:
            stress = water_table_depth * 18 + (depth - water_table_depth) * (20-9.81)
        else:
            stress = depth * 18
        factor = 1
        return stress,factor, A, B, C



def correlation(spt_data_at_this_location):
    """
    :param spt_data_at_this_location:
    :return:updated dictionary with VS30 added to individual dataframes
    """
    depth = spt_data_at_this_location["Depth"]
    N60s = spt_data_at_this_location["N60"]
    soil_type = spt_data_at_this_location["SoilType"]
    Vs_list = []
    Vs_variable_list=[]
    for j in range(len(depth)):
        d = depth[j]
        true_d = d + 0.3048  # Spt testing driven a pile 18 inches into the ground in 3 incremental steps. the
        # number of blows is ignored and only consider the total of the second and third increments. We interests
        # in the vertical effective stress after second increments hence add 12 inches(0.3 m) on top of the start
        # depth given
        N60 = N60s[j]
        stress, factor, A, B, C = effective_stress(true_d, soil_type[j])
        Vs = factor*(A*N60**B*stress**C)
        Vs_list.append(Vs)
        Vs_variable_list.append((stress, factor, A, B, C))
    spt_data_at_this_location["Vs"] = Vs_list
    spt_data_at_this_location["VsVariables"] = Vs_variable_list
    return spt_data_at_this_location

def plot_depth_Vs(para_distributed):
    key = list(para_distributed[2].index.to_numpy())[0]
    sampled_depth = para_distributed[2]["Depth"]
    plot_depth = pd.concat([pd.Series(0), sampled_depth])
    fig, ax = plt.subplots()
    for para_index, dist_para in para_distributed.items():
        if para_index == 0:
            continue
        else:
            sampled_Vs = dist_para["Vs"]
            Vs_list = sampled_Vs.tolist()
            Vs_list.insert(0, Vs_list[0])
            plt.step(Vs_list, -plot_depth, color="grey", linestyle="--", alpha=0.5)
    mean_spt = para_distributed[0]
    mean_Vs = mean_spt["Vs"]
    mean_Vs_list = mean_Vs.tolist()
    mean_Vs_list.insert(0, mean_Vs_list[0])
    plt.step(mean_Vs_list, -plot_depth, color="Black")
    ax.set_title(key)
    ax.set_xlabel("shear wave velocity, randomly filled parameter")
    ax.set_ylabel("Depth of soil")



pd.options.display.max_columns = None

# Create the parser and add arguments
# Edit test parser by -> run -> Edit Configuration -> Parameters (Pycharm)
parser = argparse.ArgumentParser()
parser.add_argument("--spt_file_path", "-s", help="Input spt file path into this argument")
parser.add_argument("--location_file_path", "-l", help="Input spt location path into this argument")
parser.add_argument("--output_path", "-o", default="outputs/peerc_output.csv", help="Input path to save the output csv file")
parser.add_argument("--plot_Vs_depth", "-p", action="store_true", help="Plot Vs vs Depth, True or False, default False")
parser.add_argument("--NumberOfPlots", "-N", default=10, help="Only Input this parameter if plot_Vs_depth is also "
                                                              "inputted, default value for this parameter is 10")
parser.add_argument("--model", "-m", default="Brandenberg2010", help="Input the model you want to run, currently "
                                                                      "supported 'Brandenberg2010', 'Peerc2012'")

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
# ###############################################################################################################



# iterate through the spt file, complete process for each location completely before next to save on memory in case
# of larger data set.
output_dict = {}  # save the mean Vs data in form of dictionary, so that can be easily transformed into pandas
# dataframe to csv file.
count = 0
total_dist_spt = {}
all_spt_dist_spt_dict = {}
all_spt_total_case_dict = {}
for key, item in spt_dict.items():
    dist_spt_dict = {}
    dist_location_dict = {}
    # dictionary index 0 = mean, 1 = original_interpretation, 2-102 are randomly generated parameters for soil type,
    # borehole diameter, hammer type.
    N60_spt_data = N60Conversion.N60Convert(item, location_dict[key])  # Original N60 without random sampling.
    N60_spt_data["SoilType"] = "Clay"
    """
    if correlation_model in ["Brandenberg2010"]:
        dist_spt_dict[1] = Brandenberg_VsCorrelation.correlation(N60_spt_data)  # Original Vs conversion without error.
    elif correlation_model in ["Peerc2012"]:
    """
    dist_spt_dict[1] = correlation(N60_spt_data)
    dist_location_dict[1] = location_dict[key]
    for i in range(0, 100):
        """randomly generate parameters include soil type, borehole diameter, hammertype for missing information.
            100 samples were generated to get a distribution."""
        temp_spt = rng.add_soil_type(spt_dict[key], correlation_model)
        temp_loc_1 = rng.add_bore_dia(location_dict[key])
        temp_loc_2 = rng.add_hammer_type(temp_loc_1)
        temp_loc_3 = rng.add_water_table_depth(temp_loc_2)
        if correlation_model in ["Peerc 2012"]:
            temp_loc_3 = rng.add_age(temp_loc_3)
        # Random entry completed for missing data
        N60_spt_data = N60Conversion.N60Convert(temp_spt, temp_loc_3)  # Finished N60 Conversion
        """
        if correlation_model in ["Brandenberg2010"]:
            dist_spt_dict[i + 2] = Brandenberg_VsCorrelation.correlation(N60_spt_data)  # Randomly sampled Vs Conversion with error
        elif correlation_model in ["Peerc2012"]:
        """
        dist_spt_dict[i + 2] = correlation(N60_spt_data)
        dist_location_dict[i + 2] = temp_loc_3
    count += 1
    print("Stage 4 {}/{}...".format(count, len(spt_dict)))

    # acquire mean Vs from the above 100 samples
    dist_spt_dict[0] = get_mean.for_100_sample(dist_spt_dict)
    mean_spt = dist_spt_dict[0]
    filepath = "outputs/processed_spt/{}_Peerc.csv".format(key)
    mean_spt.to_csv(filepath)
    # log Vs30 mean
    sampled_location_data = dist_location_dict[1]
    latitude, longitude, Vs30_mean = Vs2Vs30.convert(mean_spt, sampled_location_data)
    data = {'Latitude': latitude,
            'Longitude': longitude,
            'Vs30': Vs30_mean}
    output_dict[key] = data
    total_dist_spt[key] = dist_spt_dict

# ###########################################################################################################
if do_plot:
    count = 0
    for key, item in total_dist_spt.items():
        if count < int(max_plot):
            # plot depth against Vs value for the above 102 set on one figure. since there are multiple spt data and
            # plotting all of them takes too much resource, a maximum number of plot to be generated need to be
            # inputted into run parameter.
            plot_depth_Vs(item)  # only plot one case
            count += 1


print("Stage 4 complete")
final_df = pd.DataFrame.from_dict(output_dict, orient='index')
final_df.to_csv(output_path)
print("Stage 5 complete")
plt.show()
print("Stage 6 complete")