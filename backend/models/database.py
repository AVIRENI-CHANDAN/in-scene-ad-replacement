"""Database Module for the Application

This module provides functionality for initializing and managing the database within the 
application. It utilizes SQLAlchemy as the ORM to interact with the database and includes functions 
for creating models, saving objects, and configuring the database connection.

Key Features:
- Initializes the database with the specified configuration.
- Creates all database models defined in the application.
- Provides functions to save single or multiple model objects to the database.

Functions:
- initialize_db(app: Flask) -> None: Configures the database connection for the Flask application.
- create_db_models() -> None: Creates all database tables based on the defined models.
- save_object(model_object: db.Model) -> None: Saves a single model object to the database.
- save_objects(object_list: List[db.Model]) -> None: Saves a list of model objects to the database 
in bulk.

Usage:
This module is intended for use within the application to manage database interactions. It should 
be imported and utilized to set up the database and perform CRUD operations on models.

Example:
    from backend.models.database import initialize_db, create_db_models, save_object
    from backend.models.annotation import Annotation

    app = Flask(__name__)
    initialize_db(app)
    create_db_models()
    new_annotation = Annotation(
        project_id=1, 
        timestamp=1625256000, 
        points={"x": 10, "y": 20}, 
        image_url="http://example.com/image.png"
    )
    save_object(new_annotation)
"""

from functools import wraps
from typing import List

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from backend.utils import get_environment_variable

db = SQLAlchemy()


def initialize_db(app: Flask) -> None:
    """Initialize the database for the given Flask application.

    This function configures the database connection for the Flask application using
    the SQLAlchemy database URI retrieved from the environment variables. It sets up
    the necessary configurations to enable database interactions within the application.

    Args:
        app (Flask): The Flask application instance to configure for database use.

    Returns:
        None: This function does not return a value.

    Example:
        >>> from flask import Flask
        >>> app = Flask(__name__)
        >>> initialize_db(app)
    """

    print("Initialising the database")
    app.config["SQLALCHEMY_DATABASE_URI"] = get_environment_variable(
        "SQLALCHEMY_DATABASE_URI"
    )
    db.init_app(app)


def create_db_models() -> None:
    """Create all database tables based on the defined models.

    This function initializes the database by creating all tables that are defined
    in the SQLAlchemy models. It should be called after the database has been initialized
    and configured.

    Returns:
        None: This function does not return a value.

    Example:
        >>> create_db_models()
    """

    db.create_all()


def transactional(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        try:
            result = f(*args, **kwargs)
            db.session.commit()
            return result
        except Exception as e:
            db.session.rollback()
            raise e

    return wrapper


@transactional
def save_object(model_object: db.Model) -> None:
    """Save a single model object to the database.

    This function adds the provided model object to the current database session
    and commits the session to persist the changes. It is used to store new records
    or update existing records in the database.

    Args:
        model_object (db.Model): The model object to be saved to the database.

    Returns:
        None: This function does not return a value.

    Example:
        >>> from backend.models.annotation import Annotation
        >>> new_annotation = Annotation(
            project_id=1,
            timestamp=1625256000,
            points={"x": 10, "y": 20},
            image_url="http://example.com/image.png"
        )
        >>> save_object(new_annotation)
    """
    db.session.add(model_object)


@transactional
def save_objects(object_list: List[db.Model]) -> None:
    """Save a list of model objects to the database in bulk.

    This function adds multiple model objects to the current database session and
    commits the session to persist the changes. It is optimized for performance by
    using bulk operations to save multiple records at once.

    Args:
        object_list (List[db.Model]): A list of model objects to be saved to the database.

    Returns:
        None: This function does not return a value.

    Example:
        >>> from backend.models.video import Video
        >>> video_list = [
        ...     Video(project_id=1, filename="video1.mp4"),
        ...     Video(project_id=1, filename="video2.mp4"),
        ... ]
        >>> save_objects(video_list)
    """
    db.session.bulk_save_objects(object_list)


@transactional
def delete_object(model_object: db.Model) -> None:
    """Delete a model object from the database.

    This function removes the specified model object from the current database session
    and commits the changes to the database. It is important to ensure that the object
    to be deleted exists in the session before calling this function.

    Args:
        model_object (db.Model): The model object to be deleted from the database.

    Returns:
        None: This function does not return a value.

    Raises:
        Exception: If the deletion fails for any reason, an exception may be raised.
    """

    db.session.delete(model_object)
