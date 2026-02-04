from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, Length


class RegisterForm(FlaskForm):
   email = StringField("Email", validators=[DataRequired(), Email(), Length(max=255)])
   password = PasswordField("Mot de passe", validators=[DataRequired(), Length(min=6)])
   submit = SubmitField("Créer le compte")


class LoginForm(FlaskForm):
   email = StringField("Email", validators=[DataRequired(), Email(), Length(max=255)])
   password = PasswordField("Mot de passe", validators=[DataRequired()])
   submit = SubmitField("Se connecter")