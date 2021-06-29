# -*- coding: utf-8 -*-

import time
from pathlib import Path

from dfply import *
import pandas as pd


@dfpipe
def new_index(df_: pd.DataFrame) -> pd.DataFrame:
    df = df_.copy(deep=True)
    df.index = df.Date
    df.drop('Date', axis=1, inplace=True)
    return df


def main():

    # Introduction
    print("Enter full path and filename of data: ")
    print(r"Example: C:\Users\User\Desktop\data_export_2021-06-28.csv", "\n")
    time.sleep(5)

    # Set path names
    '''
    while True:
        try:
            in_file = Path(input("Enter full path and filename of data: "))
            out_file = in_file.stem + "_processed" + in_file.suffix
            break
        except FileNotFoundError:
            continue
    '''
    in_file = Path(r"C:\Users\User\Desktop\data_export_2021-06-28.csv")
    out_file = in_file.stem + "_processed" + in_file.suffix

    print(f"\nImporting data: {in_file}")
    df = pd.read_csv(in_file)

    print("Wrangling data")
    to_drop = [
        'Contact Number',
        'Zone/Purok',
        'Street',
        'City',
        'Remarks',
        'Province',
        'Reinfected',
        'Added By',
        'Date Added',
        'Updated By',
        'Date Updated'
    ]

    new_order = [
        'Case Number',
        'Age',
        'Sex',
        'Barangay',
        'Case Type',
        'Exposure',
        'Symptom Nature',
        'Quarantine Location',
        'Date Identified',
        'Recovered',
        'Died'
    ]

    new_columns = [
        'CaseNo',
        'Age',
        'Sex',
        'Barangay',
        'Type',
        'Exposure',
        'NatureOfSymptoms',
        'QuarantineLocation',
        'DateIdentified',
        'Recovered',
        'Died'
    ]

    # Drop, reorder, and change column names
    df = df.drop(to_drop, axis=1)[new_order]
    df.columns = new_columns

    df = (
        df >>
        mutate(Date = X.DateIdentified.apply(pd.to_datetime)) >>
        drop(X.DateIdentified) >>
        new_index
    )

    # Subset only `Barangay`
    barangay = df >> select(X.Barangay)

    barangay = barangay.Barangay.replace(
        {
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

    df = barangay.sort_index().reset_index()

    # Separate `Date` and `Barangay`
    date = sorted(list(set(df.Date)))
    bar = sorted(list(set(df.Barangay.apply(str))))

    df = pd.DataFrame(columns=date, index=bar).fillna(0)

    for bar in df.index:
        for col in df.columns:
            dates = list(barangay[barangay == bar].index)

            if col in dates:

                counts = list()

                for date in dates:
                    if date == col:
                        counts.append(date)

                        df.loc[bar, col] = len(counts)

    df = df.drop('nan', axis=0)

    print("Exporting DataFrame to csv file")

    df.to_csv(
        Path.joinpath(
            in_file.parent,
            out_file
        )
    )

    print("Done. \n")
    print(f"Filename: {out_file}")
    print(f"Location: {in_file.parent}")


if __name__ == '__main__':
    main()
