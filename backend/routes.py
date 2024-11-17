import os
import re
from functools import wraps
from http import HTTPStatus

import boto3
import jwt
import requests
from flask import current_app as app
from flask import jsonify, make_response, request, send_from_directory

from .cognito_util import cognito_client, login_user, sign_up, verify_sign_up
from .environ import get_environment_variable


def decode_and_verify_token(token, is_id_token=True):
    """
    Decodes and verifies the given token (ID or access) against the public keys from AWS Cognito.

    Args:
        token (str): The token to verify.
        is_id_token (bool): Flag indicating if the token is an ID token (True) or access token (False).

    Returns:
        dict: Decoded token if verification is successful.
    """
    region = get_environment_variable("AWS_REGION")
    user_pool_id = get_environment_variable("USER_POOL_ID")
    cognito_client_id = get_environment_variable("COGNITO_CLIENT_ID")

    # URL for Cognito's JWKS (JSON Web Key Set)
    cognito_keys_url = f"https://cognito-idp.{region}.amazonaws.com/{user_pool_id}/.well-known/jwks.json"
    jwks_client = jwt.PyJWKClient(cognito_keys_url)

    try:
        # Retrieve the signing key from Cognito based on the token's key ID
        signing_key = jwks_client.get_signing_key_from_jwt(token)

        # Prepare verification options based on token type
        verification_options = {
            "algorithms": ["RS256"],
            "issuer": f"https://cognito-idp.{region}.amazonaws.com/{user_pool_id}",
            "leeway": 60,  # Add a 60-second leeway to account for clock skew
        }

        if is_id_token:
            # Set audience for ID token
            verification_options["audience"] = cognito_client_id
        else:
            # Disable audience verification for access tokens, as they often lack the 'aud' claim
            verification_options["options"] = {"verify_aud": False}

        # Decode the token using the signing key
        decoded_token = jwt.decode(token, signing_key.key, **verification_options)

        print(
            "Decoded token:", decoded_token
        )  # Debugging: Print the decoded token to inspect claims
        return decoded_token

    except jwt.ExpiredSignatureError:
        print("Token has expired.")
        raise jwt.ExpiredSignatureError("Token has expired")
    except jwt.InvalidAudienceError:
        print(
            "Invalid audience claim in token. Verify if 'audience' should match 'user_pool_id' instead of 'cognito_client_id'."
        )
        raise jwt.InvalidAudienceError("Invalid audience in token")
    except jwt.InvalidIssuerError:
        print("Invalid issuer claim in token.")
        raise jwt.InvalidIssuerError("Invalid issuer in token")
    except jwt.PyJWTError as e:
        print(f"Token verification failed with error: {e}")
        raise jwt.InvalidTokenError("Invalid token")


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        token = request.cookies.get("id_token")  # Or use access_token if preferred

        if not token:
            return jsonify({"error": "Authorization required"}), HTTPStatus.UNAUTHORIZED

        try:
            # Decode and verify the token
            decoded_token = decode_and_verify_token(token)
            # You can add any additional verification logic here if needed
            request.user = (
                decoded_token  # Store the decoded token if you want user info
            )

        except jwt.ExpiredSignatureError:
            return jsonify({"error": "Token has expired"}), HTTPStatus.UNAUTHORIZED
        except jwt.InvalidTokenError:
            return jsonify({"error": "Invalid token"}), HTTPStatus.UNAUTHORIZED

        return f(*args, **kwargs)

    return decorated_function


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

    def set_secure_http_only_cookie(response, cookie_name, value):
        """
        Set an HTTP-only secure cookie on the response for authentication tokens.

        Args:
            response (Response): Flask response object.
            cookie_name (str): The name of the cookie to set.
            value (str): The value to store in the cookie.
        """
        response.set_cookie(
            cookie_name,
            value,
            httponly=True,
            secure=True,
            samesite="Strict",
        )

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
            set_secure_http_only_cookie(response, "id_token", tokens["id_token"])
            set_secure_http_only_cookie(
                response, "access_token", tokens["access_token"]
            )
            set_secure_http_only_cookie(
                response, "refresh_token", tokens["refresh_token"]
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

    @app.route("/auth/verify_access_token", methods=["POST"])
    def verify_access_token():
        """
        Verify the given access token stored in an HTTP-only secure cookie against AWS Cognito.

        Returns:
            Response: JSON indicating verification success or failure, with relevant HTTP status.
        """
        # Retrieve the token from the secure HTTP-only cookie
        access_token = request.cookies.get("access_token")
        id_token = request.cookies.get("id_token")
        if not access_token:
            return (
                jsonify({"error": "Access token is missing in cookies"}),
                HTTPStatus.UNAUTHORIZED,
            )

        try:
            # Decode and verify the token
            decoded_token = decode_and_verify_token(access_token, is_id_token=False)
            decoded_id_token = decode_and_verify_token(id_token, is_id_token=True)
            return (
                jsonify(
                    {
                        "message": "Token is valid",
                        "decoded_token": decoded_token,
                        "decoded_id_token": decoded_id_token,
                    }
                ),
                HTTPStatus.OK,
            )
        except jwt.ExpiredSignatureError:
            return jsonify({"error": "Token has expired"}), HTTPStatus.UNAUTHORIZED
        except jwt.InvalidTokenError:
            return jsonify({"error": "Invalid token"}), HTTPStatus.UNAUTHORIZED
        except Exception as e:
            print(f"Token verification error: {e}")
            return (
                jsonify({"error": "Failed to verify token"}),
                HTTPStatus.INTERNAL_SERVER_ERROR,
            )

    @app.route("/auth/refresh_token", methods=["POST"])
    def refresh_access_token():
        """
        Refreshes the access token using the refresh token stored in an HTTP-only secure cookie.

        Returns:
            Response: JSON indicating success with a new access token or an error message with relevant HTTP status.
        """
        # Retrieve the refresh token from the secure HTTP-only cookie
        refresh_token = request.cookies.get("refresh_token")

        if not refresh_token:
            return (
                jsonify({"error": "Refresh token is missing in cookies"}),
                HTTPStatus.UNAUTHORIZED,
            )

        try:
            # Call Cognito to refresh the tokens
            response = cognito_client.initiate_auth(
                ClientId=get_environment_variable("COGNITO_CLIENT_ID"),
                AuthFlow="REFRESH_TOKEN_AUTH",
                AuthParameters={"REFRESH_TOKEN": refresh_token},
            )

            # Extract the new access token
            new_access_token = response["AuthenticationResult"]["AccessToken"]

            # Create response and set the new access token in cookies
            resp = make_response(
                jsonify({"message": "Token refreshed successfully"}), HTTPStatus.OK
            )
            set_secure_http_only_cookie(resp, "access_token", new_access_token)

            return resp

        except cognito_client.exceptions.NotAuthorizedException:
            # Handle expired or invalid refresh token
            print("Refresh token has expired or is invalid.")
            response = make_response(
                jsonify({"error": "Refresh token has expired. Please log in again."}),
                HTTPStatus.UNAUTHORIZED,
            )
            # Clear cookies
            response.set_cookie("access_token", "", expires=0)
            response.set_cookie("id_token", "", expires=0)
            response.set_cookie("refresh_token", "", expires=0)
            return response
        except Exception as e:
            print(f"Token refresh error: {e}")
            return (
                jsonify({"error": "Failed to refresh token"}),
                HTTPStatus.INTERNAL_SERVER_ERROR,
            )

    @app.route("/auth/logout", methods=["POST"])
    @login_required
    def logout():
        """
        Clears authentication cookies on logout.
        """
        response = make_response(
            jsonify({"message": "Logout successful"}), HTTPStatus.OK
        )
        response.set_cookie("access_token", "", expires=0)
        response.set_cookie("id_token", "", expires=0)
        response.set_cookie("refresh_token", "", expires=0)
        return response


def register_projects_endpoint():
    @app.route("/api/projects", methods=["POST"])
    @login_required
    def create_project():
        if not request.is_json:
            return {"error": "Content-Type must be application/json"}, 400
        data = request.json
        if not data or "title" not in data or "description" not in data:
            return {"error": "Title and description are required"}, 400
        project = Project(title=data["title"], description=data["description"])
        db.session.add(project)
        db.session.commit()
        return jsonify({"message": "Project created", "project_id": project.id}), 201

    @app.route("/api/projects", methods=["GET"])
    @login_required
    def list_projects():
        projects = Project.query.all()
        return jsonify(
            [
                {"id": p.id, "title": p.title, "description": p.description}
                for p in projects
            ]
        )

    @app.route("/api/projects/<int:project_id>/upload", methods=["POST"])
    @login_required
    def upload_video(project_id):
        video = request.files["video"]
        filename = secure_filename(video.filename)
        path = os.path.join("uploads", filename)
        video.save(path)

        video_entry = Video(project_id=project_id, filename=filename)
        db.session.add(video_entry)
        db.session.commit()

        return jsonify({"message": "Video uploaded", "video_id": video_entry.id}), 201

    @app.route("/api/projects/<int:project_id>/annotations", methods=["POST"])
    @login_required
    def add_annotations(project_id):
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
        with db.session.begin():
            db.session.bulk_save_objects(annotations)
        db.session.commit()
        return jsonify({"message": "Annotations added"}), 201

    @app.route("/api/projects/<int:project_id>/apply", methods=["POST"])
    @login_required
    def apply_annotations(project_id):
        # Locate video, load annotations, and process frames
        # Use OpenCV to overlay images at specified timestamps
        pass
