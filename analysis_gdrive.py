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

    # Create new dataframe for totals
    df_new = pd.DataFrame()

    #print(df_new)
    
    # Show dataframe
    print(df[df['Barangay'] == 'Abuno'].to_list())


if __name__ == '__main__':
    main()