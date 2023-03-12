# fmt: off
from pickle import GLOBAL, NONE
# from turtle import setpos
from types import NoneType
import cv2
# from cv2 import bitwise_and
import numpy as np
# import colorsys
# fmt: on

CAMERANUMBER = 0
TRACKBAR1 = 146
TRACKBAR2 = 112
AREA = 2400

frameWidth = 600
frameHeight = 600
cap = cv2.VideoCapture(CAMERANUMBER, cv2.CAP_DSHOW)

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


def updateCamera(cameraNumber):
    global CAMERANUMBER, cap
    CAMERANUMBER = cameraNumber
    cap = cv2.VideoCapture(CAMERANUMBER, cv2.CAP_DSHOW)


def getPos():
    return POSX, POSY


def crop(img):
    width, height = 600, 600
    pts1 = np.float32([[40, 7], [593, 49], [30, 453], [558, 469]])
    pts2 = np.float32([[0, 0], [width, 0], [0, height], [width, height]])
    matrix = cv2.getPerspectiveTransform(pts1, pts2)
    output = cv2.warpPerspective(img, matrix, (width, height))
    return output


def check_boundaries(value, tolerance, ranges, upper_or_lower):
    if ranges == 0:
        boundary = 180
    elif ranges == 1:
        boundary = 255

    if (value + tolerance > boundary):
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
    if event == cv2.EVENT_LBUTTONDBLCLK:
        #     # cv2.circle(img, (x, y), 100, (255, 0, 0), -1)
        print(f"x={x} y={y}")


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
        # minArea = cv2.getTrackbarPos("Area", "Parameters")
        minArea = AREA
        if area > minArea:
            cv2.drawContours(imgContour, cont, -1, (226, 135, 67), 3)
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


# cap = cv2.VideoCapture('https://192.168.31.189:8080/video')
# cap = cv2.VideoCapture(CAMERANUMBER)
# cv2.namedWindow("Parameters")
# cv2.resizeWindow("Parameters", 640, 240)
# cv2.createTrackbar("Threshold1", "Parameters", TRACKBAR1, 255, empty)
# cv2.createTrackbar("Threshold2", "Parameters", TRACKBAR2, 255, empty)
# cv2.createTrackbar("Area", "Parameters", AREA, 30000, empty)


def getImageCoordinates():
    global hsv_img, upper, lower, cropping, x_start, y_start, x_end, y_end
    try:
        success, img = cap.read()
    except Exception as e:
        img = cv2.imread("assets/brain2.png")
    # img = cv2.imread('RedC.jpeg')
    # img = cv2.flip(img, 0)
    # img = cv2.flip(img, 1)
    img = crop(img)
    imgContour = img.copy()
    # # threshold1 = cv2.getTrackbarPos("Threshold1", "Parameters")
    # # threshold2 = cv2.getTrackbarPos("Threshold2", "Parameters")
    imgBlur = cv2.GaussianBlur(img, (7, 7), 3)
    hsv_img = cv2.cvtColor(imgBlur, cv2.COLOR_BGR2HSV)
    blackMask = cv2.inRange(hsv_img, (0, 0, 0), (164, 135, 108))
    redMask = cv2.inRange(hsv_img, (0, 110, 0), (180, 255, 255))
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


def adjustHSV(h_min, h_max, s_min, s_max, v_min, v_max):
    _, img = cap.read()
    # img = cv2.flip(img, 0)
    # img = cv2.flip(img, 1)
    img = crop(img)
    # img = cv2.imread('RedC.jpeg')
    imgHsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    # h_min = cv2.getTrackbarPos("HUE Min", "HSV")
    # h_max = cv2.getTrackbarPos("HUE Max", "HSV")
    # s_min = cv2.getTrackbarPos("SAT Min", "HSV")
    # s_max = cv2.getTrackbarPos("SAT Max", "HSV")
    # v_min = cv2.getTrackbarPos("VALUE Min", "HSV")
    # v_max = cv2.getTrackbarPos("VALUE Max", "HSV")

    lower = np.array([h_min, s_min, v_min])
    upper = np.array([h_max, s_max, v_max])
    mask = cv2.inRange(imgHsv, lower, upper)
    result = cv2.bitwise_and(img, img, mask=mask)

    mask = cv2.cvtColor(mask, cv2.COLOR_GRAY2BGR)
    # hStack = np.hstack([img, mask, result])
    # cv2.imshow('Original', img)
    # cv2.imshow('HSV Color Space', imgHsv)
    # cv2.imshow('Mask', mask)
    # cv2.imshow('Result', result)
    # cv2.imshow('Mask', mask)

    return (result, mask)


if __name__ == "__main__":
    while True:
        try:
            success, img = cap.read()
        except Exception as e:
            img = cv2.imread("assets/brain2.png")
        # img = cv2.imread('RedC.jpeg')
        # img = cv2.flip(img, 0)
        # img = cv2.flip(img, 1)
        # img = crop(img)
        imgContour = img.copy()
        # # threshold1 = cv2.getTrackbarPos("Threshold1", "Parameters")
        # # threshold2 = cv2.getTrackbarPos("Threshold2", "Parameters")
        imgBlur = cv2.GaussianBlur(img, (7, 7), 3)
        hsv_img = cv2.cvtColor(imgBlur, cv2.COLOR_BGR2HSV)
        blackMask = cv2.inRange(hsv_img, (0, 0, 0), (139, 223, 44))
        redMask = cv2.inRange(hsv_img, (0, 119, 0), (180, 255, 255))
        blueMask = cv2.inRange(hsv_img, (95, 105, 72), (103, 253, 200))
        bitwise1 = cv2.bitwise_or(blackMask, redMask)
        bitwise2 = cv2.bitwise_or(bitwise1,  blueMask)
        # colorMask = cv2.inRange(hsv_img, lower, upper)
        getContours(bitwise2, imgContour)
        cv2.imshow("Result", imgContour)
        cv2.setMouseCallback('Result', mouseClickHandler)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
