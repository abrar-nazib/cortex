from pickle import GLOBAL, NONE
# from turtle import setpos
from types import NoneType
import cv2
import numpy as np
import colorsys

CAMERANUMBER = 2
TRACKBAR1 = 146
TRACKBAR2 = 112
AREA = 2500

mouseX = 100
mouseY = 100
hsv_img = None
upper = np.array([35, 55, 100])
lower = np.array([10, 10, 10])
POSX = None
POSY = None


def empty(a):
    pass


def getPos():
    return POSX, POSY


def crop(img):
    width, height = 600, 600
    pts1 = np.float32([[147, 33], [599, 59], [131, 394], [575, 416]])
    pts2 = np.float32([[0, 0], [width, 0], [0, height], [width, height]])
    matrix = cv2.getPerspectiveTransform(pts1, pts2)
    output = cv2.warpPerspective(img, matrix, (width, height))
    return output


def check_boundaries(value, tolerance, ranges, upper_or_lower):
    if ranges == 0:
        boundary = 180
    elif ranges == 1:
        boundary = 255

    if(value + tolerance > boundary):
        value = boundary
    elif (value - tolerance < 0):
        value = 0
    else:
        if upper_or_lower == 1:
            value = value + tolerance
        else:
            value = value - tolerance
    return value


def mouseClickHandler(event):
    global mouseX, mouseY, lower, upper, hsv_img
    # if event == cv2.EVENT_RBUTTONDBLCLK:
    print(f"x={event.x} y={event.y}")
    pixel = hsv_img[event.y, event.x]
    H_upper = check_boundaries(pixel[0], 10, 0, 1)
    H_lower = check_boundaries(pixel[0], 10, 0, 0)
    S_upper = check_boundaries(pixel[1], 10, 1, 1)
    S_lower = check_boundaries(pixel[1], 10, 1, 0)
    V_upper = check_boundaries(pixel[2], 40, 1, 1)
    V_lower = check_boundaries(pixel[2], 40, 1, 0)

    upper = np.array([H_upper, S_upper, V_upper])
    lower = np.array([H_lower, S_lower, V_lower])
    print(lower, upper)

    # elif event == cv2.EVENT_RBUTTONDBLCLK:
    #     # cv2.circle(img, (x, y), 100, (255, 0, 0), -1)
    #     print(f"x={x} y={y}")


def getContours(img, imgContour):
    global POSX
    global POSY
    contours, hierarchy = cv2.findContours(
        img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

    for cont in contours:
        area = cv2.contourArea(cont)
        cx = 0
        cy = 0
        minArea = cv2.getTrackbarPos("Area", "Parameters")
        if area > minArea:
            cv2.drawContours(imgContour, cont, -1, (255, 0, 255), 3)
            peri = cv2.arcLength(cont, True)
            approx = cv2.approxPolyDP(cont, 0.02*peri, True)
            moments = cv2.moments(cont)
            cx = int(moments["m10"] / moments["m00"])
            cy = int(moments["m01"] / moments["m00"])
            POSX = cx
            POSY = cy
            x, y, w, h = cv2.boundingRect(approx)
            cv2.circle(imgContour, (cx, cy), 5, (0, 0, 255), -1)
            cv2.rectangle(imgContour, (x, y), (x+w, y+h), (0, 255, 0), 3)


frameWidth = 600
frameHeight = 600
cap = cv2.VideoCapture(CAMERANUMBER, cv2.CAP_DSHOW)
# cap = cv2.VideoCapture('https://192.168.0.101:8080/video')
# cap = cv2.VideoCapture(CAMERANUMBER)

cv2.namedWindow("Parameters")
cv2.resizeWindow("Parameters", 640, 240)
cv2.createTrackbar("Threshold1", "Parameters", TRACKBAR1, 255, empty)
cv2.createTrackbar("Threshold2", "Parameters", TRACKBAR2, 255, empty)
cv2.createTrackbar("Area", "Parameters", AREA, 30000, empty)


def getImageCoordinates():
    global hsv_img, upper, lower
    success, img = cap.read()
    # img = cv2.imread('blackC.jpg')
    img = cv2.flip(img, 0)
    img = cv2.flip(img, 1)
    img = crop(img)
    imgContour = img.copy()
    threshold1 = cv2.getTrackbarPos("Threshold1", "Parameters")
    threshold2 = cv2.getTrackbarPos("Threshold2", "Parameters")
    hsv_img = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    colorMask = cv2.inRange(hsv_img, lower, upper)
    getContours(colorMask, imgContour)
    # cv2.imshow("Result", imgContour)
    # cv2.setMouseCallback('Result', mouseClickHandler)
    return imgContour


if __name__ == "__main__":
    while True:
        # success, img = cap.read()
        # # img = cv2.imread('blackC.jpg')
        # img = cv2.flip(img, 0)
        # img = cv2.flip(img, 1)
        # # img = crop(img)
        # imgContour = img.copy()
        # threshold1 = cv2.getTrackbarPos("Threshold1", "Parameters")
        # threshold2 = cv2.getTrackbarPos("Threshold2", "Parameters")
        # hsv_img = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        # # lower_black = np.array([0, 0, 0])
        # # upper_black = np.array([35, 55, 100])
        # colorMask = cv2.inRange(hsv_img, lower, upper)
        # getContours(colorMask, imgContour)
        # cv2.imshow("Result", imgContour)
        # cv2.setMouseCallback('Result', mouseClickHandler)
        getImageCoordinates()

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
