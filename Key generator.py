import hashlib, time, random, string

CONFIG = {
    "salt": "secret_salt",
    "xor_shift": 7,
    "header": "GGL-sandbox",
    "split_char": "|",
    "execute_payload": True,
    "signal_expiry": True,
    "validfor": 60,
    "varexpiry": "myexpiry",
    "varpayload": "mypayload",
    "varexpired": "myexpired",
    "varisexpired": "is_expired"
}

def xor_obfuscate(data, salt, shift):
    return ''.join(chr(ord(c) ^ (ord(salt[i % len(salt)]) ^ shift)) for i, c in enumerate(data))

def generate_nonce(length=8):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

def generate_key(payload):
    split = CONFIG["split_char"]
    salt = CONFIG["salt"]
    shift = CONFIG["xor_shift"]
    header = CONFIG["header"]
    validfor = CONFIG["validfor"]
    expiresat = int(time.time()) + validfor
    nonce = generate_nonce()
    digest_input = f"{validfor}{split}{expiresat}{split}{payload}{split}{nonce}{split}{salt}"
    digest = hashlib.sha256(digest_input.encode()).hexdigest()
    raw_key = split.join([header, str(validfor), str(expiresat), payload, nonce, digest])
    return xor_obfuscate(raw_key, salt, shift)

if __name__ == "__main__":
    key = generate_key("sandbox_payload")
    print("Generated Key:", key)
