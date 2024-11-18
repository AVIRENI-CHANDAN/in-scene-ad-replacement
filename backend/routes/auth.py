"""Authentication Routes Module

This module defines the authentication routes for the application, providing endpoints
for user registration, verification, login, token refresh, logout, and access token verification.
It integrates with AWS Cognito for user management and authentication, ensuring secure
handling of user credentials and tokens.

Key Features:
- User registration with AWS Cognito.
- Verification of user sign-up using confirmation codes.
- User login with token generation and secure cookie management.
- Token refresh functionality using refresh tokens stored in secure cookies.
- Logout functionality that clears authentication cookies.
- Access token verification against AWS Cognito.

Routes:
- POST /auth/register: Registers a new user in AWS Cognito.
- POST /auth/verify_sign_up: Verifies the user's sign-up with a confirmation code.
- POST /auth/login: Authenticates a user and returns tokens as HTTP-only cookies.
- POST /auth/refresh_token: Refreshes the access token using the refresh token.
- POST /auth/logout: Clears authentication cookies on logout.
- POST /auth/verify_access_token: Verifies the access token stored in cookies.

Usage:
This module is intended to be imported and used within the Flask application to manage
user authentication and authorization. It should be integrated with the main application
to handle user-related operations securely.

Example:
    from backend.routes.auth import app as auth_app

    # Register the authentication blueprint in the main application
    main_app.register_blueprint(auth_app)
"""

from http import HTTPStatus

import jwt
from flask import Blueprint, jsonify, make_response, request

from backend.utils import get_environment_variable
from backend.utils.cognito import cognito_client, login_user, sign_up, verify_sign_up

from .util import (
    decode_and_verify_token,
    login_required,
    set_secure_http_only_cookie,
    validate_input,
)

app = Blueprint("auth", __name__, url_prefix="/auth")


@app.route("/register", methods=["POST"])
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


@app.route("/verify_sign_up", methods=["POST"])
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


@app.route("/login", methods=["POST"])
@validate_input
def login_user_endpoint():
    """
    Authenticate a user with AWS Cognito, returning tokens as HTTP-only cookies.

    Expects JSON input with:
        - username (str): The user's username.
        - password (str): The user's password.

    Returns:
        Response: JSON containing a success message if login is successful,
        or an error message if failed.
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
        set_secure_http_only_cookie(response, "access_token", tokens["access_token"])
        set_secure_http_only_cookie(response, "refresh_token", tokens["refresh_token"])

        return response

    except cognito_client.exceptions.NotAuthorizedException:
        return (
            jsonify({"error": "Invalid username or password"}),
            HTTPStatus.UNAUTHORIZED,
        )
    except Exception as e:
        print(f"Login error: {e}")
        return jsonify({"error": str(e)}), HTTPStatus.INTERNAL_SERVER_ERROR


@app.route("/refresh_token", methods=["POST"])
def refresh_access_token():
    """
    Refreshes the access token using the refresh token stored in an HTTP-only secure cookie.

    Returns:
        Response: JSON indicating success with a new access token or an
        error message with relevant HTTP status.
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


@app.route("/logout", methods=["POST"])
@login_required
def logout():
    """
    Clears authentication cookies on logout.
    """
    response = make_response(jsonify({"message": "Logout successful"}), HTTPStatus.OK)
    response.set_cookie("access_token", "", expires=0)
    response.set_cookie("id_token", "", expires=0)
    response.set_cookie("refresh_token", "", expires=0)
    return response


@app.route("/verify_access_token", methods=["POST"])
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
