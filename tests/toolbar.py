import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QAction, QStatusBar, QLabel, QToolBar
)
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt, QSize


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setWindowTitle("Toolbar Sample")
        self.setMinimumSize(QSize(500, 500))

        label = QLabel("Hello")
        label.setAlignment(Qt.AlignCenter)


app = QApplication(sys.argv)
window = MainWindow()
window.show()
app.exec()
