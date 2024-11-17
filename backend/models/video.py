from .database import db


class Video(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    project_id = db.Column(
        db.Integer, db.ForeignKey("project.id"), nullable=False, index=True
    )
    filename = db.Column(db.String(255), unique=True, nullable=False)
    __table_args__ = (
        db.UniqueConstraint(
            "project_id", "filename", name="unique_filename_per_project"
        ),
    )
