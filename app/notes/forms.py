from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired
from flask_wtf import FlaskForm

class DeleteForm(FlaskForm):
   pass

class NoteForm(FlaskForm):
   title = StringField("Titre", validators=[DataRequired()])
   content = TextAreaField("Contenu", validators=[DataRequired()])
   submit = SubmitField("Enregistrer")