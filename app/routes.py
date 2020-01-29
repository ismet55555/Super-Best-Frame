#!/usr/bin/env python3

# ---------------------------------------------------------
# Definition off all flask app endpoints/routes
# ---------------------------------------------------------

import logging
import os
import subprocess

from app import api  # Import the app (Controller)
from app import start_stop  # Starts and stops slideshow
from app import data_storage

from flask import jsonify, send_from_directory
from flask import render_template, request  # Import the view renderer (View)

from pprint import pprint  # For troubleshooting and debugging


# Flask application base directory (CHECK ME)
base_app_dir = os.path.abspath(os.path.dirname(__file__))

# FIXME: somethign is not right here.... we get "..app/resources/cell"
base_dir = os.path.join(base_app_dir, '..')



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
    return render_template('index.html', base_app_dir=base_app_dir, base_dir=base_dir)


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

@api.route('/current_img', methods=['GET'])
def current_img():
    """
    REST API endpoint to get the name and path to current img
    :return: json confirmation message and image name and path
    """

    # Loading the info of current image
    img_filename = data_storage.slideshow_current_img_filename
    img_abs_path = data_storage.slideshow_current_img_abs_path
    img_rel_path = data_storage.slideshow_current_img_rel_path
    success = True
    message = "Successfully found current image"

    # Logging message
    logging.info(message) if success else logging.error(message)
    return jsonify({
        'success': success,
        'message': message,
        'img_filename': img_filename,
        'img_abs_path': img_abs_path,
        'img_rel_path': img_rel_path
    })


@api.route('/current_img_info', methods=['POST'])
def current_img_info():
    """
    REST API endpoint to set the current immage info
    :return: json confirmation message and image name and path
    """
    ########################################
    # TODO: Only allow internal calls from, change endpoint to somethign like /utility/current_img_info
    ########################################

    try:
        data_storage.slideshow_current_img_filename = request.args.get('img_filename', default='', type=str).strip()
        data_storage.slideshow_current_img_abs_path = request.args.get('img_abs_path', default='', type=str).strip()
        data_storage.slideshow_current_img_rel_path = request.args.get('img_rel_path', default='', type=str).strip()

        success = True
        message = "Successfully reported current image information"
    except Exception as e:
        success = False
        message = "Failed to report current image information. Exception: {}".format(e)

    # Logging message
    logging.info(message) if success else logging.error(message)
    return jsonify({
        'success': success,
        'message': message,
        'reported_filename': data_storage.slideshow_current_img_filename,
        'reported_img_abs_path': data_storage.slideshow_current_img_abs_path,
        'reported_img_rel_path': data_storage.slideshow_current_img_rel_path
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


@api.route('/report_slidewhow_status', methods=['POST'])
def report_slideshow_status():
    """
    REST API endpoint to set the current status of the slideshow
    :return: json confirmation message and image name and path
    """
    try:
        # Basic slideshow settings
        data_storage.settings['img_delay_ms'] = request.args.get('img_delay_ms', default=-1, type=int)
        data_storage.settings['img_order'] = request.args.get('img_order', default='', type=str).strip()

        # Current Image Information
        data_storage.img_now['img_now_filename'] = request.args.get('img_now_filename', default='', type=str).strip()
        data_storage.img_now['img_now_abs_path'] = request.args.get('img_now_abs_path', default='', type=str).strip()
        data_storage.img_now['img_now_rel_path'] = request.args.get('img_now_rel_path', default='', type=str).strip()
        data_storage.img_now['img_now_index'] = request.args.get('img_now_index', default=-1, type=int)
        data_storage.img_now['img_now_height_px'] = request.args.get('img_now_height_px', default=-1, type=int)
        data_storage.img_now['img_now_width_px'] = request.args.get('img_now_width_px', default=-1, type=int)

        # Previous Image Information
        data_storage.img_last['img_last_filename'] = request.args.get('img_last_filename', default='', type=str).strip()
        data_storage.img_last['img_last_abs_path'] = request.args.get('img_last_abs_path', default='', type=str).strip()
        data_storage.img_last['img_last_rel_path'] = request.args.get('img_last_rel_path', default='', type=str).strip()
        data_storage.img_last['img_last_index'] = request.args.get('img_last_index', default=-1, type=int)
        data_storage.img_last['img_last_height_px'] = request.args.get('img_last_height_px', default=-1, type=int)
        data_storage.img_last['img_last_width_px'] = request.args.get('img_last_width_px', default=-1, type=int)

        # Current image transition effect information
        data_storage.effect['effect_name'] = request.args.get('effect_name', default='', type=str).strip()
        data_storage.effect['effect_index'] = request.args.get('effect_index', default=-1, type=int)
        data_storage.effect['effect_mode'] = request.args.get('effect_mode', default='', type=str).strip()
        data_storage.effect['effect_delay_ms'] = request.args.get('effect_delay_ms', default=-1, type=int)

        # Display information
        data_storage.display['display_index'] = request.args.get('display_index', default=-1, type=int)
        data_storage.display['display_width_px'] = request.args.get('display_width_px', default=-1, type=int)
        data_storage.display['display_height_px'] = request.args.get('display_height_px', default=-1, type=int)

        success = True
        message = "Successfully reported current image information"
    except Exception as e:
        success = False
        message = "Failed to report current image information. Exception: {}".format(e)

    # Logging message
    logging.info(message) if success else logging.error(message)
    return jsonify({
        'success': success,
        'message': message
    })



@api.route('/status', methods=['GET'])
def status():
    """
    REST API endpoint to get the complete status of slideshow
    :return: json confirmation message
    """

    success = True

    # Logging message
    logging.info(status) if success else logging.error(status)
    return jsonify({
        'success': success,
        'slideshow': data_storage.slideshow,
        'img_now': data_storage.img_now,
        'img_last': data_storage.img_last,
        'effect': data_storage.effect,
        'settings': data_storage.settings,
        'display': data_storage.display
    })

###############################################################################

@api.route('/api_map', methods=['GET'])
def api_map():
    """
    REST API endpoint to show all possible api endpoints
    :return: json confirmation message
    """

    return jsonify({
        '/start': "Start the image slideshow",
        '/stop' : "Stop the image slideshow",
        '/kill' : "Forcefully kill all system processes related with this web app",
        'TODO'  : "TODO"
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
                # Filter data_storage from blank data_storage
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

@api.route('/Images/<path:filename>')
def images(filename):
    """
    REST API Securely send files form image directory.
    Essentially this is creating a static directory
    to reference from just like the "static" directory.
    :param filename: The specific file name (or relative path)
    :return: file from file directory
    """
    print('IMAGES')
    print(os.path.join(api.root_path + '/..' + '/Images/', filename))
    return send_from_directory(directory=api.root_path + '/..' + '/Images/', filename=filename)


###############################################################################

@api.errorhandler(404)
def page_not_found(e):
    """
    REST API endpoint for any 404 page
    :return: html of 404 page processed by jinja2
    """
    return render_template('404.html'), 404

###############################################################################
