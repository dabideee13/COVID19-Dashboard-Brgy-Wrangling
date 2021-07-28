import sys
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication, QFileDialog, QListWidgetItem, QMessageBox
from PyQt5.uic import loadUi
from pathlib import Path
from dfply import *
import pandas as pd

class Wrangler(QtWidgets.QMainWindow):
    def __init__(self):
        super(Wrangler, self).__init__()
        loadUi("ui/mainwin.ui", self)

        width  = self.frameGeometry().width()
        height = self.frameGeometry().height()

        self.setFixedSize(width, height)
        self.configureWidgets()

    def configureWidgets(self):
        self.browsefileButton.clicked.connect(self.browsefileClicked)
        self.wrangleButton.clicked.connect(self.wrangleClicked)


    def browsefileClicked(self):
        self.wrangleButton.setText('Wrangle')
        self.listWidget.clear()

        self.file_name = QFileDialog.getOpenFileName(self, "Open File", "", "CSV(*.csv)")
        if self.file_name:
            self.filename = self.file_name[0]
            self.lineEdit.setText(self.filename)


    def wrangleClicked(self):

        self.out_path = Path('data/processed')
        try:
            self.df = pd.read_csv(self.filename)
        except:
            QMessageBox.information(self, "Wrangle.", "Please use a valid file path.")
            return

        QListWidgetItem('DONE: Importing DataFrame', self.listWidget)

        self.to_drop  = [
            'Contact Number',
            'Zone/Purok',
            'Street',
            'City',
            'Remarks',
            'Province',
        ]

        self.new_order = [
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

        self.new_columns = [
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
        self.df         = self.df.drop(self.to_drop, axis=1)[self.new_order]
        self.df.columns = self.new_columns

        QListWidgetItem('DONE: Dropping unnecessary columns and changing column names.', self.listWidget)

        self.df = (
                self.df >> mutate(Date=X.DateIdentified.apply(pd.to_datetime)) >>
                drop(X.DateIdentified) >> self.new_index()
        )

        QListWidgetItem('DONE: Wrangling `Date Identified`', self.listWidget)

        # subset only `Barangay`
        self.barangay = self.df >> select(X.Barangay)

        self.barangay = self.barangay.Barangay.replace(
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

        self.df = self.barangay.sort_index().reset_index()
        QListWidgetItem('DONE: Wrangling barangay', self.listWidget)

        # separate `Date` and `Barangay`
        self.date = sorted(list(set(self.df.Date)))
        self.bar = sorted(list(set(self.df.Barangay.apply(str))))

        self.df = pd.DataFrame(columns=self.date, index=self.bar).fillna(0)
        QListWidgetItem('DONE: Filling missing values with 0', self.listWidget)

        for bar in self.df.index:
            for col in self.df.columns:
                dates = list(self.barangay[self.barangay == bar].index)

                if col in dates:

                    counts = list()

                    for date in dates:
                        if date == col:
                            counts.append(date)

                            self.df.loc[bar, col] = len(counts)

        QListWidgetItem('DONE: Main loop', self.listWidget)

        self.df.to_csv(
            Path.joinpath(
                Path.cwd(),
                self.out_path,
                Path(self.filename).stem + '_processed' + Path(self.filename).suffix
            )
        )
        QListWidgetItem('DONE: Exporting file', self.listWidget)



    @dfpipe
    def new_index(df_: pd.DataFrame) -> pd.DataFrame:

        df       = df_.copy(deep=True)
        df.index = df.Date

        df.drop('Date', axis=1, inplace=True)
        return df




app = QApplication(sys.argv)
window = Wrangler()
window.show()
sys.exit(app.exec_())