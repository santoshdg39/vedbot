from cryptography.fernet import Fernet

key = Fernet.generate_key()
print("SECRET_KEY:", key.decode())

f = Fernet(key)

print("Encrypted username:", f.encrypt(b"Admin").decode())
print("Encrypted password:", f.encrypt(b"admin123").decode())
