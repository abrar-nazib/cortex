import sys

from PyQt5.QtCore import Qt, QSize
from PyQt5.QtWidgets import (
    QMainWindow, QApplication, QSlider, QDial, QWidget, QVBoxLayout, QHBoxLayout
)
from PyQt5.QtGui import QPixmap, QPalette, QColor


class Color(QWidget):
    def __init__(self, color: str):
        super(Color, self).__init__()
        self.setAutoFillBackground(True)
        palette = self.palette()
        palette.setColor(QPalette.Window, QColor(color))
        self.setPalette(palette)


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()


app = QApplication(sys.argv)
window = MainWindow()
window.show()
app.exec()
