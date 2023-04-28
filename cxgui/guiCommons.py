
from PyQt5.QtWidgets import QWidget
from PyQt5.QtGui import QColor, QPalette


class ColoredWidget(QWidget):
    def __init__(self, color: str):
        super().__init__()
        self.setAutoFillBackground(True)
        palette = self.palette()
        palette.setColor(QPalette.Window, QColor(color))
        palette.setColor(QPalette.WindowText, QColor('white'))
        self.setPalette(palette)
