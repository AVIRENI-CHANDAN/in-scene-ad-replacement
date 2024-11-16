import os

from flask_cors import CORS

from backend import (
    create_app,
    create_db_models,
    get_environment_variable,
    initialize_db,
    register_cognito_auth_endpoints,
    register_react_base,
    run_application,
)

app = create_app(
    static_folder=get_environment_variable("STATIC_FOLDER"),
    template_folder=get_environment_variable("TEMPLATE_FOLDER"),
    root_path=os.path.dirname(__file__),
)
initialize_db(app)
with app.app_context():
    create_db_models()
    register_react_base()
    register_cognito_auth_endpoints()

if __name__ == "__main__":
    CORS(
        app,
        resources={
            r"/auth/*": {  # Apply CORS only to endpoints under /auth/
                "origins": [
                    "http://localhost:3000",
                    "http://localhost:5000",
                ],  # Specify allowed origins
                "methods": ["GET", "POST"],
            }
        },
    )
    run_application(app)
