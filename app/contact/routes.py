from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app
from ..models import Trip
from .forms import ContactForm
from ..email import send_email

bp = Blueprint("contact", __name__)

@bp.route("/", methods=["GET", "POST"])
def contact():
        form = ContactForm()
        trips = Trip.query.filter_by(is_active=True).order_by(Trip.title.asc()).all()
        form.destination.choices = [("", "Not yet decided")] + [(t.slug, t.title) for t in trips]
        selected = request.args.get("dest")
        if selected and any(t.slug == selected for t in trips):
            form.destination.data = selected
            if request.method == "GET" and not form.message.data:
                title = next((t.title for t in trips if t.slug == selected), selected)
                form.message.data = (
                f"Hello,\nWe are interested in your trip: {next(t.title for t in trips if t.slug==selected)}.\n\n"
                "1. Can we arrange a call to discuss specifics?\n"
                )
        if request.method == "GET" and not form.message.data:
            form.message.data = (
            "Hello,\n"
            "We are a group of 10 from the University of Ohio.\n"
            "We are interested in your safari trip and we would like to ask some questions.\n\n"
            "1. Can we arrange a call to discuss specifics?\n"
            )

        if form.validate_on_submit():
            body = f"""Name: {form.name.data}
                        Email: {form.email.data}
                        Start: {form.start_date.data}
                        End: {form.end_date.data}
                        People: {form.num_people.data}
                        Destination: {form.destination.data}
                        ---
                        {form.message.data}
                        """
            to_addr = current_app.config.get("CONTACT_EMAIL", "info@example.com")
            sent = send_email("New Travel Inquiry", body, to_addr)
            flash("Thanks! We'll get back to you shortly." if sent else "Received. (Email not sent: email service not configured)", "ok")
            return redirect(url_for("contact.contact"))
        

        # Pass trips for preview (hero image + short description)
        return render_template("contact.html", form=form, trips=trips, contact_email=current_app.config.get("CONTACT_EMAIL", "info@example.com"))
