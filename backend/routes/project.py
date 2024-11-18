"""Project Routes Module

This module defines the routes for managing projects within the application. It provides
endpoints for creating projects, listing projects, uploading videos, adding annotations,
and applying annotations to videos. The module integrates with the database models and
utilizes Flask's Blueprint for modular route management.

Key Features:
- Create a new project with a title and description.
- List all projects associated with the authenticated user.
- Upload videos associated with a specific project.
- Add annotations to a project, including timestamps and image URLs.
- Apply annotations to videos, processing frames as needed.

Routes:
- POST /api/projects/: Creates a new project.
- GET /api/projects/: Lists all projects for the authenticated user.
- POST /api/projects/<int:project_id>/upload: Uploads a video for the specified project.
- POST /api/projects/<int:project_id>/annotations: Adds annotations to the specified project.
- POST /api/projects/<int:project_id>/apply: Applies annotations to the specified project.

Usage:
This module is intended to be imported and used within the Flask application to manage
project-related operations. It should be integrated with the main application to handle
user-related project functionalities securely.

Example:
    from backend.routes.project import app as project_app

    # Register the project blueprint in the main application
    main_app.register_blueprint(project_app)
"""

import os

from flask import Blueprint, jsonify, request

from backend.models import (
    Annotation,
    Project,
    Video,
    delete_object,
    save_object,
    save_objects,
)

from .util import login_required, secure_filename

app = Blueprint("project", __name__, url_prefix="/api/projects")


@app.route("/", methods=["POST"])
@login_required
def create_project():
    """Create a new project for the authenticated user.

    This function handles the creation of a new project by validating the incoming JSON
    request and extracting the necessary information. It ensures that the title and description
    are provided and non-empty before saving the project to the database.

    Args:
        None: This function does not take any parameters.

    Returns:
        Response: A JSON response indicating the success of the project creation along with
        the newly created project's ID, or an error message with the appropriate HTTP status.

    Raises:
        BadRequest: If the request does not contain valid JSON or if required fields are missing.

    Examples:
        >>> response = create_project()
        >>> response.status_code
        201
    """

    if not request.is_json:
        return {"error": "Content-Type must be application/json"}, 400
    data = request.json
    decoded_id_token = request.id_token
    user_cognito_sub = decoded_id_token["sub"]
    if not data or ("title" not in data) or ("description" not in data):
        return {"error": "Title and description are required"}, 400
    if (len(data["title"]) <= 0) or (len(data["description"]) <= 0):
        return {"error": "Title or description is empty"}, 400
    project = Project(
        title=data["title"], description=data["description"], sub=user_cognito_sub
    )
    save_object(project)
    return jsonify({"message": "Project created", "project_id": project.id}), 201


@app.route("/", methods=["GET"])
@login_required
def list_projects():
    """Retrieve a list of projects associated with the authenticated user.

    This function handles the retrieval of projects from the database that are linked
    to the currently authenticated user. It extracts the user's unique identifier from
    the decoded ID token and queries the database for the corresponding projects.

    Args:
        None: This function does not take any parameters.

    Returns:
        Response: A JSON response containing a list of projects, each represented by its
        ID, title, and description.

    Raises:
        Unauthorized: If the user is not authenticated, access to this endpoint is restricted.

    Examples:
        >>> response = list_projects()
        >>> response.status_code
        200
    """

    decoded_id_token = request.id_token
    cognito_sub = decoded_id_token["sub"]
    projects = Project.query.filter_by(sub=cognito_sub)
    return jsonify(
        [{"id": p.id, "title": p.title, "description": p.description} for p in projects]
    )


@app.route("/<path:project_id>/delete", methods=["POST"])
@login_required
def delete_project(project_id: str):
    """Delete a project associated with the authenticated user.

    This function handles the deletion of a specified project from the database. It verifies
    that the project belongs to the authenticated user before proceeding with the deletion.

    Args:
        project_id (str): The unique identifier of the project to be deleted.

    Returns:
        Response: A JSON response indicating the success of the deletion or an error message
        if the project is not found.

    Raises:
        NotFound: If the project does not exist for the authenticated user.

    Examples:
        >>> response = delete_project("12345")
        >>> response.status_code
        200
    """

    decoded_id_token = request.id_token
    user_cognito_sub = decoded_id_token["sub"]
    project = Project.query.filter_by(id=project_id, sub=user_cognito_sub).first()
    if not project:
        return {"error": "Project not found"}, 404
    delete_object(project)
    return {"message": "Project deleted"}, 200


@app.route("/<int:project_id>/upload", methods=["POST"])
@login_required
def upload_video(project_id: int):
    """Upload a video file associated with a specific project.

    This function handles the uploading of a video file to the server and associates
    it with the specified project. It saves the video file to a designated directory
    and creates a corresponding entry in the database.

    Args:
        project_id (int): The unique identifier of the project to which the video is associated.

    Returns:
        Response: A JSON response indicating the success of the upload along with the
        ID of the newly created video entry.

    Raises:
        BadRequest: If the uploaded file is not valid or if the video file is missing.

    Examples:
        >>> response = upload_video(1)
        >>> response.status_code
        201
    """

    video = request.files["video"]
    filename = secure_filename(video.filename)
    path = os.path.join("uploads", filename)
    video.save(path)

    video_entry = Video(project_id=project_id, filename=filename)
    save_object(video_entry)

    return jsonify({"message": "Video uploaded", "video_id": video_entry.id}), 201


@app.route("/<int:project_id>/annotations", methods=["POST"])
@login_required
def add_annotations(project_id: int):
    """Add annotations to a specific project.

    This function processes a list of annotations provided in the request body and
    associates them with the specified project. It saves the annotations to the database
    and returns a success message upon completion.

    Args:
        project_id (int): The unique identifier of the project to which the annotations are added.

    Returns:
        Response: A JSON response indicating the success of the operation.

    Raises:
        BadRequest: If the request does not contain valid JSON or if the annotations are missing.

    Examples:
        >>> response = add_annotations(1)
        >>> response.status_code
        201
    """

    data = request.json
    annotations = [
        Annotation(
            project_id=project_id,
            timestamp=entry["timestamp"],
            points=entry["points"],
            image_url=entry["image_url"],
        )
        for entry in data["annotations"]
    ]
    save_objects(annotations)
    return jsonify({"message": "Annotations added"}), 201


@app.route("/<int:project_id>/apply", methods=["POST"])
@login_required
def apply_annotations(project_id: int):
    """Apply annotations to a specific project.

    This function processes the annotations associated with the specified project and
    applies them to the corresponding video. It is intended to overlay images at specified
    timestamps using OpenCV, enhancing the video with the provided annotations.

    Args:
        project_id (int): The unique identifier of the project for which annotations are applied.

    Returns:
        None: This function does not return a value.

    Raises:
        NotFound: If the project or associated video cannot be found.

    Examples:
        >>> apply_annotations(1)
    """

    # Locate video, load annotations, and process frames
    # Use OpenCV to overlay images at specified timestamps
    print(f"Applying annotation to project id: {project_id}")
