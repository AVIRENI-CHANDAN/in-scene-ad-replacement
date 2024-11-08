import os
from http import HTTPStatus

from flask import current_app as app
from flask import jsonify, request, send_from_directory

from .cognito_util import sign_up, verify_sign_up
from .environ import get_environment_variable


def register_react_base():
    """
    Registers the route to serve the base React application.

    This function serves the main `index.html` or any other static files
    requested, based on the provided path. It allows the application
    to work as a single-page application with a React frontend.

    Returns:
        None
    """

    @app.route("/")
    @app.route("/<path:path>")
    def serve_react_app(path=""):
        """
        Serve React static files based on the provided path.

        Args:
            path (str): The path to the requested file.

        Returns:
            Response: The static file if found or the React `index.html` as default.
        """
        print(f"Attempting to serve path: {path}")
        try:
            # Check for common static file types
            if path and path.endswith((".js", ".css", ".png", ".jpg", ".svg")):
                return send_from_directory(app.static_folder, path), HTTPStatus.OK
            # Default to serving `index.html` for undefined paths
            return send_from_directory(app.template_folder, "index.html"), HTTPStatus.OK
        except Exception as e:
            print(f"Error serving file: {e}")
            return jsonify({"error": "File not found"}), HTTPStatus.NOT_FOUND


def register_cognito_auth_endpoints():
    """
    Registers authentication-related endpoints for user registration
    and verification using AWS Cognito.

    Endpoints:
        - POST /auth/register: Register a new user.
        - POST /auth/verify_sign_up: Verify a user's sign-up with a code.

    Returns:
        None
    """

    @app.route("/auth/register", methods=["POST"])
    def register_user():
        """
        Register a new user with AWS Cognito.

        Expects JSON data in the request with keys:
            - username (str): The username for the new user.
            - email (str): The email address of the user.
            - password (str): The password for the user.

        Returns:
            Response: JSON response indicating success or failure of the registration.
        """
        try:
            data = request.json
            print(f"Registering user: {data}")

            # Extract user data from request
            username = data.get("username")
            email = data.get("email")
            password = data.get("password")

            # Call to Cognito sign-up utility
            response = sign_up(
                username=username,
                password=password,
                email=email,
                user_attributes=[{"Name": "email", "Value": email}],
            )
            return jsonify(response), HTTPStatus.CREATED
        except Exception as e:
            print(f"Error registering user: {e}")
            return jsonify({"error": "Failed to register user"}), HTTPStatus.BAD_REQUEST

    @app.route("/auth/verify_sign_up", methods=["POST"])
    def verify_user_sign_up():
        """
        Verify a user's sign-up with AWS Cognito.

        Expects JSON data in the request with keys:
            - username (str): The username of the user to verify.
            - code (str): The verification code sent to the user's email.

        Returns:
            Response: JSON response indicating success or failure of verification.
        """
        try:
            data = request.json
            print(f"Verifying sign up: {data}")

            # Extract data for verification
            username = data.get("username")
            code = data.get("code")

            # Call to Cognito verify utility
            response = verify_sign_up(username, code)
            return jsonify(response), HTTPStatus.OK
        except Exception as e:
            print(f"Error verifying sign up: {e}")
            return (
                jsonify({"error": "Failed to verify sign up"}),
                HTTPStatus.BAD_REQUEST,
            )
