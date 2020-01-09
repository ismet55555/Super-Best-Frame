#!/usr/bin/env python3

# ---------------------------------------------------------
# Definition off all flask app endpoints/routes
# ---------------------------------------------------------

import logging
import os
import subprocess

from app import api  # Import the app (Controller)
from app import start_stop  # Starts and stops slideshow
from app import temp_data

from flask import flash, redirect, request, jsonify
from flask import render_template  # Import the view renderer (View)

from pprint import pprint  # For troubleshooting and debugging


# Flask application base directory (CHECK ME)
base_app_dir = os.path.abspath(os.path.dirname(__file__))

# FIXME: somethign is not right here.... we get "..app/resources/cell"
base_dir = os.path.join(base_app_dir, '..')


###############################################################################


@api.route('/start', methods=['GET', 'POST'])
def start():
    """
    REST API endpoint to start the image slideshow.
    :return: json confirmation message
    """
    try:
        # Starting the slideshow
        start_stop.start_slideshow()
        success = True
        message = 'Successfully started picture frame slidshow'
    except Exception as e:
        success = False
        message = 'Failed to start picture frame slideshow. Exception: {}'.format(e)

    # Logging message
    logging.info(message) if success else logging.error(message)
    return jsonify({
        'success': success,
        'message': message
    })

###############################################################################


@api.route('/stop', methods=['GET', 'POST'])
def stop():
    """
    REST API endpoint to stop the image slideshow.
    :return: json confirmation message
    """
    try:
        # Stopping slideshow
        start_stop.stop_slideshow()
        success = True
        message = 'Successfully stopped picture frame slidshow'
    except Exception as e:
        success = False
        message = 'Failed to stop picture frame slideshow. Exception: {}'.format(e)

    # Logging message
    logging.info(message) if success else logging.error(message)
    return jsonify({
        'success': success,
        'message': message
    })

###############################################################################


@api.route('/status', methods=['GET', 'POST'])
def status():
    """
    REST API endpoint to get the complete status of slideshow
    :return: json confirmation message
    """

    # FIXME: Make sure to update the temp_data stuff where appropriate

    status = {}
    status['running'] = not temp_data.slideshow_thread_stop
    if temp_data.slideshow_thread:
        thread_id = temp_data.slideshow_thread.ident
    else:
        thread_id = None

    status['thread_id'] = thread_id

    img = {}
    img['img_name'] = "TEMP NAME"
    img['img_index'] = 0
    img['img_height_px'] = 999
    img['img_width_px'] = 888

    effect = {}
    effect['effect_name'] = "TEMP EFFECT NAME"
    effect['effect_index'] = 0

    settings = {}
    settings['img_delay_ms'] = 1000
    settings['effect_delay_ms'] = 50
    
    display = {}
    display['display_index'] = 0
    display['display_width_px'] = 1920
    display['display_height_px'] = 720

    success = True

    # Logging message
    logging.info(status) if success else logging.error(status)
    return jsonify({
        'success': success,
        'status': status,
        'img' : img,
        'effect': effect,
        'settings': settings,
        'display': display
    })

###############################################################################


@api.route('/kill', methods=['GET', 'POST'])
def kill():
    """
    REST API endpoint to command system to shutdown flask application.
    :return: json confirmation message
    """
    try:
        # Get all processes matching web application process. Reformat, strip, and split.
        process_port = '5555'
        processes = subprocess.Popen(['lsof -i :{}'.format(process_port)],
                                     stdout=subprocess.PIPE, shell=True).stdout.read().decode('utf-8').strip().split('\n')
        if processes[0]:
            # Loop through all running processes (omit heading row)
            pids = []
            for process in processes[1:]:
                # Split string by space
                process_parts = process.split(' ')
                # Strip all white space
                map(str.strip, process_parts)
                # Filter temp_data from blank temp_data
                process_columns = []
                for process_part in process_parts:
                    if process_part != '':
                        process_columns.append(process_part)
                # Store the PID for process (second column)
                pids.append(process_columns[1])
            logging.info('Web application endpoint "/kill" was engaged. Terminating web application ...')
            # Remove duplicates
            pids = list(set(pids))
            # Kill application (ommiting PID heading item)
            logging.critical('Local processes with the following PID will be killed: {}'.format(pids))
            for pid in pids:
                os.system('kill -9 {}'.format(pid))
        else:
            success = False
            message = 'Failed to shut down web application. Local system process running on port {} was not found.'.format(process_port)
    except Exception as e:
        success = False
        message = 'Failed to shut down web application running on port {}. Exception: {}'.format(process_port, e)
    # Logging message
    logging.info(message) if success else logging.error(message)
    return jsonify({
        'success': success,
        'message': message
    })

###############################################################################


@api.errorhandler(404)
def page_not_found(e):
    """
    REST API endpoint for any 404 page
    :return: html of 404 page processed by jinja2
    """
    return render_template('404.html'), 404


###############################################################################

@api.route('/')
@api.route('/index', methods=['GET'])
def index():
    """
    REST API endpoint for home page (index).
    :return: html of index processed by jinja2
    """
    logging.info('Successfully hit the index page!!!')

    # Rendering index.html
    return render_template('index.html')











###############################################################################









# import cv2
# import sys
# import threading

# def image_test():
#     currentDirectory = os.path.abspath(os.path.dirname(sys.argv[0]))
#     imageDirectory = "Images"
#     imageDirectory = os.path.join(currentDirectory, imageDirectory) + "//"
#     filename = 'DSC02055.JPG'

#     print('cv2.namedWindow')
#     cv2.namedWindow('Image', cv2.WND_PROP_FULLSCREEN)

#     print('cv2.setWindowProperty')
#     cv2.setWindowProperty("Image", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

#     img = cv2.imread(imageDirectory + filename, cv2.IMREAD_UNCHANGED)

#     while True:
#         print('cv2.imshow')
#         cv2.imshow('Image', img)
#         if cv2.waitKey(1500) == ord('q'):
#             break

#     print('cv2.destroyAllWindows()')
#     cv2.destroyAllWindows()


# @api.route('/test', methods=['GET', 'POST'])
# def test():
#     """
#     REST API endpoint to test some stuff
#     :return: json confirmation message
#     """

#     # thread = threading.Thread(target=image_test)
#     # thread.start()

#     image_test()

#     success = True
#     message = 'TESTING'

#     # Logging message
#     logging.info(message) if success else logging.error(message)
#     return jsonify({
#         'success': success,
#         'message': message
#     })