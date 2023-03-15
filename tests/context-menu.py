import sys
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtWidgets import QAction, QApplication, QLabel, QMainWindow, QMenu
from PyQt5 import QtGui


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Context Menu Test")
        self.setMinimumSize(QSize(400, 300))

    def contextMenuEvent(self, event: QtGui.QContextMenuEvent) -> None:
        context = QMenu(self)
        context.addAction(QAction("Test1", self))
        context.addAction(QAction("Test2", self))
        context.exec(event.globalPos())


app = QApplication(sys.argv)

window = MainWindow()
window.show()

app.exec()
