import re
from PyQt5.QtCore import QObject, pyqtSlot, pyqtSignal
from pybtex.database import BibliographyData
from pybtex.database.input import bibtex

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

    def modifiedKeys(self, keyPattern):
        newBib = BibliographyData()

        for bib_id in self._bibdata.entries:
            persons = self._bibdata.entries[bib_id].persons
            fields = self._bibdata.entries[bib_id].fields

            new_bib_id = ''

            for kp in keyPattern:
                if kp:
                    if kp in persons.keys():
                        new_bib_id += ''.join(a.last()[0] for a in persons[kp])
                    elif kp in fields.keys():
                        new_bib_id += ''.join(a for a in fields[kp])

            if new_bib_id:
                new_bib_id = self._cleanLaTeXFromKey(new_bib_id)
                newBib.entries[new_bib_id] = self._bibdata.entries[bib_id]
            else:
                newBib.entries[bib_id] = self._bibdata.entries[bib_id]

        return newBib

    @staticmethod
    def _cleanLaTeXFromKey(key):
        key = re.sub(r'[\\\{\}()"]', '', key)
        key = re.sub(r'[: _]', '-', key)
        return key

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
