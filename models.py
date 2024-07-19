from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()  

class Blog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    imageURL = db.Column(db.String(80), nullable=False)
    author = db.Column(db.String(80), nullable=False)
    title = db.Column(db.String(120), nullable=False)
    content = db.Column(db.Text, nullable=False)
    createdAt = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'imageURL': self.imageURL,
            'author': self.author,
            'title': self.title,
            'content': self.content,
            'createdAt': self.createdAt.isoformat()
        }


class InstructionalVideo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    author = db.Column(db.String(80), nullable=False)
    title = db.Column(db.String(120), nullable=False)
    url_video = db.Column(db.String(120), nullable=False)
    createdAt = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'author': self.author,
            'title': self.title,
            'url_video': self.url_video,
            'createdAt': self.createdAt.isoformat()
        }