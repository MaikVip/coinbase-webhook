from flask import Flask, request, jsonify
import hmac
import hashlib
import os

app = Flask(__name__)

# Konfigurierbare Umgebungsvariablen (setzen auf Render!)
WEBHOOK_SECRET = os.getenv("COINBASE_SHARED_SECRET", "dein_shared_secret")
VIP_TELEGRAM_CHAT_ID = os.getenv("VIP_TELEGRAM_CHAT_ID", "dein_chat_id")
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "dein_bot_token")

def verify_signature(payload, signature, secret):
    computed = hmac.new(secret.encode(), payload, hashlib.sha256).hexdigest()
    return hmac.compare_digest(computed, signature)

def grant_telegram_access(user_id):
    # Hier müsste die Telegram-API-Funktion rein, z. B.:
    # requests.post(f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/inviteLink?chat_id=...")
    print(f"Access granted to Telegram user: {user_id}")
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
        user_id = metadata.get("telegram_id")
        if user_id:
            grant_telegram_access(user_id)
            return "Success", 200
    
    return "Ignored", 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))

