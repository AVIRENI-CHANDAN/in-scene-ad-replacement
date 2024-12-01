"""React Routes Module

This module defines the routes for serving the static files of the React application.
It provides an endpoint to serve the main `index.html` file and other static assets
such as JavaScript, CSS, and image files. The module is designed to support single-page
application behavior by routing all requests to the appropriate static files.

Key Features:
- Serves static files for the React app based on the requested path.
- Defaults to serving `index.html` for unrecognized paths, enabling SPA functionality.
- Handles common static file types including JavaScript, CSS, and images.

Routes:
- GET /: Serves the main `index.html` file or the requested static file.

Usage:
This module is intended to be imported and used within the Flask application to manage
the serving of static files for the React frontend. It should be integrated with the main
application to ensure that the React app is accessible.

Example:
    from backend.routes.react import app as react_app

    # Register the React blueprint in the main application
    main_app.register_blueprint(react_app)
"""

from http import HTTPStatus

from flask import Blueprint, current_app, jsonify, send_from_directory

app = Blueprint("react", __name__, url_prefix="/")


@app.route("/")
@app.route("/<path:path>")
def serve_react_app(path=""):
    """
    Serve static files for the React app based on the given path.

    Args:
        path (str): Path to the requested file. If it's an empty string or
        not a recognized file type, `index.html` will be served by default.

    Returns:
        Response: The requested static file if found or the main `index.
        html` if the path is undefined, enabling single-page application
        behavior.
    """
    try:
        # Serve common static file types directly
        if path and path.endswith((".js", ".css", ".png", ".jpg", ".svg", ".jpeg")):
            return send_from_directory(current_app.static_folder, path), HTTPStatus.OK
        # Default to `index.html` for unrecognized paths
        return (
            send_from_directory(current_app.template_folder, "index.html"),
            HTTPStatus.OK,
        )
    except Exception as e:
        print(f"Error serving file: {e}")
        return jsonify({"error": "File not found"}), HTTPStatus.NOT_FOUND
