from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField
from wtforms.validators import DataRequired, Length


class NoteForm(FlaskForm):
   title = StringField(
       "Nom du rassemblement",
       validators=[DataRequired(), Length(min=2, max=80)],
   )
   content = TextAreaField(
       "Description",
       validators=[DataRequired(), Length(min=2, max=2000)],
   )