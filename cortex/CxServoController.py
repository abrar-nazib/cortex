import time
import math
import coordinateconverter
import serial

PORT = "/dev/ttyACM0"
INITIALANGLES = [90, 210, 45]
GRABANGLE = 156
ANGLECORRECTIONS = [11, 0, 3]
SERVOPINS = [9, 10, 11, 6]


def connect(port=PORT):

    global board
    try:
        board = serial.Serial(port, 115200)
        time.sleep(1)
        return True
    except Exception as e:
        print(e)
        time.sleep(1)
        return False


def map_range(x, in_min, in_max, out_min, out_max):
    return (x - in_min) * (out_max - out_min) // (in_max - in_min) + out_min


# def rotateServo(pin, angle):
#     if (0 <= angle <= 180):
#         board.digital[pin].write(angle)
    # time.sleep(0.015)


def sendData(servo1Angle, servo2Angle, servo3Angle):
    # if (servo1Angle > 90):
    #     servo1Angle = servo1Angle + 3
    # if (servo1Angle < 90):
    #     servo1Angle = servo1Angle - 3
    # rotateServo(SERVOPINS[0], map_range(
    #     (servo1Angle + ANGLECORRECTIONS[0]), 0, 180, 0, 153))
    # if servo2Angle < 90:
    #     servo2Angle = 90
    # if servo2Angle > 250:
    #     servo2Angle = 250
    # rotateServo(SERVOPINS[1], map_range(
    #     (servo2Angle - 90+ANGLECORRECTIONS[1]), 0, 180, 0, 153))
    # if (servo3Angle < 40):
    #     servo3Angle = 40
    # rotateServo(SERVOPINS[2], map_range(
    #     (servo3Angle-45+ANGLECORRECTIONS[2]), 0, 180, 0, 160))
    transmissionString = f"{servo1Angle}:{servo2Angle}:{servo3Angle}\n"

    board.write(transmissionString.encode())
    time.sleep(0.001)


def guiControl(servo1Angle, servo2Angle, servo3Angle, servo4Angle):
    sendData(servo1Angle, servo2Angle, servo3Angle)
    # rotateServo(SERVOPINS[3], servo4Angle)
    # time.sleep(0.01)


def drawFromCoordinates(coordinate, previousCoordinate):
    servoAngles = coordinateconverter.convertCoordstoAngles(coordinate)
    if (math.dist(coordinate, previousCoordinate) > 0.2):
        previousAngles = coordinateconverter.convertCoordstoAngles(
            previousCoordinate)
        stabilizeAngles(servoAngles, previousAngles)
    else:
        sendData(servoAngles[0], servoAngles[1], servoAngles[2])
        time.sleep(0.05)


def stabilizeAngles(servoAngles, previousAngles):
    smoothAngleExecution([previousAngles[0], previousAngles[1], previousAngles[2]],
                         [previousAngles[0], previousAngles[1] + 25, previousAngles[2]+25])

    smoothAngleExecution([previousAngles[0], previousAngles[1] + 25, previousAngles[2] + 25],
                         [servoAngles[0], servoAngles[1] + 25, servoAngles[2]+25])

    smoothAngleExecution([servoAngles[0], servoAngles[1] + 25, servoAngles[2]+25],
                         [servoAngles[0], servoAngles[1], servoAngles[2]])


def smoothAngleExecution(previousAngles, targetAngles):
    distances = []
    distances.append(targetAngles[0] - previousAngles[0])
    distances.append(targetAngles[1] - previousAngles[1])
    distances.append(targetAngles[2] - previousAngles[2])

    servo1Angle = previousAngles[0]
    servo2Angle = previousAngles[1]
    servo3Angle = previousAngles[2]

    sendData(servo1Angle, servo2Angle, servo3Angle)
    for i in range(0, 91, 1):
        servo1Angle = int(previousAngles[0] +
                          distances[0] * math.sin(math.radians(i)))
        servo2Angle = int(previousAngles[1] +
                          distances[1] * math.sin(math.radians(i)))
        servo3Angle = int(previousAngles[2] +
                          distances[2] * math.sin(math.radians(i)))
        sendData(servo1Angle, servo2Angle, servo3Angle)
        time.sleep(0.02)
    return [servo1Angle, servo2Angle, servo3Angle]


def down(previousAngles, targetAngles):
    distances = []
    distances.append(targetAngles[0] - previousAngles[0])
    distances.append((targetAngles[1] - previousAngles[1])/2)
    distances.append(targetAngles[2] - previousAngles[2])

    presentAngles = smoothAngleExecution(previousAngles, [
        targetAngles[0], previousAngles[1] + distances[1], targetAngles[2]])
    smoothAngleExecution(presentAngles, targetAngles)


def up(previousAngles, targetAngles):
    distances = []
    distances.append((targetAngles[0] - previousAngles[0]))
    distances.append(targetAngles[1] - previousAngles[1])
    distances.append(targetAngles[2] - previousAngles[2])

    presentAngles = smoothAngleExecution(previousAngles, [
        previousAngles[0], (previousAngles[1] + distances[1]/2), previousAngles[2]])
    smoothAngleExecution(presentAngles, targetAngles)


def angleTest(servoPin):
    sendData(INITIALANGLES[0], INITIALANGLES[1], INITIALANGLES[2])
    while True:
        angle = int(input("angle: "))
        # rotateServo(pin, map_range(angle, 0, 180, 0, 150))
        # rotateServo(servoPin, angle)
        time.sleep(0.01)


def grabObject():
    for i in range(120, GRABANGLE, 1):
        # rotateServo(SERVOPINS[3], i)
        time.sleep(0.03)


def releaseObject():
    for i in range(GRABANGLE, 120, -1):
        # rotateServo(SERVOPINS[3], i)
        time.sleep(0.03)


def pickObject(coordinates):
    # releaseObject()
    # rotateServo(SERVOPINS[3], 120)
    targetAngles = coordinateconverter.convertCoordstoAngles(coordinates)
    # smoothAngleExecution(
    #     INITIALANGLES, targetAngles)
    down(INITIALANGLES, targetAngles)
    grabObject()
    time.sleep(0.1)
    up(targetAngles, INITIALANGLES)


def placeObject(coordinates):
    targetAngles = coordinateconverter.convertCoordstoAngles(coordinates)
    down(INITIALANGLES, targetAngles)
    releaseObject()
    time.sleep(0.1)
    up(targetAngles, INITIALANGLES)


# try:
#     connect(PORT)
# except Exception as e:
#     board = None

if (__name__ == "__main__"):
    connect()
    for i in range(180):
        guiControl(i, 90, 45, 0)
        time.sleep(0.01)
    pass

    # targetAngles = [116, 135, 59]

    #

    # releaseObject()
    # time.sleep(2)
    # while True:
    #     pickObject([-8, 13])
    #     placeObject([8, 5])
    #     pickObject([8, 5])
    #     placeObject([-8, 13])
    # angleTest(6)
