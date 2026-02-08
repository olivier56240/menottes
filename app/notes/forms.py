from flask_wtf import FlaskForm
from wtforms import (
   StringField,
   TextAreaField,
   SelectField,
   DateTimeLocalField
)
from wtforms.validators import DataRequired, Optional, Length

# Catégories disponibles dans toute l'app
CATEGORY_CHOICES = [
   ("voiture", "Voiture"),
   ("moto", "Moto"),
   ("enduro", "Enduro"),
   ("campingcar", "Camping-car"),
   ("4x4", "4x4"),
   ("bourse", "Bourse"),
   ("ballade", "Balade"),
]

class NoteForm(FlaskForm):
   title = StringField(
       "Nom du rassemblement",
       validators=[DataRequired(), Length(min=2, max=80)]
   )

   category = SelectField(
       "Catégorie",
       choices=CATEGORY_CHOICES,
       validators=[DataRequired()]
   )

   content = TextAreaField(
       "Description",
       validators=[Optional()]
   )

   location = StringField(
       "Lieu",
       validators=[Optional()]
   )

   start_at = DateTimeLocalField(
       "Date et heure",
       format="%Y-%m-%dT%H:%M",
       validators=[Optional()]
   )

   