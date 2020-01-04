#!/usr/bin/env python3

import logging
import threading

from app import temp_data
from app import slideshow


###############################################################################

def start_slideshow():
    """
    TODO
    """
    if not temp_data.slideshow_thread:
        # lowering flag for thread to stop
        temp_data.slideshow_thread_stop = False
        # Creating the background thread for the slideshow
        temp_data.slideshow_thread = threading.Thread(target=slideshow.slideshow_thread)
        # Starting the slideshow
        temp_data.slideshow_thread.start()
        logging.info("Successfully started image slideshow (Thread: {})".format(temp_data.slideshow_thread.ident))
        return True
    else:
        logging.critical("The picture-frame slideshow is already running (Thread: {})".format(temp_data.slideshow_thread.ident))
        return False

def stop_slideshow():
    """
    TODO
    """
    if temp_data.slideshow_thread:
        # Raising flag for thread to stop
        temp_data.slideshow_thread_stop = True
        logging.info("Stopping active slideshow thread (Thread: {}) ...".format(temp_data.slideshow_thread.ident))
        # Waiting for the thread to stop
        temp_data.slideshow_thread.join()
        temp_data.slideshow_thread = None
        logging.info("Successfully stopped slideshow thread")
        return True
    else:
        logging.critical("The picture-frame slideshow is currently not running")
        return False