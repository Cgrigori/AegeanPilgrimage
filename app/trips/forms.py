from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, IntegerField, SubmitField, BooleanField, RadioField
from wtforms.validators import DataRequired, Length, Optional, URL, NumberRange

class TripForm(FlaskForm):
	title = StringField("Title", validators=[DataRequired(), Length(max=180)])
	slug = StringField("Slug", validators=[DataRequired(), Length(max=200)])
	short_description = StringField("Short Description", validators=[Optional(), Length(max=300)])
	detailed_plan = TextAreaField("Detailed Plan", validators=[Optional()])
	hero_image_url = StringField("Main Image URL", validators=[Optional(), URL()])
	price_cents = IntegerField("Price (cents)", validators=[Optional(), NumberRange(min=0)])

	# Admin-only controls (rendered conditionally)
	is_active = BooleanField("Active")
	booking_mode = RadioField(
		"Booking Mode",
		choices=[("none","No booking button"),("direct","Direct payment (Stripe)"),("inquiry","Inquiry (Contact)")],
		default="none"
	)

	submit = SubmitField("Save")

class TripPhotoForm(FlaskForm):
	image_url = StringField("Photo URL", validators=[DataRequired(), URL()])
	caption = StringField("Caption", validators=[Optional(), Length(max=300)])
	submit = SubmitField("Add Photo")
