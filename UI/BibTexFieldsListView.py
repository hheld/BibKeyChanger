from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QListView


class BibTexFieldsListView(QListView):
    selectedIndicesChanged = pyqtSignal(list)

    def __init__(self, parent):
        super().__init__(parent)

    def selectionChanged(self, selected, deselected):
        selectedIndices = self.selectedIndexes()
        self.selectedIndicesChanged.emit([field.data() for field in selectedIndices])
