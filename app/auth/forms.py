from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, Length, EqualTo

class LoginForm(FlaskForm):
	email = StringField("Email", validators=[DataRequired(), Email()])
	password = PasswordField("Password", validators=[DataRequired()])
	submit = SubmitField("Login")

class SignupForm(FlaskForm):
	name = StringField("Name", validators=[Length(max=120)])
	email = StringField("Email", validators=[DataRequired(), Email()])
	password = PasswordField("Password", validators=[DataRequired(), Length(min=6)])
	password_confirm = PasswordField("Confirm Password", validators=[DataRequired(), EqualTo('password', message='Passwords must match')])
	submit = SubmitField("Sign Up")
