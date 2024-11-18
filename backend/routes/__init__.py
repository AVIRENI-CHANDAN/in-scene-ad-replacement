"""Routes Package Initialization Module

This module serves as the initialization point for the routes package within the application.
It imports the necessary blueprints for authentication, project management, and serving
the React application. The module provides a function to register these blueprints with
the main Flask application.

Key Features:
- Imports blueprints for handling authentication, project-related operations, and serving
  the React frontend.
- Provides a utility function to register multiple blueprints with a Flask application.

Functions:
- register_blueprint(app: Flask, *blueprints: List[Blueprint]) -> None: 
  Registers one or more blueprints with the specified Flask application.

Usage:
This module is intended to be imported and used within the Flask application to manage
the routing of various functionalities. It should be integrated with the main application
to ensure that all routes are accessible.

Example:
    from backend.routes import register_blueprint

    # Register the blueprints in the main application
    register_blueprint(app, auth_blueprint, project_blueprint, react_blueprint)
"""

from typing import List

from flask import Blueprint, Flask

from .auth import app as auth_blueprint
from .project import app as project_blueprint
from .react import app as react_blueprint


def register_blueprint(app: Flask, *blueprints: List[Blueprint]) -> None:
    """Register one or more blueprints with the Flask application.

    This function iterates over the provided blueprints and registers each one with
    the specified Flask application. It also prints a confirmation message for each
    blueprint that is successfully registered.

    Args:
        app (Flask): The Flask application instance to which the blueprints will be registered.
        *blueprints: A variable number of Blueprint instances to register with the application.

    Returns:
        None: This function does not return a value.

    Examples:
        >>> register_blueprint(app, auth_app, project_app)
    """

    for blueprint in blueprints:
        app.register_blueprint(blueprint)
        print(f"Registered blueprint: {blueprint.name}")
