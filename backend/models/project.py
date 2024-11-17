from .database import db


class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255), nullable=False, unique=False, index=True)
    title = db.Column(db.String(100), nullable=False, default="Untitled Project")
    description = db.Column(db.Text)
