from flask import Blueprint, request, redirect, url_for, render_template, abort, current_app, jsonify
from ..models import Trip
import stripe

bp = Blueprint("bookings", __name__)

def _stripe():
    stripe.api_key = current_app.config.get("STRIPE_SECRET_KEY", "")
    return stripe

@bp.get("/<int:trip_id>/start")
def start(trip_id: int):
    trip = Trip.query.get_or_404(trip_id)
    if getattr(trip, "booking_mode", "none") != "direct":
        abort(404)
    try:
        guests = int(request.args.get("guests", "1"))
    except Exception:
        guests = 1
    amount_cents = max(1, guests) * (trip.price_cents or 0)
    if amount_cents <= 0:
        abort(400, "Trip price not configured.")

    s = _stripe()
    session = s.checkout.Session.create(
        mode="payment",
        line_items=[{
            "price_data": {
                "currency": (trip.currency or "EUR").lower(),
                "unit_amount": amount_cents,
                "product_data": {"name": trip.title},
            },
            "quantity": 1
        }],
        metadata={"trip_id": str(trip.id), "slug": trip.slug, "guests": str(guests)},
        success_url=url_for("bookings.success", _external=True) + "?session_id={CHECKOUT_SESSION_ID}",
        cancel_url=url_for("bookings.cancel", _external=True),
    )
    return redirect(session.url, code=303)

@bp.get("/success")
def success():
    return render_template("booking_success.html")

@bp.get("/cancel")
def cancel():
    return render_template("booking_cancel.html")

@bp.post("/webhook")
def webhook():
    payload = request.data
    sig_header = request.headers.get("Stripe-Signature", "")
    endpoint_secret = current_app.config.get("STRIPE_WEBHOOK_SECRET", "")
    s = _stripe()
    try:
        event = s.Webhook.construct_event(payload, sig_header, endpoint_secret)
    except Exception:
        return "Invalid signature", 400

    if event.get("type") == "checkout.session.completed":
        # TODO: mark booking as paid when you add Booking/Payment models
        pass
    return jsonify(received=True)