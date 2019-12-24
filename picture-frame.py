#!/usr/bin/env/python3

import sys
import os
import random
import cv2
import numpy as np


def effect_none(img_end):
    cv2.imshow('Image', img_end)

def effect_fade_in(img_begin, img_end, len=10, fade_delay=1):
    fading = True
    while fading:
        for index in range(0, len):
            fade_in_radio = index/float(len)
            mergedImageFrame = cv2.addWeighted(img_begin, 1 - fade_in_radio, img_end, fade_in_radio, 0)
            cv2.imshow('Image', mergedImageFrame)
            if cv2.waitKey(fade_delay) == ord(' '):
                fading = False
                break
        cv2.imshow('Image', img_end)
        fading = False


# SCREEN SIZE: xrandr | grep '*'

def effect_fade_in_2(image1, image2):

    foreground, background = image1.copy(), image2.copy()

    foreground_height = foreground.shape[0]
    foreground_width = foreground.shape[1]
    alpha = 0.5

    # do composite on the upper-left corner of background image.
    blended_portion = cv2.addWeighted(foreground,
                alpha,
                background[:foreground_height,:foreground_width,:],
                1 - alpha,
                0,
                background)
    background[:foreground_height,:foreground_width,:] = blended_portion
    cv2.imshow('Image', background)

    input('asdf')


print('===================')
print('Start')
print('')


# Image delay
image_delay = 3000

# Set up current directory path
currentDirectory = os.path.abspath(os.path.dirname(sys.argv[0])) 

# Path for images
imageDirectory  = "Images"
imageDirectory  = os.path.join(currentDirectory, imageDirectory) + "//"

# Array of opencv image objects
imageNames = []
imagePaths = []

# Map out through all images in the directory
for filename in os.listdir(imageDirectory):
    # Only consider files, not directories
    if os.path.isfile(imageDirectory + filename):
        # Add image path
        imagePaths.append(imageDirectory + filename)
        # Add the name of the image to an array
        imageNames.append(filename)


# Opening openCV window
cv2.namedWindow('Image', cv2.WND_PROP_FULLSCREEN)
# Setting up openCV window for full screen mode
cv2.setWindowProperty("Image", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

#TODO: imshow a screen size blank image

# Beginning image index
img_begin_index = -1
img_end_index = -1

# try:
while True:
    # Picking a random image from directory - Target
    random.seed()
    while img_end_index == img_begin_index:
        img_end_index = random.randint(0, len(imagePaths)-1)

    print('------')
    print(img_begin_index, img_end_index)

    # print('Showing Image {} of {} ({})'.format(img_end_index, len(imagePaths), imageNames[img_end_index]))

    # Load the starting image images
    if img_begin_index == -1:
        imageFileObject_begin = np.zeros((4000, 6000, 3), np.uint8)
    else:
        imageFileObject_begin = cv2.imread(imagePaths[img_begin_index], cv2.IMREAD_UNCHANGED)

    # Loading the ending image
    imageFileObject_end = cv2.imread(imagePaths[img_end_index], cv2.IMREAD_UNCHANGED)

    # Fade transition effect
    effect_fade_in(imageFileObject_begin, imageFileObject_end)

    # Waiting 2 seconds and watching out for key press to quit
    if cv2.waitKey(image_delay) == ord(' ') :
        break

    # The next beginning image is the last end image
    img_begin_index = img_end_index

# except Exception as e:
#     print(e)
    
# finally:
#Close all open openCV windows
cv2.destroyAllWindows()

print('')
print('DONE!')
print('===================')
