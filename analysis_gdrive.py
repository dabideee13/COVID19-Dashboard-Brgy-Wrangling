#!/Users/d.e.magno/Projects/mini/GabrielEngcong/gab/bin/python
# -*- coding: utf-8 -*-
"""Analysis of data in Google Drive"""

import os
import pandas as pd
pd.set_option('display.max_columns', 10)


def main():

    # Define working directory path of raw data
    DIR = '/Users/d.e.magno/Projects/mini/GabrielEngcong/data/processed'
    path = lambda filename: os.path.join(DIR, filename)

    # Define filenames of data
    data = 'gdrive-data.csv'

    # Import gdrive data
    df = pd.read_csv(path(data))
    df2 = pd.read_csv('gdrive-data2.csv')

    df2 = df2.rename(columns={'Unnamed: 0': 'Barangay'})
    print(df2[df2.Barangay == 'Tubod'].sum(axis=1))


if __name__ == '__main__':
    main()