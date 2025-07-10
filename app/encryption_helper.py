from cryptography.fernet import Fernet

# Fixed key from Adarsh’s CLI encryption
key = b'r5t9Ci7sgQTMuoCeBu5BBRLJ5iGlkvpq5Rb0ZUXp_oo='
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
