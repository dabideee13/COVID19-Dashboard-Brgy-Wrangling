# -*- coding: utf-8 -*-

from pathlib import Path

from dfply import *
import pandas as pd

from logger import stream_logger


@dfpipe
def new_index(df_: pd.DataFrame) -> pd.DataFrame:
    df = df_.copy(deep=True)
    df.index = df.Date
    df.drop('Date', axis=1, inplace=True)
    return df


def main():

    # Set path to data
    in_path = Path('data/raw')
    out_path = Path('data/processed')
    filename = (
        list(
            Path.joinpath(
                Path.cwd(),
                in_path
            )
            .glob('./*.csv')
        )[0]
    )

    df = pd.read_csv(filename)
    stream_logger.info('DONE: Importing DataFrame')

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
    stream_logger.info(
        'DONE: Dropping unnecessary columns'
        'and changing column names.'
    )

    df = (
        df >>
        mutate(Date = X.DateIdentified.apply(pd.to_datetime)) >>
        drop(X.DateIdentified) >>
        new_index
    )
    stream_logger.info('DONE: Wrangling `DateIdentified`')

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
    stream_logger.info('DONE: Wrangling barangay')

    # Separate `Date` and `Barangay`
    date = sorted(list(set(df.Date)))
    bar = sorted(list(set(df.Barangay.apply(str))))

    df = pd.DataFrame(columns=date, index=bar).fillna(0)
    stream_logger.info('DONE: Filling missing values with 0')

    for bar in df.index:
        for col in df.columns:
            dates = list(barangay[barangay == bar].index)

            if col in dates:

                counts = list()

                for date in dates:
                    if date == col:
                        counts.append(date)

                        df.loc[bar, col] = len(counts)
    stream_logger.info('DONE: Main loop')

    df.to_csv(
        Path.joinpath(
            Path.cwd(),
            out_path,
            filename.stem + '_processed' + filename.suffix
        )
    )
    stream_logger.info('DONE: Exporting file')


if __name__ == '__main__':
    main()
