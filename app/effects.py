#!/usr/bin/env python3

# ---------------------------------------------------------
# Image transition effects
# ---------------------------------------------------------

from pprint import pprint  # For troubleshooting and debugging

import cv2
import numpy as np

###############################################################################


def effect_none(img_end):
    """
    Image change transition effect: None
    NOTE: Images must be the same pixel size
    :param img_end: Ending OpenCV image object
    """
    cv2.imshow("Image", img_end)


def effect_fade(img_begin, img_end, len=20, delay=5):
    """
    Image change transition effect: Fade
    NOTE: Images must be the same pixel size
    :param img_begin: Beginning OpenCV image object
    :param img_end: Ending OpenCV image object
    :param len: Number of frames for this transition
    :param delay: Delay (ms) between transition frames
    """
    changing = True
    while changing:
        # Loop through transition frame numbers
        for index in range(0, len):
            fade_in_radio = index / float(len)
            mergedImageFrame = cv2.addWeighted(
                img_begin, 1 - fade_in_radio, img_end, fade_in_radio, 0
            )
            cv2.imshow("Image", mergedImageFrame)
            # Wait a little before continuing
            cv2.waitKey(delay)
        cv2.imshow("Image", img_end)
        changing = False


def effect_slide(img_begin, img_end, direction, screen_width_px, screen_height_px, len=10, delay=2):
    """
    Image change transition effect: Slide
    NOTE: Images must be the same pixel size
    :param img_begin: Beginning OpenCV image object
    :param img_end: Ending OpenCV image object
    :param direction: Direction of image slide (TODO)
    :param screen_width_px: Pixel width of the screen (TODO: Make global)
    :param screen_height_px: Pixel height of the screen (TODO: Make global)
    :param len: Number of frames for this transition
    :param delay: Delay (ms) between transition frames
    """
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
            cv2.imshow("Image", img_cropped)
            # Wait a little before continuing
            cv2.waitKey(delay)
        changing = False


def effect_zoom_out(img_begin, img_end, len=20, delay=1):
    """
    Image change transition effect: Zoom Out
    NOTE: Images must be the same pixel size
    :param img_begin: Beginning OpenCV image object
    :param img_end: Ending OpenCV image object
    :param len: Number of frames for this transition
    :param delay: Delay (ms) between transition frames
    """
    # NOTE: Images must be the same pixel dimensions
    img_width_init = img_begin.shape[1]
    img_height_init = img_begin.shape[0]
    changing = True
    while changing:
        # Loop through transition frame numbers
        for i in range(0, len):
            crop_percent = i / float(len)  # Percent to crop
            xi = int(crop_percent * (img_width_init / 2))
            xf = int(img_width_init - (crop_percent * (img_width_init / 2)))
            yi = int(crop_percent * (img_height_init / 2))
            yf = int(img_height_init - (crop_percent * (img_height_init / 2)))
            img_cropped = img_begin[yi:yf, xi:xf]
            cv2.imshow("Image", img_cropped)
            # Wait a little before continuing
            cv2.waitKey(delay)
        cv2.imshow("Image", img_end)
        changing = False
