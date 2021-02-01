"""
Author: Sirui Wang
Last edit: 1/18/2021
contact email: sirui_wang@outlook.com
"""

import random
import numpy as np

def add_soil_type(spt_data, correlation_model="Brandenberg2010"):
    if correlation_model in ["Brandenberg2010"]:
        soiltypes = ["Sand", "Silt", "Clay"]
    elif correlation_model in ["Peerc2012"]:
        soiltypes = ["Sand", "Silt", "Clay", "Gravels"]
    soiltype_fill_in_list = []
    for i in range(0,len(spt_data)):
        soiltype_fill_in_list.append(random.choice(soiltypes))
    spt_data["SoilType"] = soiltype_fill_in_list
    return spt_data

def add_age(spt_data):
    geological_age = ["Holocene","Pleistocene"," Quaternary"]
    age_fill_in_list = []
    for i in range(0,len(spt_data)):
        age_fill_in_list.append(random.choice(geological_age))
    spt_data["GeoAge"] = age_fill_in_list
    return spt_data

def add_bore_dia(sliced_location_data):
    location_data = sliced_location_data.copy(deep=True)
    bore_dia_choice = [100, 150, 200]
    try:
        bore_dia = int(location_data.loc["BoreholeDiameter"])
        if bore_dia >= 65 and bore_dia <= 115:
            return location_data
        elif bore_dia == 150:
            return location_data
        elif bore_dia == 200:
            return location_data
        else:
            bore_dia = random.choice(bore_dia_choice)
            location_data.loc["BoreholeDiameter"] = bore_dia
            return location_data
    except (TypeError, ValueError) as e:
        bore_dia = random.choice(bore_dia_choice)
        location_data.loc["BoreholeDiameter"] = bore_dia
        return location_data


def add_hammer_type(sliced_location_data):
    location_data = sliced_location_data.copy(deep=True)
    hammer_type_choice = ["Auto", "Standard", "Safety"]
    hammer_type = location_data.loc["HammerType"]
    STD_list = ['STD', 'Standard (donut)', 'Cylindrical/donut']
    if any(str(hammer_type) in s for s in STD_list):
        location_data.loc["HammerType"] = "Standard"
        return location_data
    elif str(hammer_type) in ["Auto"]:
        return location_data
    else:
        location_data.loc["HammerType"] = random.choice(hammer_type_choice)
        return location_data

def add_water_table_depth(sliced_location_data):
    location_data = sliced_location_data.copy(deep=True)
    random_water_table_depth = random.randint(0,20) # This is only a assumtpion, assume the water table depth has a
    # maximum of 20 m
    location_data.loc["WaterTableDepth"] = random_water_table_depth
    return location_data
