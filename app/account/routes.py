import os, time
from flask import Blueprint, render_template, redirect, url_for, flash, current_app, request
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
from werkzeug.security import check_password_hash, generate_password_hash
from .. import db
from .forms import ProfileForm, PasswordChangeForm

bp = Blueprint("account", __name__)

DEFAULT_AVATAR = "https://api.dicebear.com/7.x/initials/svg?seed={}".format
ALLOWED_EXTS = {"jpg","jpeg","png","gif"}

def _is_allowed(filename: str) -> bool:
	ext = (filename.rsplit(".", 1)[-1] or "").lower()
	return ext in ALLOWED_EXTS

@bp.route("/", methods=["GET","POST"])
@login_required
def profile():
	form = ProfileForm(obj=current_user)
	password_form = PasswordChangeForm()
	
	# Handle profile update (only if profile form was submitted)
	if form.validate_on_submit() and form.submit.data:
		current_user.name = form.name.data or current_user.name
		current_user.bio = form.bio.data or None

		file = form.avatar_file.data
		if file and getattr(file, "filename", ""):
			filename = secure_filename(file.filename)
			if not _is_allowed(filename):
				flash("Unsupported image type. Use JPG, PNG, or GIF.", "error")
				return redirect(url_for("account.profile"))
			ext = filename.rsplit(".", 1)[-1].lower()
			new_name = f"user_{current_user.id}_{int(time.time())}.{ext}"
			upload_dir = current_app.config["AVATAR_UPLOAD_FOLDER"]
			os.makedirs(upload_dir, exist_ok=True)
			file_path = os.path.join(upload_dir, new_name)
			file.save(file_path)
			current_user.avatar_url = url_for("static", filename=f"uploads/avatars/{new_name}")

		db.session.commit()
		flash("Profile updated.", "ok")
		return redirect(url_for("account.profile"))

	avatar = current_user.avatar_url or DEFAULT_AVATAR(current_user.email or "User")
	return render_template("account/profile.html", user=current_user, form=form, password_form=password_form, avatar=avatar)

@bp.route("/change-password", methods=["POST"])
@login_required
def change_password():
	password_form = PasswordChangeForm()
	
	if password_form.validate_on_submit():
		if not check_password_hash(current_user.password_hash, password_form.current_password.data):
			flash("Current password is incorrect.", "error")
		else:
			current_user.password_hash = generate_password_hash(password_form.new_password.data)
			db.session.commit()
			flash("Password changed successfully.", "ok")
	else:
		flash("Please fill all password fields correctly.", "error")
	
	return redirect(url_for("account.profile"))