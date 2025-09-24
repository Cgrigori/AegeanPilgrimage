from flask import current_app
import requests

def send_email(subject: str, body: str, to_email: str) -> bool:
	api_key = current_app.config.get("SENDGRID_API_KEY", "")
	from_email = current_app.config.get("FROM_EMAIL", "no-reply@example.com")
	if not api_key:
		return False
	res = requests.post(
		"https://api.sendgrid.com/v3/mail/send",
		headers={
			"Authorization": f"Bearer {api_key}",
			"Content-Type": "application/json",
		},
		json={
			"personalizations":[{"to":[{"email": to_email}]}],
			"from":{"email": from_email},
			"subject": subject,
			"content":[{"type":"text/plain","value": body}],
		},
		timeout=15,
	)
	return res.status_code in (200, 202)