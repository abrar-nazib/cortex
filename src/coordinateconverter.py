import math
baseArmLength = 6.8
shoulderArmLength = 10.4
elbowArmLength = 15.1


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
