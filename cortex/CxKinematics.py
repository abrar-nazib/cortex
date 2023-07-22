import math
import matplotlib.pyplot as plt
import numpy as np
from typing import List
import time

np.set_printoptions(precision=3, suppress=True)

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




def d(angle: float):
    return angle*np.pi/180


class Frame:
    def __init__(self,parent=None, relative_position=[0,0,0]):
        self.parent = parent
        if(parent != None):
            self.parent.child = self
        self.homogeneousMatrix = np.array([
            [1, 0, 0, 0],
            [0, 1, 0, 0],
            [0, 0, 1, 0],
            [0, 0, 0, 1]
        ])
        self.position_matrix = np.array([
            [1, 0, 0, relative_position[0]],
            [0, 1, 0, relative_position[1]] ,
            [0, 0, 1, relative_position[2]],
            [0, 0, 0, 1]
        ])
            
        if(parent != None):
            self.homogeneousMatrix_global = np.matmul(np.matmul(self.homogeneousMatrix, self.position_matrix), self.parent.homogeneousMatrix_global)
            # print(self.homogeneousMatrix_global)
        else:
            self.homogeneousMatrix_global = np.copy(self.homogeneousMatrix)        
        
        self.child = None
        
        
        self.axis_x_init = np.copy(self.homogeneousMatrix)
        self.axis_x_init[0, 3] = 2
        self.axis_x_init[1, 3] = 0
        self.axis_x_init[2, 3] = 0
        self.axis_x = np.copy(self.axis_x_init)
        
        self.axis_y_init = np.copy(self.homogeneousMatrix)
        self.axis_y_init[0, 3] = 0
        self.axis_y_init[1, 3] = 2
        self.axis_y_init[2, 3] = 0
        self.axis_y = np.copy(self.axis_y_init)
        
        self.axis_z_init = np.copy(self.homogeneousMatrix)
        self.axis_z_init[0, 3] = 0
        self.axis_z_init[1, 3] = 0
        self.axis_z_init[2, 3] = 2        
        self.axis_z = np.copy(self.axis_z_init)
        
        self.set_axes()
        
        self.x_angle = 0
        self.y_angle = 0
        self.z_angle = 0
        

    
    def multiply(self, matrix):
        self.homogeneousMatrix = np.matmul(matrix, self.homogeneousMatrix_init)
        self.set_axes()

    def rotate_x(self, theta):
        rotationHomogenousMatrix = np.array([
            [1, 0, 0, 0],
            [0, np.cos(d(theta)), -np.sin(d(theta)), 0],
            [0, np.sin(d(theta)), np.cos(d(theta)), 0],
            [0, 0, 0, 1]
            ])
        self.homogeneousMatrix = np.matmul(self.homogeneousMatrix, rotationHomogenousMatrix)
        if(self.parent != None):
            elevationMatrix = np.matmul(self.parent.homogeneousMatrix_global, self.position_matrix)
            rotatedMatrix = np.matmul(elevationMatrix, self.homogeneousMatrix)
            self.homogeneousMatrix_global = np.copy(rotatedMatrix)
        else:
            self.homogeneousMatrix_global = np.matmul(self.homogeneousMatrix_global, rotationHomogenousMatrix)        
        
        self.set_axes()
        self.x_angle += theta
        self.update_children()


    def rotate_y(self, theta):
        rotationHomogenousMatrix = np.array([
            [np.cos(d(theta)), 0, np.sin(d(theta)), 0],
            [0, 1, 0, 0],
            [-np.sin(d(theta)), 0, np.cos(d(theta)), 0],
            [0, 0, 0, 1]
            ])
        self.homogeneousMatrix = np.matmul(rotationHomogenousMatrix, self.homogeneousMatrix)
        
        self.homogeneousMatrix = np.matmul(self.homogeneousMatrix, rotationHomogenousMatrix)
        if(self.parent != None):
            elevationMatrix = np.matmul(self.parent.homogeneousMatrix_global, self.position_matrix)
            rotatedMatrix = np.matmul(elevationMatrix, self.homogeneousMatrix)
            self.homogeneousMatrix_global = np.copy(rotatedMatrix)
        else:
            self.homogeneousMatrix_global = np.matmul(self.homogeneousMatrix_global, rotationHomogenousMatrix)


        self.set_axes()
        self.y_angle += theta
        self.update_children()
    
    def rotate_z(self, theta):
        rotationHomogenousMatrix = np.array([
            [np.cos(d(theta)), -np.sin(d(theta)), 0, 0],
            [np.sin(d(theta)), np.cos(d(theta)), 0, 0],
            [0, 0, 1, 0],
            [0, 0, 0, 1]
        ])
        self.homogeneousMatrix = np.matmul(self.homogeneousMatrix, rotationHomogenousMatrix)
        if(self.parent != None):
            elevationMatrix = np.matmul(self.parent.homogeneousMatrix_global, self.position_matrix)
            rotatedMatrix = np.matmul(elevationMatrix, self.homogeneousMatrix)
            self.homogeneousMatrix_global = np.copy(rotatedMatrix)
        else:
            self.homogeneousMatrix_global = np.matmul(self.homogeneousMatrix_global, rotationHomogenousMatrix)
            
        self.set_axes()
        self.z_angle += theta
        self.update_children()

    def update_global_matrix(self):
        rotationHomogenousMatrix = np.array([
            [1, 0, 0, 0],
            [0, 1, 0, 0],
            [0, 0, 1, 0],
            [0, 0, 0, 1]
        ])
        self.homogeneousMatrix = np.matmul(self.homogeneousMatrix, rotationHomogenousMatrix)
        if(self.parent != None):
            elevationMatrix = np.matmul(self.parent.homogeneousMatrix_global, self.position_matrix)
            rotatedMatrix = np.matmul(elevationMatrix, self.homogeneousMatrix)
            self.homogeneousMatrix_global = np.copy(rotatedMatrix)
        else:
            self.homogeneousMatrix_global = np.matmul(self.homogeneousMatrix_global, rotationHomogenousMatrix)
        self.set_axes()


    def set_axes(self):
        # Set the axes accordingly as they depend on the frame
        self.axis_x = np.matmul(self.homogeneousMatrix_global, self.axis_x_init)
        self.axis_y = np.matmul(self.homogeneousMatrix_global, self.axis_y_init)
        self.axis_z = np.matmul(self.homogeneousMatrix_global, self.axis_z_init)
        
    def get_child(self):
        return self.child
    
    def update_children(self):
        if(self.child != None):
            self.child.update_global_matrix()
            self.child.update_children()
        return
    
    def print_all(self):
        print("Homogeneous Matrix")
        print(self.homogeneousMatrix)
        
        print("Axis X")
        print(self.axis_x)
        
        print("Axis Y")
        print(self.axis_y)
        
        print("Axis Z")
        print(self.axis_z)
    
    def get_positions(self):
        frame_pos = self.homogeneousMatrix_global[0:3, 3]
        axis_x_pos = self.axis_x[0:3, 3]
        axis_y_pos = self.axis_y[0:3, 3]
        axis_z_pos = self.axis_z[0:3, 3]
        
        return (
            frame_pos,
            axis_x_pos,
            axis_y_pos,
            axis_z_pos
        )
    
    def set_x_angle(self, angle):
        # Rotate the frame to the desired angle from previous angle
        self.rotate_x(angle - self.x_angle)

    
    def set_y_angle(self, angle):
        # Rotate the frame to the desired angle from previous angle
        self.rotate_y(angle - self.y_angle)
    
    def set_z_angle(self, angle):
        # Rotate the frame to the desired angle from previous angle
        self.rotate_z(angle - self.z_angle)
           

    

class Arm:
    def __init__():
        pass
 
if __name__ == "__main__":
    frame = Frame()
    for i in range(0, 90):
        frame.rotate_z(-1)
        print(frame.get_positions())