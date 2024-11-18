"""Backend Module for the Application

This module serves as the backend for the application, providing the necessary functionality to 
manage data, handle business logic, and interact with the database. It includes models, database 
operations, and routes for handling API requests.

Key Features:
- Database models for representing application data.
- Functions for adding, retrieving, and managing model objects.
- API routes for handling incoming requests and returning responses.

Usage:
To use this module, ensure that the Flask application is properly configured and that the database 
is initialized. The module can be imported and utilized to manage application data and handle 
requests.

Example:
    from backend import create_app, run_application

    app = create_app()
    run_application(app)
"""

from backend.models import Annotation, Project, Video, create_db_models, initialize_db
from backend.routes import (
    auth_blueprint,
    react_blueprint,
    register_blueprint,
    project_blueprint,
)
from backend.utils import get_environment_variable, parse_bool, sign_up, verify_sign_up

from .application import create_app, run_application
