#!/usr/bin/env python3

# ---------------------------------------------------------
# Initialization off all flask app components
# ---------------------------------------------------------

from config import Config
from flask import Flask  # NOTE: Uppercase Flask is the class, lowercase flask is the module
from flask_cors import CORS

# Define Flask application class instance
api = Flask(__name__)

# Cross Origin Resource Sharing (CORS) Support on all routes. Allows browser based communication with this API.
CORS(api)

# Importing all application configurations stored in config.py
api.config.from_object(Config)

# Importing all custom code
from app import routes  # Web application routes/endpoints
from app import data_storage
from app import effects  # Image transition effects
from app import utility  # Useful and custom functions
from app import slideshow  # main slideshow thread (runs in background)

