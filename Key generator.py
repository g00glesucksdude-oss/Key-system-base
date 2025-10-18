import base64
import time

# 🔐 CONFIG
SALT = "monkey"
EXPIRY_SECONDS = 3600  # 1 hour from now

def generate_key():
    expiry = int(time.time()) + EXPIRY_SECONDS
    payload = f"{expiry}{SALT}"
    encoded = base64.b64encode(payload.encode()).decode()
    return encoded

# 🧪 Example usage
if __name__ == "__main__":
    key = generate_key()
    print("Generated Key:", key)
