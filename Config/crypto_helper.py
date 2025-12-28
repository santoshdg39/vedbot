import os
from cryptography.fernet import Fernet


class CryptoHelper:

    @staticmethod
    def decrypt(value: str) -> str:
        if not value or value == "not_found":
            return value

        key = os.getenv("SECRET_KEY")
        if not key:
            raise RuntimeError("SECRET_KEY environment variable not set")

        f = Fernet(key.encode())
        return f.decrypt(value.encode()).decode()
