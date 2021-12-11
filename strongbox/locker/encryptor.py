import os
import json
import base64
from abc import ABC, abstractclassmethod, abstractmethod
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from strongbox.locker.utils import create_parent_folder


class IEncryptor(ABC):
    @abstractmethod
    def encrypt(self, data: str) -> str:
        pass

    @abstractmethod
    def decrypt(self, data: str) -> str:
        pass

    @abstractmethod
    def to_json(self) -> str:
        pass

    def to_file(self, filepath: str):
        create_parent_folder(filepath)
        with open(filepath, "w") as file:
            file.write(self.to_json())


class IEncryptorPassword(IEncryptor):
    @abstractclassmethod
    def from_json(cls, s: str, password: str) -> 'IEncryptorPassword':
        pass

    @classmethod
    def from_file(cls, filepath: str, password: str) -> 'IEncryptorPassword':
        with open(filepath, "r") as file:
            return cls.from_json(file.read(), password)


class FernetWithPasswordEncryptor(IEncryptorPassword):
    def __init__(self, password: str, salt: bytes = os.urandom(16)):
        self.salt = salt
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=390000,
        )
        self.fernet = Fernet(base64.urlsafe_b64encode(kdf.derive(password.encode())))

    def encrypt(self, data: str) -> str:
        return str(self.fernet.encrypt(data.encode()), "utf-8")

    def decrypt(self, data: str) -> str:
        return str(self.fernet.decrypt(data.encode()), "utf-8")

    def to_json(self) -> str:
        return json.dumps({"salt": str(base64.b64encode(self.salt), "utf-8")})

    @classmethod
    def from_json(cls, s: str, password: str) -> 'FernetWithPasswordEncryptor':
        salt = json.loads(s).get("salt", None)
        if not salt:
            raise ValueError()
        return FernetWithPasswordEncryptor(password, base64.b64decode(salt))
