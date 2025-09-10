import logging
from flask import Flask, jsonify
from flask_cors import CORS
from twilio.rest import Client
import os

app = Flask(__name__)
CORS(app)

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s [%(levelname)s] %(message)s')

# Load credentials from environment variables (fail fast if missing)
ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID")
AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
TWILIO_NUMBER = os.getenv("TWILIO_NUMBER")
SOS_TARGET_NUMBER = os.getenv("SOS_TARGET_NUMBER")

if not all([ACCOUNT_SID, AUTH_TOKEN, TWILIO_NUMBER, SOS_TARGET_NUMBER]):
    logging.error("Missing Twilio configuration. Please set all required environment variables.")
    raise RuntimeError("Missing Twilio configuration. Please set all required environment variables.")

client = Client(ACCOUNT_SID, AUTH_TOKEN)

@app.route("/trigger-sos", methods=["POST"])
def trigger_sos():
    try:
        # Basic phone number validation
        if not SOS_TARGET_NUMBER.startswith("+"):
            logging.error("Invalid SOS target number format.")
            return jsonify({"status": "error", "message": "Invalid target number format."}), 400

        msg = client.messages.create(
            body="Emergency! SOS triggered from Safe Mode app.",
            from_=TWILIO_NUMBER,
            to=SOS_TARGET_NUMBER
        )
        logging.info(f"SOS message sent successfully. SID: {msg.sid}")
        return jsonify({"status": "success", "sid": msg.sid})
    except Exception as e:
        logging.error(f"Failed to send SOS message: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
