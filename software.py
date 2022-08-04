from pydoc import TextRepr
from typing import Text
from numpy import pad
import guiframes
import tkinter as tk
import servocontroller
from matplotlib.pyplot import xscale
import threading
import cv2
from PIL import Image, ImageTk
import objectdetector

WIDTH = 1366
HEIGHT = 768
BACKGROUND = "#1B2430"
FONTCOLOR = "#D6D5A8"
OBJX = None
OBJY = None
BUTTONFONTSIZE = 15
CONNECTED = False


def hello(*args, **kwargs):
    print(WIDTH)


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

        self.updateScreenGeometry()

        self.pages = {}
        self.raised = []
        for P in (WelcomePage, PickAndPlacePage, SettingsPage, ManualControlPage):
            page = P(self)
            self.pages[P] = page

        self.showPage(WelcomePage)

    def showPage(self, page):
        self.raised = []
        self.raised.append(page)
        frame = self.pages[page]
        frame.tkraise()

    def updateScreenGeometry(self):
        global WIDTH, HEIGHT
        WIDTH = self.winfo_screenwidth()
        HEIGHT = self.winfo_screenheight()


class Page(tk.Frame):
    def __init__(self, containerWindow):
        super().__init__(containerWindow, bg=BACKGROUND)
        self.container = containerWindow
        self.grid(row=0, column=0, sticky="nsew")


class TextLabel(tk.Label):
    def __init__(self, page, text, fontsize=20):
        super().__init__(
            page,
            fg=FONTCOLOR,
            text=text,
            font=('Arial', fontsize),
            bg=BACKGROUND
        )


class ImageLabel(tk.Label):
    def __init__(self, page, location, size, bg=BACKGROUND):
        imageRaw = Image.open(location)
        imageRaw = imageRaw.resize(size)
        self.image = ImageTk.PhotoImage(imageRaw)  # Avoid garbage collection
        super().__init__(page, bg=BACKGROUND, image=self.image)


class ButtonLabel(tk.Button):
    def __init__(self, page, text, fontsize=15, command=hello, width=50, borderwidth=3):
        super().__init__(page,
                         text=text,
                         font=('Arial', fontsize),
                         relief=tk.RAISED,
                         bg=BACKGROUND,
                         fg=FONTCOLOR,
                         width=width,
                         borderwidth=borderwidth,
                         command=command,
                         activebackground=FONTCOLOR,
                         activeforeground=BACKGROUND
                         )


class SliderLabel(tk.Scale):
    def __init__(self, page, from_, to, resolution, length=300, command=hello):
        super().__init__(
            page,
            from_=from_,
            to=to,
            orient=tk.HORIZONTAL,
            length=length,
            background=BACKGROUND,
            fg=FONTCOLOR,
            resolution=resolution,
            command=command
        )


class WelcomePage(Page):
    def __init__(self, container):
        super().__init__(container)

        text = TextLabel(self, text="CORTEX", fontsize=40)
        text.pack(fill="x")

        headingImage = ImageLabel(
            self,
            location="assets/brain.png",
            size=(450, 450)
        )
        headingImage.pack(fill='x', pady=10)

        self.pickAndPlaceButton = ButtonLabel(
            self,
            text="Pick & Place Mode",
            command=lambda: self.container.showPage(PickAndPlacePage)
        )
        self.pickAndPlaceButton.pack()

        self.manualButton = ButtonLabel(
            self,
            text="Manual Mode",
            command=lambda: self.container.showPage(ManualControlPage)
        )
        self.manualButton.pack()

        self.writingButton = ButtonLabel(
            self,
            text="Writing Mode",
            # command=lambda: showFrame(writingPage)

        )
        self.writingButton.pack()

        self.settingsButton = ButtonLabel(
            self,
            text="Settings",
            command=lambda: self.container.showPage(SettingsPage)
        )
        self.settingsButton.pack()

        self.exitButton = ButtonLabel(
            self,
            text="Exit",
            command=self.container.destroy
        )
        self.exitButton.pack()

        self.disableButtons()

    def disableButtons(self):
        self.pickAndPlaceButton["state"] = tk.DISABLED
        self.writingButton["state"] = tk.DISABLED
        self.manualButton["state"] = tk.DISABLED

    def enableButtons(self):
        self.pickAndPlaceButton["state"] = tk.NORMAL
        self.writingButton["state"] = tk.NORMAL
        self.manualButton["state"] = tk.NORMAL


class PickAndPlacePage(Page):
    def __init__(self, container):
        super().__init__(container)
        pickAndPlaceHeader = TextLabel(
            self,
            text="PICK & PLACE",
            fontsize=20,
        )
        pickAndPlaceHeader.pack(fill='x')

        videoFeed = ImageLabel(
            self,
            location="assets/brain.png",
            size=(600, 600)
        )
        videoFeed.place(x=600, y=70)
        videoFeed.bind("<Button-3>", objectdetector.mouseClickHandler)
        self.videoFeed = videoFeed

        backButton = ButtonLabel(
            self,
            text="Back",
            command=lambda: self.container.showPage(WelcomePage)
        )
        backButton.pack(pady=5, padx=10, side="bottom", anchor="w")

        colorCalibrationButton = ButtonLabel(
            self,
            text="Calibrate",
            # command=lambda: threading.Thread(target=placeObjectGUI).start()
        )
        colorCalibrationButton.pack(pady=2, padx=10, side="bottom", anchor="w")

        placeButton = ButtonLabel(
            self,
            text="Place",
            command=lambda: threading.Thread(
                target=self.placeObjectGUI).start()
        )
        placeButton.pack(pady=2, padx=10, side="bottom", anchor="w")

        pickButton = ButtonLabel(
            self,
            text="Pick",
            command=lambda: threading.Thread(target=self.pickObjectGUI).start()
        )
        pickButton.pack(pady=2, padx=10, side="bottom", anchor="w")

        autoButton = ButtonLabel(
            self,
            text="Auto Pick Up",
            command=lambda: threading.Thread(
                target=self.autoPickObject).start()
        )
        autoButton.pack(pady=2, padx=10, side="bottom", anchor="w")

        xSlider = SliderLabel(self,
                              from_=-15,
                              to=15,
                              length=300,
                              resolution=0.01,
                              command=self.sliderUpdate
                              )
        xSlider.place(x=40, y=100)
        xSliderLabel = TextLabel(self, "X")
        xSliderLabel.place(x=10, y=105)
        self.xSlider = xSlider

        ySlider = SliderLabel(self,
                              from_=0,
                              to=20,
                              command=self.sliderUpdate,
                              resolution=0.01
                              )
        ySlider.set(10)
        ySlider.place(x=40, y=150)
        ySliderLabel = TextLabel(self,
                                 text="Y",
                                 )
        ySliderLabel.place(x=10, y=155)
        self.ySlider = ySlider

        coordinateLabel = TextLabel(self,
                                    text="( X , Y )",
                                    )
        coordinateLabel.place(x=10, y=255)
        self.coordinateLabel = coordinateLabel

        objectPositionLabel = TextLabel(self,
                                        text="( X , Y )",
                                        )
        objectPositionLabel.place(x=10, y=355)
        self.objectPositionLabel = objectPositionLabel

    def placeObjectGUI(self):
        servocontroller.placeObject([self.xSlider.get(), self.ySlider.get()])

    def pickObjectGUI(self):
        servocontroller.pickObject([self.xSlider.get(), self.ySlider.get()])

    def sliderUpdate(self, *args):
        self.coordinateLabel['text'] = f'Manual Coordinates: ( {self.xSlider.get()} , {self.ySlider.get()} )'

    def autoPickObject(self):
        servocontroller.pickObject([OBJX, OBJY])

    def calculateActualPosition(self, objX, objY):
        xx = (((12+12)/600)*objX)-12
        yy = (19.2) - ((19.2)/600 * objY)
        yy = yy + 1.57
        try:
            self.objectPositionLabel.configure(
                text=f"Object Detected At: ( {round(OBJX, 2)}, {round(OBJY, 2)} )")
        except Exception as e:
            print(e)
        return xx, yy

    def showPositionIndicator(self, img):
        try:
            xPix = int((self.xSlider.get() + 12) * (600/24))
            yPix = int(600-((self.ySlider.get() - 1.57) * (600/19.2)))
            cv2.rectangle(img, (xPix, yPix),
                          (xPix+5, yPix+5), (0, 0, 120), thickness=10)
        except Exception as e:
            cv2.rectangle(img, (10, 10),
                          (20, 20), (120, 0, 0), 2)
            print(e)


class SettingsOption():
    def __init__(self, container,  posX, posY, labelText, inputText, buttonText, statusText, buttonCommand=hello):
        self.container = container
        self.posX = posX
        self.posY = posY

        self.text = TextLabel(self.container, text=labelText)
        self.text.place(x=self.posX, y=self.posY)

        self.input = tk.Entry(self.container, width=10,
                              font=("Arial", 20))
        self.input.insert(0, inputText)
        self.input.place(y=self.posY, x=int(WIDTH*(1/4))+10)

        self.button = ButtonLabel(self.container, buttonText,
                                  width=20, command=buttonCommand)
        self.button.place(y=self.posY, x=int(WIDTH*(2/4))+10)

        self.status = TextLabel(self.container, text=statusText)
        self.status.place(y=self.posY, x=int(WIDTH*(3/4))+10)

    def updateStatusText(self, updatedText):
        self.status.configure(text=updatedText)

    def getInputText(self):
        return self.input.get()


class SettingsPage(Page):
    def __init__(self, container):
        super().__init__(container)
        backButton = ButtonLabel(
            self,
            text="Back",
            command=lambda: self.container.showPage(WelcomePage)
        )
        backButton.pack(pady=5, padx=10, side="bottom")

        self.comPortOption = SettingsOption(
            self,
            posX=10,
            posY=self.postoY(0),
            labelText="Com Port: ",
            inputText="COM5",
            buttonText="Connect",
            statusText="Not Connected",
            buttonCommand=self.connectToArduino
        )

        self.cameraOption = SettingsOption(
            self,
            posX=10,
            posY=self.postoY(1),
            labelText="Camera Number",
            inputText=objectdetector.CAMERANUMBER,
            buttonText="Save",
            statusText=f"Current Camera: {objectdetector.CAMERANUMBER}",
            buttonCommand=self.updateCamera
        )
        baseLength = SettingsOption(
            self,
            posX=10,
            posY=self.postoY(2),
            labelText="Length of Base",
            inputText="0",
            buttonText="Save",
            statusText="Current Length:"
        )
        upperArmLength = SettingsOption(
            self,
            posX=10,
            posY=self.postoY(3),
            labelText="Length of Upper Arm:",
            inputText="0",
            buttonText="Save",
            statusText="Current Length:"
        )
        foreArmLength = SettingsOption(
            self,
            posX=10,
            posY=self.postoY(4),
            labelText="Length of Base:",
            inputText="0",
            buttonText="Save",
            statusText="Current Length:"
        )
        baseServoAngleCorrection = SettingsOption(
            self,
            posX=10,
            posY=self.postoY(5),
            labelText="BS Angle Correction:",
            inputText="0",
            buttonText="Save",
            statusText="Current Correction: "
        )
        shoulderServoAngleCorrection = SettingsOption(
            self,
            posX=10,
            posY=self.postoY(6),
            labelText="SS Angle Correction: ",
            inputText="0",
            buttonText="Save",
            statusText="Current Correction: "
        )
        elbowServoAngleCorrection = SettingsOption(
            self,
            posX=10,
            posY=self.postoY(7),
            labelText="ES Angle Correction: ",
            inputText="0",
            buttonText="Save",
            statusText="Current Correction: "
        )

    def postoY(self, pos):
        return 20+pos*60

    def connectToArduino(self):
        global CONNECTED
        port = self.comPortOption.getInputText()
        self.comPortOption.updateStatusText(f"Connecting...")
        self.container.update()
        CONNECTED = servocontroller.connect(port)

        if(CONNECTED):
            self.comPortOption.updateStatusText(f"Connected to {port}")
            self.container.pages[WelcomePage].enableButtons()

        else:
            self.comPortOption.updateStatusText(f"Not Connected")
            self.container.pages[WelcomePage].disableButtons()

    def updateCamera(self):
        newCameraNumber = int(self.cameraOption.getInputText())
        objectdetector.updateCamera(newCameraNumber)
        self.cameraOption.updateStatusText(
            f"Current Camera: {newCameraNumber}")


class ManualControlPage(Page):
    def __init__(self, container):
        super().__init__(container)

        manualControlHeader = TextLabel(
            self,
            text="Manual Control",
        )
        manualControlHeader.pack(fill='x')

        videoFeed = ImageLabel(
            self,
            "assets/brain.png", size=(600, 600)
        )
        videoFeed.place(x=600, y=70)
        self.videoFeed = videoFeed

        backButton = ButtonLabel(
            self,
            text="Back",
            command=lambda: self.container.showPage(WelcomePage)
        )
        backButton.pack(pady=5, padx=10, side="bottom", anchor="w")

        baseServoSlider = SliderLabel(self, from_=0, to=180,
                                      resolution=0.01,
                                      command=self.manualControl
                                      )
        baseServoSlider.set(90)
        baseServoSlider.place(x=200, y=100)
        baseServoSliderLabel = TextLabel(self,
                                         text="Base",
                                         )
        baseServoSliderLabel.place(x=50, y=100)
        self.baseServoSlider = baseServoSlider

        shoulderServoSlider = SliderLabel(self,
                                          from_=0,
                                          to=270,
                                          resolution=0.01,
                                          command=self.manualControl
                                          )
        shoulderServoSlider.set(210)
        shoulderServoSlider.place(x=200, y=200)
        shoulderServoSliderLabel = TextLabel(self,
                                             text="Shoulder",
                                             )
        shoulderServoSliderLabel.place(x=50, y=200)
        self.shoulderServoSlider = shoulderServoSlider

        elbowServoSlider = SliderLabel(self,
                                       from_=0,
                                       to=180,
                                       resolution=0.01,
                                       command=self.manualControl
                                       )
        elbowServoSlider.set(45)
        elbowServoSlider.place(x=200, y=300)
        elbowServoSliderLabel = TextLabel(self,
                                          text="Elbow",
                                          )
        elbowServoSliderLabel.place(x=50, y=300)
        self.elbowServoSlider = elbowServoSlider

        grabberServoSlider = SliderLabel(self,
                                         from_=120,
                                         to=180,
                                         resolution=0.01,
                                         command=self.manualControl
                                         )
        grabberServoSlider.set(120)
        grabberServoSlider.place(x=200, y=400)
        grabberServoSliderLabel = TextLabel(self,
                                            text="Grabber",
                                            )
        grabberServoSliderLabel.place(x=50, y=400)
        self.grabberServoSlider = grabberServoSlider

    def manualControl(self, *args):
        servo1Angle = self.baseServoSlider.get()
        servo2Angle = self.shoulderServoSlider.get()
        servo3Angle = self.elbowServoSlider.get()
        servo4Angle = self.grabberServoSlider.get()
        servocontroller.guiControl(
            servo1Angle, servo2Angle, servo3Angle, servo4Angle)


window = GUI()

while True:
    cv2image = objectdetector.getImageCoordinates()
    objX, objY = objectdetector.getPos()
    if objX != None:
        OBJX, OBJY = window.pages[PickAndPlacePage].calculateActualPosition(
            objX, objY
        )
    cv2image = cv2.cvtColor(cv2image, cv2.COLOR_BGR2RGB)

    window.pages[PickAndPlacePage].showPositionIndicator(cv2image)

    img = Image.fromarray(cv2image)
    img = img.resize((650, 650))

    # Convert image to PhotoImage
    imgtk = ImageTk.PhotoImage(image=img)

    window.pages[PickAndPlacePage].videoFeed.configure(image=imgtk)
    window.pages[ManualControlPage].videoFeed.configure(image=imgtk)
    window.update()


window.mainloop()
