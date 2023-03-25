import math
import matplotlib.pyplot as plt
import numpy as np
from typing import List


baseArmLength = 6.8
shoulderArmLength = 10.4
elbowArmLength = 15.7


def convertCoordstoAngles(coordinate, Origin=[0, 0]):
    distanceFromOrigin = math.dist(coordinate, Origin)
    # print(int(distanceFromOrigin/30))
    servo1Angle = math.degrees(
        math.acos((coordinate[0]-Origin[0])/distanceFromOrigin))

    hypotenuse = math.sqrt(
        distanceFromOrigin*distanceFromOrigin + baseArmLength * baseArmLength)
    # print(hypotenuse)
    helperTheta1 = math.degrees(math.acos(baseArmLength / hypotenuse))

    nominator = (hypotenuse*hypotenuse) + (shoulderArmLength *
                                           shoulderArmLength) - (elbowArmLength * elbowArmLength)
    denominator = 2 * hypotenuse * shoulderArmLength

    helperTheta2 = math.degrees(math.acos(
        nominator/denominator
    ))
    # dunno why had to be minused from 180
    servo2Angle = (helperTheta1 + helperTheta2)
    nominator_2 = (elbowArmLength * elbowArmLength) + (shoulderArmLength *
                                                       shoulderArmLength) - (hypotenuse * hypotenuse)
    denominator_2 = 2 * elbowArmLength * shoulderArmLength

    servo3Angle = math.degrees(math.acos(
        nominator_2/denominator_2
    ))
    servoAngles = [servo1Angle, servo2Angle, servo3Angle]
    # print(helperTheta1)
    return servoAngles


def simulate_arm(servoAngles):
    ax = plt.axes(projection="3d")

    X = [0, 0, 0, 0]
    Y = [0, 0, shoulderArmLength, shoulderArmLength+elbowArmLength]
    Z = [0, baseArmLength, baseArmLength, baseArmLength]

    # ax.plot_surface(X, Y, Z, cmap="plasma")
    ax.plot(X, Y, Z, marker="o", markersize=10, linewidth=5)
    plt.xlim([-20, 20])
    plt.ylim([0, 30])
    # plasma is a color map scheme

    ax.set_xlabel("X")
    ax.set_ylabel("Y")
    ax.set_zlabel("Z")
    plt.show()


class Joint:
    """Robot Joint Link
    """

    def __init__(self, pos: List[float], child=None):
        self.child = child
        self.x = pos[0]
        self.y = pos[1]
        self.z = pos[2]
        self.xy = 0
        self.yz = 0

    def rotatexy(self, angle: float):
        self.dist = math.sqrt((self.x - self.child.x)**2 +
                              (self.y - self.child.y)**2+(self.z - self.child.z)**2)

    def roateyz(self, degree: float):
        self.dist = math.sqrt((self.x - self.child.x)**2 +
                              (self.y - self.child.y)**2+(self.z - self.child.z)**2)


class Arm:
    def __init__(self, ):
        pass


simulate_arm(1)
