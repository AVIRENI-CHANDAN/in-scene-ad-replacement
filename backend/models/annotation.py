"""Annotation Model Module

This module defines the `Annotation` model, which represents an annotation entity in the database. 
It is part of the application's data layer and is used to store information related to annotations 
made on projects, including associated metadata such as timestamps and image URLs.

Key Features:
- Defines the structure of the `Annotation` entity in the database.
- Establishes relationships with other models, specifically linking annotations to projects.

Model Attributes:
- project_id (int): A foreign key linking the annotation to a specific project.
- timestamp (float): The timestamp indicating when the annotation was created.
- points (JSON): A JSON object storing the points associated with the annotation.
- image_url (str): A URL pointing to the image related to the annotation.

Usage:
This model is intended for use with SQLAlchemy to facilitate interactions with the database. It can 
be used to create, read, update, and delete annotation records within the application.

Example:
    from backend.models.annotation import Annotation

    new_annotation = Annotation(
        timestamp=1625256000, 
        points={"x": 10, "y": 20}, 
        image_url="http://example.com/image.png"
    )
"""

from .database import db
import uuid


class Annotation(db.Model):
    """Represents an annotation associated with a project in the database.

    This class defines the structure of the `Annotation` entity, which stores information
    related to annotations made on projects. Each annotation includes a timestamp, a set of
    points, and a URL to an associated image.

    Attributes:
        project_id (int): A foreign key linking the annotation to a specific project.
        timestamp (float): The timestamp indicating when the annotation was created.
        points (dict): A JSON object storing the points associated with the annotation.
        image_url (str): A URL pointing to the image related to the annotation.

    Usage:
        This model is intended for use with SQLAlchemy to facilitate interactions with the
        database. It can be used to create, read, update, and delete annotation records
        within the application.

    Example:
        >>> new_annotation = Annotation(
            timestamp=1625256000, p
            oints={"x": 10, "y": 20},
            image_url="http://example.com/image.png"
        )
    """

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    project_id = db.Column(
        db.Integer, db.ForeignKey("project.id"), nullable=False, index=True
    )
    timestamp = db.Column(db.Float)
    points = db.Column(db.JSON)
    image_url = db.Column(db.String(2048))
