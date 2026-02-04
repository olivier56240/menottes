from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, DateTimeLocalField, SubmitField
from wtforms.validators import DataRequired

class ActivityForm(FlaskForm):
   title = StringField("Titre", validators=[DataRequired()])
   description = TextAreaField("Description", validators=[DataRequired()])
   type = StringField("Type (moto, camping-car, marche...)", validators=[DataRequired()])
   location = StringField("Lieu", validators=[DataRequired()])
   date = DateTimeLocalField("Date", format='%Y-%m-%dT%H:%M', validators=[DataRequired()])
   submit = SubmitField("Créer la sortie")