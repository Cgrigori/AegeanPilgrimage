from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from werkzeug.security import generate_password_hash
from .config import Config

db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()
login_manager.login_view = "auth.login"

def create_app():
	app = Flask(__name__)
	app.config.from_object(Config)

	db.init_app(app)
	migrate.init_app(app, db)
	login_manager.init_app(app)

	from . import models  # noqa

	from .pages.routes import bp as pages_bp
	from .trips.routes import bp as trips_bp
	from .contact.routes import bp as contact_bp
	from .auth.routes import bp as auth_bp
	from .account.routes import bp as account_bp
	from .admin.routes import bp as admin_bp
	from .bookings.routes import bp as bookings_bp

	app.register_blueprint(pages_bp)
	app.register_blueprint(trips_bp, url_prefix="/trips")
	app.register_blueprint(contact_bp, url_prefix="/contact")
	app.register_blueprint(auth_bp, url_prefix="/auth")
	app.register_blueprint(account_bp, url_prefix="/account")
	app.register_blueprint(admin_bp, url_prefix="/admin")
	app.register_blueprint(bookings_bp, url_prefix="/bookings")

	# Ensure DB tables exist
	with app.app_context():
		try:
			from sqlalchemy import text
			db.session.execute(text("SELECT 1"))
			db.create_all()
		except Exception as e:
			print(f"DB setup error: {e}")

	return app

from .models import User

@login_manager.user_loader
def load_user(user_id: str):
	return User.query.get(int(user_id))