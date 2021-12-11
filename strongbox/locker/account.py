from dataclasses import dataclass
from strongbox.locker.io import IO
from strongbox.locker.encryptor import IEncryptor


@dataclass
class Field(IO):
    selector: str
    value: str

    def encrypt(self, encryptor: IEncryptor) -> 'Field':
        return Field(self.selector, encryptor.encrypt(self.value))

    def decrypt(self, encryptor: IEncryptor) -> 'Field':
        return Field(self.selector, encryptor.decrypt(self.value))


@dataclass
class Website(IO):
    url: str

    def match(self, url: str) -> bool:
        return self.url == url


@dataclass
class Account(IO):
    website: Website
    username: Field
    password: Field

    def encrypt(self, encryptor: IEncryptor) -> 'Account':
        this = Account.copy(self)
        this.password = this.password.encrypt(encryptor)
        return this

    def decrypt(self, encryptor: IEncryptor) -> 'Account':
        this = Account.copy(self)
        this.password = this.password.decrypt(encryptor)
        return this
