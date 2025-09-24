from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField, PasswordField
from wtforms.validators import Optional, Length, DataRequired, EqualTo
from flask_wtf.file import FileField, FileAllowed

class ProfileForm(FlaskForm):
	name = StringField("Display Name", validators=[Optional(), Length(max=120)])
	avatar_file = FileField("Avatar Image", validators=[Optional(), FileAllowed(['jpg','jpeg','png','gif'], 'Images only!')])
	bio = TextAreaField("Short Bio", validators=[Optional(), Length(max=500)])
	submit = SubmitField("Save Changes")

class PasswordChangeForm(FlaskForm):
	current_password = PasswordField("Current Password", validators=[DataRequired()])
	new_password = PasswordField("New Password", validators=[DataRequired(), Length(min=6)])
	new_password_confirm = PasswordField("Confirm New Password", validators=[DataRequired(), EqualTo('new_password', message='Passwords must match')])
	submit = SubmitField("Change Password")
