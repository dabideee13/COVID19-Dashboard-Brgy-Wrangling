#!/Users/d.e.magno/Projects/mini/GabrielEngcong/gab/bin/python
# -*- coding: utf-8 -*-

import os
import datetime as dt
from dfply import *
import pandas as pd
#pd.set_option('display.max_columns', None)


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

    # Define filenames of data
    data1 = 'data.csv'
    data2 = 'dash-data-0411.csv'
    
    # Import dataframes
    df1 = pd.read_csv(path(data1))
    df2 = pd.read_csv(path(data2))

    # Wrangle df2; dashboard data
    #df2['Case No.'] = df2['Case No.'].apply(lambda x: x.replace(' ', ''))

    new_columns = ['CaseNo', 'Age', 'Sex', 'Barangay', 'Type', 'Exposure',
                   'NatureOfSymptoms', 'QuarantineLocation',
                   'DateIdentified', 'Recovered', 'Died']

    # Change column names of df2
    df2.columns = new_columns

    # Wrangle IIT dashboard covid data
    df2 = (df2 >> 
           mutate(CaseNo = X.CaseNo.apply(lambda x: x.replace(' ', ''))) >>
           mutate(Age = X.Age.fillna(0).apply(int)) >>
           mutate(Date = X.DateIdentified.apply(pd.to_datetime)) >>
           drop(X.DateIdentified) >> 
           new_index)

    # Subset only 'Barangay'
    barangay = df2 >> select(X.Barangay)
    
    # NOTE: 38 barangays only in barangay dataframe

    # Wrangle the other data to be updated
    df1 = df1.rename(columns = {df1.columns[0]: 'Barangay'})

    # Separate barangay from the dates
    df1_brgy = df1.iloc[:, 0]
    df1_ = df1.iloc[:, 1:]
    df1_.columns = pd.to_datetime(df1_.columns)

    barangay = barangay.Barangay.replace({
        'Bagong Silang': 'BagongSilang',
        'Buruun': 'Buru-un',
        'Del Carmen': 'DelCarmen',
        'Lanao del sur': 'Lanao Del Sur',
        'Maria Cristina': 'MariaCristina',
        'Pala-o': 'Palao',
        'Puga-an': 'Pugaan',
        'San Miguel': 'SanMiguel',
        'San Roque': 'SanRoque',
        'Sta. Elena': 'SantaElena',
        'Sta. Filomena': 'SantaFilomena',
        'Sto. Rosario': 'SantoRosario',
        'Tomas Cabili': 'TomasCabili',
        'Ubaldo Laya': 'UbaldoLaya',
        'Upper Hinaplanon': 'UpperHinaplanon',
        'Villaverde': 'VillaVerde',
        'Upper Tominobo': 'TominoboUpper'
        }
    )

    df_ = barangay.sort_index().reset_index()

    # Separate 'Date' and 'Barangay'
    date = sorted(list(set(df_.Date)))
    bar = sorted(list(set(df_.Barangay)))

    df_blank = pd.DataFrame(columns=date, index=bar).fillna(0)

    df1 = pd.concat([df1_brgy, df1_], axis=1)

    df1.index = df1.Barangay
    df1 = df1.drop('Barangay', axis=1)
    
    # Mapping for gdrive-data.csv
    for bar in df1.index:
        if bar in set(barangay):
            for col in df1.columns:
                dates = list(barangay[barangay == bar].index)
                if col in dates:
                    counts = list()
                    for date in dates:
                        if date == col:
                            counts.append(date)
                            df1.loc[bar, col] = len(counts)
    df1.to_csv('gdrive-data.csv')

    # Mapping for gdrive-data2.csv
    # Loop through each barangay (index)
    for bar in df_blank.index:

        # Loop through each date (column)
        for col in df_blank.columns:

            # Use dates from dashboard data
            dates = list(barangay[barangay == bar].index)

            # If current column (a date) can be found in dashboard data,
            # loop through it and look for occurences.
            if col in dates:

                # Create list to store dates
                counts = list()

                for date in dates:
                    if date == col:

                        # If dates has the same value in dashboard data,
                        # store in list to get counts
                        counts.append(date)

                        # Let the value of this cell be equal to the
                        # number of its occurences
                        df_blank.loc[bar, col] = len(counts)
    
    #print(df_blank)
    # Export to csv 
    df_blank.to_csv('gdrive-data2.csv')
            

if __name__ == '__main__':
    main()
