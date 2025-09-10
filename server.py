from flask import Flask, jsonify
from flask_cors import CORS
from twilio.rest import Client
import os

app = Flask(__name__)
CORS(app)

# Load credentials from environment variables
ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID", "YOUR_TWILIO_ACCOUNT_SID")
AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN", "YOUR_TWILIO_AUTH_TOKEN")
TWILIO_NUMBER = os.getenv("TWILIO_NUMBER", "YOUR_TWILIO_PHONE_NUMBER")
SOS_TARGET_NUMBER = os.getenv("SOS_TARGET_NUMBER", "+91XXXXXXXXXX")  # Replace with your mobile number

client = Client(ACCOUNT_SID, AUTH_TOKEN)

@app.route("/trigger-sos", methods=["POST"])
def trigger_sos():
    try:
        msg = client.messages.create(
            body="Emergency! SOS triggered from Safe Mode app.",
            from_=TWILIO_NUMBER,
            to=SOS_TARGET_NUMBER
        )
        return jsonify({"status": "success", "sid": msg.sid})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})

if __name__ == "__main__":
    app.run(debug=True)
