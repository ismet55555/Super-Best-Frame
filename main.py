#!/usr/bin/env python3

# ---------------------------------------------------------
# Picture-Frame: Main flask application entry point
# Run with command: python3 main.py
# ---------------------------------------------------------

# Import all modules for app
import logging
from logging.handlers import RotatingFileHandler
import sys

from app import api  # Flask application
from gevent.pywsgi import WSGIServer

# Running flask server
if __name__ == '__main__':
    # Setting up logger and a local log file
    file_handler = logging.handlers.RotatingFileHandler(filename='picture-frame.log', mode='w', maxBytes=10000000, backupCount=0)
    stdout_handler = logging.StreamHandler(sys.stdout)
    logging.basicConfig(level=logging.INFO,
                        format='[Picture-Frame] - [%(asctime)s] - %(levelname)-10s - %(message)s',
                        datefmt='%d-%b-%y %H:%M:%S',
                        handlers=[file_handler, stdout_handler])

    logging.info('Starting flask server application (picture-frame) ...  ')
    logging.info('Web application port:  5555')

    # NOTE: DEVELOPMENT: Using default flask server
    logging.info('NOTE: Using default flask server (DEVELOPMENT ONLY)')
    api.run(host='0.0.0.0', port=5555)

    # # NOTE: PRODUCTION: Using gevent standalone Web Server Gateway Interface (WSGI) container
    # logging.info('NOTE: Using gevent standalone Web Server Gateway Interface (WSGI) server for production deployment\n\n')
    # http_server = WSGIServer(('', 5555), api, log=logging)
    # http_server.serve_forever()

# NOTE: Enviromental variables and settings are set in .flaskenv
