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
        user_attributes (dict): Additional attributes for the user (e.g., email).

    Returns:
        tuple: JSON response and HTTP status code.
            - On success: A JSON response with a success message and HTTP 200.
            - If the username exists: JSON with an error message and HTTP 400.
            - On other exceptions: JSON with an error message and HTTP 500.

    Example:
        >>> sign_up("testuser", "SecurePassword123", "test@example.com", {"email": "test@example.com"})
    """
    try:
        # Send the sign-up request to AWS Cognito
        response = cognito_client.sign_up(
            ClientId=get_environment_variable("COGNITO_CLIENT_ID"),
            Username=username,
            Password=password,
            UserAttributes=user_attributes,
        )
        # On success, return a confirmation message
        return (
            jsonify(
                {
                    "message": "User registered successfully. Check your email for verification."
                }
            ),
            HTTPStatus.OK,
        )
    except cognito_client.exceptions.UsernameExistsException:
        # Handle case where the username already exists in Cognito
        return jsonify({"error": "User already exists"}), 400
    except Exception as e:
        # Handle other exceptions and provide error details
        return jsonify({"error": str(e)}), 500


def verify_sign_up(username: str, code: str):
    """
    Confirms a new user's registration with AWS Cognito.

    This function verifies a user's registration by checking the confirmation code sent to the
    user's email during sign-up. The code must be submitted with the username for verification.

    Args:
        username (str): The unique username for the user to be verified.
        code (str): The confirmation code sent to the user’s email.

    Returns:
        tuple: JSON response and HTTP status code.
            - On success: JSON response with a success message and HTTP 200.
            - If the code is invalid: JSON with an error message and HTTP 400.
            - On other exceptions: JSON with an error message and HTTP 500.

    Example:
        >>> verify_sign_up("testuser", "123456")
    """
    data = request.json
    try:
        # Verify the user's sign-up using the confirmation code
        cognito_client.confirm_sign_up(
            ClientId=get_environment_variable("COGNITO_CLIENT_ID"),
            Username=data["username"],
            ConfirmationCode=data["code"],
        )
        # On success, return a confirmation message
        return jsonify({"message": "User verified successfully."}), 200
    except cognito_client.exceptions.CodeMismatchException:
        # Handle case where the confirmation code is invalid
        return jsonify({"error": "Invalid verification code"}), 400
    except Exception as e:
        # Handle other exceptions and provide error details
        return jsonify({"error": str(e)}), 500
