# fmt: off
import sys
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from cortex import CxConfManager, CxKinematics

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


    def plot_3d(self, frame: CxKinematics.Frame=None, azim=-60, elev=30):
        fig = self.canvas.figure
        self.ax = fig.add_subplot(111, projection='3d')
        self.ax.set_facecolor(CxConfManager.themeConf["Dark"]["foreground"])
        self.ax.azim = azim
        self.ax.elev = elev
        
        frame_positions = []
        while(frame != None):
        # Draw lines between the points
            frame_pos, axis_x_pos, axis_y_pos, axis_z_pos = frame.get_positions()
            frame_positions.append(frame_pos)
            self.ax.plot([frame_pos[0], axis_x_pos[0]], [frame_pos[1], axis_x_pos[1]], [frame_pos[2], axis_x_pos[2]], c='r', linewidth=3)
            self.ax.plot([frame_pos[0], axis_y_pos[0]], [frame_pos[1], axis_y_pos[1]], [frame_pos[2], axis_y_pos[2]], c='b', linewidth=3)
            self.ax.plot([frame_pos[0], axis_z_pos[0]], [frame_pos[1], axis_z_pos[1]], [frame_pos[2], axis_z_pos[2]], c='g', linewidth=3)
            frame = frame.get_child()
        
        x_arr = []
        y_arr = []
        z_arr = []
        for position in frame_positions:
            x_arr.append(position[0])
            y_arr.append(position[1])
            z_arr.append(position[2])
        self.ax.plot(x_arr[:2], y_arr[:2], z_arr[:2], c='#5BB318', linewidth=25)
        self.ax.plot(x_arr[1:3], y_arr[1:3], z_arr[1:3], c='#7DCE13', linewidth=20)
        self.ax.plot(x_arr[2:4], y_arr[2:4], z_arr[2:4], c='#7DCE13', linewidth=15)
        self.ax.plot(x_arr[3:], y_arr[3:], z_arr[3:], c='#EAE509', linewidth=8)
            # Set the axes limit
        self.ax.set_xlim([-15, 15])
        self.ax.set_ylim([-15, 15])
        self.ax.set_zlim([0, 25])
        
        self.ax.set_xlabel('X Label')
        self.ax.set_ylabel('Y Label')
        self.ax.set_zlabel('Z Label')
        
        self.canvas.draw()
    
    def update_plot(self, frame: CxKinematics.Frame):
        # Delete the previous plot
        azim = self.ax.azim
        elev = self.ax.elev
        self.canvas.figure.clear() 
        self.plot_3d(frame, azim, elev)
        