import os
import re
from functools import wraps
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

    def validate_username(username):
        """
        Validate the username based on custom criteria.

        A valid username must be between 3 and 30 characters and contain only alphanumeric
        characters or underscores.

        Args:
            username (str): The username to validate.

        Returns:
            bool: True if valid, False otherwise.
        """
        return bool(
            username
            and 3 <= len(username) <= 30
            and re.match("^[a-zA-Z0-9_]+$", username)
        )

    def validate_password(password):
        """
        Validate the password based on custom criteria.

        A valid password must be between 8 and 50 characters.

        Args:
            password (str): The password to validate.

        Returns:
            bool: True if valid, False otherwise.
        """
        return bool(password and 8 <= len(password) <= 50)

    def validate_input(func):
        """
        Decorator function to validate the presence and format of `username` and `password` fields in the JSON request data.

        Args:
            func (function): The function to be decorated.

        Returns:
            function: The wrapped function with input validation.
        """

        @wraps(func)
        def wrapper(*args, **kwargs):
            if not request.is_json:
                return (
                    jsonify({"error": "Request must be JSON"}),
                    HTTPStatus.BAD_REQUEST,
                )

            try:
                data = request.json
            except ValueError:
                return jsonify({"error": "Invalid JSON format"}), 400
            if not data or "username" not in data or "password" not in data:
                return (
                    jsonify({"error": "Username and password are required"}),
                    HTTPStatus.BAD_REQUEST,
                )

            username = data["username"]
            password = data["password"]

            # Validate username and password
            if not (validate_username(username) and validate_password(password)):
                return (
                    jsonify({"error": "Invalid username or password format"}),
                    HTTPStatus.BAD_REQUEST,
                )
            return func(*args, **kwargs)

        return wrapper

    @app.route("/auth/register", methods=["POST"])
    @validate_input
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
            email = data.get("email")

            # Register user with Cognito
            response = sign_up(
                username=data["username"],
                password=data["password"],
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
    @validate_input
    def login_user_endpoint():
        """
        Authenticate a user with AWS Cognito, returning tokens as HTTP-only cookies.

        Expects JSON input with:
            - username (str): The user's username.
            - password (str): The user's password.

        Returns:
            Response: JSON containing a success message if login is successful, or an error message if failed.
        """
        try:
            # Authenticate user with Cognito
            data = request.json
            response_data = login_user(data["username"], data["password"])
            tokens = {
                "id_token": response_data["AuthenticationResult"]["IdToken"],
                "access_token": response_data["AuthenticationResult"]["AccessToken"],
                "refresh_token": response_data["AuthenticationResult"]["RefreshToken"],
            }

            # Create response object
            response = make_response(
                jsonify({"message": "Login successful"}), HTTPStatus.OK
            )

            # Set cookies with HttpOnly, Secure, and SameSite attributes for each token
            response.set_cookie(
                "id_token",
                tokens["id_token"],
                httponly=True,
                secure=True,
                samesite="Strict",
            )
            response.set_cookie(
                "access_token",
                tokens["access_token"],
                httponly=True,
                secure=True,
                samesite="Strict",
            )
            response.set_cookie(
                "refresh_token",
                tokens["refresh_token"],
                httponly=True,
                secure=True,
                samesite="Strict",
            )

            return response

        except cognito_client.exceptions.NotAuthorizedException:
            return (
                jsonify({"error": "Invalid username or password"}),
                HTTPStatus.UNAUTHORIZED,
            )
        except Exception as e:
            print(f"Login error: {e}")
            return jsonify({"error": str(e)}), HTTPStatus.INTERNAL_SERVER_ERROR
