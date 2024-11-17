from backend.models import Annotation, Project, Video, create_db_models, initialize_db
from backend.utils import get_environment_variable, parse_bool, sign_up, verify_sign_up

from .application import create_app, run_application
from .routes import (
    register_cognito_auth_endpoints,
    register_projects_endpoint,
    register_react_base,
)
