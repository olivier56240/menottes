from flask import render_template, redirect, url_for
from flask_login import login_required, current_user

from . import bp
from .forms import ActivityForm
from ..extensions import db
from ..models import Activity


@bp.route("/")
#@login_required
def list_activities():
   activities = Activity.query.order_by(Activity.date).all()
   return render_template("activities/list.html", activities=activities)


@bp.route("/create", methods=["GET", "POST"])
@login_required
def create_activity():
   form = ActivityForm()

   if form.validate_on_submit():
       activity = Activity(
           title=form.title.data,
           description=form.description.data,
           type=form.type.data,
           location=form.location.data,
           date=form.date.data,
           creator=current_user
       )
       db.session.add(activity)
       db.session.commit()
       return redirect(url_for('activities.list_activities'))

   return render_template("activities/create.html", form=form)