import base64
import time
import random

# 🔐 CONFIG
SALT = "monkey"

def generate_key(expiry_seconds):
    expiry = int(time.time()) + expiry_seconds
    nonce = str(int(time.time() * 1000))[-6:]  # last 6 digits of ms timestamp
    payload = f"{expiry}{SALT}{nonce}"
    encoded = base64.b64encode(payload.encode()).decode()
    return encoded

if __name__ == "__main__":
    try:
        user_input = input("⏳ Enter how many seconds until the key expires: ")
        expiry_seconds = int(user_input)
        key = generate_key(expiry_seconds)
        print("\n🔑 Unique Key:\n" + key)
    except ValueError:
        print("❌ Invalid input. Please enter a number.")
