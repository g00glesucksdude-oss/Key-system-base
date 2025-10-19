import time
import base64
import hashlib
import random
import string

def generate_nonce(length=8):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

def generate_key(expiry_seconds, payload="default"):
    expiry = int(time.time()) + expiry_seconds
    nonce = generate_nonce()
    raw = f"{expiry}:{nonce}:{payload}"
    hash = hashlib.sha256(raw.encode()).hexdigest()
    key = f"GGL-sandbox-{expiry}-{nonce}-{payload}-{hash}"
    encoded = base64.b64encode(key.encode()).decode()
    return encoded

# 🧠 Prompt user for expiry
try:
    seconds = int(input("⏳ How many seconds should the key be valid? "))
    payload = input("📦 Optional payload (press Enter for default): ") or "default"
    key = generate_key(seconds, payload)
    print("\n🔐 Generated Key:\n", key)
except ValueError:
    print("⚠️ Invalid input. Please enter a number of seconds.")
