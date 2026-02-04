
from flask import render_template, redirect, url_for, flash
from flask_login import login_required, current_user

from app.extensions import db
from app.models.note import Note
from . import bp
from .forms import NoteForm


@bp.get("/")
@login_required
def list_notes():
   notes = (
       Note.query
       .filter_by(user_id=current_user.id)
       .order_by(Note.id.desc())
       .all()
   )
   return render_template("notes/list.html", notes=notes)


@bp.route("/create", methods=["GET", "POST"])
@login_required
def create_note():
   form = NoteForm()

   if form.validate_on_submit():
       note = Note(
           content=form.content.data,
           user_id=current_user.id
       )

       db.session.add(note)
       db.session.commit()
       flash("Note créée ✅", "success")
       return redirect(url_for("notes.list_notes"))

   return render_template("notes/create.html", form=form)

@bp.route("/<int:note_id>/edit", methods=["GET", "POST"])
@login_required
def edit_note(note_id: int):
   note = Note.query.filter_by(
   id=note_id,
   user_id=current_user.id
).first_or_404()
   form = NoteForm(obj=note)
   if form.validate_on_submit():
       note.content = form.content.data
       db.session.commit()
       flash("Note modifiée ✅", "success")
       return redirect(url_for("notes.list_notes"))
   return render_template("notes/edit.html", form=form, note=note)



@bp.route("/<int:note_id>/delete", methods=["POST"])
@login_required
def delete_note(note_id: int):
 note = Note.query.filter_by(
   id=note_id,
   user_id=current_user.id
).first_or_404()
 
 db.session.delete(note)
 db.session.commit()
 flash("Note supprimée 🗑️", "success")
 return redirect(url_for("notes.list_notes"))