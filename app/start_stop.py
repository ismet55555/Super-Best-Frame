#!/usr/bin/env python3

import logging
import threading

from app import temp_data
from app import slideshow

from multiprocessing import Process, Queue

###############################################################################

# Creating a process queue to communicate with independent process
process_is_running_queue = Queue()
process_is_running_queue.put(False)


def start_slideshow():
    """
    TODO
    """
    print('\n STARTING ...')
    if not process_is_running_queue.get():
        # Adding a process stop queue 
        process_is_running_queue.put(True)

        # Creating the background thread for the slideshow
        temp_data.slideshow_process = Process(target=slideshow.slideshow_thread, args=(process_is_running_queue,))

        # Starting the slideshow
        temp_data.slideshow_process.start()

        logging.info("Successfully started independent slideshow process (Process: {})".format(temp_data.slideshow_process.ident))
        return True
    else:
        logging.critical("The picture-frame slideshow is already running")
        return False

import time

def stop_slideshow():
    """
    TODO
    """
    print('\n STOPPING ...')
    if process_is_running_queue.get():
        logging.info("Stopping independent slideshow process (Process: {}) ...".format(temp_data.slideshow_process.ident))

        # Raise Flag to stop slide show process
        temp_data.slideshow_process_stop = True

        # Signaling the process to stop through the Queue
        process_is_running_queue.put(False)

        # Waiting for the process to stop
        temp_data.slideshow_process.join()

        temp_data.slideshow_process.close()

        logging.info("Successfully stopped independent slideshow process")
        return True
    else:
        logging.critical("The picture-frame slideshow is currently not running")
        return False

    