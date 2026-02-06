from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SelectField, SubmitField
from wtforms.validators import DataRequired, Length


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

   submit = SubmitField("Enregistrer")