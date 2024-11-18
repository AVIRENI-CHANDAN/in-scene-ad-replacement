"""Video Model Module

This module defines the `Video` model, which represents a video entity in the database. It is part 
of the application's data layer and is used to store information related to videos associated with 
projects, including metadata such as filenames.

Key Features:
- Defines the structure of the `Video` entity in the database.
- Establishes relationships with other models, specifically linking videos to projects.

Model Attributes:
- project_id (int): A foreign key linking the video to a specific project.
- filename (str): The name of the video file, which must be unique across all videos.

Table Constraints:
- UniqueConstraint: Ensures that the combination of `project_id` and `filename` is unique, 
preventing multiple videos with the same filename within the same project.

Usage:
This model is intended for use with SQLAlchemy to facilitate interactions with the database. It can 
be used to create, read, update, and delete video records within the application.

Example:
    from backend.models.video import Video

    new_video = Video(project_id=1, filename="my_video.mp4")
"""

import uuid

from .database import db


class Video(db.Model):
    """Represents a video associated with a project in the database.

    This class defines the structure of the `Video` entity, which stores information
    related to videos linked to specific projects. Each video includes a filename and
    is associated with a project through the project_id attribute.

    Attributes:
        project_id (int): A foreign key linking the video to a specific project.
        filename (str): The name of the video file, which must be unique across all videos.

    Table Constraints:
        UniqueConstraint: Ensures that the combination of `project_id` and `filename` is unique,
        preventing multiple videos with the same filename within the same project.

    Usage:
        This model is intended for use with SQLAlchemy to facilitate interactions with the
        database. It can be used to create, read, update, and delete video records
        within the application.

    Example:
        >>> new_video = Video(project_id=1, filename="my_video.mp4")
    """

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    project_id = db.Column(
        db.Integer, db.ForeignKey("project.id"), nullable=False, index=True
    )
    filename = db.Column(db.String(255), unique=True, nullable=False)
    __table_args__ = (
        db.UniqueConstraint(
            "project_id", "filename", name="unique_filename_per_project"
        ),
    )
