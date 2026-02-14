
from flask import render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from datetime import datetime

from app.extensions import db
from app.models.note import Note
from . import bp
from .forms import NoteForm


# =========================
# LISTE DES NOTES
# =========================
@bp.route("/", methods=["GET"])
@login_required
def list_notes():

   selected_cat = (request.args.get("cat") or "").strip().lower()

   # Récupération des notes utilisateur
   query = Note.query.filter_by(user_id=current_user.id)

   if hasattr(Note, "start_at"):
       query = query.order_by(Note.start_at.asc().nulls_last())
   else:
       query = query.order_by(Note.id.desc())

   notes = query.all()

   # Textes panneau droite
   category_texts = {
       "moto": "Tous les évènements à venir pour les passionnés de moto.",
       "voiture": "Tous les évènements à venir pour les passionnés d'auto.",
       "enduro": "Sorties et évènements enduro à venir.",
       "balade": "Balades et rendez-vous à venir.",
       "4x4": "Évènements tout-terrain et sorties 4x4 à venir.",
       "campingcar": "Rassemblements et sorties camping-car à venir.",
       "bourse": "Bourses, brocantes et évènements à venir.",
   }

   # Filtrage si catégorie sélectionnée
   if selected_cat:
       filtered = [
           n for n in notes
           if (n.category or "").strip().lower() == selected_cat
       ]
   else:
       filtered = notes

   # 3 prochains événements
   now = datetime.utcnow()
   events = []

   if hasattr(Note, "start_at"):
       future = [n for n in filtered if n.start_at and n.start_at >= now]
       future.sort(key=lambda n: n.start_at)
       events = future[:3]

   return render_template(
       "notes/list.html",
       notes=notes,
       selected_cat=selected_cat,
       category_texts=category_texts,
       events=events,
   )


# =========================
# CREATE
# =========================
@bp.route("/create", methods=["GET", "POST"])
@login_required
def create_note():

   form = NoteForm()

   if form.validate_on_submit():

       note = Note(
           title=form.title.data.strip(),
           content=form.content.data.strip(),
           category=(form.category.data or "voiture").strip().lower(),
           user_id=current_user.id,
           location=form.location.data.strip() if form.location.data else None,
           start_at=form.start_at.data,
       )

       db.session.add(note)
       db.session.commit()

       flash("Rassemblement créé ✅", "success")
       return redirect(url_for("notes.list_notes"))

   return render_template("notes/create.html", form=form)


# =========================
# EDIT
# =========================
@bp.route("/<int:note_id>/edit", methods=["GET", "POST"])
@login_required
def edit_note(note_id):

   note = Note.query.filter_by(
       id=note_id,
       user_id=current_user.id
   ).first_or_404()

   form = NoteForm(obj=note)

   if form.validate_on_submit():

       note.title = form.title.data.strip()
       note.content = form.content.data.strip()
       note.category = (form.category.data or "voiture").strip().lower()

       if hasattr(note, "location"):
           note.location = form.location.data.strip() if form.location.data else None

       if hasattr(note, "start_at"):
           note.start_at = form.start_at.data

       db.session.commit()

       flash("Événement modifié ✅", "success")
       return redirect(url_for("notes.list_notes"))

   return render_template("notes/edit.html", form=form, note=note)


# =========================
# DELETE
# =========================
@bp.route("/<int:note_id>/delete", methods=["POST"])
@login_required
def delete_note(note_id):

   note = Note.query.filter_by(
       id=note_id,
       user_id=current_user.id
   ).first_or_404()

   db.session.delete(note)
   db.session.commit()

   flash("Rassemblement supprimé 🗑️", "success")
   return redirect(url_for("notes.list_notes"))