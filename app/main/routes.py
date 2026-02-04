from flask import render_template, redirect, url_for
from flask_login import current_user
from . import bp



@bp.get("/")
def home():
   if current_user.is_authenticated:
       return redirect(url_for("notes.list_notes"))
   return render_template("home.html")