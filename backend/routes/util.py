"""Utility Functions Module

This module provides various utility functions and decorators for handling authentication,
input validation, and secure cookie management within the application. It includes functions
for decoding and verifying JWT tokens, validating usernames and passwords, and managing
HTTP-only secure cookies.

Key Features:
- Decodes and verifies JWT tokens against AWS Cognito.
- Validates usernames and passwords based on custom criteria.
- Sets HTTP-only secure cookies for authentication tokens.
- Provides decorators for input validation and login requirements.

Functions:
- decode_and_verify_token(token, is_id_token=True): 
    Decodes, verifies the given token against AWS Cognito.
- validate_username(username): 
    Validates the username based on specified criteria.
- validate_password(password): 
    Validates the password based on specified criteria.
- set_secure_http_only_cookie(response, cookie_name, value): 
    Sets an HTTP-only secure cookie on the response.
- validate_input(func): 
    Decorator to validate the presence and format of `username` and `password` fields.
- login_required(f): 
    Decorator to enforce authentication for specific routes.
- generate_sha256_coded_string(input_string: str) -> str: 
    Generates a SHA-256 hash of the input string.
- secure_filename(file_name: str) -> str: 
    Generates a secure filename by hashing the original filename.

Usage:
This module is intended to be imported and used within the Flask application to manage
authentication and input validation. It should be integrated with the main application to
ensure secure handling of user credentials and tokens.

Example:
    from backend.routes.util import validate_input, login_required

    @app.route("/some_route", methods=["POST"])
    @login_required
    @validate_input
    def some_protected_route():
        ...
"""

import base64
import hashlib
import re
from functools import wraps
from http import HTTPStatus

import jwt
from flask import jsonify, request

from backend.utils import get_environment_variable


def decode_and_verify_token(token, is_id_token=True):
    """
    Decodes and verifies the given token (ID or access) against the public keys from AWS Cognito.

    Args:
        token (str): The token to verify.
        is_id_token (bool): Flag indicating if the token is an ID token (True)
        or access token (False).

    Returns:
        dict: Decoded token if verification is successful.
    """
    region = get_environment_variable("AWS_REGION")
    user_pool_id = get_environment_variable("USER_POOL_ID")
    cognito_client_id = get_environment_variable("COGNITO_CLIENT_ID")

    # URL for Cognito's JWKS (JSON Web Key Set)
    cognito_keys_domain = f"https://cognito-idp.{region}.amazonaws.com"
    cognito_keys_url = f"{cognito_keys_domain}/{user_pool_id}/.well-known/jwks.json"
    jwks_client = jwt.PyJWKClient(cognito_keys_url)

    try:
        # Retrieve the signing key from Cognito based on the token's key ID
        signing_key = jwks_client.get_signing_key_from_jwt(token)

        # Prepare verification options based on token type
        verification_options = {
            "algorithms": ["RS256"],
            "issuer": f"{cognito_keys_domain}/{user_pool_id}",
            "leeway": 60,  # Add a 60-second leeway to account for clock skew
        }

        if is_id_token:
            # Set audience for ID token
            verification_options["audience"] = cognito_client_id
        else:
            # Disable audience verification for access tokens, as they often lack the 'aud' claim
            verification_options["options"] = {"verify_aud": False}

        return jwt.decode(token, signing_key.key, **verification_options)
    except jwt.ExpiredSignatureError as err:
        print("Token has expired.")
        raise jwt.ExpiredSignatureError("Token has expired") from err
    except jwt.InvalidAudienceError as err:
        print(
            "Invalid audience claim in token.\
            Verify if 'audience' should match 'user_pool_id' instead of 'cognito_client_id'."
        )
        raise jwt.InvalidAudienceError("Invalid audience in token") from err
    except jwt.InvalidIssuerError as err:
        print("Invalid issuer claim in token.")
        raise jwt.InvalidIssuerError("Invalid issuer in token") from err
    except jwt.PyJWTError as e:
        print(f"Token verification failed with error: {e}")
        raise jwt.InvalidTokenError("Invalid token") from e


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
        username and 3 <= len(username) <= 30 and re.match("^[a-zA-Z0-9_]+$", username)
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
    Decorator function to validate the presence and format of `username`
    and `password` fields in the JSON request data.

    Args:
        func (function): The function to be decorated.

    Returns:
        function: The wrapped function with input validation.
    """

    @wraps(func)
    def wrapper(*args, **kwargs):
        if not request.is_json:
            return jsonify({"error": "Request must be JSON"}), HTTPStatus.BAD_REQUEST

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


def login_required(f):
    """Decorator to enforce authentication for a route.

    This decorator checks for the presence of a valid authentication token in the request
    cookies before allowing access to the decorated route. If the token is missing or invalid,
    it returns an unauthorized error response.

    Args:
        f (function): The function to be decorated, representing the route handler.

    Returns:
        function: The wrapped function with authentication enforcement.

    Raises:
        Unauthorized: If the token is missing, expired, or invalid.

    Examples:
        @app.route("/protected")
        @login_required
        def protected_route():
            return jsonify({"message": "Access granted"})
    """

    @wraps(f)
    def decorated_function(*args, **kwargs):
        token = request.cookies.get("id_token")  # Or use access_token if preferred

        if not token:
            return jsonify({"error": "Authorization required"}), HTTPStatus.UNAUTHORIZED

        try:
            # Decode and verify the token
            decoded_token = decode_and_verify_token(token)
            # You can add any additional verification logic here if needed
            request.id_token = (
                decoded_token  # Store the decoded token if you want user info
            )

        except jwt.ExpiredSignatureError:
            return jsonify({"error": "Token has expired"}), HTTPStatus.UNAUTHORIZED
        except jwt.InvalidTokenError:
            return jsonify({"error": "Invalid token"}), HTTPStatus.UNAUTHORIZED

        return f(*args, **kwargs)

    return decorated_function


def generate_sha256_coded_string(input_string: str) -> str:
    """Generate a SHA-256 hash of the input string and encode it in a URL-safe format.

    This function takes an input string, computes its SHA-256 hash, and then encodes
    the resulting binary hash into a URL-safe base64 string. This is useful for creating
    secure identifiers or tokens.

    Args:
        input_string (str): The string to be hashed and encoded.

    Returns:
        str: The URL-safe base64 encoded SHA-256 hash of the input string.

    Examples:
        >>> hash_string = generate_sha256_coded_string("my_secure_string")
    """

    # Generate SHA-256 hash
    sha256_hash = hashlib.sha256(input_string.encode()).digest()

    return base64.urlsafe_b64encode(sha256_hash).decode()


def secure_filename(file_name: str) -> str:
    """Generate a secure filename by hashing the original filename.

    This function takes a filename as input and returns a SHA-256 hash of the filename
    encoded in a URL-safe format. This is useful for ensuring that filenames are unique
    and secure when storing files.

    Args:
        file_name (str): The original filename to be secured.

    Returns:
        str: The URL-safe base64 encoded SHA-256 hash of the original filename.

    Examples:
        >>> secure_name = secure_filename("my_file.txt")
    """

    return generate_sha256_coded_string(file_name)
