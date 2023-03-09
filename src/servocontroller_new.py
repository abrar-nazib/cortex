from pyfirmata import Arduino, SERVO
import time
import math
import coordinateconverter

PORT = "COM3"


def connect(port):
    try:
        global board
        board = Arduino(port)
        return True
    except Exception as e:
        print(e)
        return False


class ServoMotor:
    __name = "Servo"
    __initAngle = 90
    __angle = 90
    __range = (0, 180)
    __mapRange = (0, 180)
    __angleCorrection = 0
    __pin = 2

    def __init__(self, board: Arduino):
        self.board = board
        pass

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, name):
        self.__name = name

    @property
    def initAngle(self):
        return self.__initAngle

    @initAngle.setter
    def initAngle(self, angle):
        if self.__range[0] <= angle <= self.__range[1]:
            self.__initAngle = angle

    def rotateServo(self, angle):
        board.digital[self.__pin].write(angle)

    @staticmethod
    def map_range(x, in_min, in_max, out_min, out_max):
        return (x - in_min) * (out_max - out_min) // (in_max - in_min) + out_min
