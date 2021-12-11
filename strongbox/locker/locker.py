import os
from typing import Optional
from strongbox.locker.encryptor import IEncryptor
from strongbox.locker.user import User
from strongbox.locker.account import Account


class Locker:
    USER_FILENAME = "user.json"
    ENCRYPTOR_FILENAME = "encryptor.json"

    def __init__(self, user: User, encryptor: IEncryptor):
        self.user = user
        self.encryptor = encryptor

    def add_account(self, account: Account):
        self.user.add_account(account, self.encryptor)

    def get_account(self, url: str) -> Optional[Account]:
        return self.user.get_account(url, self.encryptor)

    def get_accounts(self) -> list[Account]:
        return self.user.get_all_accounts(self.encryptor)

    def save(self, directory: str, save_user: bool = True, save_encryptor: bool = False):
        if save_user:
            self.user.to_file(os.path.join(directory, Locker.USER_FILENAME))
        if save_encryptor:
            self.encryptor.to_file(os.path.join(directory, Locker.ENCRYPTOR_FILENAME))
