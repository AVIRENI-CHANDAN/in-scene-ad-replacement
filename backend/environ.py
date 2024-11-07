import os

from dotenv import load_dotenv

load_dotenv()


def get_environment_variable(variable_name: str) -> str:
    """Retrieve the value of an environment variable.

    This function attempts to access the specified environment variable by its name.
    If the variable does not exist, it raises a KeyError with a descriptive message.

    Args:
        variable_name (str): The name of the environment variable to retrieve.

    Returns:
        str: The value of the environment variable.

    Raises:
        KeyError: If the environment variable does not exist.

    Examples:
        >>> os.environ["TEST_VAR"] = "test_value"
        >>> get_environment_variable("TEST_VAR")
        "test_value"
        >>> get_environment_variable("NON_EXISTENT_VAR")
        KeyError: "Environment variable NON_EXISTENT_VAR does not exist. Please set it in your .env file or system environment variables"
    """
    try:
        return os.environ[variable_name]
    except KeyError as e:
        raise KeyError(
            f"Environment variable {variable_name} does not exist. \
                Please set it in your .env file or system environment variables"
        ) from e


def parse_bool(value: str) -> bool:
    """Convert a string to its boolean representation.

    This function evaluates a string input and determines if it represents a true value.
    It recognizes variations such as "true", "1", "yes", and "on" (case insensitive) as true.

    Args:
        value (str): The string to be evaluated as a boolean.

    Returns:
        bool: True if the string represents a true value, otherwise False.

    Examples:
        >>> parse_bool("true")
        True
        >>> parse_bool("no")
        False
    """
    return value.lower() in {"true", "1", "yes", "on"}
