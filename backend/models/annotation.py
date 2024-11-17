from .database import db


class Annotation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    project_id = db.Column(
        db.Integer, db.ForeignKey("project.id"), nullable=False, index=True
    )
    timestamp = db.Column(db.Float)
    points = db.Column(db.JSON)
    image_url = db.Column(db.String(2048))
