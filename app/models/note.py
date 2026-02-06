from datetime import datetime
from app.extensions import db

class Note(db.Model):
   id = db.Column(db.Integer, primary_key=True)
   title = db.Column(db.String(120), nullable=False)
   content = db.Column(db.Text, nullable=False)
   created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
   user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
   category = db.Column(db.String(30), nullable=False, default="voiture")