from http import HTTPStatus

import boto3

from .environ import get_environment_variable

# Initialize the Cognito client to interact with AWS Cognito
cognito_client = boto3.client("cognito-idp")


def sign_up(
    username: str, password: str, email: str, user_attributes: dict, *args, **kwargs
):
    """
    Registers a new user with AWS Cognito.

    This function sends a sign-up request to AWS Cognito using the provided username, password,
    and user attributes (such as email). Upon successful registration, AWS Cognito may send a
    verification code to the user's email.

    Args:
        username (str): The unique username for the new user.
        password (str): The password for the new user.
        email (str): The user's email address.
        user_attributes (list): Additional attributes for the user (e.g., email).

    Returns:
        tuple: A tuple containing the JSON response and HTTP status code.
            - On success: A JSON response with a success message and HTTPStatus.OK (200).
            - If the username exists: JSON with an error message and HTTPStatus.BAD_REQUEST (400).
            - On other exceptions: JSON with an error message and HTTPStatus.INTERNAL_SERVER_ERROR (500).

    Example:
        >>> sign_up("testuser", "SecurePassword123", "test@example.com", [{"Name": "email", "Value": "test@example.com"}])
    """
    return cognito_client.sign_up(
        ClientId=get_environment_variable("COGNITO_CLIENT_ID"),
        Username=username,
        Password=password,
        UserAttributes=user_attributes,
    )


def verify_sign_up(username: str, code: str):
    """
    Confirms a new user's registration with AWS Cognito.

    This function verifies a user's registration by checking the confirmation code sent to the
    user's email during sign-up. The code must be submitted with the username for verification.

    Args:
        username (str): The unique username for the user to be verified.
        code (str): The confirmation code sent to the user’s email.

    Returns:
        tuple: A tuple containing the JSON response and HTTP status code.
            - On success: JSON response with a success message and HTTPStatus.OK (200).
            - If the code is invalid: JSON with an error message and HTTPStatus.BAD_REQUEST (400).
            - On other exceptions: JSON with an error message and HTTPStatus.INTERNAL_SERVER_ERROR (500).

    Example:
        >>> verify_sign_up("testuser", "123456")
    """
    # Verify the user's sign-up using the confirmation code
    return cognito_client.confirm_sign_up(
        ClientId=get_environment_variable("COGNITO_CLIENT_ID"),
        Username=username,
        ConfirmationCode=code,
    )
