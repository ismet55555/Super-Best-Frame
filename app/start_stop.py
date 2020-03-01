#!/usr/bin/env python3

# ---------------------------------------------------------
# Starting and Stopping of the Image Slideshow
# ---------------------------------------------------------

import logging
from multiprocessing import Process, Value

from app import data_storage, slideshow

###############################################################################

# Creating a boolean ('b') process value to communicate with independent process
process_is_running = Value("b", False)


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
        data_storage.process = Process(
            target=slideshow.slideshow_process, args=[process_is_running]
        )

        # Starting the slideshow
        data_storage.process.start()

        # Log it
        data_storage.slideshow["process"] = data_storage.process.ident
        data_storage.slideshow["running"] = True

        logging.info(
            "Successfully started independent slideshow process (Process: {})".format(
                data_storage.process.ident
            )
        )
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
        logging.info(
            "Stopping independent slideshow process (Process: {}) ...".format(
                data_storage.process.ident
            )
        )

        # Signaling the process to stop through the Queue
        process_is_running.value = False

        # Waiting for the independent process to stop
        data_storage.process.join()

        # Closing the independent process
        data_storage.process.close()

        # Log it
        data_storage.slideshow["process"] = -1
        data_storage.slideshow["running"] = False

        logging.info("Successfully stopped independent slideshow process")
        return True
    else:
        logging.critical("The picture-frame slideshow is currently not running")
        return False
