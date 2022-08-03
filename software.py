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
        self.state("zoomed")
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)
        self.title("CORTEX")
        icon = tk.PhotoImage(file="assets/brain.png")
        self.iconphoto(True, icon)
        self.config(background=BACKGROUND)

    def showPage(self, page):
        page.tkraise()


class Page(tk.Frame):
    def __init__(self, master):
        super().__init__(master, bg=BACKGROUND)
        self.grid(row=0, column=0, sticky="nsew")


class Text(tk.Label):
    def __init__(self, page, text, fontSize):
        super().__init__(
            page,
            fg=FONTCOLOR,
            text=text,
            font=('Arial', fontSize), bg=BACKGROUND
        )


class WelcomePage(Page):
    def __init__(self, master):
        super().__init__(master)
        text = Text(self, (1, 2))
        text.pack(fill="x")


window = GUI()
welcomePage = WelcomePage(window)
window.mainloop()
