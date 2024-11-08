import os

from backend import (
    create_app,
    get_environment_variable,
    register_react_base,
    run_application,
)

app = create_app(
    static_folder=get_environment_variable("STATIC_FOLDER"),
    template_folder=get_environment_variable("TEMPLATE_FOLDER"),
    root_path=os.path.dirname(__file__),
)
register_react_base(app)

if __name__ == "__main__":
    run_application(app)
