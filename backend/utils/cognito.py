"""Cognito Utility Module

This module provides utility functions for interacting with AWS Cognito, enabling user
registration, verification, and authentication. It utilizes the Boto3 library to communicate
with AWS services and manage user accounts effectively.

Key Features:
- Registers new users with AWS Cognito.
- Verifies user registration using confirmation codes.
- Authenticates users and retrieves JWT tokens for session management.

Functions:
- sign_up(username: str, password: str, email: str, user_attributes: dict, *args, **kwargs) -> dict: 
  Registers a new user with AWS Cognito and returns the response from the sign-up request.
  
- verify_sign_up(username: str, code: str) -> dict: 
  Confirms a new user's registration using a verification code sent to their email.
  
- login_user(username: str, password: str) -> dict: 
  Authenticates a user with AWS Cognito and returns JWT tokens for session management.

Usage:
This module is intended for use within the application to manage user accounts through AWS Cognito.
It should be imported and utilized to handle user registration, verification, and authentication.

Example:
    from backend.utils.cognito import sign_up, verify_sign_up, login_user

    # Register a new user
    sign_up(
        "testuser", 
        "SecurePassword123", 
        "test@example.com", [
            {"Name": "email", "Value": "test@example.com"}
        ]
    )

    # Verify the user's registration
    verify_sign_up("testuser", "123456")

    # Log in the user
    login_user("testuser", "SecurePassword123")
"""

import boto3

from backend.utils.environ import get_environment_variable

# Initialize the Cognito client to interact with AWS Cognito
cognito_client = boto3.client("cognito-idp")


def sign_up(
    username: str, password: str, email: str, user_attributes: dict, *args, **kwargs
):
    """
    Registers a new user with AWS Cognito.

    Sends a sign-up request to AWS Cognito using the provided username, password,
    and user attributes (such as email). Upon successful registration, AWS Cognito
    may send a verification code to the user's email for account confirmation.

    Args:
        username (str): The unique username for the new user.
        password (str): The password for the new user.
        email (str): The user's email address.
        user_attributes (list): Additional attributes for the user (e.g., email).
        *args, **kwargs: Additional arguments for flexibility.

    Returns:
        dict: A dictionary containing the AWS Cognito response, which includes
        user details and sign-up confirmation status.

    Raises:
        botocore.exceptions.ClientError: If an error occurs during sign-up, such as
        username already existing, an error message is returned.

    Example:
        >>> sign_up(
            "testuser",
            "SecurePassword123",
            "test@example.com", [
                {"Name": "email", "Value": "test@example.com"}
            ]
        )
    """
    return cognito_client.sign_up(
        ClientId=get_environment_variable("COGNITO_CLIENT_ID"),
        Username=username,
        Password=password,
        UserAttributes={"email": email, **user_attributes},
    )


def verify_sign_up(username: str, code: str):
    """
    Confirms a new user's registration with AWS Cognito using a verification code.

    This function verifies a user's registration by validating the confirmation code sent
    to the user's email during sign-up. Both the username and code are required.

    Args:
        username (str): The unique username for the user to be verified.
        code (str): The confirmation code sent to the user’s email.

    Returns:
        dict: AWS Cognito response confirming the account's verified status.

    Raises:
        botocore.exceptions.ClientError: If the code is invalid or expired, an error
        message is returned, indicating verification failure.

    Example:
        >>> verify_sign_up("testuser", "123456")
    """
    return cognito_client.confirm_sign_up(
        ClientId=get_environment_variable("COGNITO_CLIENT_ID"),
        Username=username,
        ConfirmationCode=code,
    )


def login_user(username: str, password: str):
    """
    Authenticates a user with AWS Cognito and initiates a session, returning JWT tokens.

    This function uses the AWS Cognito "USER_PASSWORD_AUTH" authentication flow to verify
    a user's credentials. On successful authentication, JWT tokens (ID token, access token,
    and refresh token) are returned for session management.

    Args:
        username (str): The username of the user attempting to log in.
        password (str): The user's password.

    Returns:
        dict: A dictionary containing the authentication result, including JWT tokens.

    Raises:
        botocore.exceptions.ClientError: If authentication fails due to invalid credentials,
        an error message is returned.

    Example:
        >>> login_user("testuser", "SecurePassword123")
    """
    return cognito_client.initiate_auth(
        ClientId=get_environment_variable("COGNITO_CLIENT_ID"),
        AuthFlow="USER_PASSWORD_AUTH",
        AuthParameters={"USERNAME": username, "PASSWORD": password},
    )
