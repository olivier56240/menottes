from flask import render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from datetime import datetime

from app.extensions import db
from app.models.note import Note
from . import bp
from .forms import NoteForm


@bp.route("/", methods=["GET"])
@login_required
def list_notes():
   q = Note.query.filter_by(user_id=current_user.id)

   if hasattr(Note, "start_at"):
       q = q.order_by(Note.start_at.asc().nulls_last())
   else:
       q = q.order_by(Note.id.desc())

   notes = q.all()
 
   return render_template("notes/list.html", notes=notes, now=datetime.utcnow())
   


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


@bp.route("/<int:note_id>/edit", methods=["GET", "POST"])
@login_required
def edit_note(note_id):
   note = Note.query.filter_by(id=note_id, user_id=current_user.id).first_or_404()
   form = NoteForm(obj=note)

   if form.validate_on_submit():
       note.title = form.title.data.strip()
       note.content = form.content.data.strip()
       note.category = (form.category.data or "voiture").strip().lower()

       # Champs optionnels (ne cassent jamais)
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