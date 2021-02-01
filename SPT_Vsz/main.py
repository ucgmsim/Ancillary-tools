"""
Author: Sirui Wang
Last edit: 2/1/2021
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
import time
start_time = time.time()



pd.options.display.max_columns = None

# Create the parser and add arguments
# Edit test parser by -> run -> Edit Configuration -> Parameters (Pycharm)
parser = argparse.ArgumentParser()
parser.add_argument("--spt_file_path", "-s", help="Input spt file path into this argument")
parser.add_argument("--location_file_path", "-l", help="Input spt location path into this argument")
parser.add_argument("--output_path", "-o", default="outputs/output.csv", help="Input path to save the output csv file")
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

# Universal for all model(above)
# ----------------------------------------------------------------------------------------------------------------------
# specific to a particular model(below)


# iterate through the spt file, complete process for each location completely before next to save on memory in case
# of larger data set.
output_dict = {}  # save the mean Vs data in form of dictionary, so that can be easily transformed into pandas
# dataframe to csv file.
count = 0

total_dist_Vs30 = {}
all_spt_dist_spt_dict = {}
all_spt_total_case_dict = {}
plot_count = 0
for key, item in spt_dict.items():
    dist_spt_dict = {}
    dist_location_dict = {}
    # dictionary index 0 = mean, 1 = original_interpretation, 2-102 are randomly generated parameters for soil type,
    # borehole diameter, hammer type.
    N60_spt_data = N60Conversion.N60Convert(item, location_dict[key])  # Original N60 without random sampling.
    N60_spt_data["SoilType"] = "Clay"
    dist_spt_dict[1] = Brandenberg_VsCorrelation.correlation(N60_spt_data)  # Original Vs conversion without error.
    dist_location_dict[1] = location_dict[key]
    for i in range(0, 100):
        """randomly generate parameters include soil type, borehole diameter, hammertype for missing information.
            100 samples were generated to get a distribution."""
        temp_spt = rng.add_soil_type(spt_dict[key])
        temp_loc_1 = rng.add_bore_dia(location_dict[key])
        temp_loc_2 = rng.add_hammer_type(temp_loc_1)
        temp_loc_3 = rng.add_water_table_depth(temp_loc_2)
        # Random entry completed for missing data
        N60_spt_data = N60Conversion.N60Convert(temp_spt, temp_loc_3)  # Finished N60 Conversion
        dist_spt_dict[i + 2] = Brandenberg_VsCorrelation.correlation(N60_spt_data)  # Randomly sampled Vs Conversion with error
        dist_location_dict[i + 2] = temp_loc_3
    count += 1
    print("Stage 4 {}/{}...".format(count, len(spt_dict)))

    # acquire mean Vs from the above 100 samples
    dist_spt_dict[0] = get_mean.for_100_sample(dist_spt_dict)
    mean_spt = dist_spt_dict[0]
    # log Vs30 mean
    sampled_location_data = dist_location_dict[1]
    latitude, longitude, Vs30_mean = Vs2Vs30.convert(mean_spt, sampled_location_data)

    # introduce normal distribution
    dist_Vs30_dict = {}
    total_case_dict = {}
    for case_index, item in dist_spt_dict.items():
        if case_index == 0:
            continue
        else:
            case_dict = {}
            dist_Vs30 = []
            for i in range(0, 100):
                depth_dict = {}
                row_count = 0
                for dist_index, row in item.iterrows():
                    lnVs, b0, b1, b2, stress, total_std = row["VsVariables"]
                    Vs = row["Vs"]
                    depth = row["Depth"]
                    Vs_dist = get_mean.apply_distribution(lnVs, total_std)
                    data = {'Depth': depth,
                            'Vs': Vs_dist}
                    depth_dict[row_count] = data
                    row_count += 1
                case_dict[i] = pd.DataFrame.from_dict(depth_dict, orient="index")
                latitude_na, longitude_na, Vs30 = Vs2Vs30.convert(case_dict[i], sampled_location_data)
                dist_Vs30.append(Vs30)
            dist_Vs30_dict[case_index] = dist_Vs30
            total_case_dict[case_index] = case_dict


    data = {'Latitude': latitude,
            'Longitude': longitude,
            'Vs30': Vs30_mean,
            'std': total_std}
    output_dict[key] = data
    filepath = "outputs/processed_spt/{}_Brandenberg.csv".format(key)
    dist_spt_dict[0].to_csv(filepath)

    if do_plot and plot_count <= int(max_plot):
        total_dist_Vs30[key] = dist_Vs30_dict
        all_spt_dist_spt_dict[key] = dist_spt_dict
        all_spt_total_case_dict[key] = total_case_dict
    plot_count +=1

# plot histogram for all 10000 Vs30 plot one histogram for one case include 100 Vs30 plot Vs/Depth step graph for all
# cases of random selection. then choose one of them plot all cases of distributed error for that one random selection.
if do_plot:
    count = 0
    for key, item in total_dist_Vs30.items():
        if count < int(max_plot):
            plotting.hist10000(key, item)
            plotting.hist100(key, 1, item[1])
            # plot depth against Vs value for the above 102 set on one figure. since there are multiple spt data and
            # plotting all of them takes too much resource, a maximum number of plot to be generated need to be
            # inputted into run parameter.
            plotting.depth_Vs(all_spt_dist_spt_dict[key], all_spt_total_case_dict[key])  # only plot one case
            count += 1


print("Stage 4 complete")
final_df = pd.DataFrame.from_dict(output_dict, orient='index')
final_df.to_csv(output_path)
print("Stage 5 complete")

print("--- %s seconds ---" % (time.time() - start_time))
plt.show()