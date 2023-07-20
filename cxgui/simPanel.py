# fmt: off
import sys
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from cortex import CxConfManager

# fmt: on

class SimulationPanel(QVBoxLayout):
  def __init__(self):
    super().__init__()
    
    # Setting the background and foreground color
    self.backgroundColor = CxConfManager.themeConf["Dark"]["background"]
    self.foregroundColor = CxConfManager.themeConf["Dark"]["foreground"]
    
    self.simulationWindow = Matplotlib3DWidget(self)

class Matplotlib3DWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__()
        self.parent = parent
        # Set the colors of the text
        matplotlib.rcParams['text.color'] = 'white'
        matplotlib.rcParams['axes.labelcolor'] = 'white'
        matplotlib.rcParams['xtick.color'] = 'white'
        matplotlib.rcParams['ytick.color'] = 'white'
        
        self.canvas = FigureCanvas(plt.figure(facecolor=CxConfManager.themeConf["Dark"]["foreground"]))
        # layout.addWidget(self.canvas)
        self.parent.addWidget(self.canvas)

        self.plot_3d()


    def plot_3d(self):
        fig = self.canvas.figure
        ax = fig.add_subplot(111, projection='3d')
        
        # Set the background color
        ax.set_facecolor(CxConfManager.themeConf["Dark"]["foreground"])
        

        # Sample data for demonstration
        x = np.linspace(-5, 5, 100)
        y = np.linspace(-5, 5, 100)
        X, Y = np.meshgrid(x, y)
        Z = np.sin(np.sqrt(X ** 2 + Y ** 2))

        ax.plot_surface(X, Y, Z, cmap='viridis')
        ax.set_xlabel('X')
        ax.set_ylabel('Y')
        ax.set_zlabel('Z')
        ax.set_title('Robotic Arm Simulation')

        self.canvas.draw()