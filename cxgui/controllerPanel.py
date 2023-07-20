# fmt: off
import sys
from PyQt5.QtWidgets import  QVBoxLayout, QHBoxLayout, QSlider, QLabel, QWidget
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor, QPalette
from cortex import CxConfManager
from cxgui import guiCommons

# fmt: on

class ControllerPanel(QVBoxLayout):
  def __init__(self):
    super().__init__()
    
    # Setting the background and foreground color
    self.backgroundColor = CxConfManager.themeConf["Dark"]["background"]
    self.foregroundColor = CxConfManager.themeConf["Dark"]["foreground"]
    
    self.panel = guiCommons.ColoredWidget(self.foregroundColor)
    self.panelLayout = QVBoxLayout()
    self.panel.setLayout(self.panelLayout)
    self.addWidget(self.panel)
    
    for i in range(1, 7):
      self.panelLayout.addLayout(SliderElement(f"JOINT {7-i}", value=90))





class SliderElement(QHBoxLayout):
  def __init__(self, name, min: float = 0, max: float = 180, value: float = 50):
    super().__init__()
    self.name = name
    # Change the color of the label
    self.nameLabel = QLabel(self.name)
    self.nameLabel.setStyleSheet(f"QLabel {{color: {CxConfManager.themeConf['Dark']['font_color']};}}")
    
    self.slider = SliderWidget(self, min, max, value)

    self.valueLabel = QLabel(str(value))
    self.valueLabel.setStyleSheet(f"QLabel {{color: {CxConfManager.themeConf['Dark']['font_color']};}}")
    
    self.addWidget(self.nameLabel)
    self.addWidget(self.slider)
    self.addWidget(self.valueLabel)
    
class SliderWidget(QSlider):
  def __init__(self,parent, min: float = 0, max: float = 180, value: float = 50):
    super().__init__(Qt.Horizontal)
    self.parent = parent  
    self.setMinimum(min)
    self.setMaximum(max)
    self.setValue(value)
    self.setTickInterval(1)
    self.sliderMoved.connect(self.valueChangedHandler)
  
  def valueChangedHandler(self, value: float):
    self.parent.valueLabel.setText(str(value))