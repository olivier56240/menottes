
from flask_wtf import FlaskForm
from wtforms import SubmitField
from flask_wtf.file import FileField, FileAllowed

class ProfileForm(FlaskForm):
   avatar = FileField("Photo de profil", validators=[
       FileAllowed(["jpg", "jpeg", "png", "webp"], "Images uniquement (jpg, png, webp).")
   ])
   submit = SubmitField("Enregistrer")