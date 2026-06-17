from flask import Flask, request, jsonify
from flask_mail import Mail, Message
from flask_cors import CORS

app = Flask(__name__)
CORS(
    app,
    resources={r"/*": {"origins": "*"}},
    supports_credentials=False,
    allow_headers=["Content-Type", "Authorization"],
    methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"]
    )

app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'ronneyomondi14@gmail.com'
app.config['MAIL_PASSWORD'] = 'ypmd dawv bwjt jpyb'

mail = Mail(app)

@app.route("/api/register", methods=["POST"])
def register():
    data = request.json

    name = data.get("name")
    email = data.get("email")

    msg = Message(
        subject="Mezani Barista Competition 2026",
        sender=app.config["MAIL_USERNAME"],
        recipients=[email]
    )

    msg.body = f"""
Hello {name},
Thank you for registering for the Mezani Barista Competition 2026.
Your registration has been received successfully.

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