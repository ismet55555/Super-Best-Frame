#!/usr/bin/env python3

import sys
import os
import random
import cv2
import imutils
from math import floor, ceil
import numpy as np
import logging

from app import temp_data
from app import effects  # Image transition effects
from app import utility  # Useful and custom functions


###############################################################################

def slideshow_thread():
    # Supported image file extensions
    # TODO: Load from app/config/img_formats.yml
    supported_formats = ['.png', '.jpg', '.jpeg', '.bmp', '.dib', '.jpe', '.jp2', '.pgm', '.tiff', '.tif', '.ppm']

    # Finding the screen width and height
    screen_width_px, screen_height_px = utility.get_screen_size()
    # Finding the aspact ratio
    screen_aspect_ratio = screen_width_px / screen_height_px
    logging.info('Display/Screen size determined:')
    logging.info('    Width:        {}'.format(screen_width_px))
    logging.info('    Height:       {}'.format(screen_height_px))
    logging.info('    Aspect Ratio: {:.2f}'.format(screen_aspect_ratio))

    # Image delay
    # TODO: Load from configurations: app/config/defaults.yml
    image_delay = 1500

    # Set up current directory path
    currentDirectory = os.path.abspath(os.path.dirname(sys.argv[0])) 
    print(currentDirectory)

    # Path for images
    imageDirectory  = "Images"  # TODO: Load from configurations: app/config/defaults.yml
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

    # Destroy any open windows, if any
    cv2.destroyAllWindows()

    logging.info('Configuring full screen image window ...')
    

    #############################
    # FIX ME: Stuck the second time around!!!
    #############################


    # Opening openCV window
    print('ok')
    cv2.namedWindow('Image', cv2.WND_PROP_FULLSCREEN)
    # Setting up openCV window for full screen mode
    print('ok2')
    cv2.setWindowProperty("Image", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

    # Initializing beginning and ending image index
    img_begin_index = -1
    img_end_index = -1

    print('')
    logging.info('Beginning picture frame image rotation. Use SPACEBAR to quit ...')
    error = None
    try:
        while True and not temp_data.slideshow_thread_stop:
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
            imageFileObject_begin = utility.process_fit_image(imageFileObject_begin, screen_width_px, screen_height_px)
            imageFileObject_end = utility.process_fit_image(imageFileObject_end, screen_width_px, screen_height_px)

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
                effects.effect_fade(imageFileObject_begin, imageFileObject_end)
            elif effect_index == 1:
                # Slide transition effect
                effects.effect_slide(imageFileObject_begin, imageFileObject_end, 'right', screen_width_px, screen_height_px)
            else:
                # Zoom in transition effect
                effects.effect_zoom_out(imageFileObject_begin, imageFileObject_end)

            # Waiting and watching out for key press to quit
            if cv2.waitKey(image_delay) == ord(' '):
                print('')
                logging.info('SPACEBAR key detected. Exiting ...')
                break  # Stopping program

            # The next beginning image is the last end image
            img_begin_index = img_end_index

    except Exception as error:
        logging.critical(error)
        
    finally:
        #Close all open openCV windows
        logging.info('Closing all open image windows')
        cv2.destroyWindow('Image')
        cv2.destroyAllWindows()

        temp_data.slideshow_thread_stop = True
        temp_data.slideshow_thread = None

