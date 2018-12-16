"""
@author: Srihari
@date: 12/10/2018
@desc: Main file to run EDA on crime analysis
"""

import math
from ast import literal_eval
import numpy as np
import folium
from folium import plugins
from folium.plugins import MarkerCluster
import branca.colormap as cm
import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from VizTools import *
from DataUtils import *

class CrimeStudy:

    def __init__(self, data):
        self._data = data

    def plot_subtypes(self, crime):

        ptype_colname = "Primary Type"
        arrest_colname = "Arrest"

        print("\n Studying Crime type :", crime)
        crime_subset = self._data.loc[self._data[ptype_colname] == crime]

        crime_type_subtypes = crime_subset["Description"].unique()
        print(" sub crime types : ", crime_type_subtypes)
        grouped_crime_subset = \
            crime_subset.groupby(by="Description", axis=0,
                                 as_index=False).count()
        grouped_crime_subset.sort_values([arrest_colname],
                                         inplace=True, ascending=False)

        plot_bar(df=grouped_crime_subset,
                 x="Description",
                 y=arrest_colname,
                 title=crime,
                 xrot=60)

    def histogram_study(self, data, study_sub_crimes=False):

        ptype_colname = "Primary Type"
        arrest_colname = "Arrest"

        # Let's plot the Primary type graph
        # Get all the kinds of Primary types
        primary_types = data[ptype_colname].unique()

        print(" Primary types of crimes : ", primary_types)

        primary_col_agg = \
            data.groupby(by=[ptype_colname], axis=0, as_index=False).count()
        primary_col_agg.sort_values([arrest_colname],
                                    inplace=True,
                                    ascending=False)

        print(primary_col_agg.columns)
        plot_bar(df=primary_col_agg,
                 x=ptype_colname,
                 y=arrest_colname,
                 xrot=60)

        if study_sub_crimes:
            # Study sub crimes?
            for crime_type in primary_types:

                # if "theft" != crime_type.lower():
                #     continue

                self.plot_subtypes(crime_type)

    def heatmap_study(self, data):

        # data = data.groupby(by=["month", "Primary Type"],
        #                     as_index=False).count()
        grouped_data = \
            data.groupby(by=["month", "Location Description"],
                         as_index=False).count()
        grouped_data["crime_count_thousands"] = \
            data.apply(lambda row: row["crime_count"]/1000, axis=1)

        # heatmap_data = \
        #   data.pivot("Primary Type", "month", "crime_count_thousands")
        heatmap_data = \
            grouped_data.pivot("Location Description",
                               "month", "crime_count_thousands")
        sns.heatmap(heatmap_data, cmap="Blues")
        plt.show()

    def time_series_study(self, data):

        grouped_data = \
            data.groupby(by=["month", "Year"],
                         as_index=False).count()

        grouped_data.sort_values(by="Year", ascending=True, inplace=True)
        grouped_data.reset_index(inplace=True, drop=True)

        grouped_data["month_year"] = \
            grouped_data.apply(lambda row:
                               str(row["month"])+"_"+str(row["Year"]),
                               axis=1)



    def count_study(self, data):
        groupedvalues = data.groupby(by=["month"], as_index=False).sum()

        pal = sns.color_palette(palette="Reds_d", n_colors=len(groupedvalues))
        # pal = sns.diverging_palette(10, 20, n=len(groupedvalues))
        rank = groupedvalues["crime_count"].argsort().argsort()

        sns.barplot(x="month", y="crime_count",
                    data=groupedvalues, palette=np.array(pal[::-1])[rank])
        plt.show()

    def geo_study(self, data, data_path, fname, threshold_scale,
                  heatmap=False, lats=[], lons=[], mag=[],
                  markerclusters=False):

        chicago_coordinates = (41.895140898, -87.624255632)

        # definition of the boundaries in the map
        district_geo = os.path.join(data_path, 'Boundaries_Wards.geojson')

        # creating choropleth map for Chicago
        map1 = folium.Map(location=chicago_coordinates, zoom_start=11)
        map1.choropleth(geo_data=district_geo,
                        data=data,
                        columns=['ward', 'crime_count'],
                        key_on='feature.properties.ward',
                        fill_color='Reds',
                        fill_opacity=0.7,
                        line_opacity=0.2,
                        threshold_scale=threshold_scale,
                        legend_name='Number of incidents per police ward',
                        name="Ward Map")

        if markerclusters:
            # add a marker for every record in the filtered data
            # use a clustered view
            locations = list(zip(lats, lons))
            markers = MarkerCluster(locations=locations,
                                    overlay=True,
                                    control=True,
                                    name="Count")
            map1.add_child(markers)

        if heatmap:
            # I am using the magnitude as the weight for the heatmap
            hm = plugins.HeatMap(zip(lats, lons, mag), radius=10)
            hm.layer_name = "Heat Map"
            map1.add_child(hm)

        # add the layer control
        folium.LayerControl().add_to(map1)

        import webbrowser
        filepath = os.path.join(data_path, fname+'.html')
        map1.save(filepath)
        webbrowser.open('file://' + filepath)

    def heatmap_geo_study(self, data, data_path, fname):

        chicago_coordinates = (41.895140898, -87.624255632)

        # creating choropleth map for Chicago
        map1 = folium.Map(location=chicago_coordinates, zoom_start=11)

        lats = []
        lons = []
        mag = []

        for index, row in data.iterrows():
            loc = row["Location"]
            lats.append(float(loc.split(",")[0][1:]))
            lons.append(float(loc.split(",")[1][:-1]))
            mag.append(1)

        # I am using the magnitude as the weight for the heatmap
        map1.add_children(plugins.HeatMap(zip(lats, lons, mag), radius=10))

        import webbrowser
        filepath = os.path.join(data_path, fname + '.html')
        map1.save(filepath)
        webbrowser.open('file://' + filepath)

    @staticmethod
    def merc(coords):

        Coordinates = literal_eval(coords)

        lat = Coordinates[0]
        lon = Coordinates[1]

        r_major = 6378137.000
        x = r_major * math.radians(lon)
        scale = x / lon
        y = 180.0 / math.pi * \
            math.log(math.tan(math.pi / 4.0 + lat *
                              (math.pi / 180.0) / 2.0)) * scale

        return x, y

