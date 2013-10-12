from PyQt5.QtWidgets import QApplication
import sys
from UI.MainWindow import MainWindow

app = QApplication(sys.argv)

mw = MainWindow()
mw.show()

sys.exit(app.exec_())
