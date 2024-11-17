import os

from flask import Flask

from backend.utils import get_environment_variable, parse_bool


def create_app(*args, **kwargs) -> Flask:
    """Create and configure a Flask application instance.

    This function initializes a new Flask application with the provided arguments
    and keyword arguments. It serves as a factory function for creating app instances.

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
    """Run the Flask application with optional debugging.

    This function starts the Flask application server, allowing it to handle incoming requests.
    It determines whether to run in debug mode based on the environment variable "DEBUG" or the provided debug argument.

    Args:
        app (Flask): The Flask application instance to run.
        debug (bool, optional): A flag to enable or disable debug mode. Defaults to False.

    Returns:
        None: This function does not return a value.

    Examples:
        >>> run_application(app)
    """
    DEBUG = parse_bool(get_environment_variable("DEBUG")) or debug
    app.run(debug=DEBUG)
