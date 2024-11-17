"""Project Model Module

This module defines the `Project` model, which represents a project entity in the database. It is 
part of the application's data layer and is used to store information related to user projects, 
including associated metadata such as titles and descriptions.

Key Features:
- Defines the structure of the `Project` entity in the database.
- Supports basic attributes for managing project data.

Model Attributes:
- id (int): The unique identifier for the project.
- sub (str): The sub of user associated with the project.
- title (str): The title of the project, defaulting to "Untitled Project".
- description (str): A textual description of the project.

Usage:
This model is intended for use with SQLAlchemy to facilitate interactions with the database. It can 
be used to create, read, update, and delete project records within the application.

Example:
    from backend.models.project import Project

    new_project = Project(
        sub="user1", 
        title="My First Project", 
        description="This is a description of my first project."
    )
"""

from .database import db


class Project(db.Model):
    """Represents a project in the database.

    This class defines the structure of the `Project` entity, which stores information
    related to user projects. Each project includes a title, a description, and is
    associated with a specific user through the sub attribute of user.

    Attributes:
        id (int): The unique identifier for the project.
        sub (str): The sub of the user associated with the project.
        title (str): The title of the project, defaulting to "Untitled Project".
        description (str): A textual description of the project.

    Usage:
        This model is intended for use with SQLAlchemy to facilitate interactions with the
        database. It can be used to create, read, update, and delete project records
        within the application.

    Example:
        >>> new_project = Project(
            sub="asdf9u-fvdf9u8y-9sud9f-sdf8sdj8",
            title="My First Project",
            description="This is a description of my first project."
        )
    """

    id = db.Column(db.Integer, primary_key=True)
    sub = db.Column(db.String(255), nullable=False, unique=False, index=True)
    title = db.Column(db.String(100), nullable=False, default="Untitled Project")
    description = db.Column(db.Text)
