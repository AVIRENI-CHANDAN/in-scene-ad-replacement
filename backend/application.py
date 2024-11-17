"""Application module for initializing and running a Flask web application.

This module provides functions to create a Flask application instance and to run the application
server. It includes configuration for debugging and allows customization through various parameters.

Functions:
    create_app(*args, **kwargs) -> Flask: Create and configure a new instance 
    of a Flask application.
    run_application(app: Flask, debug: bool = False) -> None: Start the Flask 
    application server with optional debugging enabled.
"""

from flask import Flask

from backend.utils import get_environment_variable, parse_bool


def create_app(*args, **kwargs) -> Flask:
    """Create and configure a new instance of a Flask application.

    This function serves as a factory for creating Flask application instances, allowing for
    customization through variable arguments and keyword arguments. It sets up the application
    with the necessary configurations to handle web requests.

    Args:
        *args: Variable length argument list for Flask initialization.
        **kwargs: Arbitrary keyword arguments for Flask initialization.

    Returns:
        Flask: An instance of the Flask application.

    Examples:
        >>> app = create_app()
        >>> app.name
        '__main__'
    """
    return Flask(__name__, *args, **kwargs)


def run_application(app: Flask, debug: bool = False) -> None:
    """Start the Flask application server with optional debugging enabled.

    This function launches the Flask application, allowing it to process incoming web requests.
    It checks the environment variable "DEBUG" and the provided debug argument to determine
    whether to run the application in debug mode, which provides detailed error messages and
    automatic reloading during development.

    Args:
        app (Flask): The Flask application instance to be run.
        debug (bool, optional): A flag indicating whether to enable debug mode. Defaults to False.

    Returns:
        None: This function does not return a value.

    Examples:
        >>> run_application(app)
    """
    is_debug_mode = parse_bool(get_environment_variable("DEBUG")) or debug
    app.run(debug=is_debug_mode)
