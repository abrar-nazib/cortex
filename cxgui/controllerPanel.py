# fmt: off
import sys
from PyQt5.QtWidgets import  QVBoxLayout, QHBoxLayout, QSlider, QLabel, QWidget
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor, QPalette
from cortex import CxConfManager, CxKinematics
from cxgui import guiCommons

# fmt: on
frame1 = CxKinematics.Frame()
frame2 = CxKinematics.Frame(parent=frame1, relative_position=[0,0,5])
frame3 = CxKinematics.Frame(parent=frame2,relative_position=[0,0,5])
frame4 = CxKinematics.Frame(parent=frame3,relative_position=[0,0,5])
frame5 = CxKinematics.Frame(parent=frame4,relative_position=[0,0,5])
frame6 = CxKinematics.Frame(parent=frame5,relative_position=[0,0,2])

simWindow = None
class ControllerPanel(QVBoxLayout):
  def __init__(self, simLayout):
    super().__init__()
    global simWindow
    simWindow = simLayout.simulationWindow
    # Setting the background and foreground color
    self.backgroundColor = CxConfManager.themeConf["Dark"]["background"]
    self.foregroundColor = CxConfManager.themeConf["Dark"]["foreground"]
    
    self.panel = guiCommons.ColoredWidget(self.foregroundColor)
    self.panelLayout = QVBoxLayout()
    self.panel.setLayout(self.panelLayout)
    self.addWidget(self.panel)
    
    self.slider1 = SliderElement("Joint 1", -90, 90, 0, frame1)
    self.slider2 = SliderElement("Joint 2", -90, 90, 0, frame2)
    self.slider3 = SliderElement("Joint 3", -90, 90, 0, frame3)
    self.slider4 = SliderElement("Joint 4", -90, 90, 0, frame4)
    self.slider5 = SliderElement("Joint 5", -90, 90, 0, frame5)
    self.slider6 = SliderElement("Joint 6", -90, 90, 0, frame6)
    
    self.panelLayout.addLayout(self.slider6)
    self.panelLayout.addLayout(self.slider5)
    self.panelLayout.addLayout(self.slider4)
    self.panelLayout.addLayout(self.slider3)
    self.panelLayout.addLayout(self.slider2)
    self.panelLayout.addLayout(self.slider1)
    
    simWindow.update_plot(frame1)
    




class SliderElement(QHBoxLayout):
  def __init__(self, name, min: float = 0, max: float = 180, value: float = 50, frame:CxKinematics.Frame=None):
    super().__init__()
    self.name = name
    self.frame = frame
    # Change the color of the label
    self.nameLabel = QLabel(self.name)
    self.nameLabel.setStyleSheet(f"QLabel {{color: {CxConfManager.themeConf['Dark']['font_color']};}}")
    
    self.slider = SliderWidget(self, min, max, value, self.frame, name)

    self.valueLabel = QLabel(str(value))
    self.valueLabel.setStyleSheet(f"QLabel {{color: {CxConfManager.themeConf['Dark']['font_color']};}}")
    
    self.addWidget(self.nameLabel)
    self.addWidget(self.slider)
    self.addWidget(self.valueLabel)
    
class SliderWidget(QSlider):
  def __init__(self,parent, min: float = 0, max: float = 180, value: float = 50, frame:CxKinematics.Frame=None, name=""):
    super().__init__(Qt.Horizontal)
    self.frame = frame
    self.name = name
    self.parent = parent  
    self.setMinimum(min)
    self.setMaximum(max)
    self.setValue(value)
    self.setTickInterval(1)
    self.valueChanged.connect(self.valueChangedHandler)
  
  def valueChangedHandler(self, value: float):
    self.parent.valueLabel.setText(str(value))
    if(self.name == "Joint 1" or self.name == "Joint 6"):
      self.frame.set_z_angle(value)
    else:
      self.frame.set_x_angle(value)
    simWindow.update_plot(frame1)