#!/usr/bin/env python3

import json
import logging
import os
import random
import sys
import time
from math import ceil
from pprint import pprint
from threading import Thread

import cv2
import imutils
import numpy as np
import requests

from app import effects  # Image transition effects
from app import utility  # Useful and custom functions

###############################################################################

# TODO: Convert all this to an class


# Flag to stop any independently running threads
stop_thread_flag = False
process_communication_data = None


def _process_communication_get_thread():
    """
    TODO
    """
    # Define as global to this file
    global stop_thread_flag
    global process_communication_data

    # Time between REST requests (seconds)
    wait_between_requests = 0.200

    while not stop_thread_flag:
        # Retrieving information data from main process via REST
        response = requests.get(url="http://localhost:5555/utility/process_communication_get")
        if not response.ok:
            logging.error(
                "[Slideshow Process] Failed to retrieve information from main process. Response text: {}".format(
                    response.text
                )
            )
        else:
            logging.debug(
                "[Slideshow Process] Successfully retrieved information from main process. Response text: {}".format(
                    response.text
                )
            )

        # Store information into dictionary
        process_communication_data = json.loads(response.text)

        print(process_communication_data["controls"])

        # If successful, wait before trying again, else try again immediately
        if process_communication_data["success"]:
            time.sleep(wait_between_requests)

    return


def slideshow_process(process_is_running):
    """
    TODO
    """
    # Supported image file extensions
    # TODO: Load from app/config/img_formats.yml
    supported_formats = [
        ".png",
        ".jpg",
        ".jpeg",
        ".bmp",
        ".dib",
        ".jpe",
        ".jp2",
        ".pgm",
        ".tiff",
        ".tif",
        ".ppm",
    ]

    # Finding the screen width and height
    screen_width_px, screen_height_px = utility.get_screen_size()
    # Finding the aspact ratio
    screen_aspect_ratio = screen_width_px / screen_height_px
    logging.info("[Slideshow Process] Display/Screen size determined:")
    logging.info("[Slideshow Process]     Width:        {}".format(screen_width_px))
    logging.info("[Slideshow Process]     Height:       {}".format(screen_height_px))
    logging.info("[Slideshow Process]     Aspect Ratio: {:.2f}".format(screen_aspect_ratio))

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
    logging.info(
        "[Slideshow Process] Mapping out all available image files in directory: {}".format(
            imageDirectory
        )
    )
    for filename in os.listdir(imageDirectory):
        # Only consider files, not directories
        if os.path.isfile(imageDirectory + filename):
            # Add image path
            imagePaths.append(imageDirectory + filename)
            # Add the name of the image to an array
            imageNames.append(filename)
    logging.info("[Slideshow Process] Successfully mapped out {} images".format(len(imagePaths)))

    logging.info("[Slideshow Process] Configuring full screen image window ...")

    # Creating a new OpenCV window
    cv2.namedWindow("Image", cv2.WND_PROP_FULLSCREEN)
    # Setting up openCV window for full screen mode
    cv2.setWindowProperty("Image", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

    # Initializing beginning and ending image index
    img_begin_index = -1
    img_end_index = -1

    # Starting independent thread for process communication
    global stop_thread_flag
    global process_communication_data
    thread = Thread(target=_process_communication_get_thread, daemon=True)
    thread.start()

    # Wait a second for thread to get some initial data
    time.sleep(0.5)

    print("")
    logging.info(
        "[Slideshow Process] Beginning picture frame image rotation. Use SPACEBAR to quit ..."
    )
    try:
        # Main slideshow loop
        while process_is_running.value:

            # Check if paused or not
            if not process_communication_data["controls"]["pause_continue"]:
                # Picking a random image from directory - Target
                # TODO: Option to go in order, not random
                random.seed()
                while img_end_index == img_begin_index:
                    img_end_index = random.randint(0, len(imagePaths) - 1)

                # Load the starting image images
                if img_begin_index == -1:
                    imageFileObject_begin = np.zeros((4000, 6000, 3), np.uint8)
                    # imageFileObject_begin = cv2.imread(imageDirectory + "smile.png", cv2.IMREAD_UNCHANGED)
                else:
                    imageFileObject_begin = cv2.imread(
                        imagePaths[img_begin_index], cv2.IMREAD_UNCHANGED
                    )

                # Loading the ending image
                imageFileObject_end = cv2.imread(imagePaths[img_end_index], cv2.IMREAD_UNCHANGED)

                logging.info(
                    '[Slideshow Process] Showing image "{}" (Index: {}, Size: {}x{})'.format(
                        imageNames[img_end_index],
                        img_end_index,
                        imageFileObject_end.shape[1],
                        imageFileObject_end.shape[0],
                    )
                )

                # Process the beginning and ending image
                imageFileObject_begin = utility.process_fit_image(
                    imageFileObject_begin, screen_width_px, screen_height_px
                )
                imageFileObject_end = utility.process_fit_image(
                    imageFileObject_end, screen_width_px, screen_height_px
                )

                # Account for slight difference when border is added
                avg_width = ceil(
                    (imageFileObject_begin.shape[1] + imageFileObject_end.shape[1]) / 2
                )
                avg_height = ceil(
                    (imageFileObject_begin.shape[0] + imageFileObject_end.shape[0]) / 2
                )

                # Resize to average dimensions
                imageFileObject_begin = imutils.resize(
                    imageFileObject_begin, width=avg_width, height=avg_height
                )
                imageFileObject_end = imutils.resize(
                    imageFileObject_end, width=avg_width, height=avg_height
                )

                # Pick a random effect
                random.seed()
                effect_index = random.randint(0, 2)

                # Do the transition between images
                if effect_index == 0:
                    # Fade transition effect
                    effects.effect_fade(imageFileObject_begin, imageFileObject_end)
                elif effect_index == 1:
                    # Slide transition effect
                    effects.effect_slide(
                        imageFileObject_begin,
                        imageFileObject_end,
                        "right",
                        screen_width_px,
                        screen_height_px,
                    )
                else:
                    # Zoom in transition effect
                    effects.effect_zoom_out(imageFileObject_begin, imageFileObject_end)

                # Storing information of current image by sending it to other/origin process
                # TODO: Nest this Dictionary
                current_status_settings = {"img_delay_ms": image_delay, "img_order": "random"}
                current_status_img_now = {
                    "img_now_filename": imageNames[img_end_index],
                    "img_now_abs_path": imagePaths[img_end_index],
                    "img_now_rel_path": imagePaths[img_end_index].strip(currentDirectory),
                    "img_now_index": img_end_index,
                    "img_now_height_px": imageFileObject_end.shape[0],
                    "img_now_width_px": imageFileObject_end.shape[1],
                }
                current_status_img_last = {
                    "img_last_filename": imageNames[img_begin_index],
                    "img_last_abs_path": imagePaths[img_begin_index],
                    "img_last_rel_path": imagePaths[img_begin_index].strip(currentDirectory),
                    "img_last_index": img_begin_index,
                    "img_last_height_px": imageFileObject_begin.shape[0],
                    "img_last_width_px": imageFileObject_begin.shape[1],
                }
                current_status_effect = {
                    "effect_name": "TODO",
                    "effect_index": effect_index,
                    "effect_mode": "random",
                    "effect_delay_ms": -1,
                }
                current_status_display = {
                    "display_index": -1,
                    "display_width_px": screen_width_px,
                    "display_height_px": screen_height_px,
                }
                # Compiling all sections
                current_status = {
                    **current_status_settings,
                    **current_status_img_now,
                    **current_status_img_last,
                    **current_status_effect,
                    **current_status_display,
                }
                response = requests.post(
                    url="http://localhost:5555/utility/process_communication_post",
                    params=current_status,
                )
                if not response.ok:
                    logging.error(
                        "[Slideshow Process] Failed to report current image information to main process. Response text: {}".format(
                            response.text
                        )
                    )
                else:
                    logging.debug(
                        "[Slideshow Process] Successfully reportedcurrent image information to main process. Response text: {}".format(
                            response.text
                        )
                    )

            # Waiting and watching out for key press to quit
            if cv2.waitKey(image_delay) == ord(" "):
                logging.info("***********************************************")
                logging.info('*     "SPACEBAR" key detected. Exiting ...    *')
                logging.info("***********************************************")
                # Exiting loop, stopping process
                break

            # The next beginning image is the last end image
            img_begin_index = img_end_index

    except Exception as error:
        logging.critical(
            "[Slideshow Process] An error has occurred while displaying images. Exception: {}".format(
                error
            )
        )

    # Stopping Process Communication Thread
    stop_thread_flag = True
    thread.join()

    # Close all open openCV windows
    logging.info("[Slideshow Process] Closing open image window ...")
    cv2.destroyWindow("Image")

    # Setting the process stop flag to false
    process_is_running.value = False
