import os
from http import HTTPStatus

from flask import current_app as app
from flask import jsonify, send_from_directory


def register_react_base():
    """Register the route to serve the React base application.

    Args:
        None

    Returns:
        None
    """

    @app.route("/")
    @app.route("/<path:path>")
    def serve_react_app(path=""):
        """Serve React static files based on the provided path.

        Args:
            path (str): The path to the requested file.

        Returns:
            Response: The static file if found or the React index.html.
        """
        print(f"Attempting to serve path: {path}")
        try:
            if path and path.endswith((".js", ".css", ".png", ".jpg", ".svg")):
                return (
                    send_from_directory(app.static_folder, path),
                    HTTPStatus.OK,
                )
            return (
                send_from_directory(app.template_folder, "index.html"),
                HTTPStatus.OK,
            )
        except Exception as e:
            print(f"Error serving file: {e}")
            return jsonify({"error": "File not found"}), HTTPStatus.NOT_FOUND
