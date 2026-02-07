from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SelectField, SubmitField
from wtforms.validators import DataRequired, Length
from wtforms.fields import DateTimeLocalField
from wtforms.validators import Optional

class NoteForm(FlaskForm):
   title = StringField(
       "Nom du rassemblement",
       validators=[DataRequired(), Length(min=2, max=80)],
   )

   category = SelectField(
       "Catégorie",
       choices=[
           ("voiture", "Voiture"),
           ("moto", "Moto"),
           ("balade", "Balade"),
       ],
       validators=[DataRequired()],
   )

   content = TextAreaField(
       "Description",
       validators=[DataRequired(), Length(min=2, max=2000)],
   )

   location = StringField(
       "Lieu",
       validators=[Optional()],
   )

   start_at = DateTimeLocalField(
       "Date et heure",
       format="%Y-%m-%dT%H:%M",
       validators=[Optional()],
   )

   submit = SubmitField("Enregistrer")