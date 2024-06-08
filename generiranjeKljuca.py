from cryptography.fernet import Fernet

# Generiraj ključ
key = Fernet.generate_key()
print(key.decode()) # Ovo se koristi za postavljanje ENCRYPTION_KEY varijable
