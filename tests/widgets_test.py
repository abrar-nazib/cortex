import sys

from PyQt5.QtCore import Qt, QSize
from PyQt5.QtWidgets import (QMainWindow, QApplication, QLabel)
from PyQt5.QtGui import QPixmap


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Yo")

        # self.setMinimumSize(QSize(400, 300))

        # label = QLabel("Label Text")
        # font = label.font()
        # font.setPointSizeF(30.3)
        # label.setFont(font)
        label = QLabel()
        label.setPixmap(QPixmap('../cortex.ico'))
        label.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)

        self.setCentralWidget(label)


app = QApplication(sys.argv)
window = MainWindow()
window.show()
app.exec()
