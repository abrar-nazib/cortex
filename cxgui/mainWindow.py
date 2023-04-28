# fmt: off
import sys
import os
from pathlib import Path


# For removing import error
fpath = os.path.join(os.path.dirname(__file__), '..')
sys.path.append(fpath)
#------ 
import PyQt5
from PyQt5.QtCore import Qt, QSize, QTimer
from PyQt5.QtWidgets import (
    QMainWindow,
    QHBoxLayout,
    QVBoxLayout,
    QWidget,
    QToolBar,
    QAction,
    QStatusBar,
)
from PyQt5.QtGui import QPalette, QColor, QIcon, QCursor, QImage, QPixmap

import numpy as np
import cv2

# Handles the conflict issue with opencv and pyqt5 https://stackoverflow.com/questions/68417682/qt-and-opencv-app-not-working-in-virtual-environment
os.environ["QT_QPA_PLATFORM_PLUGIN_PATH"] = os.fspath(
    Path(PyQt5.__file__).resolve().parent / "Qt5" / "plugins"
)

from cortex import CxConfManager
from cxgui import guiCommons, videoPanel, simPanel, settingsPanel

# fmt: on


class MainWindowLayout(QWidget):
    """Main Window Layout Design

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
        camLayout = videoPanel.VideoFeedPanel()
        simLayout = QVBoxLayout()
        optionsLayout = QVBoxLayout()

        # Container layout Organization
        containerLayout.addLayout(optionsLayout, 30)
        containerLayout.addLayout(camLayout, 35)
        containerLayout.addLayout(simLayout, 35)
        containerLayout.setSpacing(10)
        containerLayout.setContentsMargins(10, 10, 10, 10)
        # Cam Layout Organization
        # camwidget = ColoredWidget(self.foregroundColor)
        # camwidget.setCursor(Qt.PointingHandCursor)

        # Option Layout Organization
        optionsLayout.addWidget(
            guiCommons.ColoredWidget(self.foregroundColor), 70)
        optionsLayout.addWidget(
            guiCommons.ColoredWidget(self.foregroundColor), 20)

        # Simulation Layout Organization
        simLayout.addWidget(guiCommons.ColoredWidget(self.foregroundColor), 75)
        simLayout.addWidget(guiCommons.ColoredWidget(self.foregroundColor), 25)

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
        settingsDialog = settingsPanel.SettingsDialog()
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

        window = MainWindowLayout()

        self.setStatusBar(QStatusBar(self))
        self.addToolBar(toolbar)
        self.setCentralWidget(window)
        # self.setCursor(Qt.PointingHandCursor)
