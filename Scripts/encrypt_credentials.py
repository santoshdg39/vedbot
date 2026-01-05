from cryptography.fernet import Fernet

# key = Fernet.generate_key()
# f = Fernet(key)
# print("SECRET_KEY:", key.decode())
# To view the secrete key form powershell use -- echo $env:SECRET_KEY
SECRET_KEY = b'YshpJ-mScrYk6nAcPsj-EBWjB_l2SKsE6nz5IqOQXq0='
f = Fernet(SECRET_KEY)

print("Encrypted username:", f.encrypt(b"Admin").decode())
print("Encrypted password:", f.encrypt(b"Santosh24011992#").decode())
