from PyQt5 import uic
from PyQt5.QtCore import pyqtSlot, QStringListModel
from PyQt5.QtWidgets import QMainWindow, QFileDialog
import io
from pybtex.database import BibliographyData
from BibTexUtils import BibTexReader
from pybtex.database.output.bibtex import Writer


class MainWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)

        self._bibReader = None

        self.ui = uic.loadUi('UI/MainWindow.ui', self)
        self.ui.actionOpen.triggered.connect(self.onActionOpenFile)

        self._modelFields = QStringListModel()
        self.ui.lv_fields.setModel(self._modelFields)

        self._modelPersons = QStringListModel()
        self.ui.lv_persons.setModel(self._modelPersons)

    @pyqtSlot()
    def onActionOpenFile(self):
        selectedFile, filter = QFileDialog.getOpenFileName(self, 'Open BibTex file', '', 'BibTex files (*.bib)')

        if selectedFile:
            self._bibReader = BibTexReader(self, selectedFile)

            self._bibReader.bibdataAvailable.connect(self.onBibDataAvailable)
            self._bibReader.fieldsAvailable.connect(self.onFieldDataAvailable)
            self._bibReader.personsAvailable.connect(self.onPersonDataAvailable)

            self._bibReader.read()

    @pyqtSlot(BibliographyData)
    def onBibDataAvailable(self, bibdata):
        writer = Writer()
        bibdata_str = io.StringIO()
        writer.write_stream(bibdata, bibdata_str)
        self.ui.tb_preview.setText(bibdata_str.getvalue())

    @pyqtSlot(set)
    def onFieldDataAvailable(self, fieldData):
        self._modelFields.setStringList([fd for fd in fieldData])

    @pyqtSlot(set)
    def onPersonDataAvailable(self, personData):
        self._modelPersons.setStringList([pd for pd in personData])
