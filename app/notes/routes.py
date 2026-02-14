from datetime import datetime

from flask import render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user

from app.extensions import db
from app.models.note import Note
from . import bp
from .forms import NoteForm


@bp.route("/", methods=["GET"])
@login_required
def list_notes():
   selected_cat = (request.args.get("cat") or "").strip().lower()

   categories = ["moto", "voiture", "enduro", "balade", "4x4", "campingcar", "bourse"]

   image_map = {
       "moto": "moto.jpg",
       "voiture": "voiture.jpg",
       "enduro": "enduro.jpg",
       "balade": "balade.jpg",
       "4x4": "4x4.jpg",
       "campingcar": "campingcar.jpg",
       "bourse": "bourse.jpg",
   }

   category_texts = {
       "moto": "Tous les évènements à venir pour les passionnés de moto.",
       "voiture": "Tous les évènements à venir pour les passionnés d'auto.",
       "enduro": "Sorties et évènements enduro à venir.",
       "balade": "Balades et rendez-vous à venir.",
       "4x4": "Évènements tout-terrain et sorties 4x4 à venir.",
       "campingcar": "Rassemblements et sorties camping-car à venir.",
       "bourse": "Bourses, brocantes et évènements à venir.",
   }

   # Notes user
   q = Note.query.filter_by(user_id=current_user.id)
   if hasattr(Note, "start_at"):
       q = q.order_by(Note.start_at.asc().nulls_last())
   else:
       q = q.order_by(Note.id.desc())
   notes = q.all()

   # Counts
   counts = {}
   for cat in categories:
       counts[cat] = sum(1 for n in notes if (n.category or "").strip().lower() == cat)

   # Filtered notes
   if selected_cat:
       filtered_notes = [
           n for n in notes if (n.category or "").strip().lower() == selected_cat
       ]
   else:
       filtered_notes = notes

   # Prochains évènements (3) pour la catégorie
   now = datetime.utcnow()
   events = []
   if selected_cat and hasattr(Note, "start_at"):
       events = [n for n in filtered_notes if n.start_at and n.start_at >= now]
       events.sort(key=lambda n: n.start_at)
       events = events[:3]

   return render_template(
       "notes/list.html",
       notes=notes,
       filtered_notes=filtered_notes,
       now=now,
       categories=categories,
       image_map=image_map,
       category_texts=category_texts,
       selected_cat=selected_cat,
       events=events,
       counts=counts,
   )


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
           location=form.location.data.strip() if getattr(form, "location", None) and form.location.data else None,
           start_at=form.start_at.data if getattr(form, "start_at", None) else None,
       )
       db.session.add(note)
       db.session.commit()
       flash("Rassemblement créé ✅", "success")
       return redirect(url_for("notes.list_notes"))

   return render_template("notes/create.html", form=form)


@bp.route("/<int:note_id>/edit", methods=["GET", "POST"])
@login_required
def edit_note(note_id):
   note = Note.query.filter_by(id=note_id, user_id=current_user.id).first_or_404()
   form = NoteForm(obj=note)

   if form.validate_on_submit():
       note.title = form.title.data.strip()
       note.content = form.content.data.strip()
       note.category = (form.category.data or "voiture").strip().lower()

       if hasattr(form, "location") and hasattr(note, "location"):
           note.location = form.location.data.strip() if form.location.data else None

       if hasattr(form, "start_at") and hasattr(note, "start_at"):
           note.start_at = form.start_at.data

       db.session.commit()
       flash("Événement modifié ✅", "success")
       return redirect(url_for("notes.list_notes"))

   return render_template("notes/edit.html", form=form, note=note)


@bp.route("/<int:note_id>/delete", methods=["POST"])
@login_required
def delete_note(note_id):
   note = Note.query.filter_by(id=note_id, user_id=current_user.id).first_or_404()
   db.session.delete(note)
   db.session.commit()
   flash("Rassemblement supprimé 🗑️", "success")
   return redirect(url_for("notes.list_notes"))