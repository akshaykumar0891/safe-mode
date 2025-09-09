#https://chatgpt.com/share/68be7e78-1a04-800c-ba33-c1346de0da02
from flask import Flask, request, jsonify

from flask_cors import CORS
from twilio.rest import Client

app = Flask(__name__)
CORS(app)

# Twilio credentials (replace with your real ones)
ACCOUNT_SID = "YOUR_ACCOUNT_SID"
AUTH_TOKEN = "YOUR_AUTH_TOKEN"
TWILIO_NUMBER = "YOUR_TWILIO_PHONE"

client = Client(ACCOUNT_SID, AUTH_TOKEN)

@app.route("/send-sms", methods=["POST"])
def send_sms():
    data = request.get_json()
    numbers = data.get("numbers", [])
    message_text = data.get("message", "")

    responses = []
    for number in numbers:
        msg = client.messages.create(
            body=message_text,
            from_=TWILIO_NUMBER,
            to=number
        )
        responses.append({"to": number, "status": msg.status})

    return jsonify({"sent": responses})

if __name__ == "__main__":
    app.run(debug=True)
