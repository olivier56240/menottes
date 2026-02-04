from app.extensions import db

class Membership(db.Model):
   id = db.Column(db.Integer, primary_key=True)

   user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
   activity_id = db.Column(db.Integer, db.ForeignKey('activity.id'))

   user = db.relationship('User', backref='memberships')
   activity = db.relationship('Activity', backref='members')