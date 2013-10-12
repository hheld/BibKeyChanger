from PyQt4.QtCore import QObject, pyqtSlot, pyqtSignal
from pybtex.database import BibliographyData
from pybtex.database.input import bibtex
#from pybtex.database.output.bibtex import Writer

class BibTexReader(QObject):
    bibdataAvailable = pyqtSignal(BibliographyData)
    fieldsAvailable = pyqtSignal(set)
    personsAvailable = pyqtSignal(set)

    def __init__(self, parent, bibtexfile):
        super(BibTexReader, self).__init__(parent)

        self._bibtexfile = bibtexfile
        self._availableFields = set()
        self._availablePersons = set()
        self._bibdata = None

    @pyqtSlot()
    def read(self):
        parser = bibtex.Parser()
        self._bibdata = parser.parse_file(self._bibtexfile)

        for bib_id in self._bibdata.entries:
            p = self._bibdata.entries[bib_id].persons
            b = self._bibdata.entries[bib_id].fields
            self._availableFields |= b.keys()
            self._availablePersons |= p.keys()

        self.bibdataAvailable.emit(self._bibdata)
        self.fieldsAvailable.emit(self._availableFields)
        self.personsAvailable.emit(self._availablePersons)

    @property
    def bibdata(self):
        return self._bibdata

    @property
    def fields(self):
        return self._availableFields

    @property
    def persons(self):
        return self._availablePersons

    @property
    def bibtexfile(self):
        return self._bibtexfile
