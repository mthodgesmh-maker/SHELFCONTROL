import hashlib
import os

def hash_password(password):
    salt = os.urandom(16)
    hashed = hashlib.pbkdf2_hmac(
        "sha256",
        password.encode("utf-8"),
        salt,
        100000
    )
    return salt.hex() + ":" + hashed.hex()

def verify_password(stored, provided):
    salt, hashed = stored.split(":")
    salt = bytes.fromhex(salt)
    check = hashlib.pbkdf2_hmac(
        "sha256",
        provided.encode("utf-8"),
        salt,
        100000
    )
    return check.hex() == hashed
