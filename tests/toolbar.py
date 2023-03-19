import sys
import os

from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QAction, QStatusBar, QLabel, QToolBar
)
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt, QSize


basedir = os.path.dirname(__file__)
hearticonpath = os.path.join(basedir, '../icons/heart.png')
darkmodeiconpath = os.path.join(basedir, '../icons/dark-mode.png')


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setWindowTitle("Toolbar Sample")
        self.setMinimumSize(QSize(500, 500))

        label = QLabel("Hello")
        label.setAlignment(Qt.AlignCenter)
        self.setCentralWidget(label)

        toolbar = QToolBar("My Main ToolBar")
        self.addToolBar(toolbar)

        # button_action = QAction("Button", self)  # For text based button
        button_action = QAction(QIcon(darkmodeiconpath), "dark-mode", self)
        # Sets the status text. This works as a helping tool for the user
        button_action.setStatusTip("This is a button")
        button_action.triggered.connect(self.click_handle)
        # To make the status bar button checkable
        button_action.setCheckable(True)
        toolbar.addAction(button_action)

        # Status bar shows the statustip in the bottom of the screen
        self.setStatusBar(QStatusBar(self))

    def click_handle(self, s):
        print(s)


app = QApplication(sys.argv)
window = MainWindow()
window.show()
app.exec()
