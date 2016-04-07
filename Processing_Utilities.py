#! python3

from multiprocessing import Process
from PIL import Image
import os
import numpy

#takes images from a file and puts them into an array
def collectImages(filePath):
    # testing
    if not isinstance(filePath, str):
        raise TypeError("File path %s not acceptable") % (filePath)
        quit()
    # array to store images
    images = []
    # append images to array
    for fileName in os.listdir(filePath):
        currentFile = os.path.join(filePath, fileName)
        # open image files
        image = Image.open(currentFile)
        images.append(image)
    # return array of images
    return images


# takes array of PIL images
# outputs array of numpy matrices
def imageToMatrix(images):
    pixelMatrices = []
    for image in images:
        # turn the PIL images to numpy arrays
        pixelMatrices.append(numpy.asarray(image))
    return pixelMatrices

# kron products matrices in array, and
# returns the kron producted matrix
def kronArray(pixelMatrices):
    # declare matrix
    kronMatrix = []
    # throwaway int to prepare kronMatrix variable
    i = 0
    for matrix in pixelMatrices:
        # put first pixel matrix into kronMatrix variable
        # to prepare for kron products
        if len(kronMatrix) == 0:
            kronMatrix.append(matrix)
            i += 1
            continue
        # otherwise do kron products
        kronMatrix[0] = numpy.kron(kronMatrix[0], matrix)
    return kronMatrix[0]

# subtract matrices in array two by two
def firstOrderListSubtraction(matrices):
    subtractedMatrices = []
    # subtract matrices
    for x in range(len(matrices)):
        # hit end of matrix array and finish
        if x == len(matrices) - 1:
            break
        # otherwise subtract matrices
        subtractedMatrices.append(matrices[x] - matrices[x + 1])
    return subtractedMatrices

# normalization with given high and low values
def matrixNormalize(matrix, high, low):
    numpy.divide(matrix, 1/matrix.max(), matrix, casting="unsafe")
    numpy.multiply(matrix, high - low, matrix, casting="unsafe")
    numpy.add(matrix, low, matrix, casting="unsafe")
    return matrix

# normalization ignoring previous high/low values
def matrixNormalize2(matrix):
    numpy.multiply(matrix, 255/matrix.max(), matrix, casting="unsafe")
    return matrix


# Magnitude threshold to zero to wipe out low numbers
def thresholdLimit1(matrixArray, threshold):
    for image in matrixArray:
        for index, cell in numpy.ndenumerate(image):
            if abs(cell) < threshold:
                image[index] = 0
    return;

# threshold to zero to wipe out low numbers
def thresholdLimit2(matrixArray, threshold):
    for image in matrixArray:
        for index, cell in numpy.ndenumerate(image):
            if cell < threshold:
                image[index] = 0
    return;

# magnitude threshold to zero to wipe out low numbers with flipping
def thresholdLimit3(matrixArray, threshold):
    for image in matrixArray:
        for index, cell in numpy.ndenumerate(image):
            if abs(cell) < threshold:
                image[index] = 0
            else:
                image[index] = 200
    return;

# multiprocessing threshold to zero to wipe out low numbers
def multiThresholdLimit(matrixArray, threshold):
    if __name__ == '__main__':
        for matrix in matrixArray:
            p = Process(target=singleThresholdLimit, args=(matrix,threshold))
            p.start()
            p.join(30)
    return;

# multiprocessing helper function
def singleThresholdLimit(matrix, threshold):
    for index, cell in numpy.ndenumerate(matrix):
        if abs(cell) < threshold:
            matrix[index] = 0
        else:
            matrix[index] = 200
    return;
