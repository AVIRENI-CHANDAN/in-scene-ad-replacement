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


class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255), nullable=False, unique=False, index=True)
    title = db.Column(db.String(100), nullable=False, default="Untitled Project")
    description = db.Column(db.Text)


class Video(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    project_id = db.Column(
        db.Integer, db.ForeignKey("project.id"), nullable=False, index=True
    )
    filename = db.Column(db.String(255), unique=True)
    __table_args__ = (
        db.UniqueConstraint(
            "project_id", "filename", name="unique_filename_per_project"
        ),
    )


class Annotation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    project_id = db.Column(
        db.Integer, db.ForeignKey("project.id"), nullable=False, index=True
    )
    timestamp = db.Column(db.Float)
    points = db.Column(db.JSON)
    image_url = db.Column(db.String(2048))
