#!/usr/bin/env python3

# ---------------------------------------------------------
# Definition off all flask app endpoints/routes
# ---------------------------------------------------------

import logging
import subprocess

import cv2
import imutils
from math import floor, ceil

from pprint import pprint  # For troubleshooting and debugging


# =============================================================================================

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

# =============================================================================================

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

    # Determine where to place the border filler addition
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
