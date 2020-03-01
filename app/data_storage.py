#!/usr/bin/env python3

# ---------------------------------------------------------
# Definition off all flask app global variables
# ---------------------------------------------------------

# TODO: Create a DataStorage Object like a real program !!!

# # Current image inforamation
# slideshow_current_img_filename = ''
# slideshow_current_img_abs_path = ''
# slideshow_current_img_rel_path = ''

# Slideshow process reference
process = None


# Slideshow controls
controls = {}
controls["pause_continue"] = False


# Slideshow information
slideshow = {}
slideshow["running"] = False
slideshow["process"] = -1

# Basic slideshow settings
settings = {}
settings["img_delay_ms"] = 1000
settings["img_order"] = "random"

# Current Image Information
img_now = {}
img_now["img_now_filename"] = ""
img_now["img_now_abs_path"] = ""
img_now["img_now_rel_path"] = ""
img_now["img_now_index"] = -1
img_now["img_now_height_px"] = -1
img_now["img_now_width_px"] = -1

# Previous Image Information
img_last = {}
img_last["img_last_filename"] = ""
img_last["img_last_abs_path"] = ""
img_last["img_last_rel_path"] = ""
img_last["img_last_index"] = -1
img_last["img_last_height_px"] = -1
img_last["img_last_width_px"] = -1

# Current image transition effect information
effect = {}
effect["effect_name"] = ""
effect["effect_index"] = -1
effect["effect_mode"] = "random"
effect["effect_delay_ms"] = 50

# Display information
display = {}
display["display_index"] = -1
display["display_width_px"] = -1
display["display_height_px"] = -1
