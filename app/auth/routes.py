from flask import render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required
from . import bp
from .forms import RegisterForm, LoginForm
from ..extensions import db
from ..models.user import User


@bp.route("/register", methods=["GET", "POST"])
def register():
   form = RegisterForm()
   if form.validate_on_submit():
       email = form.email.data.lower().strip()

       existing = User.query.filter_by(email=email).first()
       if existing:
           flash("Email déjà utilisé.", "warning")
           return redirect(url_for("auth.register"))

       user = User(email=email)
       user.set_password(form.password.data)

       db.session.add(user)
       db.session.commit()

       flash("Compte créé ✅ Tu peux te connecter.", "success")
       return redirect(url_for("auth.login"))

   return render_template("auth/register.html", form=form)


@bp.route("/login", methods=["GET", "POST"])
def login():
   form = LoginForm()
   if form.validate_on_submit():
       email = form.email.data.lower().strip()
       user = User.query.filter_by(email=email).first()

       if user and user.check_password(form.password.data):
           login_user(user)
           next_url = request.args.get("next") or url_for("main.home")
           return redirect(next_url)

       flash("Identifiants invalides.", "danger")

   return render_template("auth/login.html", form=form)


@bp.get("/logout")
@login_required
def logout():
   logout_user()
   flash("Déconnecté.", "info")
   return redirect(url_for("main.home"))