import time, hmac, hashlib, base64, random

def generate_key(salt="monkey", expiry_offset=3600):
    expiry = int(time.time()) + expiry_offset
    nonce = str(random.randint(100000, 999999))
    raw = f"{expiry}|{nonce}"
    hash = hmac.new(salt.encode(), raw.encode(), hashlib.sha256).hexdigest()
    full = f"{expiry}|{nonce}|{hash}"
    encoded = base64.b64encode(full.encode()).decode()
    return encoded

# 🧠 Prompt for expiry
try:
    user_input = input("⏳ How long should the key last (in seconds)? ")
    offset = int(user_input)
except:
    offset = 3600
    print("⚠️ Invalid input. Defaulting to 1 hour.")

# 🔐 Generate and print key
print("\n🔑 Your HMAC key:")
print(generate_key(expiry_offset=offset))
