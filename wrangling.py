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

    b1 = list(set(list(df1_brgy)))
    b2 = list(set(barangay.to_list()))

    df1 = pd.concat([df1_brgy, df1_], axis=1)

    df1.index = df1.Barangay
    df1 = df1.drop('Barangay', axis=1)
    #print(df1.loc['Abuno'], df1.columns[0])
    
    # Scan through each barangay in gdrive data
    for i, bar in enumerate(df1.index):

        # Cross-check with dashboard data
        if bar in list(set(barangay)):
            
            # Go through each date or column
            for col in df1.columns:

                # Cross-check with dashboard data
                if col in barangay.index.to_list():

                    # Add '1' in that cell
                    df1.loc[bar, col] = 1

    df1.to_csv('gdrive-data.csv')


        #print(f'{i}: ', df1.loc[bar, df1.columns[0]])


if __name__ == '__main__':
    main()
