"""
@file_name : DataExtractor.py
@author : Srihari Seshadri
@description : This file does the following operations :
                1. Reads the datafile.csv for getting all info required
                2. Populates a pandas dataframe
            Potential upgrades include
                1. Analysis modules
@date : 11-14-2018
"""

import pandas as pd


class DataExtractor:

    def __init__(self):
        pass

    @staticmethod
    def read_csv(fpath, sep=",", names=None, nrows_to_read=None,
                 na_vals=None):
        """
        Populates a pandas dataframe by reading a csv file or buffer
        :param fpath: file_path of .csv or buffer
        :param sep: Delimiter
        :param names: Column names to use when reading csv
        :param nrows_to_read: number of rows to read from file/buffer
        :param na_vals: list of values in cells that will be considered as NA
        :return: dataframe with data if success. Empty dataframe if failure
        """
        try:
            if nrows_to_read is not None:
                if nrows_to_read < 0:
                    nrows_to_read = None
            df = pd.read_csv(filepath_or_buffer=fpath,
                             sep=sep, names=names,
                             nrows=nrows_to_read,
                             na_values=na_vals)
        except Exception as e:
            print(" Exception thrown while reading CSV file/buffer :", e)
            return pd.DataFrame()
        return df


def main():

    file_path = "C:\\Users\\SSrih\\OneDrive\\UChicago\\DEP\\Project\\data" \
                "\\Crime\\crime_10krows.csv"

    data_extractor = DataExtractor()
    data = data_extractor.read_csv(fpath=file_path)
    if data.empty:
        return
    print(data.head())


if __name__ == "__main__":
    main()
