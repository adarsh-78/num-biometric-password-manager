from cryptography.fernet import Fernet
import getpass

# Step 1: Generate a key (In real use, save this to a secure place and reuse)
key = Fernet.generate_key()
cipher = Fernet(key)

# Step 2: Get password from user (hidden input)
password = getpass.getpass("Enter your password to encrypt: ")

# Step 3: Encrypt the password
password_bytes = password.encode()
encrypted_password = cipher.encrypt(password_bytes)
print("\n Encrypted Password:", encrypted_password.decode())

# Step 4: Decrypt the password
decrypted_password = cipher.decrypt(encrypted_password).decode()
print("Decrypted Password:", decrypted_password)

# Step 5: Show the encryption key (you must save this securely for future use)
print("Encryption Key (Save this!):", key.decode())