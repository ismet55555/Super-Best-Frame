#!/usr/bin/env python3

# ---------------------------------------------------------
# Image transition effects
# ---------------------------------------------------------

import logging

import cv2
import numpy as np

from pprint import pprint  # For troubleshooting and debugging


# =============================================================================================

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
