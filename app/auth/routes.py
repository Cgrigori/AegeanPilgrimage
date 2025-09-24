from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from .. import db
from ..models import User
from .forms import LoginForm, SignupForm

bp = Blueprint("auth", __name__)

@bp.route("/login", methods=["GET", "POST"])
def login():
	if current_user.is_authenticated:
		return redirect(url_for("account.profile"))
	form = LoginForm()
	if form.validate_on_submit():
		user = User.query.filter_by(email=form.email.data.lower()).first()
		if user and check_password_hash(user.password_hash, form.password.data):
			login_user(user)
			return redirect(url_for("account.profile"))
		flash("Invalid email or password", "error")
	return render_template("auth/login.html", form=form)

@bp.route("/signup", methods=["GET", "POST"])
def signup():
	if current_user.is_authenticated:
		return redirect(url_for("account.profile"))
	form = SignupForm()
	if form.validate_on_submit():
		if User.query.filter_by(email=form.email.data.lower()).first():
			flash("Email already in use", "error")
		else:
			user = User(
				email=form.email.data.lower(),
				name=form.name.data or "",
				password_hash=generate_password_hash(form.password.data),
				role="user",
			)
			db.session.add(user)
			db.session.commit()
			login_user(user)
			return redirect(url_for("account.profile"))
	return render_template("auth/signup.html", form=form)

@bp.get("/logout")
def logout():
	logout_user()
	return redirect(url_for("pages.home"))
