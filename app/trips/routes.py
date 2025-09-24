from flask import Blueprint, render_template, abort, redirect, url_for, request, flash
from flask_login import login_required, current_user
from ..models import Trip, TripPhoto, db
from ..utils import require_role
from .forms import TripForm, TripPhotoForm

bp = Blueprint("trips", __name__)

@bp.get("/")
def index():
	featured = Trip.query.filter_by(is_active=True).order_by(Trip.created_at.desc()).first()
	others = Trip.query.filter(Trip.is_active==True, Trip.id != (featured.id if featured else 0)).order_by(Trip.created_at.desc()).all()
	return render_template("trips/index.html", featured=featured, trips=others)

@bp.get("/<slug>")
def detail(slug):
	trip = Trip.query.filter_by(slug=slug, is_active=True).first_or_404()
	return render_template("trips/detail.html", trip=trip)

@bp.get("/manage")
@login_required
@require_role("admin","creator")
def manage_index():
	trips = Trip.query.order_by(Trip.created_at.desc()).all()
	return render_template("trips/manage_index.html", trips=trips)

@bp.route("/manage/new", methods=["GET","POST"])
@login_required
@require_role("admin","creator")
def manage_new():
	form = TripForm()
	if form.validate_on_submit():
		if Trip.query.filter_by(slug=form.slug.data).first():
			flash("Slug already exists", "error")
		else:
			t = Trip(
				title=form.title.data,
				slug=form.slug.data,
				short_description=form.short_description.data or "",
				detailed_plan=form.detailed_plan.data or "",
				hero_image_url=form.hero_image_url.data or "",
				price_cents=form.price_cents.data or 0,
			)
			# Admin-only: active and booking mode
			if current_user.role == "admin":
				t.is_active = bool(form.is_active.data)
				t.booking_mode = form.booking_mode.data or "none"
			else:
				# Creator defaults
				t.is_active = False
				t.booking_mode = "none"
			db.session.add(t); db.session.commit()
			return redirect(url_for("trips.manage_edit", slug=t.slug))
	return render_template("trips/manage_edit.html", form=form, trip=None, photos=[])

@bp.route("/manage/<slug>", methods=["GET","POST"])
@login_required
@require_role("admin","creator")
def manage_edit(slug):
	trip = Trip.query.filter_by(slug=slug).first_or_404()
	form = TripForm(obj=trip)
	photo_form = TripPhotoForm()

	if form.validate_on_submit():
		# Common fields everyone can edit
		trip.title = form.title.data
		trip.slug = form.slug.data
		trip.short_description = form.short_description.data or ""
		trip.detailed_plan = form.detailed_plan.data or ""
		trip.hero_image_url = form.hero_image_url.data or ""
		trip.price_cents = form.price_cents.data or 0

		# Admin-only fields: enforce regardless of submitted values
		if current_user.role == "admin":
			trip.is_active = bool(form.is_active.data)
			trip.booking_mode = form.booking_mode.data or "none"
		else:
			trip.is_active = trip.is_active and trip.is_active  # no-op safeguard
			trip.booking_mode = trip.booking_mode  # no-op safeguard

		db.session.commit()
		flash("Saved", "ok")
		return redirect(url_for("trips.manage_edit", slug=trip.slug))

	# Add gallery photo
	if request.method == "POST" and photo_form.validate_on_submit():
		p = TripPhoto(trip_id=trip.id, image_url=photo_form.image_url.data, caption=photo_form.caption.data or "", position=len(trip.photos))
		db.session.add(p); db.session.commit()
		return redirect(url_for("trips.manage_edit", slug=trip.slug))

	return render_template("trips/manage_edit.html", form=form, trip=trip, photo_form=photo_form, photos=trip.photos)