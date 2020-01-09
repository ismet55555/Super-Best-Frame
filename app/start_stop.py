#!/usr/bin/env python3

# ---------------------------------------------------------
# Starting and Stopping of the Image Slideshow
# ---------------------------------------------------------

import logging

from app import temp_data
from app import slideshow

from multiprocessing import Process, Value

###############################################################################

# Creating a boolean ('b') process value to communicate with independent process
process_is_running = Value('b', False)

def start_slideshow():
    """
    Starting the picture frame slideshow.
    This starts the independent background process.
    :return: success
    """
    if not process_is_running.value:
        # Chaning the process value
        process_is_running.value = True

        # Creating the background process for the slideshow
        temp_data.slideshow_process = Process(target=slideshow.slideshow_process, args=[process_is_running])

        # Starting the slideshow
        temp_data.slideshow_process.start()

        logging.info("Successfully started independent slideshow process (Process: {})".format(temp_data.slideshow_process.ident))
        return True
    else:
        logging.critical("The picture-frame slideshow is already running")
        return False


def stop_slideshow():
    """
    Ends the picture frame slideshow.
    This stops the independent background process.
    :return: success
    """
    if process_is_running.value:
        logging.info("Stopping independent slideshow process (Process: {}) ...".format(temp_data.slideshow_process.ident))

        # Signaling the process to stop through the Queue
        process_is_running.value = False

        # Waiting for the independent process to stop
        temp_data.slideshow_process.join()

        # Closing the independent process
        temp_data.slideshow_process.close()

        logging.info("Successfully stopped independent slideshow process")
        return True
    else:
        logging.critical("The picture-frame slideshow is currently not running")
        return False

    