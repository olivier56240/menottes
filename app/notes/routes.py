from flask import render_template, redirect, url_for, flash, request, abort, session
from flask_login import login_required, current_user
from datetime import datetime
from app.services.cloudinary_service import upload_image
from app.extensions import db
from app.models.note import Note
from . import bp
from .forms import NoteForm
from app.models.participant import Participant

@bp.route("/", methods=["GET"])
@login_required
def list_notes():
   selected_cat = (request.args.get("cat") or "").strip().lower()

   dept = session.get("dept")
   if not dept:
       return redirect(url_for("main.map_index"))

   # 🔥 Filtrage par utilisateur + département
   q = Note.query.filter_by(
       user_id=current_user.id,
       dept_code=dept
   )

   if hasattr(Note, "start_at"):
       q = q.order_by(Note.start_at.asc().nulls_last())
   else:
       q = q.order_by(Note.id.desc())

   notes = q.all()

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

   if selected_cat:
       filtered_notes = [n for n in notes if (n.category or "").strip().lower() == selected_cat]
   else:
       filtered_notes = notes

   counts = {
       cat: sum(1 for n in notes if (n.category or "").strip().lower() == cat)
       for cat in categories
   }

   now = datetime.utcnow()
   events = []
   if selected_cat and hasattr(Note, "start_at"):
       events = [n for n in filtered_notes if getattr(n, "start_at", None) and n.start_at >= now]
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
       dept=dept,
   )


@bp.route("/create", methods=["GET", "POST"])
@login_required
def create_note():
   form = NoteForm()

   if request.method == "GET":
       form.dept_code.data = session.get("dept", "")

   if form.validate_on_submit():
       note = Note(
           title=form.title.data.strip(),
           content=form.content.data.strip(),
           category=(form.category.data or "voiture").strip().lower(),
           user_id=current_user.id,
           location=form.location.data.strip() if getattr(form, "location", None) else None,
           start_at=form.start_at.data if hasattr(form, "start_at") else None,
       )

       # Photo cover (optionnelle)
       if getattr(form, "cover", None) and form.cover.data:
           url = upload_image(form.cover.data, folder="rassoride/events")
           if url:
               note.cover_url = url
           else:
               flash("Photo non envoyée (Cloudinary non configuré).", "warning")

       # Dept code (TOUJOURS, même sans photo)
       note.dept_code = (form.dept_code.data or session.get("dept") or "").strip()

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

   if request.method == "GET":
       form.dept_code.data = session.get("dept", "") or getattr(note, "dept_code", "")

   if form.validate_on_submit():
       note.title = form.title.data.strip()
       note.content = form.content.data.strip()
       note.category = (form.category.data or "voiture").strip().lower()

       if hasattr(form, "location") and hasattr(note, "location"):
           note.location = form.location.data.strip() if form.location.data else None

       if hasattr(form, "start_at") and hasattr(note, "start_at"):
           note.start_at = form.start_at.data

       note.dept_code = (form.dept_code.data or session.get("dept") or note.dept_code or "").strip()

       db.session.commit()
       flash("Événement modifié ✅", "success")
       return redirect(url_for("notes.list_notes"))

   return render_template("notes/edit.html", form=form, note=note)

@bp.route("/<int:note_id>")
def view_note(note_id):
   note = Note.query.get_or_404(note_id)

   participants = Participant.query.filter_by(note_id=note.id).all()
   participant_count = len(participants)

   is_participant = False
   if current_user.is_authenticated:
       is_participant = Participant.query.filter_by(
           user_id=current_user.id,
           note_id=note.id
       ).first() is not None

   return render_template(
       "notes/detail.html",
       note=note,
       participants=participants,
       participant_count=participant_count,
       is_participant=is_participant,
   )
@bp.route("/<int:note_id>/delete", methods=["POST"])
@login_required
def delete_note(note_id):
   note = Note.query.get_or_404(note_id)

   if note.user_id != current_user.id:
       abort(403)

   db.session.delete(note)
   db.session.commit()
   flash("Évènement supprimé.")
   return redirect(url_for("notes.list_notes"))

@bp.route("/<int:note_id>/join", methods=["POST"])
@login_required
def join_note(note_id):
   note = Note.query.get_or_404(note_id)

   existing = Participant.query.filter_by(
       user_id=current_user.id,
       note_id=note.id
   ).first()

   if not existing:
       participant = Participant(user_id=current_user.id, note_id=note.id)
       db.session.add(participant)
       db.session.commit()
       flash("Tu participes à cet événement ✅", "success")
   else:
       flash("Tu participes déjà à cet événement.", "info")

   return redirect(url_for("notes.view_note", note_id=note.id))


@bp.route("/<int:note_id>/leave", methods=["POST"])
@login_required
def leave_note(note_id):
   note = Note.query.get_or_404(note_id)

   existing = Participant.query.filter_by(
       user_id=current_user.id,
       note_id=note.id
   ).first()

   if existing:
       db.session.delete(existing)
       db.session.commit()
       flash("Tu ne participes plus à cet événement.", "info")

   return redirect(url_for("notes.view_note", note_id=note.id))