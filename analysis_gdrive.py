#!/Users/d.e.magno/Projects/mini/GabrielEngcong/gab/bin/python
# -*- coding: utf-8 -*-
"""Analysis of data in Google Drive"""

import os
import pandas as pd


def main():

    # Define working directory path of raw data
    DIR = '/Users/d.e.magno/Projects/mini/GabrielEngcong/data/processed'
    path = lambda filename: os.path.join(DIR, filename)

    # Define filenames of data
    data = 'gdrive-data.csv'

    # Import gdrive data
    df = pd.read_csv(path(data))

    # Show dataframe
    print(df)


if __name__ == '__main__':
    main()