
import pandas as pd


def group_ward_data(data):

    ward_data = pd.DataFrame(data['Ward'].value_counts().astype(float))
    ward_data = ward_data.reset_index()
    ward_data.columns = ['ward', 'crime_count']
    return ward_data

def clean_data(data):

    # What all columns do we want to drop?
    # drop_col_list = ["Case Number",
    #                  "Updated On"]
    #
    # data.drop(labels=drop_col_list, axis=1, inplace=True)

    # Drop rows with NA
    data.dropna(inplace=True)

    # Check and drop for duplicates
    print("Number of duplicate IDs ", data.ID.duplicated().sum())
    # Drop them
    data.drop_duplicates(subset=None, keep='first', inplace=True)

    # getting rid of decimal in
    # District, Ward, Community Area
    # and turning them into string type.
    data[['District', 'Ward', 'Community Area']] = \
        data[['District', 'Ward', 'Community Area']].astype('int')
    data[['District', 'Ward', 'Community Area']] = \
        data[['District', 'Ward', 'Community Area']].astype('str')

    return data
