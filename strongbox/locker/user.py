from typing import Optional
from dataclasses import dataclass, field
from strongbox.locker.io import IO
from strongbox.locker.encryptor import IEncryptor
from strongbox.locker.account import Account


@dataclass
class User(IO):
    name: str
    accounts: list[Account] = field(default_factory=list)

    def add_account(self, account: Account, encryptor: IEncryptor):
        self.accounts.append(account.encrypt(encryptor))

    def get_account(self, url: str, encryptor: IEncryptor) -> Optional[Account]:
        for account in self.accounts:
            if account.website.match(url):
                return account.decrypt(encryptor)
        return None

    def get_all_accounts(self, encryptor: IEncryptor) -> list[Account]:
        return [account.decrypt(encryptor) for account in self.accounts]
