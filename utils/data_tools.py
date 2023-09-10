import pandas as pd
import os, sys
import re
import sqlite3
import pandas as pd

"""
In this file we'll need to build out the following:
- A method to bind the data together
- A method to parse/load the data

"""
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def make_local_sqlite_db(dataframes: dict):
    cnx = sqlite3.connect(':memory:')
    for key, df in dataframes.items():
        df.to_sql(key, cnx)
    return cnx


def load_data():
    data_1 = pd.read_csv('data/population_estimations.csv')
    data_2 = pd.read_csv('data/school_enrollment_data.csv')
    data_3 = pd.read_csv('data/detailed_demographics.csv')
    return {
        "data/population_estimations.csv": data_1,
        "data/school_enrollment_data.csv": data_2,
        "data/detailed_demographics.csv": data_3
    }


def american_community_to_csv():
    # drop rows with only NA
    # df = df.dropna(how='all')
    # Load the Excel file
    file_path = '../data/2021_american_community_survey_by_county_sample.xlsx'
    df = pd.read_excel(file_path, header=[0,1, 2, 3, 4])  # adjust header levels based on your Excel structure
    new_cols = []
    for col in df.columns:
        cols = [c.replace(' ', '_') for c in col if ('Unnamed' not in c) and (c != '') and (c != ' ') and (c != '\\')]
        new_column = '_'.join(cols)
        new_cols.append(new_column)
    df.columns = new_cols

    # Write to a CSV file
    output_csv_path = '../data/population_estimations.csv'
    df.to_csv(output_csv_path, index=False)


if __name__ == "__main__":

    american_community_to_csv()

