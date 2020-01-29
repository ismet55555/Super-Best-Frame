#!/usr/bin/env python3

import sys
import os
import random
import cv2
import imutils
from math import ceil
import numpy as np
import logging
import requests

from app import effects  # Image transition effects
from app import utility  # Useful and custom functions

###############################################################################


def slideshow_process(process_is_running):
    '''
    TODO
    '''
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

    # Path for images
    imageDirectory = "Images"  # TODO: Load from configurations: app/config/defaults.yml
    imageDirectory = os.path.join(currentDirectory, imageDirectory) + "/"

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

    # Creating a new OpenCV window
    cv2.namedWindow('Image', cv2.WND_PROP_FULLSCREEN)
    # Setting up openCV window for full screen mode
    cv2.setWindowProperty("Image", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

    # Initializing beginning and ending image index
    img_begin_index = -1
    img_end_index = -1

    print('')
    logging.info('Beginning picture frame image rotation. Use SPACEBAR to quit ...')
    error = None
    try:
        while process_is_running.value:
            # Picking a random image from directory - Target
            random.seed()
            while img_end_index == img_begin_index:
                img_end_index = random.randint(0, len(imagePaths)-1)

            # Load the starting image images
            if img_begin_index == -1:
                imageFileObject_begin = np.zeros((4000, 6000, 3), np.uint8)
                # imageFileObject_begin = cv2.imread(imageDirectory + "smile.png", cv2.IMREAD_UNCHANGED)
            else:
                imageFileObject_begin = cv2.imread(imagePaths[img_begin_index], cv2.IMREAD_UNCHANGED)

            # Loading the ending image
            imageFileObject_end = cv2.imread(imagePaths[img_end_index], cv2.IMREAD_UNCHANGED)

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


            # Storing information of current image by sending it to other/origin process
            # TODO: Nest this Dictionary!
            current_status_settings = {
                'img_delay_ms': image_delay,
                'img_order': 'random'
            }
            current_status_img_now = {
                'img_now_filename': imageNames[img_end_index],
                'img_now_abs_path': imagePaths[img_end_index],
                'img_now_rel_path': imagePaths[img_end_index].strip(currentDirectory),
                'img_now_index': img_end_index,
                'img_now_height_px': imageFileObject_end.shape[0],
                'img_now_width_px': imageFileObject_end.shape[1]
            }
            current_status_img_last = {
                'img_last_filename': imageNames[img_begin_index],
                'img_last_abs_path': imagePaths[img_begin_index],
                'img_last_rel_path': imagePaths[img_begin_index].strip(currentDirectory),
                'img_last_index': img_begin_index,
                'img_last_height_px': imageFileObject_begin.shape[0],
                'img_last_width_px': imageFileObject_begin.shape[1]
            }
            current_status_effect = {
                'effect_name': 'TODO',
                'effect_index': effect_index,
                'effect_mode': 'random',
                'effect_delay_ms': -1
            }
            current_status_display = {
                'display_index': -1,
                'display_width_px': screen_width_px,
                'display_height_px': screen_height_px
            }

            current_status = {
                **current_status_settings,
                **current_status_img_now,
                **current_status_img_last,
                **current_status_effect,
                **current_status_display
            }

            response = requests.post(url='http://localhost:5555/report_slidewhow_status', params=current_status)
            if not response.ok:
                logging.error('Failed to report current image information to main process. Response text: {}'.format(response.text))
            else:
                logging.debug('Successfully reportedcurrent image information to main process. Response text: {}'.format(response.text))

            # Waiting and watching out for key press to quit
            if cv2.waitKey(image_delay) == ord(' '):
                logging.info('***********************************************')
                logging.info('*     "SPACEBAR" key detected. Exiting ...    *')
                logging.info('***********************************************')
                break  # Stopping program

            # The next beginning image is the last end image
            img_begin_index = img_end_index

    except Exception as error:
        logging.critical('An error has occurred while displaying images. Exception: {}'.format(error))

    # Close all open openCV windows
    logging.info('Closing open image window ...')
    cv2.destroyWindow('Image')

    # Setting the process stop flag to false
    process_is_running.value = False
