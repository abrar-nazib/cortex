# fmt: off
import sys
import os
from pathlib import Path


# For removing import error
fpath = os.path.join(os.path.dirname(__file__), 'cortex')
sys.path.append(fpath)
#------ 
import PyQt5
from PyQt5.QtCore import Qt, QSize, QTimer
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
    QComboBox
)
from PyQt5.QtGui import QPalette, QColor, QIcon, QCursor, QImage, QPixmap

import numpy as np
import cv2

# Handles the conflict issue with opencv and pyqt5 https://stackoverflow.com/questions/68417682/qt-and-opencv-app-not-working-in-virtual-environment
os.environ["QT_QPA_PLATFORM_PLUGIN_PATH"] = os.fspath(
    Path(PyQt5.__file__).resolve().parent / "Qt5" / "plugins"
)

from cortex import CxConfManager, CxObjectDetector

# fmt: on


class ColoredWidget(QWidget):
    def __init__(self, color: str):
        super().__init__()
        self.setAutoFillBackground(True)
        palette = self.palette()
        palette.setColor(QPalette.Window, QColor(color))
        palette.setColor(QPalette.WindowText, QColor('white'))
        self.setPalette(palette)


class VideoFeedPanel(QVBoxLayout):
    def __init__(self):
        super().__init__()

        # Setting the background and foreground color
        self.backgroundColor = CxConfManager.themeConf["Dark"]["background"]
        self.foregroundColor = CxConfManager.themeConf["Dark"]["foreground"]

        # Setting camera feed window
        self.cameraFeedWindow = QLabel()
        self.display_width = self.cameraFeedWindow.frameGeometry().width()
        self.display_height = self.cameraFeedWindow.frameGeometry().height()
        self.cameraNotConnectedImg = cv2.imread(
            CxConfManager.images["camera-not-found"])
        self.cameraFeedWindow.setStyleSheet(
            f"QLabel {{background-color: {self.foregroundColor};}}")

        # Camera Info Panel Setup
        self.cameraInfoWidget = ColoredWidget(self.foregroundColor)
        self.cameraInfoLayout = QVBoxLayout()
        self.cameraSelectorLayout = QHBoxLayout()

        # Camera Number Selector box
        self.cameraSelectorLabel = QLabel("Select Camera: ")
        self.cameraSelectorBox = QComboBox()
        self.cameraSelectorBox.addItems(['0', '1', '2', '3'])
        self.cameraSelectorBox.setCurrentIndex(
            CxConfManager.cameraConf['last-used'])
        self.cameraSelectorBox.currentIndexChanged.connect(
            self.cameraSelectorHandler)
        self.cameraSelectorLayout.addWidget(self.cameraSelectorLabel, 60)
        self.cameraSelectorLayout.addWidget(self.cameraSelectorBox, 40)
        # Adding layout to widget
        self.cameraInfoLayout.addLayout(self.cameraSelectorLayout)
        self.cameraInfoWidget.setLayout(self.cameraInfoLayout)

        # Add widgets to the main layout
        self.addWidget(self.cameraFeedWindow, 70)
        self.addWidget(self.cameraInfoWidget, 30)

        # Setting camera recurring camera feed capture
        self.timer = QTimer()
        self.timer.setInterval(10)
        self.timer.timeout.connect(self.getImage)
        self.timer.start()

    def getImage(self):
        self.display_width = self.cameraFeedWindow.frameGeometry().width()
        self.display_height = self.cameraFeedWindow.frameGeometry().height()
        try:
            cvFrame = CxObjectDetector.get_image()
            qtFrame = self.convert_cv_qt(cvFrame)
            self.cameraFeedWindow.setPixmap(qtFrame)
        except:
            cvFrame = self.cameraNotConnectedImg
            qtFrame = self.convert_cv_qt(cvFrame)

            self.cameraFeedWindow.setPixmap(qtFrame)

    def convert_cv_qt(self, cv_img):
        """Convert from an opencv image to QPixmap"""
        rgb_image = cv2.cvtColor(cv_img, cv2.COLOR_BGR2RGB)
        h, w, ch = rgb_image.shape
        bytes_per_line = ch * w
        convert_to_Qt_format = QImage(
            rgb_image.data, w, h, bytes_per_line, QImage.Format_RGB888)
        p = convert_to_Qt_format.scaled(
            self.display_width, self.display_height, Qt.KeepAspectRatio)
        return QPixmap.fromImage(p)

    def cameraSelectorHandler(self, camera_num):
        CxConfManager.cameraConf["last-used"] = camera_num
        CxConfManager.saveSettingsData()
        CxObjectDetector.connect_cam(CxConfManager.cameraConf['last-used'])


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
        camLayout = VideoFeedPanel()
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
