import sys
import os

from cortex import CxConfManager

from PyQt5.QtCore import Qt, QSize
from PyQt5.QtWidgets import (
    QApplication,
    QHBoxLayout,
    QLabel,
    QMainWindow,
    QPushButton,
    QStackedLayout,
    QVBoxLayout,
    QWidget,
    QTabWidget,
    QToolBar,
    QAction,
    QStatusBar,
    QDialog,
    QDialogButtonBox,
    QLineEdit,
    QDoubleSpinBox,
)
from PyQt5.QtGui import QPalette, QColor, QIcon, QCursor


class ColoredWidget(QWidget):
    def __init__(self, color: str):
        super().__init__()
        self.setAutoFillBackground(True)
        palette = self.palette()
        palette.setColor(QPalette.Window, QColor(color))
        self.setPalette(palette)


class VideoFeed(QWidget):
    def __init__(self):
        pass


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

        # layout.addWidget(SettingsOption("Servo1 Correction"))
        # layout.addWidget(SettingsOption("Servo1 Min"))
        # layout.addWidget(SettingsOption("Servo1 Max"))

        # layout.addWidget(SettingsOption("Servo2 Home"))
        # layout.addWidget(SettingsOption("Servo2 Correction"))
        # layout.addWidget(SettingsOption("Servo2 Min"))
        # layout.addWidget(SettingsOption("Servo2 Max"))
        for confkey in CxConfManager.servoConf:
            obj = CxConfManager.servoConf[confkey]
            for key in obj:
                print(f"Servo-{confkey} {key} {obj[key]}")
                layout.addWidget(SettingsOption(
                    f"Servo-{confkey} {key}", obj[key]))
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
        tabs.addTab(ColoredWidget(self.fgColor), "Camera")
        tabs.addTab(ColoredWidget(self.fgColor), "Hardware")
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


class WindowLayout(QWidget):
    """Window for manual control of the robot

    Args:
        QWidget (_type_): Modifies Qwidget
    """

    def __init__(self):
        super().__init__()
        self.backgroundColor = CxConfManager.themeConf["Dark"]["background"]
        self.foregroundColor = CxConfManager.themeConf["Dark"]["foreground"]

        # Setting up background color
        self.setAutoFillBackground(True)
        palette = self.palette()
        palette.setColor(QPalette.Window, QColor(self.backgroundColor))
        self.setPalette(palette)

        # Creating the layouts
        containerLayout = QHBoxLayout()
        camLayout = QVBoxLayout()
        simLayout = QVBoxLayout()
        optionsLayout = QVBoxLayout()

        # Container layout Organization
        containerLayout.addLayout(optionsLayout, 30)
        containerLayout.addLayout(camLayout, 35)
        containerLayout.addLayout(simLayout, 35)
        containerLayout.setSpacing(10)
        containerLayout.setContentsMargins(10, 10, 10, 10)
        # Cam Layout Organization
        camwidget = ColoredWidget(self.foregroundColor)
        camwidget.setCursor(Qt.PointingHandCursor)

        camLayout.addWidget(camwidget, 75)
        camLayout.addWidget(ColoredWidget(self.foregroundColor), 25)

        # Option Layout Organization
        optionsLayout.addWidget(ColoredWidget(self.foregroundColor), 70)
        optionsLayout.addWidget(ColoredWidget(self.foregroundColor), 20)

        # Simulation Layout Organization
        simLayout.addWidget(ColoredWidget(self.foregroundColor), 75)
        simLayout.addWidget(ColoredWidget(self.foregroundColor), 25)

        # Assigning the created layout to the widget
        self.setLayout(containerLayout)


class MainToolBar(QToolBar):
    def __init__(self, container):
        super().__init__()

        # Home Button Handling
        self.homeButtonIcon = CxConfManager.icons["home"]
        homeButton = QAction(
            QIcon(self.homeButtonIcon), "Home", container)
        homeButton.setStatusTip("Go To Home Page")
        homeButton.triggered.connect(self.homeButtonHandler)
        # themeSwitchButton.setCheckable(True)
        self.addAction(homeButton)

        # Plotting Button
        self.plottingButtonIcon = CxConfManager.icons["edit"]
        plottingButton = QAction(
            QIcon(self.plottingButtonIcon), "Plotting", container)
        plottingButton.setStatusTip("Enable Plotting Mode")
        plottingButton.triggered.connect(self.plottingButtonHandler)
        plottingButton.setCheckable(True)
        self.addAction(plottingButton)

        # Theme Switch Button
        self.themeSwitchIcon = CxConfManager.icons["themeswitch"]
        themeSwitchButton = QAction(
            QIcon(self.themeSwitchIcon), "Theme", container)
        themeSwitchButton.setStatusTip("Switch Theme")
        themeSwitchButton.triggered.connect(self.themeSwitchHandler)
        themeSwitchButton.setCheckable(True)
        self.addAction(themeSwitchButton)

        # Settings Button Handling
        self.settingsButtonIcon = CxConfManager.icons["settings"]
        settingsButton = QAction(
            QIcon(self.settingsButtonIcon), "Settings", container)
        settingsButton.setStatusTip("Go To Settings")
        settingsButton.triggered.connect(self.settingsButtonHandler)
        # themeSwitchButton.setCheckable(True)
        self.addAction(settingsButton)

        # Setting the style
        self.toolbarColor = CxConfManager.themeConf["Dark"]["toolbar"]
        palette = self.palette()
        palette.setColor(QPalette.Window, QColor(self.toolbarColor))
        self.setPalette(palette)
        self.setStyleSheet("QToolBar{spacing:10px;}")

    def themeSwitchHandler(self, s):
        print("Theme Switching ", s)

    def homeButtonHandler(self, s):
        print("Home Button Pressed ", s)

    def settingsButtonHandler(self, s):
        # print("Settings Button Pressed", s)
        settingsDialog = SettingsDialog()
        settingsDialog.exec()

    def plottingButtonHandler(self, s):
        if (s):
            for action in self.actions():
                if (action.text() != "Plotting"):
                    action.setDisabled(True)
        else:
            for action in self.actions():
                action.setDisabled(False)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.titleIcon = QIcon(CxConfManager.icons["window"])
        self.setWindowTitle("CORTEX - 3DOF Robotic Arm Controller")
        self.setWindowIcon(self.titleIcon)

        # Handling the toolbar
        toolbar = MainToolBar(self)

        window = WindowLayout()

        self.setStatusBar(QStatusBar(self))
        self.addToolBar(toolbar)
        self.setCentralWidget(window)
        # self.setCursor(Qt.PointingHandCursor)


app = QApplication(sys.argv)

window = MainWindow()
window.showMaximized()

app.exec()
