"""
Author: Sirui Wang
Last edit date: 1/21/2021
Category: Tools
"""

import pandas as pd

"""Input File location"""
# Edit File location/ File name here
spt_file = "data/public_spt.csv"
location_file = "data/spt_locations_20201114.csv"

"""the following line acquires the data of interests and stores in Pandas dataframe"""
public_spt_data = pd.read_csv(spt_file, header=0, index_col=0)
spt_locations_data = pd.read_csv(location_file, header=0, index_col=1)
"""Determines all site locations and compile them into a list"""
pd_index = public_spt_data.index.values.tolist()
location_ids = list(set(pd_index))

check_list = []
coordinate_lists = {}
for i in location_ids:
    spt_location = spt_locations_data.loc[i]
    x = spt_location["NZTM_X"]
    y = spt_location["NZTM_Y"]
    if (x, y) not in list(coordinate_lists.keys()):
        coordinate_lists[(x, y)] = i
    else:
        A = coordinate_lists[(x, y)]
        B = i
        print("{} and {} is duplicate".format(A, B))
        check_list.append((A, B))
        print(public_spt_data.loc[A])
        print(public_spt_data.loc[B])
        print("############################################")
