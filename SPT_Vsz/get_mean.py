"""
Author: Sirui Wang
Last edit: 1/18/2021
contact email: sirui_wang@outlook.com
"""

import numpy as np
import pandas as pd
import scipy.stats as ss

def for_100_sample(dist_spt_dict):
    num_depth = len(dist_spt_dict[1])
    depth_list = list(dist_spt_dict[1]["Depth"])
    num_index = 100
    init_array = np.zeros((num_depth,num_index))
    for i in range(0, 100):
        df = dist_spt_dict[i+2]
        depth_count = 0
        for index, row in df.iterrows():
            Vs = row["Vs"]
            init_array[depth_count, i] = Vs
            depth_count +=1
    mean_dict = {}
    row_index = 0
    for row in init_array:
        mean_dict[row_index] = [depth_list[row_index], np.mean(row)]
        row_index += 1
    mean_df = pd.DataFrame.from_dict(mean_dict, orient='index', columns=["Depth", "Vs"])
    return mean_df

def apply_distribution(lnVs, total_std):
    lnVs_with_error = ss.truncnorm(-total_std * 2, total_std * 2, loc=lnVs, scale=total_std).rvs()
    Vs_with_error = np.exp(lnVs_with_error)
    return Vs_with_error
