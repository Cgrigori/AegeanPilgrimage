from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import Optional, Length
from flask_wtf.file import FileField, FileAllowed

class ProfileForm(FlaskForm):
	name = StringField("Display Name", validators=[Optional(), Length(max=120)])
	avatar_file = FileField("Avatar Image", validators=[Optional(), FileAllowed(['jpg','jpeg','png','gif'], 'Images only!')])
	bio = TextAreaField("Short Bio", validators=[Optional(), Length(max=500)])
	submit = SubmitField("Save Changes")