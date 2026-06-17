from flask import Flask, request, jsonify
from flask_mail import Mail, Message
from flask_cors import CORS
import os

app = Flask(__name__)

frontend_urls = [
    url.strip()
    for url in os.environ.get("FRONTEND_URLS", "*").split(",")
    if url.strip()
]
CORS(app, resources={r"/api/*": {"origins": frontend_urls}})

app.config["MAIL_SERVER"] = "smtp.gmail.com"
app.config["MAIL_PORT"] = 587
app.config["MAIL_USE_TLS"] = True
app.config["MAIL_USERNAME"] = os.environ.get("MAIL_USERNAME")
app.config["MAIL_PASSWORD"] = os.environ.get("MAIL_PASSWORD")

mail = Mail(app)


@app.route("/")
def health_check():
    return jsonify({
        "success": True,
        "message": "Mezani Competition API is running"
    })


@app.route("/api/register", methods=["POST"])
def register():
    data = request.get_json(silent=True) or {}

    required_fields = [
        "name",
        "email",
        "phone",
        "gender",
        "category",
        "experience",
        "age_group",
    ]
    missing_fields = [field for field in required_fields if not data.get(field)]

    if missing_fields:
        return jsonify({
            "success": False,
            "message": f"Missing required fields: {', '.join(missing_fields)}"
        }), 400

    name = data.get("name")
    email = data.get("email")
    phone = data.get("phone")
    gender = data.get("gender")
    category = data.get("category")
    experience = data.get("experience")
    age_group = data.get("age_group")

    if not app.config["MAIL_USERNAME"] or not app.config["MAIL_PASSWORD"]:
        return jsonify({
            "success": False,
            "message": "Email service is not configured"
        }), 500

    msg = Message(
        subject="Mezani Barista Competition 2026",
        sender=app.config["MAIL_USERNAME"],
        recipients=[email]
    )

    msg.body = f"""
Hello {name},
Thank you for registering for the Mezani Barista Competition 2026.
Your registration has been received successfully.

Registration details:
Phone: {phone}
Gender: {gender}
Category: {category}
Experience: {experience} years
Age group: {age_group}

Regards,
Mezani Team
"""
    mail.send(msg)

    return jsonify({
        "success": True,
        "message": "Confirmation email sent"
    })

if __name__ == "__main__":
    app.run(debug=True, port=5000)
