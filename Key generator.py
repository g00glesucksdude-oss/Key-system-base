import time, hashlib, random, string

CONFIG = {
    "salt": "secret_salt",
    "xor_shift": 7,
    "header": "GGL-sandbox",
    "split_char": "|",
    "validfor": 60,  # seconds
}

def xor_obfuscate(data: str, salt: str, shift: int) -> str:
    out = []
    for i, ch in enumerate(data):
        key = ord(salt[i % len(salt)]) ^ shift
        out.append(chr(ord(ch) ^ key))
    return "".join(out)

def generate_key(payload: str) -> str:
    validfor = CONFIG["validfor"]
    expiresat = int(time.time()) + validfor
    nonce = ''.join(random.choices(string.ascii_letters + string.digits, k=12))

    # Build the base string (without digest)
    base_fields = [
        CONFIG["header"],
        str(validfor),
        str(expiresat),
        payload,
        nonce
    ]
    base = CONFIG["split_char"].join(base_fields)

    # Compute digest over fields (excluding header) + salt
    digest_input = CONFIG["split_char"].join([
        str(validfor),
        str(expiresat),
        payload,
        nonce,
        CONFIG["salt"]
    ])
    digest = hashlib.sha256(digest_input.encode()).hexdigest()

    full = base + CONFIG["split_char"] + digest
    return xor_obfuscate(full, CONFIG["salt"], CONFIG["xor_shift"])

# Example usage
if __name__ == "__main__":
    key = generate_key("print('Hello from payload')")
    print("Generated key:", key)
