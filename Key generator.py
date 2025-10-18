import base64
import hmac
import hashlib
import time

SALT = b"monkey"  # Secret key for HMAC

def generate_key(expiry_seconds):
    expiry = int(time.time()) + expiry_seconds
    nonce = str(int(time.time() * 1000))[-6:]  # last 6 digits of ms timestamp
    raw = f"{expiry}|{nonce}".encode()

    # HMAC-SHA256 using salt
    h = hmac.new(SALT, raw, hashlib.sha256).hexdigest()

    # Embed expiry + nonce + hash in Base64
    payload = f"{expiry}|{nonce}|{h}"
    encoded = base64.b64encode(payload.encode()).decode()
    return encoded

if __name__ == "__main__":
    expiry_seconds = int(input("⏳ Seconds until expiry: "))
    print("\n🔑 HMAC Key:\n" + generate_key(expiry_seconds))
