import os
import sys
from cxgui import mainWindow
from PyQt5.QtWidgets import QApplication

# for removing import error
# fpath = os.path.join(os.path.dirname(__file__), '.')
# sys.path.append(fpath

app = QApplication(sys.argv)

window = mainWindow.MainWindow()
window.showMaximized()

app.exec()
