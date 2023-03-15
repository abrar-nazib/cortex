import sys

from PyQt5.QtCore import Qt, QSize
from PyQt5.QtWidgets import (QMainWindow, QApplication, QLabel, QCheckBox)
from PyQt5.QtGui import QPixmap


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Yo")

        self.setMinimumSize(QSize(200, 200))

        cbox = QCheckBox()

        cbox.setCheckState(Qt.Checked)

        cbox.stateChanged.connect(self.show_state)
        self.setCentralWidget(cbox)

    def show_state(self, s):
        print(s)
        print(Qt.Checked)


app = QApplication(sys.argv)
window = MainWindow()
window.show()
app.exec()
