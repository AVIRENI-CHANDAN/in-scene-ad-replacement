import os

from flask import Flask

from .environ import get_environment_variable


def create_app(*args, **kwargs):
    return Flask(__name__, *args, **kwargs)


def run_application(app: Flask, debug: bool = False):
    DEBUG = get_environment_variable("DEBUG") == "True" or debug
    app.run(debug=DEBUG)
