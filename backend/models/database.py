from flask_sqlalchemy import SQLAlchemy

from backend.utils import get_environment_variable

db = SQLAlchemy()


def initialize_db(app):
    print("Initialising the database")
    app.config["SQLALCHEMY_DATABASE_URI"] = get_environment_variable(
        "SQLALCHEMY_DATABASE_URI"
    )
    db.init_app(app)


def create_db_models():
    db.create_all()
