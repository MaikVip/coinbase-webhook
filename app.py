from flask import Flask, request, jsonify
import hmac
import hashlib
import os

app = Flask(__name__)

WEBHOOK_SECRET = os.getenv("COINBASE_SHARED_SECRET", "dein_shared_secret")
VIP_TELEGRAM_CHAT_ID = "dein_chat_id"
TELEGRAM_BOT_TOKEN = "dein_bot_token"

def verify_signature(payload, signature, secret):
    computed = hmac.new(secret.encode(), payload, hashlib.sha256).hexdigest()
    return hmac.compare_digest(computed, signature)

def grant_telegram_access(user_id):
    # Füge hier die Telegram-API ein, um Zugriff zu gewähren
    pass

@app.route("/weipay-webhooks", methods=["POST"])
def handle_webhook():
    payload = request.data
    signature = request.headers.get("X-CC-Webhook-Signature", "")
    
    if not verify_signature(payload, signature, WEBHOOK_SECRET):
        return "Invalid signature", 400
    
    event = request.json
    event_type = event.get("event", {}).get("type")
    
    if event_type == "charge:confirmed":
        metadata = event["event"]["data"].get("metadata", {})
        user_id = metadata.get("telegram_id")  # Wichtig: diesen musst du bei Bezahlung übergeben
        if user_id:
            grant_telegram_access(user_id)
            return "Success", 200
    
    return "Ignored", 200

if __name__ == "__main__":
    app.run()
