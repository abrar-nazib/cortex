# fmt: off
from PyQt5.QtWidgets import QWidget, QHBoxLayout, QLabel, QDoubleSpinBox, QVBoxLayout, QDialog, QTabWidget, QDialogButtonBox
from PyQt5.QtGui import QPalette, QColor
from PyQt5.QtCore import QSize
import sys
import os

# For removing import error
fpath = os.path.join(os.path.dirname(__file__), '..')
sys.path.append(fpath)
# ------

from cortex import CxConfManager
from cxgui import guiCommons

# fmt: on


class SettingsOption(QWidget):
    def __init__(self, name: str, value: float):
        super().__init__()
        # Selecting the color
        self.fgColor = CxConfManager.themeConf["Dark"]["toolbar"]
        self.setAutoFillBackground(True)
        palette = self.palette()
        palette.setColor(QPalette.Window, QColor(self.fgColor))
        self.setPalette(palette)

        layout = QHBoxLayout()
        label = QLabel(name)
        input = QDoubleSpinBox()
        input.setMinimumHeight(30)
        input.setRange(-500, 500)
        input.setSingleStep(0.1)
        input.setValue(value)
        layout.addWidget(label, 50)
        layout.addWidget(input, 50)
        self.setLayout(layout)


class ServoSettings(QWidget):
    def __init__(self):
        super().__init__()

        # Selecting The Color
        self.fgColor = CxConfManager.themeConf["Dark"]["toolbar"]
        self.setAutoFillBackground(True)
        palette = self.palette()
        palette.setColor(QPalette.Window, QColor(self.fgColor))
        self.setPalette(palette)
        self.generateOptions()

    def generateOptions(self):
        layout = QVBoxLayout()

        for confkey in CxConfManager.servoConf:
            obj = CxConfManager.servoConf[confkey]
            for key in obj:
                # print(f"Servo-{confkey} {key} {obj[key]}")
                layout.addWidget(SettingsOption(
                    f"Servo-{confkey} {key.capitalize()}", obj[key]))
        self.setLayout(layout)


class SettingsDialog(QDialog):
    # Using parent makes the dialog to get created inside parent's border
    def __init__(self, parent=None):
        super().__init__(parent)

        # Set window Title
        self.setWindowTitle("Settings")
        self.setMinimumSize(QSize(500, 900))

        # Set Layout and Colors
        self.bgColor = CxConfManager.themeConf["Dark"]["background"]
        self.fgColor = CxConfManager.themeConf["Dark"]["toolbar"]

        self.layout = QVBoxLayout()
        self.setAutoFillBackground(True)
        palette = self.palette()
        palette.setColor(QPalette.Window, QColor(self.bgColor))
        # palette.setColor(QPalette.WindowText, QColor("white"))
        self.setPalette(palette)

        # Set a minimum window size

        # Set tab widget
        tabs = QTabWidget()
        tabs.setTabPosition(QTabWidget.North)
        tabs.setMovable(False)
        # tabs.addTab(ColoredWidget(self.fgColor), "Servo")
        tabs.addTab(ServoSettings(), "Servo")
        tabs.addTab(guiCommons.ColoredWidget(self.fgColor), "Camera")
        tabs.addTab(guiCommons.ColoredWidget(self.fgColor), "Hardware")
        tabs.setContentsMargins(0, 0, 0, 30)
        self.layout.addWidget(tabs)

        # Multiple set of dialogue box button by using "|"
        QBtn = QDialogButtonBox.Save | QDialogButtonBox.Close
        self.buttonBox = QDialogButtonBox(QBtn)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)
        self.layout.addWidget(self.buttonBox)
        self.setLayout(self.layout)

    def accept(self):
        print("Done")
        self.done(1)
