
# app/main/routes.py

from flask import render_template, redirect, url_for, session
from flask_login import current_user, login_required

from . import bp


@bp.get("/")
def home():
   """
   Page d'entrée :
   - Si connecté -> page carte (choix département)
   - Sinon -> home.html
   """
   if current_user.is_authenticated:
       return redirect(url_for("main.map_index"))
   return render_template("home.html")


@bp.get("/map")
@login_required
def map_index():
   """
   Carte / sélection du département.
   (template: app/templates/map/index.html)
   """
   return render_template("map/index.html")


@bp.get("/map/dept/<dept>")
@login_required
def set_dept(dept: str):
   """
   Enregistre le département choisi en session puis redirige vers la liste.
   """
   dept = (dept or "").strip()

   # Optionnel : normalise (ex: "2A", "2B", "75", "971")
   dept = dept.upper()

   session["dept"] = dept

   # Après sélection -> liste des évènements (tu filtreras ensuite par dept)
   return redirect(url_for("notes.list_notes"))