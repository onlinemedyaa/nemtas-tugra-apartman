import re
from werkzeug.security import generate_password_hash, check_password_hash

PHONE_REGEX = re.compile(r"^\+?\d{10,15}$")

def hash_pin(pin: str) -> str:
    if not re.fullmatch(r"\d{6}", pin):
        raise ValueError("PIN 6 haneli olmalı.")
    return generate_password_hash(pin)

def verify_pin(hash_val: str, pin: str) -> bool:
    return check_password_hash(hash_val, pin)

def validate_phone(phone: str) -> bool:
    return bool(PHONE_REGEX.match(phone))
