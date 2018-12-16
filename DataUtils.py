
import pandas as pd


def group_ward_data(data):

    ward_data = pd.DataFrame(data['Ward'].value_counts().astype(float))
    ward_data = ward_data.reset_index()
    ward_data.columns = ['ward', 'crime_count']
    return ward_data
