#!/usr/bin/env python3

# ---------------------------------------------------------
# Definition off all flask app global variables
# ---------------------------------------------------------

# TODO: Create a DataStorage Object like a real program !!!

# Current image inforamation
slideshow_current_img_filename = ''
slideshow_current_img_abs_path = ''
slideshow_current_img_rel_path = ''

# Slideshow information
slideshow = {}
slideshow['running'] = False
slideshow['process'] = -1

# Basic slideshow settings
settings = {}
settings['img_delay_ms'] = 1000
settings['effect_delay_ms'] = 50

# Current Image Information
img = {}
img['img_filename'] = ''
img['img_abs_path'] = ''
img['img_rel_path'] = ''
img['img_index'] = -1
img['img_height_px'] = -1
img['img_width_px'] = -1

# Current image transition effect information
effect = {}
effect['effect_name'] = ''
effect['effect_index'] = -1

# Display information
display = {}
display['display_index'] = -1
display['display_width_px'] = -1
display['display_height_px'] = -1