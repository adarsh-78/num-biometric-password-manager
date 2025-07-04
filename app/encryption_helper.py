# app/encryption_helper.py
from cryptography.fernet import Fernet
import os

# File to store the key
key_file = "secret.key"

# If key doesn't exist, generate it and save it
if not os.path.exists(key_file):
    with open(key_file, "wb") as f:
        f.write(Fernet.generate_key())

# Load the key
with open(key_file, "rb") as f:
    key = f.read()

fernet = Fernet(key)

def encrypt_password(password):
    return fernet.encrypt(password.encode()).decode()

def decrypt_password(encrypted_password):
    return fernet.decrypt(encrypted_password.encode()).decode()
