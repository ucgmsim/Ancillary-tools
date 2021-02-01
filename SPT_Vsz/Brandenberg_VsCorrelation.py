"""
Author: Sirui Wang
Last edit: 1/18/2021
contact email: sirui_wang@outlook.com
"""

import numpy as np
from math import sqrt
import scipy.stats as ss

def effective_stress(depth, soiltype="Clay", water_table_depth=2):
    """
    :param depth: integer
    :param Soil type: string, Default is "Clay"
    :param water_table_depth: integer, default set to 2 m below ground surface
    :return: stress, sigma, b0, b1, b2 factors
    """
    if soiltype in ["Sand"]:
        b0 = 4.045
        b1 = 0.096
        b2 = 0.236
        tao = 0.217
        # (Brandendberg et al, 2010)
        if depth > water_table_depth:
            stress = water_table_depth * 18 + (depth - water_table_depth) * (20-9.81)
        else:
            stress = depth * 18
        if stress <= 200:
            sigma = 0.57 - 0.07 * np.log(stress)
        else:
            sigma = 0.2
        return stress, sigma, tao, b0, b1, b2
    elif soiltype in ["Silt"]:
        b0 = 3.783
        b1 = 0.178
        b2 = 0.231
        tao = 0.227
        # (Brandendberg et al, 2010)
        if depth > water_table_depth:
            stress = water_table_depth * 19 + (depth - water_table_depth) * (17-9.81)
        else:
            stress = depth * 19
        if stress <= 200:
            sigma = 0.31 - 0.03 * np.log(stress)
        else:
            sigma = 0.15
        return stress, sigma,tao, b0, b1, b2
    elif soiltype in ["Clay"]:
        # default is clay
        b0 = 3.996
        b1 = 0.230
        b2 = 0.164
        tao = 0.227
        # (Brandendberg et al, 2010)
        if depth > water_table_depth:
            stress = water_table_depth * 16 + (depth - water_table_depth) * (18-9.81)
        else:
            stress = depth * 16
        if stress <= 200:
            sigma = 0.21 - 0.01 * np.log(stress)
        else:
            sigma = 0.16
        return stress, sigma, tao, b0, b1, b2


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
        stress, sigma, tao, b0, b1, b2 = effective_stress(true_d, soil_type[j])
        lnVs = b0 + b1 * np.log(N60) + b2 * np.log(stress)  # (Brandendberg et al, 2010)
        total_std = sqrt(tao ** 2 + sigma ** 2)
        #lnVs_with_error = ss.truncnorm(-total_std*2, total_std*2, loc=lnVs, scale=total_std).rvs()
        Vs = np.exp(lnVs)
        Vs_list.append(Vs)
        Vs_variable_list.append((lnVs, b0,b1,b2,stress,total_std))
    spt_data_at_this_location["Vs"] = Vs_list
    spt_data_at_this_location["VsVariables"] = Vs_variable_list
    return spt_data_at_this_location
