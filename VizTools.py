"""
@author: Srihari
@date: 12/10/2018
@desc: Main file to run EDA on crime analysis
"""

import os
import time
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from DataExtractor import DataExtractor


def plot_bar(df, x, y, title="", xrot=0, yrot=0):
    g = sns.barplot(x=x, y=y, data=df)
    if xrot != 0:
        g.set_xticklabels(rotation=xrot, labels=g.get_xticklabels())
    if yrot != 0:
        g.set_yticklabels(rotation=yrot, labels=g.get_yticklabels())
    plt.title(title)
    plt.show()
