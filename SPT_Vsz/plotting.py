"""
Author: Sirui Wang
Last edit: 1/18/2021
contact email: sirui_wang@outlook.com
"""

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import random


def histogram(data_path):
    data = pd.read_csv(data_path, header=0)
    sample = data["Vs30"]
    f3 = plt.figure("Vs30 Distribution")
    axes = plt.axes()
    axes.hist(sample, bins=(np.linspace(min(sample), max(sample), 20)))
    axes.set_title("Distribution of Vs30")
    axes.set_xlabel("Vs30")
    axes.set_ylabel("Count")
    axes.grid(True)


def depth_Vs(para_distributed, case_distributed):
    special_index = random.choice(range(1, len(para_distributed)))
    key = list(para_distributed[2].index.to_numpy())[0]
    sampled_depth = para_distributed[2]["Depth"]
    plot_depth = pd.concat([pd.Series(0), sampled_depth])
    fig, ax = plt.subplots()
    for para_index, dist_para in para_distributed.items():
        if para_index == 0:
            continue
        elif para_index == special_index:
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
    special_spt = para_distributed[special_index]
    special_Vs = special_spt["Vs"]
    special_Vs_list = special_Vs.tolist()
    special_Vs_list.insert(0, special_Vs_list[0])
    plt.step(special_Vs_list, -plot_depth, color="Blue")
    ax.set_title(key)
    ax.set_xlabel("shear wave velocity, randomly filled parameter")
    ax.set_ylabel("Depth of soil")
    fig2, ax2 = plt.subplots()
    for case_index, dist_case in case_distributed[special_index].items():
        sampled_Vs = dist_case["Vs"]
        Vs_list = sampled_Vs.tolist()
        Vs_list.insert(0, Vs_list[0])
        plt.step(Vs_list, -plot_depth, color="grey", linestyle="--", alpha=0.5)
    ax2.set_title("{}:{}".format(key, special_index))
    ax2.set_xlabel("shear wave velocity distributed based on case {}".format(special_index))
    ax2.set_ylabel("Depth of soil")


def hist10000(key, item):
    temp_list = []
    for index, sub_item in item.items():
        temp_list = temp_list + sub_item
        len(temp_list)
    sample = temp_list
    f3 = plt.figure("10000 Vs30 Distribution for {}".format(key))
    axes = plt.axes()
    axes.hist(sample, bins=(np.linspace(min(sample), max(sample), 20)))
    axes.set_title("10000 Vs30 Distribution for {}".format(key))
    axes.set_xlabel("Vs30")
    axes.set_ylabel("Count")
    axes.grid(True)


def hist100(key, index, item):
    sample = item
    f3 = plt.figure("100 Vs30 Distribution for {}.{}".format(key, index))
    axes = plt.axes()
    axes.hist(sample, bins=(np.linspace(min(sample), max(sample), 20)))
    axes.set_title("100 Vs30 Distribution for {}.{}".format(key, index))
    axes.set_xlabel("Vs30")
    axes.set_ylabel("Count")
    axes.grid(True)