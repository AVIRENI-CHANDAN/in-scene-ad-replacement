"""Utilities Package Initialization Module

This module serves as the initialization point for the utilities package within the application. It 
imports essential utility functions for managing environment variables and interacting with AWS 
Cognito for user authentication and registration. This structure promotes modularity and 
organization within the codebase.

Key Features:
- Provides access to functions for environment variable management.
- Facilitates user registration, verification, and authentication with AWS Cognito.

Functions:
- get_environment_variable(variable_name: str) -> str: Retrieve the value of environment variable.
- parse_bool(value: str) -> bool: Convert a string to its boolean representation.
- sign_up(username: str, password: str, email: str, user_attributes: dict, *args, **kwargs) -> dict: 
  Registers a new user with AWS Cognito.
- verify_sign_up(username: str, code: str) -> dict: 
  Confirms a new user's registration with a verification code.
- login_user(username: str, password: str) -> dict: 
  Authenticates a user with AWS Cognito and returns JWT tokens.

Usage:
This module is intended to be imported as part of the utilities package. It allows for seamless
interaction with various utility functions related to environment management and user 
authentication.

Example:
    from backend.utils import get_environment_variable, sign_up

    # Retrieve an environment variable
    db_uri = get_environment_variable("DATABASE_URI")

    # Register a new user
    sign_up(
        "testuser", 
        "SecurePassword123", 
        "test@example.com", [
            {"Name": "email", "Value": "test@example.com"}
        ]
    )
"""

from .cognito import login_user, sign_up, verify_sign_up
from .environ import get_environment_variable, parse_bool
