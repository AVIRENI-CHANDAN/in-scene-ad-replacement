"""Models Package Initialization Module

This module serves as the initialization point for the models package within the application. 
It imports the necessary model classes and database utility functions, making them available 
for use throughout the application. This structure promotes modularity and organization 
within the codebase.

Key Features:
- Imports the `Annotation`, `Project`, and `Video` models for easy access.
- Provides utility functions for database operations, including model creation and data saving.

Usage:
This module is intended to be imported as part of the models package. It allows for seamless 
interaction with the various models and database functions defined in the package.

Example:
    from backend.models import Annotation, Project, Video, create_db_models, save_object

    # Initialize database models
    create_db_models()

    # Create and save a new project
    new_project = Project(username="user1", title="My Project")
    save_object(new_project)
"""

from .annotation import Annotation
from .database import create_db_models, initialize_db, save_object, save_objects
from .project import Project
from .video import Video
