import os

from dotenv import load_dotenv

load_dotenv()


def get_environment_variable(variable_name: str) -> str:
    """
    This function retrieves the value of an environment variable.
    If the variable does not exist, it returns None.
    """
    try:
        return os.environ[variable_name]
    except KeyError as e:
        raise KeyError(f"Environment variable {variable_name} does not exist") from e
