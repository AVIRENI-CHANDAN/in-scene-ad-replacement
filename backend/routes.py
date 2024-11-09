import os
from http import HTTPStatus

import boto3
from flask import current_app as app
from flask import jsonify, request, send_from_directory

from .cognito_util import cognito_client, login_user, sign_up, verify_sign_up
from .environ import get_environment_variable


def register_react_base():
    """
    Registers the route to serve the base React application.

    This function configures the root and dynamic paths to serve the `index.html` file, enabling support for a single-page React frontend. It also allows static assets such as `.js`, `.css`, and image files to be served when requested.

    Returns:
        None
    """

    @app.route("/")
    @app.route("/<path:path>")
    def serve_react_app(path=""):
        """
        Serve static files for the React app based on the given path.

        Args:
            path (str): Path to the requested file. If it's an empty string or not a
                        recognized file type, `index.html` will be served by default.

        Returns:
            Response: The requested static file if found or the main `index.html` if the path is undefined, enabling single-page application behavior.
        """
        print(f"Attempting to serve path: {path}")
        try:
            # Serve common static file types directly
            if path and path.endswith((".js", ".css", ".png", ".jpg", ".svg")):
                return send_from_directory(app.static_folder, path), HTTPStatus.OK
            # Default to `index.html` for unrecognized paths
            return send_from_directory(app.template_folder, "index.html"), HTTPStatus.OK
        except Exception as e:
            print(f"Error serving file: {e}")
            return jsonify({"error": "File not found"}), HTTPStatus.NOT_FOUND


def register_cognito_auth_endpoints():
    """
    Registers the authentication endpoints to handle user registration, verification,
    and login with AWS Cognito.

    Endpoints:
        - POST /auth/register: Register a new user with AWS Cognito.
        - POST /auth/verify_sign_up: Confirm user sign-up with a verification code.
        - POST /auth/login: Log in a user and return authentication tokens.

    Returns:
        None
    """

    @app.route("/auth/register", methods=["POST"])
    def register_user():
        """
        Register a new user in AWS Cognito.

        Expects JSON input with:
            - username (str): The user's unique username.
            - email (str): User's email address.
            - password (str): The user's password.

        Returns:
            Response: JSON indicating success or error message, with relevant HTTP status.
        """
        try:
            data = request.json
            if not data:
                return (
                    jsonify({"error": "Missing request body"}),
                    HTTPStatus.BAD_REQUEST,
                )

            # Check required fields
            required_fields = ["username", "email", "password"]
            if not all(field in data and data[field] for field in required_fields):
                return (
                    jsonify({"error": "Missing required fields"}),
                    HTTPStatus.BAD_REQUEST,
                )

            # Extract user data from request
            username = data.get("username")
            email = data.get("email")
            password = data.get("password")

            # Register user with Cognito
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
        Verify the user's sign-up with AWS Cognito by submitting a confirmation code.

        Expects JSON input with:
            - username (str): The username of the user to verify.
            - code (str): The verification code sent to the user's email.

        Returns:
            Response: JSON indicating verification success or failure, with relevant HTTP status.
        """
        try:
            data = request.json
            # Extract verification data
            username = data.get("username")
            code = data.get("code")

            # Verify user with Cognito
            response = verify_sign_up(username, code)
            return jsonify(response), HTTPStatus.OK
        except Exception as e:
            print(f"Error verifying sign up: {e}")
            return (
                jsonify({"error": "Failed to verify sign up"}),
                HTTPStatus.BAD_REQUEST,
            )

    @app.route("/auth/login", methods=["POST"])
    def login_user_endpoint():
        """
        Authenticate a user with AWS Cognito, returning JWT tokens for session management.

        Expects JSON input with:
            - username (str): The user's username.
            - password (str): The user's password.

        Returns:
            Response: JSON containing JWT tokens (ID, access, and refresh) or an error message.
        """
        if not request.is_json:
            return {"error": "Request must be JSON"}, 400
        data = request.json
        if not data or "username" not in data or "password" not in data:
            return {"error": "Username and password are required"}, 400
        username = data.get("username")
        password = data.get("password")

        try:
            # Authenticate user with Cognito
            response = login_user(username, password)
            # Extract JWT tokens from response
            tokens = {
                "id_token": response["AuthenticationResult"]["IdToken"],
                "access_token": response["AuthenticationResult"]["AccessToken"],
                "refresh_token": response["AuthenticationResult"]["RefreshToken"],
            }

            return jsonify(tokens), HTTPStatus.OK

        except cognito_client.exceptions.NotAuthorizedException:
            return (
                jsonify({"error": "Invalid username or password"}),
                HTTPStatus.UNAUTHORIZED,
            )
        except Exception as e:
            print(f"Login error: {e}")
            return jsonify({"error": str(e)}), HTTPStatus.INTERNAL_SERVER_ERROR
