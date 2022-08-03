import guiframes
import tkinter as tk
import servocontroller
from matplotlib.pyplot import xscale
import threading
import cv2
from PIL import Image, ImageTk
import test as objectdetector

WIDTH = 1366
HEIGHT = 768
BACKGROUND = "#1B2430"
FONTCOLOR = "#D6D5A8"
OBJX = None
OBJY = None


class GUI(tk.Tk):
    def __init__(self):
        super().__init__()  # Initiating Super Method
        self.geometry("400x400")
        self.state("zoomed")
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)
        self.title("CORTEX")
        icon = tk.PhotoImage(file="assets/brain.png")
        self.iconphoto(True, icon)
        self.config(background=BACKGROUND)
        self.mainloop()


class CTX_Page


window = GUI()
