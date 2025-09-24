from flask import abort
from flask_login import current_user

def require_role(*roles):
	def wrapper(fn):
		def inner(*args, **kwargs):
			if not current_user.is_authenticated or current_user.role not in roles:
				abort(403)
			return fn(*args, **kwargs)
		inner.__name__ = fn.__name__
		return inner
	return wrapper
