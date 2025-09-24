from datetime import datetime
from . import db
from flask_login import UserMixin

class User(db.Model, UserMixin):
	id = db.Column(db.Integer, primary_key=True)
	email = db.Column(db.String(255), unique=True, index=True, nullable=False)
	password_hash = db.Column(db.String(255), nullable=False)
	name = db.Column(db.String(120))
	role = db.Column(db.String(20), default="user")  # admin, reviewer, creator, user
	avatar_url = db.Column(db.String(512))
	bio = db.Column(db.String(500))  # short description
	created_at = db.Column(db.DateTime, default=datetime.utcnow)

	def is_admin(self): return self.role == "admin"
	def is_reviewer(self): return self.role == "reviewer"
	def is_creator(self): return self.role == "creator"

class Trip(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	title = db.Column(db.String(180), nullable=False)
	slug = db.Column(db.String(200), unique=True, index=True)
	short_description = db.Column(db.String(300))
	detailed_plan = db.Column(db.Text)
	price_cents = db.Column(db.Integer, default=0)
	currency = db.Column(db.String(3), default="USD")
	hero_image_url = db.Column(db.String(512))

	# Visibility and booking controls
	is_active = db.Column(db.Boolean, default=True)
	is_bookable = db.Column(db.Boolean, default=False)  # legacy toggle; can keep for compatibility
	booking_mode = db.Column(db.String(20), default="none")  # 'none', 'direct', 'inquiry'

	created_at = db.Column(db.DateTime, default=datetime.utcnow)
	photos = db.relationship("TripPhoto", backref="trip", cascade="all, delete-orphan", order_by="TripPhoto.position.asc()")
class TripPhoto(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	trip_id = db.Column(db.Integer, db.ForeignKey("trip.id"), nullable=False)
	image_url = db.Column(db.String(512), nullable=False)
	caption = db.Column(db.String(300))
	position = db.Column(db.Integer, default=0)
	created_at = db.Column(db.DateTime, default=datetime.utcnow)