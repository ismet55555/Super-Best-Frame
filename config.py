# ---------------------------------------------------------
# General configurations for the flask app
# ---------------------------------------------------------

import os

# Defining the base directory off the flask app
basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    # Creating a secreat key / access token from enviromental variable
    # If it does nto exist make static string key
    GITHUB_ACCESS_TOKEN = os.environ.get('GITHUB_ACCESS_TOKEN') or 'NONE_NEEDED'

    # Allows for auto update on HTML file changes
    TEMPLATES_AUTO_RELOAD = True

    # NOTE: These configurations can be called by: api.config[<variable>]
    # NOTE: More configuration options here: http://flask.pocoo.org/docs/1.0/config/
