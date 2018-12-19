"""
@author: Srihari
@date: 12/10/2018
@desc: Main file to run EDA on crime analysis
"""

import os
import time
import pandas as pd
import numpy as np
import datetime
import calendar

from DataExtractor import DataExtractor
from SQLDatabaseManager import SQLDatabaseManager
from CrimeStudy import CrimeStudy
from VizTools import *
from DataUtils import *

# Week to start on Sunday [0-6] where 0 is monday and 6 is sunday
calendar.setfirstweekday(6)


def get_week_of_month(year, month, day):
    x = np.array(calendar.monthcalendar(year, month))
    week_of_month = np.where(x == day)[0][0] + 1
    return week_of_month


def add_date_info(data):
    # Convert the Date column into a datetime type
    data['Date'] = pd.to_datetime(data['Date'])

    winter_months = [1, 2, 3]
    summer_months = [4, 5, 6]
    spring_months = [7, 8, 9]
    fall_months = [10, 11, 12]
    season_months = {}
    for i in range(13):
        if i in winter_months:
            season_months[i] = 0
        if i in summer_months:
            season_months[i] = 1
        if i in spring_months:
            season_months[i] = 2
        if i in fall_months:
            season_months[i] = 3

    # Plot the aggregated crime count wrt every month
    data["month"] = \
        data.apply(lambda row: row['Date'].month, axis=1)
    data["day"] = \
        data.apply(lambda row: row['Date'].day, axis=1)
    data["quarter"] = \
        data.apply(lambda row: season_months[row['month']], axis=1)
    data["week_no"] = \
        data.apply(lambda row:
                   datetime.date(row["Date"].year,
                                 row["Date"].month,
                                 row["Date"].day).isocalendar()[1],
                   axis=1)
    return data


def main_multi_year():
    _path = "/home/srihari/Projects/Crime_analysis/datasets/crime"
    _path = os.path.join(os.getcwd(), "datasets/crime")

    data = pd.DataFrame()
    all_year_data = []

    for year in range(2015, 2018):
        # ------------------------------------------------------------------- #
        # Pull the data
        # ------------------------------------------------------------------- #

        sqldbm = SQLDatabaseManager()

        host = "localhost"
        database = 'crime_data'
        user = 'root'
        password = 'root'
        port = '3306'

        ret = sqldbm.connect(host=host,
                             database=database,
                             username=user,
                             password=password,
                             port=port)

        if ret != 1:
            print(" Closing program ")
            return

        print(sqldbm.get_tables())

        query = "SELECT * FROM crime_" + str(year) + " LIMIT 35000;"
        year_data = sqldbm.execute_query(query=query)

        sqldbm.disconnect()

        all_year_data.append(year_data)

    data = all_year_data[0]
    for ydi in range(1, len(all_year_data)):
        year_data = all_year_data[ydi]
        data = data.append(year_data, ignore_index=True)

    # ------------------------------------------------------------------------ #
    # Work with Single Years
    # ------------------------------------------------------------------------ #
    # Declare class object
    crime_study = CrimeStudy(data=data)

    # crime_study.histogram_study(data, study_sub_crimes=False)

    # crime_study.heatmap_study(data)

    crime_study.time_series_study(data)


def main_single_year():

    _path = "/home/srihari/Projects/Crime_analysis/datasets/crime"
    _path = os.path.join(os.getcwd(), "datasets/crime")

    year = 2017

    # ------------------------------------------------------------------------ #
    # Pull the data
    # ------------------------------------------------------------------------ #

    sqldbm = SQLDatabaseManager()

    host = "localhost"
    database = 'crime_data'
    user = 'root'
    password = 'root'
    port = '3306'

    ret = sqldbm.connect(host=host,
                         database=database,
                         username=user,
                         password=password,
                         port=port)

    if ret != 1:
        print(" Closing program ")
        return

    print(sqldbm.get_tables())

    query = "SELECT * FROM crime_" + str(year) + ";"
    data = sqldbm.execute_query(query=query)

    sqldbm.disconnect()

    data = clean_data(data)

    # ------------------------------------------------------------------------ #
    # Work with Single Years
    # ------------------------------------------------------------------------ #
    # Declare class object
    crime_study = CrimeStudy()

    # crime_study.histogram_study(data)

    # crime_study.heatmap_study(data)

    # crime_study.count_study(data)

    winter_data = data[data["quarter"] == 0]
    summer_data = data[data["quarter"] == 1]
    spring_data = data[data["quarter"] == 2]
    fall_data = data[data["quarter"] == 3]

    # Get the ward-grouped data
    ward_winter_data = group_ward_data(winter_data)
    ward_summer_data = group_ward_data(summer_data)
    ward_spring_data = group_ward_data(spring_data)
    ward_fall_data = group_ward_data(fall_data)

    ward_winter_data["ward"] = ward_winter_data.astype(str)
    ward_summer_data["ward"] = ward_summer_data.astype(str)
    ward_spring_data["ward"] = ward_spring_data.astype(str)
    ward_fall_data["ward"] = ward_fall_data.astype(str)

    max_val = max(max(ward_winter_data["crime_count"]),
                  max(ward_summer_data["crime_count"]),
                  max(ward_spring_data["crime_count"]),
                  max(ward_fall_data["crime_count"]))

    n_steps = 5
    step = int(max_val / n_steps)
    th_scale = list(range(0, int(max_val + step), step))

    # Winter ward
    lats, lons, mag = [], [], []
    for index, row in winter_data.iterrows():
        loc = row["Location"]
        lats.append(float(loc.split(",")[0][1:]))
        lons.append(float(loc.split(",")[1][:-1]))
        mag.append(1)
    crime_study.geo_study(ward_winter_data, _path, "Q1", th_scale,
                          True, lats, lons, mag)

    # Summer ward
    lats, lons, mag = [], [], []
    for index, row in summer_data.iterrows():
        loc = row["Location"]
        lats.append(float(loc.split(",")[0][1:]))
        lons.append(float(loc.split(",")[1][:-1]))
        mag.append(1)
    crime_study.geo_study(ward_summer_data, _path, "Q2", th_scale,
                          True, lats, lons, mag)

    # Spring ward
    lats, lons, mag = [], [], []
    for index, row in spring_data.iterrows():
        loc = row["Location"]
        lats.append(float(loc.split(",")[0][1:]))
        lons.append(float(loc.split(",")[1][:-1]))
        mag.append(1)
    crime_study.geo_study(ward_spring_data, _path, "Q3", th_scale,
                          True, lats, lons, mag)

    # Fall ward
    lats, lons, mag = [], [], []
    for index, row in fall_data.iterrows():
        loc = row["Location"]
        lats.append(float(loc.split(",")[0][1:]))
        lons.append(float(loc.split(",")[1][:-1]))
        mag.append(1)
    crime_study.geo_study(ward_fall_data, _path, "Q4", th_scale,
                          True, lats, lons, mag)


if __name__ == "__main__":

    # main_single_year()
    main_multi_year()

    # Archive
    # for year in range(2001, 2019):
    #
    #     file_name = str(year) + ".csv"
    #
    #     # Load the data
    #     data_extractor = DataExtractor()
    #     data = data_extractor.read_csv(fpath=os.path.join(_path, file_name),
    #                                    nrows_to_read=-1)
    #
    #     print(" Shape :", data.shape)
    #     print(" Columns :")
    #     for c in data.columns:
    #         print("\t", c)
    #
    #     data = clean_data(data)
    #
    #     data = add_date_info(data)
    #
    #     print(" After cleaning")
    #     print(" Shape :", data.shape)
    #     print(" Columns :")
    #     for c in data.columns:
    #         print("\t", c)
    #
    #     data["crime_count"] = 1
    #
    #     # -------------------------------------------------------------------- #
    #     # Push this data into the database
    #     # -------------------------------------------------------------------- #
