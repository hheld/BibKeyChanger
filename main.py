from PyQt4.QtGui import QApplication
import sys
from UI.MainWindow import MainWindow

app = QApplication(sys.argv)

mw = MainWindow()
mw.show()

sys.exit(app.exec_())