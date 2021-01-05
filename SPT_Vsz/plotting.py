"""
Author: Sirui Wang

Level 3 Script
"""

import numpy as np
import matplotlib.pyplot as plt
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
    plt.show()


def depth_Vs(spt_dict, sample_size=10):
    random_key_list = random.sample(list(spt_dict.keys()), sample_size)
    for key in random_key_list:
        spt_data = spt_dict[key]
        depth = spt_data["Depth"]
        Vs = spt_data["Vs"]
        fig, ax = plt.subplots()
        plot_depth = pd.concat([pd.Series(0), depth])
        Vs_list = Vs.tolist()
        Vs_list.insert(0, Vs_list[0])
        plt.step(Vs_list, -plot_depth)
        ax.set_title(key)
        ax.set_xlabel("shear wave velocity")
        ax.set_ylabel("Depth of soil")
    plt.show()
