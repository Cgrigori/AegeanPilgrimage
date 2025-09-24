import os, time
from flask import Blueprint, render_template, redirect, url_for, flash, current_app
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
from .. import db
from .forms import ProfileForm

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
	if form.validate_on_submit():
		# Update name and bio
		current_user.name = form.name.data or current_user.name
		current_user.bio = form.bio.data or None

		# Handle avatar upload (optional)
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
			# Save URL path (served from /static)
			current_user.avatar_url = url_for("static", filename=f"uploads/avatars/{new_name}")

		db.session.commit()
		flash("Profile updated.", "ok")
		return redirect(url_for("account.profile"))

	avatar = current_user.avatar_url or DEFAULT_AVATAR(current_user.email or "User")
	return render_template("account/profile.html", user=current_user, form=form, avatar=avatar)