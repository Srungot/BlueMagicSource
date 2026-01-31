import secrets
import string
import base64
import zlib
import marshal
import json
from pathlib import Path
from math import ceil
import sys
import sys
import time
import platform
import os
import hashlib
from time import sleep
from datetime import datetime, UTC
try:
    from Crypto.Cipher import AES
    from Crypto.Hash import HMAC, SHA256
except ImportError:
    print('Error: pycryptodome required. Install with: pip install pycryptodome')
    sys.exit(1)
try:
    from argon2.low_level import hash_secret_raw, Type
except ImportError:
    print('Error: argon2-cffi required. Install with: pip install argon2-cffi')
    sys.exit(1)
try:
    from colorama import init, Fore, Style
    init()
except ImportError:
    print('Error: colorama required. Install with: pip install colorama')
    sys.exit(1)
SALT_LEN = 16
NONCE_LEN = 12
TAG_LEN = 16
ARGON_TIME = 2
ARGON_MEMORY = 65536
ARGON_PARALLELISM = 1
KEY_LEN = 32
HMAC_BLOCK = 32
ARGON_TYPE = Type.ID
UI_COLOR = Fore.LIGHTCYAN_EX
ERROR_COLOR = Fore.RED
RESET = Style.RESET_ALL

def rand_ident(n=10):
    alphabet = string.ascii_letters + '_'
    return secrets.choice(alphabet) + ''.join((secrets.choice(alphabet + string.digits) for _ in range(n - 1)))

def derive_key_argon2(password: str, salt: bytes) -> bytes:
    pwd_b = (password if password is not None else '').encode('utf-8')
    return hash_secret_raw(secret=pwd_b, salt=salt, time_cost=ARGON_TIME, memory_cost=ARGON_MEMORY, parallelism=ARGON_PARALLELISM, hash_len=KEY_LEN, type=ARGON_TYPE)

def keystream_hmac_counter(key: bytes, length: int) -> bytes:
    blocks = ceil(length / HMAC_BLOCK)
    out = bytearray()
    for i in range(blocks):
        ctr = i.to_bytes(8, 'big')
        h = HMAC.new(key, digestmod=SHA256)
        h.update(ctr)
        out.extend(h.digest())
    return bytes(out[:length])

def xor_bytes(a: bytes, b: bytes) -> bytes:
    return bytes((x ^ y for x, y in zip(a, b)))

def b64enc(b: bytes) -> str:
    return base64.b64encode(b).decode('ascii')

def build_blob_with_meta(source_code: str, password: str, require_password: bool) -> str:
    junk = f'def _{rand_ident(8)}():\n    return {secrets.randbelow(10000)} * {secrets.randbelow(1000)}\n'
    source_code = junk + source_code
    code_obj = compile(source_code, '<obf>', 'exec')
    marsh = marshal.dumps(code_obj)
    comp = zlib.compress(marsh, level=9)
    salt = secrets.token_bytes(SALT_LEN)
    key = derive_key_argon2(password if password is not None else '', salt)
    ks = keystream_hmac_counter(key, len(comp))
    xored = xor_bytes(comp, ks)
    nonce1 = secrets.token_bytes(NONCE_LEN)
    cipher1 = AES.new(key, AES.MODE_GCM, nonce=nonce1)
    ct1 = cipher1.encrypt(xored)
    tag1 = cipher1.digest()
    meta = {'names': {'crypto': base64.b64encode(b'Crypto').decode('ascii'), 'cipher': base64.b64encode(b'Cipher').decode('ascii'), 'aes': base64.b64encode(b'AES').decode('ascii'), 'protocol': base64.b64encode(b'Protocol').decode('ascii'), 'kdf': base64.b64encode(b'KDF').decode('ascii'), 'pbkdf2': base64.b64encode(b'PBKDF2').decode('ascii'), 'hash': base64.b64encode(b'Hash').decode('ascii'), 'hmac': base64.b64encode(b'HMAC').decode('ascii'), 'sha256': base64.b64encode(b'SHA256').decode('ascii')}, 'messages': {'require_password': bool(require_password), 'argon_time': ARGON_TIME, 'argon_memory': ARGON_MEMORY, 'argon_parallelism': ARGON_PARALLELISM, 'key_len': KEY_LEN}}
    meta_json = json.dumps(meta, separators=(',', ':')).encode('utf-8')
    meta_comp = zlib.compress(meta_json, level=9)
    nonce2 = secrets.token_bytes(NONCE_LEN)
    cipher2 = AES.new(key, AES.MODE_GCM, nonce=nonce2)
    ct2 = cipher2.encrypt(meta_comp)
    tag2 = cipher2.digest()
    payload = nonce1 + tag1 + ct1
    payload_len = len(payload).to_bytes(8, 'big')
    assembled = salt + payload_len + payload + (nonce2 + tag2 + ct2)
    return b64enc(assembled)

def make_minimal_loader(big_b64):
    blob_var = rand_ident(8)
    loader = f'# ultra-minimal loader (packed payload)\nimport base64 as _b64, zlib as _zl, marshal as _m, sys as _sys\n'
    loader += f'{blob_var} = {repr(big_b64)}\n'
    loader += "\ndef _r():\n    try:\n        assembled = _b64.b64decode(" + blob_var + ")\n    except Exception:\n        _sys.exit('Malformed payload')\n\n    s, n, t = "
    loader += f"{SALT_LEN}, {NONCE_LEN}, {TAG_LEN}\n"
    loader += """    salt = assembled[:s]
    payload_len = int.from_bytes(assembled[s:s+8], 'big')
    pstart, pend = s + 8, s + 8 + payload_len
    payload = assembled[pstart:pend]
    meta_blob = assembled[pend:]

    nonce1, tag1, ct1 = payload[:n], payload[n:n+t], payload[n+t:]
    nonce2, tag2, ct2 = meta_blob[:n], meta_blob[n:n+t], meta_blob[n+t:]

    try:
        from argon2.low_level import hash_secret_raw, Type as _Type
    except Exception:
        _sys.exit('argon2-cffi required')

    pwd = ''
    def derive(p):
        return hash_secret_raw(secret=(p.encode('utf-8')), salt=salt, time_cost="""
    loader += f"{ARGON_TIME}, memory_cost={ARGON_MEMORY}, parallelism={ARGON_PARALLELISM}, hash_len={KEY_LEN}"
    loader += """, type=_Type.ID)

    key = derive(pwd)

    # decrypt meta (AES-GCM with nonce2)
    from Crypto.Cipher import AES as _AES
    try:
        c2 = _AES.new(key, _AES.MODE_GCM, nonce=nonce2)
        meta_comp = c2.decrypt_and_verify(ct2, tag2)
    except Exception:
        pwd = input('Enter encryption key: ').strip()
        key = derive(pwd)
        try:
            c2 = _AES.new(key, _AES.MODE_GCM, nonce=nonce2)
            meta_comp = c2.decrypt_and_verify(ct2, tag2)
        except Exception:
            _sys.exit('invalid key or corrupted payload')

    try:
        meta_json = _zl.decompress(meta_comp)
        meta = __import__('json').loads(meta_json.decode('utf-8'))
    except Exception:
        _sys.exit('meta decode error')

    if meta.get('flags', {}).get('require_password', False) and not pwd:
        pwd = input(_b64.b64decode(meta['messages']['prompt']).decode('utf-8')).strip()
        key = derive(pwd)

    # decrypt payload (AES-GCM with nonce1)
    _cipher1 = _AES.new(key, _AES.MODE_GCM, nonce=nonce1)
    try:
        xored = _cipher1.decrypt_and_verify(ct1, tag1)
    except Exception:
        _sys.exit(_b64.b64decode(meta['messages']['err_key']).decode('utf-8'))

    # rebuild keystream (HMAC-SHA256 counter)
    ln = len(xored)
    blocks = (ln + """
    loader += f"{HMAC_BLOCK} - 1) // {HMAC_BLOCK}\n"
    loader += """    out = bytearray()
    for i in range(blocks):
        ctr = i.to_bytes(8, 'big')
        from Crypto.Hash import HMAC, SHA256
        h = HMAC.new(key, digestmod=SHA256)
        h.update(ctr)
        out.extend(h.digest())
    ks = bytes(out[:ln])
    code_bytes = bytes(a ^ b for a, b in zip(xored, ks))

    try:
        marsh = _zl.decompress(code_bytes)
        code_obj = _m.loads(marsh)
        exec(code_obj, globals(), globals())
    except Exception as e:
        _sys.exit(_b64.b64decode(meta['messages']['err_exec']).decode('utf-8') + str(e))

if __name__ == '__main__':
    _r()
"""
    return loader

def main():
    banner = UI_COLOR + '  ______   __                   ______              ______                                   __\n /      \\ |  \\                 /      \\            /      \\                                 |  \\\n|  $$$$$$\\| $$____    _______ |  $$$$$$\\ __    __ |  $$$$$$\\  ______    ______    _______  _| $$_     ______    ______  \n| $$  | $$| $$    \\  /       \\| $$_  \\$$|  \\  |  \\| $$___\\$$ /      \\  /      \\  /       \\|   $$ \\   /      \\  /      \\ \n| $$  | $$| $$$$$$$\\|  $$$$$$$| $$ \\    | $$  | $$ \\$$    \\ |  $$$$$$\\|  $$$$$$\\|  $$$$$$$ \\$$$$$$  |  $$$$$$\\|  $$$$$$\\\n| $$  | $$| $$  | $$ \\$$    \\ | $$$$    | $$  | $$ _\\$$$$$$\\| $$  | $$| $$    $$| $$        | $$ __ | $$   \\$$| $$    $$\n| $$__/ $$| $$__/ $$ _\\$$$$$$\\| $$      | $$__/ $$|  \\__| $$| $$__/ $$| $$$$$$$$| $$_____   | $$|  \\| $$      | $$$$$$$$\n \\$$    $$| $$    $$|       $$| $$       \\$$    $$ \\$$    $$| $$    $$ \\$$     \\ \\$$     \\   \\$$  $$| $$       \\$$     \\\n  \\$$$$$$  \\$$$$$$$  \\$$$$$$$  \\$$        \\$$$$$$   \\$$$$$$ | $$$$$$$   \\$$$$$$$  \\$$$$$$$    \\$$$$  \\$$        \\$$$$$$$\n                                                            | $$                                                        \n                                                            | $$                                                        \n                                                             \\$$                                                        \n\n                                                                 \n┌──────────────────────────────────────────────────────────────────┐\n│  [+] ObsfucSpectre: Undetectable by antivirus                    │\n│  [+] Ultra-stealth multilayer encryption (XOR + AES-GCM + HMAC)  │\n│  [+] Argon2id key derivation for maximum security                │\n│  [+] Compressed payload with minimal loader footprint            │\n│  [+] Optional password protection at runtime                     │\n│  [+] HMAC-SHA256 keystream for advanced obfuscation              │\n│  [+] Built for stealth and anti-reverse engineering              │\n└──────────────────────────────────────────────────────────────────┘\n\n\n\n\n\n' + RESET
    print(banner)
    path = input(UI_COLOR + 'Path to Python file: ' + RESET).strip()
    file = Path(path)
    if not file.exists() or not file.is_file():
        print(ERROR_COLOR + 'Error: File not found' + RESET)
        sys.exit(1)
    pwd = input(UI_COLOR + 'Obfuscation key (leave empty => no runtime prompt): ' + RESET).strip()
    require_pwd = bool(pwd)
    try:
        src = file.read_text(encoding='utf-8')
        print(UI_COLOR + 'Obfuscating... (this may take a moment)' + RESET)
        big_b64 = build_blob_with_meta(src, pwd if pwd else '', require_pwd)
        loader_code = make_minimal_loader(big_b64)
        output_dir = file.parent / 'output'
        output_dir.mkdir(parents=True, exist_ok=True)
        out = output_dir / f'{file.stem}_obf{file.suffix}'
        out.write_text(loader_code, encoding='utf-8')
        print(UI_COLOR + f'Obfuscated file created: {out}' + RESET)
        input()
        if require_pwd:
            print(UI_COLOR + f'Run: python3 {out} (will prompt for key)' + RESET)
    except Exception as e:
        print(ERROR_COLOR + f'Error reading file: {e}' + RESET)
        sys.exit(1)

if __name__ == '__main__':
    def clear_screen():
        if os.name == 'posix':
            os.system('clear')
        else:
            os.system('cls')
    clear_screen()
    main()