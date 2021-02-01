"""
Author: Sirui Wang
last edit date: 1/21/2021
Perform Spt N value to N60 Value Conversion
"""

import get_variables_for_conversion as variables

def N60Convert(spt_data_at_this_location, spt_location):
    N60_list = []
    Variables_list = []
    NValues = spt_data_at_this_location["NValue"]
    hammer_type = spt_location["HammerType"]
    borehole_dia = spt_location["BoreholeDiameter"]
    energy_ratio = spt_location["EnergyRatio"]
    rod_length = spt_data_at_this_location["Depth"]
    for j in range(NValues.count()):
        N = NValues[j]
        Ce, Cb, Cr, Cs = variables.all_variables(energy_ratio, hammer_type, borehole_dia, rod_length[j])
        N60 = N * Ce * Cb * Cr * Cs
        N60_list.append(N60)
        Variables_list.append((Ce,Cb,Cr,Cs))
    spt_data_at_this_location["N60"] = N60_list
    spt_data_at_this_location["N60ConversionVariables"] = Variables_list
    spt_at_this_location_sorted = spt_data_at_this_location.sort_values(by="Depth")
    return spt_at_this_location_sorted
