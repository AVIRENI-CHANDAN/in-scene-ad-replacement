import boto3

from backend.utils import get_environment_variable

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