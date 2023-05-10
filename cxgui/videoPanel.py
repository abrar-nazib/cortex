# fmt: off
from pathlib import Path
import sys
import os


# For removing import error
fpath = os.path.join(os.path.dirname(__file__), '..')
sys.path.append(fpath)
#------ 
import PyQt5
from PyQt5.QtCore import Qt, QSize, QTimer
from PyQt5.QtWidgets import (
    QHBoxLayout,
    QLabel,
    QVBoxLayout,
    QComboBox
)
from PyQt5.QtGui import QImage, QPixmap

import numpy as np
import cv2

# Handles the conflict issue with opencv and pyqt5 https://stackoverflow.com/questions/68417682/qt-and-opencv-app-not-working-in-virtual-environment
os.environ["QT_QPA_PLATFORM_PLUGIN_PATH"] = os.fspath(
    Path(PyQt5.__file__).resolve().parent / "Qt5" / "plugins"
)

from cortex import CxConfManager, CxVision
from cxgui import guiCommons

# fmt: on


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
        self.cameraInfoWidget = guiCommons.ColoredWidget(self.foregroundColor)
        self.cameraInfoLayout = QVBoxLayout()
        self.cameraSelectorLayout = QHBoxLayout()

        # Camera Number Selector box
        self.cameraSelectorLabel = QLabel("Select Camera: ")
        self.cameraSelectorBox = QComboBox()
        self.cameraSelectorBox.addItems(
            ['0', '1', '2', '3', '4', '5', '6', '7'])
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
            cvFrame = CxVision.get_image()
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
        CxVision.connect_cam(CxConfManager.cameraConf['last-used'])
