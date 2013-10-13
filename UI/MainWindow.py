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
        self._keyFields = []

        self.ui = uic.loadUi('UI/MainWindow.ui', self)
        self.ui.actionOpen.triggered.connect(self.onActionOpenFile)

        self._modelFields = QStringListModel()
        self.ui.lv_fields.setModel(self._modelFields)
        self.ui.lv_fields.selectedIndicesChanged.connect(self.onFieldSelectionChanged)

        self.ui.pb_clearSelection.clicked.connect(self.onButtonClearSelectionClicked)
        self.ui.pb_preview.clicked.connect(self.onButtonPreviewClicked)

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
        if bibdata:
            writer = Writer()
            bibdata_str = io.StringIO()
            writer.write_stream(bibdata, bibdata_str)
            self.ui.tb_preview.setText(bibdata_str.getvalue())

    @pyqtSlot(set)
    def onFieldDataAvailable(self, fieldData):
        existingList = self._modelFields.stringList()

        existingList.extend([fd for fd in fieldData])

        self._modelFields.setStringList(existingList)

    @pyqtSlot(set)
    def onPersonDataAvailable(self, personData):
        existingList = self._modelFields.stringList()

        existingList.extend([pd for pd in personData])

        self._modelFields.setStringList(existingList)

    @pyqtSlot(list)
    def onFieldSelectionChanged(self, listOfFields):
        self._keyFields = listOfFields
        self.ui.le_keyPattern.setText('---'.join(self._keyFields))

    @pyqtSlot()
    def onButtonClearSelectionClicked(self):
        self.ui.lv_fields.clearSelection()

        if self._bibReader:
            self.onBibDataAvailable(self._bibReader.bibdata)

    @pyqtSlot()
    def onButtonPreviewClicked(self):
        if self._bibReader:
            self.onBibDataAvailable(self._bibReader.modifiedKeys(self.ui.le_keyPattern.text().split('---')))