#!/Users/d.e.magno/Projects/mini/GabrielEngcong/gab/bin/python
# -*- coding: utf-8 -*-
"""Analysis of data in Google Drive"""

import os
import datetime as dt
from dfply import *
import pandas as pd


@dfpipe
def new_index(df_: pd.DataFrame) -> pd.DataFrame:
    df = df_.copy(deep=True)
    df.index = df.Date
    df.drop('Date', axis=1, inplace=True)
    return df


def main():

    # Define working directory path of raw data
    DIR = '/Users/d.e.magno/Projects/mini/GabrielEngcong/data/raw'
    path = lambda filename: os.path.join(DIR, filename)

    # Import dashboard data
    df = pd.read_csv(path('dash-data-0411.csv'))

    # Wrangle data
    new_columns = ['CaseNo', 'Age', 'Sex', 'Barangay', 'Type', 'Exposure',
                   'NatureOfSymptoms', 'QuarantineLocation',
                   'DateIdentified', 'Recovered', 'Died']

    # Change column names
    df.columns = new_columns

    # Wrangle IIT dashboard covid data
    df = (df >> 
           mutate(CaseNo = X.CaseNo.apply(lambda x: x.replace(' ', ''))) >>
           mutate(Age = X.Age.fillna(0).apply(int)) >>
           mutate(Date = X.DateIdentified.apply(pd.to_datetime)) >>
           drop(X.DateIdentified) >> 
           new_index)

    df_temp = df.sort_index().reset_index()
    print(df_temp.Barangay.transpose())


    

    # Show dataframe
    #print(df)

if __name__ == '__main__':
    main()

