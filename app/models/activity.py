from datetime import datetime
from app.extensions import db

class Activity(db.Model):
   id = db.Column(db.Integer, primary_key=True)

   title = db.Column(db.String(120), nullable=False)
   description = db.Column(db.Text, nullable=False)

   type = db.Column(db.String(50), nullable=False)  # moto, camping-car, marche, bateau...

   location = db.Column(db.String(120), nullable=False)
   date = db.Column(db.DateTime, nullable=False)

   creator_id = db.Column(db.Integer, db.ForeignKey('user.id'))
   creator = db.relationship('User', backref='activities_created')

   created_at = db.Column(db.DateTime, default=datetime.utcnow)