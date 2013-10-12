from PyQt4 import uic
from PyQt4.QtCore import pyqtSlot, QUrl
from PyQt4.QtGui import QMainWindow, QFileDialog


class MainWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.ui = uic.loadUi('UI/MainWindow.ui', self)
        self.ui.actionOpen.triggered.connect(self.onActionOpenFile)

    @pyqtSlot()
    def onActionOpenFile(self):
        selectedFile = QFileDialog.getOpenFileName(self, 'Open BibTex file', '', 'BibTex files (*.bib)')

        if selectedFile:
            print('You selected file \'%s\'.' % selectedFile)

#from BibTexUtils import BibTexReader

#reader = BibTexReader(None, '/home/harry/Documents/Articles/library.bib')

#reader.read()
#print(reader.bibdata)
#print(reader.fields)
#print(reader.persons)
#print(reader.bibtexfile)
