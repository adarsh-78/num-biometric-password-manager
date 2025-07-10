from cryptography.fernet import Fernet

# Paste the fixed shared key from Adarsh here
key = b'REPLACE_WITH_ADARSH_KEY'

cipher = Fernet(key)

def encrypt_password(plain_text):
    try:
        return cipher.encrypt(plain_text.encode()).decode()
    except Exception as e:
        print("Encryption failed:", str(e))
        return plain_text

def decrypt_password(encrypted_text):
    try:
        return cipher.decrypt(encrypted_text.encode()).decode()
    except Exception as e:
        print("Decryption failed:", str(e))
        return "Decryption Failed"
