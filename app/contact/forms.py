from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, IntegerField, SelectField, DateField, SubmitField
from wtforms.validators import DataRequired, Email, Optional, NumberRange, Length

class ContactForm(FlaskForm):
	name = StringField("Your Name", validators=[DataRequired(), Length(max=120)])
	email = StringField("Your Email", validators=[DataRequired(), Email(), Length(max=255)])
	start_date = DateField("Start Date", validators=[Optional()])
	end_date = DateField("End Date", validators=[Optional()])
	num_people = IntegerField("Number of People", validators=[Optional(), NumberRange(min=1, max=500)])
	destination = SelectField("Destination", choices=[("", "Not yet decided")], validators=[Optional()])
	message = TextAreaField("Message", validators=[DataRequired(), Length(min=20)])
	submit = SubmitField("Send Inquiry")
