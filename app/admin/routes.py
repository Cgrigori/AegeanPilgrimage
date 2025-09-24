from flask import Blueprint, render_template, abort, request, redirect, url_for, flash
from flask_login import login_required, current_user
from ..models import User, db

bp = Blueprint("admin", __name__)

@bp.get("/accounts")
@login_required
def accounts():
	if current_user.role != "admin":
		abort(403)
	users = User.query.order_by(User.created_at.desc()).all()
	return render_template("admin/accounts.html", users=users)

@bp.post("/accounts/<int:user_id>/role")
@login_required
def set_role(user_id: int):
	if current_user.role != "admin":
		abort(403)
	target = User.query.get_or_404(user_id)
	if target.role == "admin":
		flash("Cannot change role of another admin.", "error")
		return redirect(url_for("admin.accounts"))

	new_role = (request.form.get("role") or "").strip()
	if new_role not in ["user", "creator", "reviewer"]:
		flash("Invalid role.", "error")
		return redirect(url_for("admin.accounts"))

	target.role = new_role
	db.session.commit()
	flash(f"Updated {target.email} to {new_role}.", "ok")
	return redirect(url_for("admin.accounts"))