from flask import Flask, request, jsonify
import requests
from bot_scripts.config import TOKEN, B24_WEBHOOK

app = Flask(__name__)

@app.route('/b24_webhook', methods=['POST'])
def handle_b24_event():
    try:
        event_data = request.json
        event_type = event_data.get('event')
        message_data = event_data.get('data', {}).get('FIELDS', {})

        if event_type == "ONIMCONNECTORMESSAGEADD":
            user_message = message_data.get("MESSAGE")
            user_id = message_data.get("USER_ID")

            send_message_to_telegram(user_id, user_message)
        return jsonify({"status": "success"}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


def send_message_to_telegram(user_id, message):
    TELEGRAM_API_URL = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    payload = {"chat_id": user_id, "text": message}
    requests.post(TELEGRAM_API_URL, data=payload)


if __name__ == "__main__":
    app.run(port=5000)