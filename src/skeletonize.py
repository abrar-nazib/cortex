from cv2 import threshold, imread, imshow, resize, THRESH_BINARY_INV, cvtColor, COLOR_BGR2GRAY, waitKey
from skimage.morphology import skeletonize
from skimage.color import rgb2gray
import matplotlib.pyplot as plt
import numpy as np
# from skimage import data
# from skimage.io import imread, imshow
# from skimage.util import invert


def skeletonizeImage(imgLocation):
    image = imread(imgLocation)
    image = resize(image, (600, 600))

    ret, invertedBinimage = threshold(image, 127, 255, THRESH_BINARY_INV)

    # perform skeletonization
    skeleton = skeletonize(invertedBinimage)

    # Coordinate Store in list
    coordinates = []
    for y in range(0, skeleton.shape[0]):
        for x in range(0, skeleton.shape[1]):
            if skeleton[y][x][0] == 0 and skeleton[y][x][1] == 255 and skeleton[y][x][2] == 0:
                coordinates.append([x, y])
    sortedCoordinates = generateSortedCoordinates(coordinates)
    return sortedCoordinates


def generateSortedCoordinates(unsortedCoordinates):
    origin = np.array((0, 0))
    distances = np.linalg.norm(unsortedCoordinates-origin, axis=1)
    min_index = np.argmin(distances)
    initialPoint = unsortedCoordinates[min_index]
    unsortedCoordinates = np.delete(unsortedCoordinates, min_index, 0)
    sorted_array = [initialPoint]
    for element in unsortedCoordinates:
        origin = initialPoint
        distances = np.linalg.norm(unsortedCoordinates-origin, axis=1)
        min_index = np.argmin(distances)
        initialPoint = unsortedCoordinates[min_index]
        sorted_array.append(initialPoint)
        unsortedCoordinates = np.delete(unsortedCoordinates, min_index, 0)
    sortedList = convertToList(sorted_array)
    return sortedList
    # return sorted_array


def convertToList(sortedArray):
    convertedList = []
    for element in sortedArray:
        unitelement = []
        unitelement.append(int(element[0]))
        unitelement.append(int(element[1]))
        convertedList.append(unitelement)
    return convertedList


if __name__ == "__main__":
    print(skeletonizeImage("images/h.jpg"))
