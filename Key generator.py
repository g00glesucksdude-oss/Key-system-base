import re

CONFIG_KEYS = {
    "salt": str,
    "xor_shift": int,
    "header": str,
    "split_char": str,
    "execute_payload": bool,
    "signal_expiry": bool,
    "validfor": int,
    "varexpiry": str,
    "varpayload": str,
    "varexpired": str,
    "varisexpired": str
}

def parse_config(content):
    return re.search(r'CONFIG\s*=\s*{(.*?)}', content, re.DOTALL).group(1)

def update_config(content, new_config):
    block = parse_config(content)
    updated = "CONFIG = {\n"
    for k, v in new_config.items():
        val = f'"{v}"' if isinstance(v, str) else str(v).lower() if isinstance(v, bool) else str(v)
        updated += f'    "{k}": {val},\n'
    updated += "}\n"
    return content.replace(f"CONFIG = {{{block}}}", updated)

def edit_config():
    new_config = {}
    for k, typ in CONFIG_KEYS.items():
        val = input(f"{k} ({typ.__name__}): ")
        try: new_config[k] = typ(val) if typ != bool else val.lower() == "true"
        except: print("Invalid, keeping original.")
    for file in ["keygen.py", "validator.lua"]:
        with open(file, 'r') as f: content = f.read()
        updated = update_config(content, new_config)
        with open(file.replace(".", "updated."), 'w') as f: f.write(updated)
        print(f"Updated {file} → {file.replace('.', 'updated.')}")
        
if __name__ == "__main__":
    edit_config()
