from flask_wtf import FlaskForm
from wtforms import (
   StringField,
   TextAreaField,
   SelectField,
   DateTimeLocalField,
   SubmitField   # ✅ AJOUT ICI
)
from wtforms.validators import DataRequired, Optional, Length

CATEGORY_CHOICES = [
   ("voiture", "Voiture"),
   ("moto", "Moto"),
   ("ballade", "Balade"),
   ("4x4", "4x4"),
   ("enduro", "Enduro"),
   ("campingcar", "Camping-car"),
   ("bourse", "Bourse"),
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
       validators=[Optional(), Length(max=2000)]
   )

   location = StringField(
       "Lieu",
       validators=[Optional(), Length(max=120)]
   )

   start_at = DateTimeLocalField(
       "Date et heure",
       format="%Y-%m-%dT%H:%M",
       validators=[Optional()]
   )
   submit = SubmitField("Publier")