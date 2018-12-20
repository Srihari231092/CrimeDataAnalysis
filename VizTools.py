"""
@author: Srihari
@date: 12/10/2018
@desc: Main file to run EDA on crime analysis
"""

import os
import time
import pandas as pd
import folium
from folium.plugins import MarkerCluster
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.plotly as py
import plotly.graph_objs as go


def plot_bar(df, x, y, title="", xrot=0, yrot=0):
    g = sns.barplot(x=x, y=y, data=df)
    if xrot != 0:
        g.set_xticklabels(rotation=xrot, labels=g.get_xticklabels())
    if yrot != 0:
        g.set_yticklabels(rotation=yrot, labels=g.get_yticklabels())
    plt.title(title)
    plt.show()


def plot_line(df, x, y, title="", xrot=0, yrot=0, sort_x=False):
    g = sns.lineplot(x=x, y=y, data=df, sort=sort_x, markers="o")
    if xrot != 0:
        g.set_xticklabels(rotation=xrot, labels=df[x])
    if yrot != 0:
        g.set_yticklabels(rotation=yrot, labels=y)
    plt.title(title)
    plt.show()


def choropleth_map(data_path, data, start_coord, threshold_scale,
                   heatmap=False, lats=[], lons=[], mag=[],
                   markerclusters=False):

    # definition of the boundaries in the map
    district_geo = os.path.join(data_path, 'Boundaries_Wards.geojson')

    # creating choropleth map for Chicago
    map1 = folium.Map(location=start_coord, zoom_start=11)
    folium.Choropleth(geo_data=district_geo,
                    data=data,
                    columns=['ward', 'crime_count'],
                    key_on='feature.properties.ward',
                    fill_color='Reds',
                    fill_opacity=0.7,
                    line_opacity=0.2,
                    threshold_scale=threshold_scale,
                    legend_name='Number of incidents per police ward',
                    name="Ward Map").add_to(map1)

    if heatmap:
        # I am using the magnitude as the weight for the heatmap
        hm = folium.plugins.HeatMap(zip(lats, lons, mag), radius=10)
        hm.layer_name = "Heat Map"
        map1.add_child(hm)

    if markerclusters:
        # add a marker for every record in the filtered data
        # use a clustered view
        locations = list(zip(lats, lons))
        markers = MarkerCluster(locations=locations,
                                overlay=True,
                                control=True,
                                name="Count")
        map1.add_child(markers)

    return map1


def print_columns(df):
    """
    Prints columns in data frame
    :param df: dataframe
    :return: None
    """
    print("Dataframe columns :")
    for c in df.columns:
        print("\t", c, end="")
