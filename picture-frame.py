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
    """
    TODO
    """
    # Setting up logger and a local log file
    file_handler = logging.handlers.RotatingFileHandler(filename='picture-frame.log', mode='w', maxBytes=10000000, backupCount=0)
    stdout_handler = logging.StreamHandler(sys.stdout)
    logging.basicConfig(level=logging.INFO,
                        format='[Picture-Frame] - [%(asctime)s] - %(levelname)-10s - %(message)s',
                        datefmt='%d-%b-%y %H:%M:%S',
                        handlers=[file_handler, stdout_handler])

def get_screen_size():
    """
    TODO
    """
    #Display number
    display_number = 0
    # Finding the size of the current screen
    processes = subprocess.Popen(["xrandr | grep '*'"],stdout=subprocess.PIPE, shell=True).stdout.read().decode('utf-8').strip().split(' ')
    # TODO: Detect a return of no display
    # Remove blanks and new line characters
    processes = [i for i in processes if (i and i != '\n')] 
    # Only find items containing "x" and get the first listed
    # TODO: Find a way to know where images are displayed
    processes = [i for i in processes if 'x' in i][display_number]
    # Split into width and height
    width_px = int(processes.split('x')[0])
    height_px = int(processes.split('x')[1])
    # TODO: Error handling
    return width_px, height_px

###############################################################################

def effect_none(img_end):
    """
    TODO
    """
    cv2.imshow('Image', img_end)

def effect_fade(img_begin, img_end, len=20, delay=5):
    """
    TODO
    """
    # NOTE: Images must be the same pixel dimensions
    changing = True
    while changing:
        for index in range(0, len):
            fade_in_radio = index/float(len)
            mergedImageFrame = cv2.addWeighted(img_begin, 1 - fade_in_radio, img_end, fade_in_radio, 0)
            cv2.imshow('Image', mergedImageFrame)
            cv2.waitKey(delay)
        cv2.imshow('Image', img_end)
        changing = False

def effect_slide(img_begin, img_end, direction, screen_width_px, screen_height_px, len=10, delay=2):
    """
    TODO
    """
    # NOTE: Images must be the same pixel dimensions

    # Combine the image horizontally
    img_combined = np.hstack((img_end, img_begin))

    # Slideing the images
    changing = True
    while changing:
        for i in range(screen_width_px, 0, -20):
            xi = i
            xf = screen_width_px + i
            yi = 0
            yf = screen_height_px
            img_cropped = img_combined[yi:yf, xi:xf]
            cv2.imshow('Image', img_cropped)
            cv2.waitKey(delay)
        changing = False

def effect_zoom_out(img_begin, img_end, len=20, delay=1):
    """
    TODO
    """
    # NOTE: Images must be the same pixel dimensions
    img_width_init = img_begin.shape[1]
    img_height_init = img_begin.shape[0]
    changing = True
    while changing:
        for i in range(0, len):
            crop_percent = i/float(len)  # Percent to crop
            xi = int(crop_percent * (img_width_init / 2))
            xf = int(img_width_init - (crop_percent * (img_width_init / 2)))
            yi = int(crop_percent * (img_height_init / 2))
            yf = int(img_height_init - (crop_percent * (img_height_init / 2)))
            img_cropped = img_begin[yi:yf, xi:xf]
            cv2.imshow('Image', img_cropped)
            cv2.waitKey(delay)
        cv2.imshow('Image', img_end)
        changing = False




###############################################################################

def process_fit_image(image, screen_width_px, screen_height_px):
    """
    TODO
    """
    screen_aspect_ratio = screen_width_px / screen_height_px

    if screen_aspect_ratio > 1:
        # Landscape
        screen_dim = screen_height_px
        image_shape_index = 1  # Image width
    else:
        # Portrait
        screen_dim = screen_width_px
        image_shape_index = 0  # Image height

    # Resize to screen
    image = imutils.resize(image, height=screen_dim)
    # Finding the filler border size
    img_fill_border_begin = floor((screen_width_px - image.shape[image_shape_index]) / 2)

    # Detrimine where to place the border filler addition
    top = bottom = left = right = 0
    if screen_aspect_ratio > 1:
        # Landscape
        left = img_fill_border_begin
        right = img_fill_border_begin
    else:
        # Portrait
        bottom = img_fill_border_begin
        top = img_fill_border_begin
        
    # Add the border filler to the image
    image = cv2.copyMakeBorder(image, top=top, bottom=bottom, left=left, right=right, borderType=cv2.BORDER_CONSTANT)

    return image


###############################################################################
###############################################################################


# Supported image file extensions
supported_formats = ['.png', '.jpg', '.jpeg', '.bmp', '.dib', '.jpe', '.jp2', '.pgm', '.tiff', '.tif', '.ppm']


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
image_delay = 1500

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

print('')
logging.info('Beginning picture frame image rotation. Use SPACEBAR to quit ...')
try:
    while True:
        # Picking a random image from directory - Target
        random.seed()
        while img_end_index == img_begin_index:
            img_end_index = random.randint(0, len(imagePaths)-1)

        # Load the starting image images
        if img_begin_index == -1:
            imageFileObject_begin = np.zeros((4000, 6000, 3), np.uint8)
        else:
            imageFileObject_begin = cv2.imread(imagePaths[img_begin_index], cv2.IMREAD_UNCHANGED)
        img_begin_aspect_ratio = imageFileObject_begin.shape[1] / imageFileObject_begin.shape[0]

        # Loading the ending image
        imageFileObject_end = cv2.imread(imagePaths[img_end_index], cv2.IMREAD_UNCHANGED)
        img_end_aspect_ratio = imageFileObject_end.shape[1] / imageFileObject_end.shape[0]

        logging.info('Showing image "{}" (Index: {}, Size: {}x{})'.format(imageNames[img_end_index], img_end_index, imageFileObject_end.shape[1], imageFileObject_end.shape[0]))

        # Process the beginning and ending image
        imageFileObject_begin = process_fit_image(imageFileObject_begin, screen_width_px, screen_height_px)
        imageFileObject_end = process_fit_image(imageFileObject_end, screen_width_px, screen_height_px)

        # Account for slight difference when border is added
        avg_width = ceil((imageFileObject_begin.shape[1] + imageFileObject_end.shape[1]) / 2)
        avg_height = ceil((imageFileObject_begin.shape[0] + imageFileObject_end.shape[0]) / 2)

        # Resize to average dimensions
        imageFileObject_begin = imutils.resize(imageFileObject_begin, width=avg_width, height=avg_height)
        imageFileObject_end = imutils.resize(imageFileObject_end, width=avg_width, height=avg_height)

        # Pick a random effect
        random.seed()
        effect_index = random.randint(0, 2)

        if effect_index == 0:
            # Fade transition effect
            effect_fade(imageFileObject_begin, imageFileObject_end)
        elif effect_index == 1:
            # Slide transition effect
            effect_slide(imageFileObject_begin, imageFileObject_end, 'right', screen_width_px, screen_height_px)
        else:
            # Zoom in transition effect
            effect_zoom_out(imageFileObject_begin, imageFileObject_end)

        # Waiting and watching out for key press to quit
        if cv2.waitKey(image_delay) == ord(' '):
            print('')
            logging.info('SPACEBAR key detected. Exiting ...')
            break  # Stopping program

        # The next beginning image is the last end image
        img_begin_index = img_end_index

except Exception as e:
    print(e)
    
finally:
    #Close all open openCV windows
    logging.info('Closing all open image windows')
    cv2.destroyAllWindows()

logging.info('Picture frame python application has ended')
