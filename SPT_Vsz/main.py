"""
Author: Sirui Wang
Main Script that produces the output
Level 1 Script
"""

import VsCorrelation
import pandas as pd
import filters
import N60Conversion
import Vs2Vs30
import argparse
import plotting

# Create the parser and add arguments
"""Input File location"""
# Edit File location by -> run -> Edit Configuration -> Parameters
parser = argparse.ArgumentParser()
parser.add_argument("--spt_file_path", "-s", help="Input spt file path into this argument")
parser.add_argument("--location_file_path", "-l", help="Input spt location path into this argument")
parser.add_argument("--output_path", "-o", default="outputs/output.csv", help="Input path to save the output csv file")
parser.add_argument("--plot_Vs_depth", "-p", action="store_true", help="Plot Vs vs Depth, True or False, default False")
parser.add_argument("--NumberOfPlots", "-N", default=10, help="Only Input this parameter if plot_Vs_depth is also "
                                                              "inputted, default value for this parameter is 10")
# args variables
args = parser.parse_args()
spt_file = args.spt_file_path
location_file = args.location_file_path
output_path = args.output_path
do_plot = args.plot_Vs_depth
Number_of_plots = args.NumberOfPlots

"""the following line acquires the data of interests and stores in Pandas dataframe"""
public_spt_data = pd.read_csv(spt_file, header=0, index_col=0)
spt_locations_data = pd.read_csv(location_file, header=0, index_col=1)

"""Determines all site CombinedName and compile them into a list"""
pd_index = public_spt_data.index.values.tolist()
location_ids = list(set(pd_index))
# All CombinedNames, Include data entries that are invalid.


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

output_dict = {}
for key in spt_dict:
    N60_spt_data = N60Conversion.N60Convert(spt_dict[key], location_dict[key])
    spt_dict[key] = VsCorrelation.correlation(N60_spt_data)
    latitude, longitude, Vs30 = Vs2Vs30.convert(spt_dict[key], location_dict[key])
    data = {'Latitude': latitude,
            'Longitude': longitude,
            'Vs30': Vs30}
    output_dict[key] = data
final_df = pd.DataFrame.from_dict(output_dict, orient='index')
final_df.to_csv(output_path)

if do_plot:
    plotting.histogram(output_path)
    plotting.depth_Vs(spt_dict, int(Number_of_plots))
