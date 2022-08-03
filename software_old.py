import guiframes
import tkinter as tk
import servocontroller
from matplotlib.pyplot import xscale
import threading
import cv2
from PIL import Image, ImageTk
import test as objectdetector

# import objectdetector


# Window sizing constants
WIDTH = 1366
HEIGHT = 768
BACKGROUND = "#1B2430"
FONTCOLOR = "#D6D5A8"
OBJX = None
OBJY = None

# cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
window = tk.Tk()

# Basic window configurations
window.state("zoomed")
window.rowconfigure(0, weight=1)
window.columnconfigure(0, weight=1)
window.title("CORTEX")
icon = tk.PhotoImage(file="assets/brain.png")
window.iconphoto(True, icon)
window.config(background=BACKGROUND)

# opencv functions
# cap = cv2.VideoCapture(0)

# # Frames
welcomePage = tk.Frame(master=window, bg=BACKGROUND)
welcomePage.grid(row=0, column=0, sticky="nsew")
# welcomePage.pack()
pickAndPlacePage = tk.Frame(master=window, bg=BACKGROUND)
pickAndPlacePage.grid(row=0, column=0, sticky="nsew")
# pickAndPlacePage.pack()
manualControlPage = tk.Frame(master=window, bg=BACKGROUND)
manualControlPage.grid(row=0, column=0, sticky="nsew")
# pickAndPlacePage.pack()


def createGridLines(img):
    # cv2.line(img, (54, 12), (22, 476), (0, 0, 0), 1)
    # pass
    try:
        xPix = int((xSlider.get() + 12) * (600/24))
        yPix = int(600-((ySlider.get() - 1.57) * (600/19.2)))
        cv2.rectangle(img, (xPix, yPix),
                      (xPix+5, yPix+5), (0, 0, 120), thickness=10)
        # print(f"done {xPix} {yPix}")
    except Exception as e:
        cv2.rectangle(img, (10, 10),
                      (20, 20), (120, 0, 0), 2)
        print(e)


def showFrame(frame):
    frame.tkraise()


def SliderUpdate(var):
    coordinateLabel['text'] = f'Manual Coordinates: ( {xSlider.get()} , {ySlider.get()} )'


def manualControl(var):
    servo1Angle = baseServoSlider.get()
    servo2Angle = shoulderServoSlider.get()
    servo3Angle = elbowServoSlider.get()
    servo4Angle = grabberServoSlider.get()
    servocontroller.guiControl(
        servo1Angle, servo2Angle, servo3Angle, servo4Angle)


def pickObjectGUI():
    servocontroller.pickObject([xSlider.get(), ySlider.get()])


def placeObjectGUI():
    servocontroller.placeObject([xSlider.get(), ySlider.get()])


def autoPickPlace():
    servocontroller.pickObject([OBJX, OBJY])
    # pass


def calculateActualPosition(objX, objY):
    xx = (((12+12)/600)*objX)-12
    yy = (19.2) - ((19.2)/600 * objY)
    yy = yy + 1.57
    return xx, yy


# Window Labels
headingLabel = tk.Label(
    text="CORTEX",
    font=('Arial', 40),
    fg=FONTCOLOR,
    bg=BACKGROUND,
    master=welcomePage
)
# headingLabel.grid(row=0, column=1)
headingLabel.pack(fill='x')

# # Image
logoImage = Image.open("assets/brain.png")
logoImage = logoImage.resize((450, 450))
logo = ImageTk.PhotoImage(logoImage)
headingImage = tk.Label(
    master=welcomePage,
    image=logo,
    bg=BACKGROUND,
)
# headingImage.grid(row=1, column=1)
headingImage.pack(fill='x', pady=10)

# Buttons
pickAndPlaceButton = tk.Button(
    text="Pick and Place Mode",
    font=('Arial', 15),
    relief=tk.RAISED,
    bg=BACKGROUND,
    fg=FONTCOLOR,
    master=welcomePage,
    width=50,
    borderwidth=3,
    command=lambda: showFrame(pickAndPlacePage),
    activebackground=FONTCOLOR,
    activeforeground=BACKGROUND
)
# pickAndPlaceButton.grid(row=2, column=1)
# pickAndPlaceButton.pack(fill='x')
pickAndPlaceButton.pack()


manualButton = tk.Button(
    text="Manual Mode",
    font=('Arial', 15),
    relief=tk.RAISED,
    bg=BACKGROUND,
    fg=FONTCOLOR,
    master=welcomePage,
    width=50,
    activebackground=FONTCOLOR,
    activeforeground=BACKGROUND,
    borderwidth=3,
    command=lambda: showFrame(manualControlPage)
)
# writingButton.grid(row=3, column=1)
# writingButton.pack(fill='x')
manualButton.pack()


writingButton = tk.Button(
    text="Writing Mode",
    font=('Arial', 15),
    relief=tk.RAISED,
    bg=BACKGROUND,
    fg=FONTCOLOR,
    master=welcomePage,
    width=50,
    activebackground=FONTCOLOR,
    activeforeground=BACKGROUND,
    borderwidth=3
)
# writingButton.grid(row=3, column=1)
# writingButton.pack(fill='x')
writingButton.pack()

exitButton = tk.Button(
    text="Exit",
    font=('Arial', 15),
    relief=tk.RAISED,
    bg=BACKGROUND,
    fg=FONTCOLOR,
    master=welcomePage,
    width=50,
    activebackground=FONTCOLOR,
    activeforeground=BACKGROUND,
    borderwidth=3,
    command=window.destroy
)
# writingButton.grid(row=3, column=1)
# writingButton.pack(fill='x')
exitButton.pack()


# -------------------------------------Object Pick up Labels----------------------
pickAndPlaceHeader = tk.Label(
    text="PICK & PLACE",
    font=('Arial', 20),
    fg=FONTCOLOR,
    bg=BACKGROUND,
    master=pickAndPlacePage
)
# headingLabel.grid(row=0, column=1)
pickAndPlaceHeader.pack(fill='x')

videoLabel = tk.Label(
    master=pickAndPlacePage,
    image=logo,
    bg=BACKGROUND,
)
# videoLabel.grid(row=1, column=1)
# videoLabel.pack(fill='x', padx=20, pady=20)
videoLabel.place(x=600, y=70)

videoLabel.bind("<Button-3>", objectdetector.mouseClickHandler)


backButton = tk.Button(
    text="Back",
    font=('Arial', 15),
    relief=tk.RAISED,
    bg=BACKGROUND,
    fg=FONTCOLOR,
    master=pickAndPlacePage,
    width=50,
    activebackground=FONTCOLOR,
    activeforeground=BACKGROUND,
    borderwidth=3,
    command=lambda: showFrame(welcomePage)
)
# writingButton.grid(row=3, column=1)
# writingButton.pack(fill='x')
backButton.pack(pady=5, padx=10, side="bottom", anchor="w")

placeButton = tk.Button(
    text="Place",
    font=('Arial', 15),
    relief=tk.RAISED,
    bg=BACKGROUND,
    fg=FONTCOLOR,
    master=pickAndPlacePage,
    width=50,
    activebackground=FONTCOLOR,
    activeforeground=BACKGROUND,
    borderwidth=3,
    command=lambda: threading.Thread(target=placeObjectGUI).start()
)
# writingButton.grid(row=3, column=1)
# writingButton.pack(fill='x')
placeButton.pack(pady=2, padx=10, side="bottom", anchor="w")


pickButton = tk.Button(
    text="Pick",
    font=('Arial', 15),
    relief=tk.RAISED,
    bg=BACKGROUND,
    fg=FONTCOLOR,
    master=pickAndPlacePage,
    width=50,
    activebackground=FONTCOLOR,
    activeforeground=BACKGROUND,
    borderwidth=3,
    command=lambda: threading.Thread(target=pickObjectGUI).start()
)
# writingButton.grid(row=3, column=1)
# writingButton.pack(fill='x')
pickButton.pack(pady=2, padx=10, side="bottom", anchor="w")

autoButton = tk.Button(
    text="Auto Mode",
    font=('Arial', 15),
    relief=tk.RAISED,
    bg=BACKGROUND,
    fg=FONTCOLOR,
    master=pickAndPlacePage,
    width=50,
    activebackground=FONTCOLOR,
    activeforeground=BACKGROUND,
    borderwidth=3,
    command=lambda: threading.Thread(target=autoPickPlace).start()
)
# writingButton.grid(row=3, column=1)
# writingButton.pack(fill='x')
autoButton.pack(pady=2, padx=10, side="bottom", anchor="w")


xSlider = tk.Scale(pickAndPlacePage, from_=-15, to=15,
                   orient=tk.HORIZONTAL, length=300, background=BACKGROUND, fg=FONTCOLOR, resolution=0.01, command=SliderUpdate)
xSlider.place(x=40, y=100)
xSliderLabel = tk.Label(pickAndPlacePage, text="X",
                        background=BACKGROUND, foreground=FONTCOLOR, font=('Arial', 20))
xSliderLabel.place(x=10, y=105)


ySlider = tk.Scale(pickAndPlacePage, from_=0, to=20,
                   orient=tk.HORIZONTAL, length=300, background=BACKGROUND, fg=FONTCOLOR, command=SliderUpdate, resolution=0.01)
ySlider.set(10)
ySlider.place(x=40, y=150)
ySliderLabel = tk.Label(pickAndPlacePage, text="Y",
                        background=BACKGROUND, foreground=FONTCOLOR, font=('Arial', 20))
ySliderLabel.place(x=10, y=155)

coordinateLabel = tk.Label(pickAndPlacePage, text="( X , Y )",
                           background=BACKGROUND, foreground=FONTCOLOR, font=('Arial', 20))
coordinateLabel.place(x=10, y=255)

objectPositionLabel = tk.Label(pickAndPlacePage, text="( X , Y )",
                               background=BACKGROUND, foreground=FONTCOLOR, font=('Arial', 20))
objectPositionLabel.place(x=10, y=355)
# -------------------------------- Manual Control Page --------------------------------------
manualControlHeader = tk.Label(
    text="Manual Control",
    font=('Arial', 20),
    fg=FONTCOLOR,
    bg=BACKGROUND,
    master=manualControlPage
)
# headingLabel.grid(row=0, column=1)
manualControlHeader.pack(fill='x')

feedLabel = tk.Label(
    master=manualControlPage,
    image=logo,
    bg=BACKGROUND,
)
# videoLabel.grid(row=1, column=1)
feedLabel.place(x=600, y=70)

backButton = tk.Button(
    text="Back",
    font=('Arial', 15),
    relief=tk.RAISED,
    bg=BACKGROUND,
    fg=FONTCOLOR,
    master=manualControlPage,
    width=50,
    activebackground=FONTCOLOR,
    activeforeground=BACKGROUND,
    borderwidth=3,
    command=lambda: showFrame(welcomePage)
)
# writingButton.grid(row=3, column=1)
# writingButton.pack(fill='x')
backButton.pack(pady=5, padx=10, side="bottom", anchor="w")


baseServoSlider = tk.Scale(manualControlPage, from_=0, to=180,
                           orient=tk.HORIZONTAL, length=300, background=BACKGROUND, fg=FONTCOLOR, resolution=0.01, command=manualControl)
baseServoSlider.set(90)
baseServoSlider.place(x=200, y=100)

baseServoSliderLabel = tk.Label(manualControlPage, text="Base",
                                background=BACKGROUND, foreground=FONTCOLOR, font=('Arial', 20))
baseServoSliderLabel.place(x=50, y=100)

shoulderServoSlider = tk.Scale(manualControlPage, from_=0, to=270,
                               orient=tk.HORIZONTAL, length=300, background=BACKGROUND, fg=FONTCOLOR, resolution=0.01, command=manualControl)
shoulderServoSlider.set(210)
shoulderServoSlider.place(x=200, y=200)
shoulderServoSliderLabel = tk.Label(manualControlPage, text="Shoulder",
                                    background=BACKGROUND, foreground=FONTCOLOR, font=('Arial', 20))
shoulderServoSliderLabel.place(x=50, y=200)


elbowServoSlider = tk.Scale(manualControlPage, from_=0, to=180,
                            orient=tk.HORIZONTAL, length=300, background=BACKGROUND, fg=FONTCOLOR, resolution=0.01, command=manualControl)
elbowServoSlider.set(45)
elbowServoSlider.place(x=200, y=300)
elbowServoSliderLabel = tk.Label(manualControlPage, text="Elbow",
                                 background=BACKGROUND, foreground=FONTCOLOR, font=('Arial', 20))
elbowServoSliderLabel.place(x=50, y=300)

grabberServoSlider = tk.Scale(manualControlPage, from_=120, to=180,
                              orient=tk.HORIZONTAL, length=300, background=BACKGROUND, fg=FONTCOLOR, resolution=0.01, command=manualControl)
grabberServoSlider.set(120)
grabberServoSlider.place(x=200, y=400)
grabberServoSliderLabel = tk.Label(manualControlPage, text="Grabber",
                                   background=BACKGROUND, foreground=FONTCOLOR, font=('Arial', 20))
grabberServoSliderLabel.place(x=50, y=400)

showFrame(welcomePage)

while True:
    # cv2image, objX, objY = objectdetector.getImageCoordinates()
    cv2image = objectdetector.getImageCoordinates()
    objX, objY = objectdetector.getPos()
    if objX != None:
        OBJX, OBJY = calculateActualPosition(objX, objY)
    # print(f'x={objX}, y={objY}')
        objectPositionLabel.configure(
            text=f"Object Detected At: ( {round(OBJX, 2)}, {round(OBJY, 2)} )")
    cv2image = cv2.cvtColor(cv2image, cv2.COLOR_BGR2RGB)

    # cv2image = cv2.rotate(cv2image, cv2.ROTATE_180)
    createGridLines(cv2image)
    img = Image.fromarray(cv2image)
    img = img.resize((650, 650))

    # Convert image to PhotoImage
    imgtk = ImageTk.PhotoImage(image=img)
    videoLabel.imgtk = imgtk
    feedLabel.imgtk = imgtk
    videoLabel.configure(image=imgtk)
    feedLabel.configure(image=imgtk)
    window.update()

window.mainloop()
