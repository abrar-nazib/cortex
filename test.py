from pickle import GLOBAL, NONE
# from turtle import setpos
from types import NoneType
import cv2
from cv2 import bitwise_and
import numpy as np
import colorsys

CAMERANUMBER = 2
TRACKBAR1 = 146
TRACKBAR2 = 112
AREA = 2400

cropping = False

x_start, y_start, x_end, y_end = 0, 0, 0, 0

mouseX = 100
mouseY = 100
hsv_img = None
upper = np.array([35, 55, 100])
lower = np.array([0, 0, 0])
POSX = None
POSY = None


def empty(a):
    pass


def getPos():
    return POSX, POSY


def crop(img):
    width, height = 600, 600
    pts1 = np.float32([[144, 34], [596, 58], [129, 393], [573, 415]])
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


def mouseClickHandler(event, x, y, flags, param):
    # grab references to the global variables
    # global x_start, y_start, x_end, y_end, cropping, hsv_img
    # # if the left mouse button was DOWN, start RECORDING
    # # (x, y) coordinates and indicate that cropping is being
    # if event == cv2.EVENT_LBUTTONDOWN:
    #     x_start, y_start, x_end, y_end = x, y, x, y
    #     cropping = True
    # # Mouse is Moving
    # elif event == cv2.EVENT_MOUSEMOVE:
    #     if cropping == True:
    #         x_end, y_end = x, y
    # # if the left mouse button was released
    # elif event == cv2.EVENT_LBUTTONUP:
    #     # record the ending (x, y) coordinates
    #     x_end, y_end = x, y
    #     cropping = False  # cropping is finished

    #     refPoint = [(x_start, y_start), (x_end, y_end)]

    #     if len(refPoint) == 2:  # when two points were found
    #         roi = hsv_img[refPoint[0][1]:refPoint[1]
    #                       [1], refPoint[0][0]:refPoint[1][0]]
    #         # cv2.imshow("Cropped", roi)
    #     lower, upper = getHSV(roi)
    #     print(lower, upper)
    global mouseX, mouseY, lower, upper, hsv_img
    if event == cv2.EVENT_LBUTTONDBLCLK:
        print(f"x={x} y={y}")
        pixel = hsv_img[y, x]
        H_upper = check_boundaries(pixel[0], 3, 0, 1)
        H_lower = check_boundaries(pixel[0], 3, 0, 0)
        S_upper = check_boundaries(pixel[1], 4, 1, 1)
        S_lower = check_boundaries(pixel[1], 4, 1, 0)
        V_upper = check_boundaries(pixel[2], 5, 1, 1)
        V_lower = check_boundaries(pixel[2], 5, 1, 0)

        upper = np.array([H_upper, S_upper, V_upper])
        lower = np.array([H_lower, S_lower, V_lower])
        print(lower, upper)

    # elif event == cv2.EVENT_RBUTTONDBLCLK:
    #     # cv2.circle(img, (x, y), 100, (255, 0, 0), -1)
    #     print(f"x={x} y={y}")


# def getHSV(roi):
#     img = roi
#     H_Range = []
#     S_Range = []
#     V_Range = []
#     height = img.shape[0]
#     width = img.shape[1]
#     for y in range(1, height - 1):
#         for x in range(1, width - 1):
#             color_h = round(hsv_img[y][x][0])
#             color_s = round(hsv_img[y][x][1])
#             color_v = round(hsv_img[y][x][2])
#             H_Range.append(color_h)
#             S_Range.append(color_s)
#             V_Range.append(color_v)

#     H_Range = np.asarray(H_Range)
#     S_Range = np.asarray(S_Range)
#     V_Range = np.asarray(V_Range)
#     lower = [round(H_Range.mean()-10), round(S_Range.mean()-10),
#              round(V_Range.mean()-10)]
#     upper = [round(H_Range.mean()+10), round(S_Range.mean()+10),
#              round(V_Range.mean()+10)]
#     return lower, upper


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
# cap = cv2.VideoCapture('https://192.168.31.189:8080/video')
# cap = cv2.VideoCapture(CAMERANUMBER)

cv2.namedWindow("Parameters")
cv2.resizeWindow("Parameters", 640, 240)
cv2.createTrackbar("Threshold1", "Parameters", TRACKBAR1, 255, empty)
cv2.createTrackbar("Threshold2", "Parameters", TRACKBAR2, 255, empty)
cv2.createTrackbar("Area", "Parameters", AREA, 30000, empty)


def getImageCoordinates():
    global hsv_img, upper, lower, cropping, x_start, y_start, x_end, y_end
    success, img = cap.read()
    # img = cv2.imread('RedC.jpeg')
    img = cv2.flip(img, 0)
    img = cv2.flip(img, 1)
    img = crop(img)
    imgContour = img.copy()
    # # threshold1 = cv2.getTrackbarPos("Threshold1", "Parameters")
    # # threshold2 = cv2.getTrackbarPos("Threshold2", "Parameters")
    imgBlur = cv2.GaussianBlur(img, (7, 7), 3)
    hsv_img = cv2.cvtColor(imgBlur, cv2.COLOR_BGR2HSV)
    blackMask = cv2.inRange(hsv_img, (0, 0, 0), (179, 218, 83))
    redMask = cv2.inRange(hsv_img, (0, 152, 0), (49, 235, 183))
    blueMask = cv2.inRange(hsv_img, (95, 105, 72), (103, 253, 200))
    bitwise1 = cv2.bitwise_or(blackMask, redMask)
    bitwise2 = cv2.bitwise_or(bitwise1,  blueMask)
    # colorMask = cv2.inRange(hsv_img, lower, upper)
    getContours(bitwise2, imgContour)
    # if not cropping:
    #     cv2.imshow("Result", imgContour)
    # elif cropping:
    #     cv2.rectangle(imgContour, (x_start, y_start),
    #                   (x_end, y_end), (255, 0, 0), 2)
    # cv2.imshow("Result", imgContour)
    # cv2.setMouseCallback('Result', mouseClickHandler)
    return imgContour


if __name__ == "__main__":
    while True:
        # success, img = cap.read()
        # img = cv2.imread('blackC.jpg')
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
