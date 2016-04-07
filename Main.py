#! python3

# Image Processing methods
from Processing_Utilities import *
# math library
import numpy
# picture library
from PIL import Image
# directories, access args
import os, sys, shutil
# parallelism library
from multiprocessing import Process

# if command line has too few argument, quit
if len(sys.argv) != 4:
    print("Incorrect Args")
    print("Input File Name, Frames/Sec, Resolution Factor")
    quit()

# make Directories:
# if directory for temporary image files
# exists, delete it to clear it, and create
# a new one
imageFilePath = os.path.join(".","ImageFiles")
if os.path.exists(imageFilePath):
    # rmtree use is acceptable here, for
    # this program will be the only
    # user of the created folder
    shutil.rmtree(imageFilePath)
os.makedirs(imageFilePath)

# if directory for temporary image files
# to use to write a new video from ffmpeg
# exists, delete it to clear it, and create
# a new one
writeImageFilePath = os.path.join(".","WriteImageFiles")
if os.path.exists(writeImageFilePath):
    # rmtree use is acceptable here, for
    # this program will be the only
    # user of the created folder
    shutil.rmtree(writeImageFilePath)
os.makedirs(writeImageFilePath)


# store the command line arguments in variables:

# tests whether the first command line arg is a valid file name,
# and exits the program if it is not
if isinstance(sys.argv[1], str) and os.path.exists(sys.argv[1]):
    input = sys.argv[1]
else:
    print("Incorrect File name/Does not Exist")
    quit()

# frameRate should be an int or float
frameRate = sys.argv[2]


# resolution should be from 0 to 1
resolution = sys.argv[3]

# TODO implement Threshold
# threshold from 0 to 255
# threshold = int(sys.argv[4])

resolutionCommand = " -vf scale=iw*" + resolution + ":ih*" + resolution

# the path to save the temporary files to
savePath = os.path.join(".","ImageFiles","output_%04d.jpg")
# the command to use ffmpeg
command = "./ffmpeg -i " + input + resolutionCommand + " -r " + frameRate + " " + savePath

# do the ffmpeg command to take the screenshots into
# the temporary file folder
os.system(command)


# start the image processing:
images = collectImages(imageFilePath)
print("Number of images: " + str(len(images)))


# turn the PIL images into numpy arrays
pixelMatrices = imageToMatrix(images)

# TODO implement normalization
# maxMinImage = []
# for image in pixelMatrices:
#     maxMinImage.append((image.max(), image.min()))


# subtract the matrices of pixels to remove static elements
backToImage = firstOrderListSubtraction(pixelMatrices)
# print("finished subtracting all matrices")

# TODO implement multiprocessing?
# multiThresholdLimit(backToImage)
# print("finished thresholding")

# path to save files for ffmpeg video creation
writePath = os.path.join(".","WriteImageFiles","img")


for x in range(len(backToImage)):
    # TODO implement better normalization
    # backToImage[x] = matrixNormalize(backToImage[x], int(maxMinImage[x][0]), int(maxMinImage[x][1]))
    backToImage[x] = matrixNormalize2(backToImage[x])


# return the subtracted arrays to PIL images, and save them in a temporary file
for x in range(len(backToImage)):
    Image.fromarray(backToImage[x], mode="RGB").save(writePath + ("%s.jpg" % (x + 1)).rjust(8, '0'), format="JPEG")

# name for output file
outputBase = os.path.basename(input)
output = os.path.splitext(outputBase)[0] + "_out.mp4"

# ffmpeg command to take images and create video
commandToVideo = "./ffmpeg -framerate 25 -start_number 0001 -i " + writePath + \
                 "%04d.jpg -c:v libx264 -r 30 -pix_fmt yuv420p " + output

# do command
os.system(commandToVideo)

# open created video
os.system("open " + output)

# clean out temporary files
shutil.rmtree(imageFilePath)
shutil.rmtree(writeImageFilePath)
quit()