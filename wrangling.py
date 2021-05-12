#!/Users/d.e.magno/Projects/mini/GabrielEngcong/gab/bin/python
# -*- coding: utf-8 -*-

import os
from dfply import *
import pandas as pd
pd.set_option('display.max_columns', None)


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
    df2['Case No.'] = df2['Case No.'].apply(lambda x: x.replace(' ', ''))


    print(df2)    

    # Show dataframes
    #print(f"{data1}:\n", df1, '\n', '\n', f"{data2}:\n", df2)


if __name__ == '__main__':
    main()