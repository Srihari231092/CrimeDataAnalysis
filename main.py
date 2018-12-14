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
from CrimeStudy import CrimeStudy
from VizTools import *

# Week to start on Sunday
calendar.setfirstweekday(6)


def get_week_of_month(year, month, day):
    x = np.array(calendar.monthcalendar(year, month))
    week_of_month = np.where(x == day)[0][0] + 1
    return week_of_month


def clean_data(data):

    # Convert the Date column into a datetime type
    data['Date'] = pd.to_datetime(data['Date'])
    # data.sort_values(by='Date', inplace=True)

    # What all columns do we want to drop?
    drop_col_list = ["Case Number",
                     "Latitude", "Longitude",
                     "Updated On"]

    data.drop(labels=drop_col_list, axis=1, inplace=True)

    # Drop rows with NA
    data.dropna(inplace=True)

    # Check and drop for duplicates
    print("Number of duplicate IDs ", data.ID.duplicated().sum())
    # Drop them
    data.drop_duplicates(subset=None, keep='first', inplace=True)

    # getting rid of decimal in District, Ward and Community Area and turning them into string type.
    data[['District', 'Ward', 'Community Area']] = data[['District', 'Ward', 'Community Area']].astype('int')
    data[['District', 'Ward', 'Community Area']] = data[['District', 'Ward', 'Community Area']].astype('str')

    return data


def add_season_info(data):
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
    data["month"] = data.apply(lambda row: row['Date'].month, axis=1)
    data["crime_count"] = 1
    data["season"] = data.apply(lambda row: season_months[row['month']], axis=1)
    data["week_no"] = data.apply(lambda row:
                                 datetime.date(row["Date"].year, row["Date"].month, row["Date"].day).isocalendar()[1],
                                 axis=1)
    return data


def main():

    _path = "/home/srihari/Projects/Crime_analysis/datasets/crime"
    file_name = "2017_2018.csv"

    # Load the data
    data_extractor = DataExtractor()
    data = data_extractor.read_csv(fpath=os.path.join(_path, file_name),
                                   nrows_to_read=-1)

    print(" Shape :", data.shape)
    print(" Columns :")
    for c in data.columns:
        print("\t", c)

    data = clean_data(data)

    data = add_season_info(data)

    # Declare class object
    crime_study = CrimeStudy(data=data)

    # crime_study.histogram_study(data)

    # crime_study.heatmap_study(data)

    # crime_study.count_study(data)

    # winter_data = data[data["season"] == 0]
    # crime_study.geo_study(winter_data, _path, "winter")
    #
    # summer_data = data[data["season"] == 1]
    # crime_study.geo_study(summer_data, _path, "summer")
    #
    # spring_data = data[data["season"] == 2]
    # crime_study.geo_study(spring_data, _path, "spring")
    #
    # fall_data = data[data["season"] == 3]
    # crime_study.geo_study(fall_data, _path, "fall")

    # for m in range(1, 13):
    #     month_data = data[data["month"] == m]
    #     crime_study.geo_study(month_data, _path, str(m))

    unique_weeks = data["week_no"].unique()

    print(unique_weeks)

    for week in unique_weeks:
        week_data = data[data["week_no"] == week]
        crime_study.geo_study(week_data, _path, str(week))


if __name__ == "__main__":

    main()
