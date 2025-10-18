import base64
import hmac
import hashlib
import time

# 🔐 CONFIG
SALT = b"monkey"  # Must be bytes for HMAC

def generate_key(expiry_seconds):
    expiry = int(time.time()) + expiry_seconds
    nonce = str(int(time.time() * 1000))[-6:]  # last 6 digits of ms timestamp
    raw = f"{expiry}|{nonce}".encode()

    # 🧠 HMAC-SHA256 using salt as key
    h = hmac.new(SALT, raw, hashlib.sha256).hexdigest()

    # 🔓 Embed expiry + nonce + hash in Base64
    payload = f"{expiry}|{nonce}|{h}"
    encoded = base64.b64encode(payload.encode()).decode()
    return encoded

if __name__ == "__main__":
    try:
        expiry_seconds = int(input("⏳ Seconds until expiry: "))
        key = generate_key(expiry_seconds)
        print("\n🔑 HMAC Key:\n" + key)
    except ValueError:
        print("❌ Invalid input. Please enter a number.")
