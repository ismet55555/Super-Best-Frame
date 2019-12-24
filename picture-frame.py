#!/usr/bin/env/python3

import sys
import os
import random
import cv2
import imutils
from math import floor, ceil
import numpy as np
import logging
from logging.handlers import RotatingFileHandler
import subprocess


###############################################################################

def create_logger():
    # Setting up logger and a local log file
    file_handler = logging.handlers.RotatingFileHandler(filename='picture-frame.log', mode='w', maxBytes=10000000, backupCount=0)
    stdout_handler = logging.StreamHandler(sys.stdout)
    logging.basicConfig(level=logging.INFO,
                        format='[Picture-Frame] - [%(asctime)s] - %(levelname)-10s - %(message)s',
                        datefmt='%d-%b-%y %H:%M:%S',
                        handlers=[file_handler, stdout_handler])

def get_screen_size():
    # Finding the size of the current screen
    processes = subprocess.Popen(["xrandr | grep '*'"],stdout=subprocess.PIPE, shell=True).stdout.read().decode('utf-8').strip().split(' ')
    # TODO: Detect a return of no display
    # Remove blanks and new line characters
    processes = [i for i in processes if (i and i != '\n')] 
    # Only find items containing "x" and get the first listed
    # TODO: Find a way to know where images are displayed
    processes = [i for i in processes if 'x' in i][0]
    # Split into width and height
    width_px = int(processes.split('x')[0])
    height_px = int(processes.split('x')[1])
    # TODO: Error handling
    return width_px, height_px

###############################################################################

def effect_none(img_end):
    cv2.imshow('Image', img_end)

def effect_fade(img_begin, img_end, len=10, fade_delay=1):
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


###############################################################################
###############################################################################


# Creating the logger for this python script
create_logger()
logging.info('Picture frame python script started')

# Finding the screen width and height
screen_width_px, screen_height_px = get_screen_size()
screen_aspect_ratio = screen_width_px / screen_height_px
logging.info('Display/Screen size determined:')
logging.info('    Width:        {}'.format(screen_width_px))
logging.info('    Height:       {}'.format(screen_height_px))
logging.info('    Aspect Ratio: {:.2f}'.format(screen_aspect_ratio))

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
logging.info('Mapping out all available image files in directory: {}'.format(imageDirectory))
for filename in os.listdir(imageDirectory):
    # Only consider files, not directories
    if os.path.isfile(imageDirectory + filename):
        # Add image path
        imagePaths.append(imageDirectory + filename)
        # Add the name of the image to an array
        imageNames.append(filename)
logging.info('Successfully mapped out {} images'.format(len(imagePaths)))

logging.info('Configuring full screen image window ...')
# Opening openCV window
cv2.namedWindow('Image', cv2.WND_PROP_FULLSCREEN)
# Setting up openCV window for full screen mode
cv2.setWindowProperty("Image", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

# Initializing beginning and ending image index
img_begin_index = -1
img_end_index = -1

logging.info('Beginning picture frame image rotation. Use SPACEBAR to quit ...')
try:
    while True:
        # Picking a random image from directory - Target
        random.seed()
        while img_end_index == img_begin_index:
            img_end_index = random.randint(0, len(imagePaths)-1)

        logging.info('Showing image index {} ("{}")'.format(img_end_index, imageNames[img_end_index]))

        # Load the starting image images
        if img_begin_index == -1:
            imageFileObject_begin = np.zeros((4000, 6000, 3), np.uint8)
        else:
            imageFileObject_begin = cv2.imread(imagePaths[img_begin_index], cv2.IMREAD_UNCHANGED)
        img_begin_aspect_ratio = imageFileObject_begin.shape[1] / imageFileObject_begin.shape[0]

        # Loading the ending image
        imageFileObject_end = cv2.imread(imagePaths[img_end_index], cv2.IMREAD_UNCHANGED)
        img_end_aspect_ratio = imageFileObject_end.shape[1] / imageFileObject_end.shape[0]

        # Resize and grow into screen
        if screen_aspect_ratio > 1:
            # Landscape screen orientation
            # Resize to screen height
            imageFileObject_begin = imutils.resize(imageFileObject_begin, height=screen_height_px)
            imageFileObject_end = imutils.resize(imageFileObject_end, height=screen_height_px)

            # Finding the filler border size
            img_fill_border_begin = floor((screen_width_px - imageFileObject_begin.shape[1]) / 2)
            img_fill_border_begin = 0 if img_fill_border_begin < 0 else img_fill_border_begin
            img_fill_border_end = floor((screen_width_px - imageFileObject_end.shape[1]) / 2)
            img_fill_border_end = 0 if img_fill_border_end < 0 else img_fill_border_end

            # Add the border
            imageFileObject_begin = cv2.copyMakeBorder(imageFileObject_begin, top=0, bottom=0, left=img_fill_border_begin, right=img_fill_border_begin, borderType=cv2.BORDER_CONSTANT)
            imageFileObject_end = cv2.copyMakeBorder(imageFileObject_end, top=0, bottom=0, left=img_fill_border_end, right=img_fill_border_end, borderType=cv2.BORDER_CONSTANT) 

            # Account for slight difference when border is added
            avg_width = ceil((imageFileObject_begin.shape[1] + imageFileObject_end.shape[1]) / 2)
            avg_height = ceil((imageFileObject_begin.shape[0] + imageFileObject_end.shape[0]) / 2)

            # Resize to average dimensions
            imageFileObject_begin = imutils.resize(imageFileObject_begin, width=avg_width, height=avg_height)
            imageFileObject_end = imutils.resize(imageFileObject_end, width=avg_width, height=avg_height)
        else:
            # Portrait screen orientation
            # Resize to screen width
            imageFileObject_begin = imutils.resize(imageFileObject_begin, height=screen_width_px)
            imageFileObject_end = imutils.resize(imageFileObject_end, height=screen_width_px)

            # Finding the filler border size
            img_fill_border_begin = floor((screen_height_px - imageFileObject_begin.shape[0]) / 2)
            img_fill_border_begin = 0 if img_fill_border_begin < 0 else img_fill_border_begin
            img_fill_border_end = floor((screen_height_px - imageFileObject_end.shape[0]) / 2)
            img_fill_border_end = 0 if img_fill_border_end < 0 else img_fill_border_end

            # Add the border
            imageFileObject_begin = cv2.copyMakeBorder(imageFileObject_begin, top=img_fill_border_begin, bottom=img_fill_border_begin, left=0, right=0, borderType=cv2.BORDER_CONSTANT)
            imageFileObject_end = cv2.copyMakeBorder(imageFileObject_end, top=img_fill_border_end, bottom=img_fill_border_end, left=0, right=0, borderType=cv2.BORDER_CONSTANT) 

            # Account for slight difference when border is added
            avg_width = ceil((imageFileObject_begin.shape[1] + imageFileObject_end.shape[1]) / 2)
            avg_height = ceil((imageFileObject_begin.shape[0] + imageFileObject_end.shape[0]) / 2)

            # Resize to average dimensions
            imageFileObject_begin = imutils.resize(imageFileObject_begin, width=avg_width, height=avg_height)
            imageFileObject_end = imutils.resize(imageFileObject_end, width=avg_width, height=avg_height)

        # Fade transition effect
        effect_fade(imageFileObject_begin, imageFileObject_end)

        # Waiting 2 seconds and watching out for key press to quit
        if cv2.waitKey(image_delay) == ord(' '):
            logging.info('SPACEBAR key detected. Exiting ...')
            break

        # The next beginning image is the last end image
        img_begin_index = img_end_index

except Exception as e:
    print(e)
    
finally:
    #Close all open openCV windows
    logging.info('Closing all open image windows')
    cv2.destroyAllWindows()

logging.info('Picture frame python application has ended')
