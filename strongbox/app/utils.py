import os
import hashlib
from typing import Optional
from strongbox.locker.locker import Locker
from strongbox.locker.user import User
from strongbox.locker.account import Account
from strongbox.locker.encryptor import FernetWithPasswordEncryptor

STRONGBOX_PARENT_PATH = os.path.expanduser("~")
STRONGBOX_DIRECTORY_NAME = ".strongbox"
STRONGBOX_PATH = os.path.join(STRONGBOX_PARENT_PATH, STRONGBOX_DIRECTORY_NAME)


def _get_profile_path(profile: str) -> str:
    return os.path.join(STRONGBOX_PATH, profile)


def _get_encryptor_path(profile: str) -> str:
    return os.path.join(_get_profile_path(profile), Locker.ENCRYPTOR_FILENAME)


def _get_user_path(profile: str) -> str:
    return os.path.join(_get_profile_path(profile), Locker.USER_FILENAME)


def _get_locker(profile: str, password: str) -> Locker:
    encryptor = FernetWithPasswordEncryptor.from_file(_get_encryptor_path(profile), password)
    user = User.from_file(_get_user_path(profile))
    return Locker(user, encryptor)


def _sha256(s: str) -> str:
    return hashlib.sha256(s.encode("utf-8")).hexdigest()


def create_profile(profile: str, password: str):
    output = _get_profile_path(profile)
    encryptor = FernetWithPasswordEncryptor(_sha256(password))
    locker = Locker(User(profile), encryptor)
    locker.save(output, save_encryptor=True)


def get_profiles() -> list[str]:
    return os.listdir(STRONGBOX_PATH)


def add_account(profile: str, password: str, account: Account):
    locker = _get_locker(profile, password)
    locker.add_account(account)
    locker.save(_get_profile_path(profile))


def get_account(profile: str, password: str, url: str) -> Optional[Account]:
    locker = _get_locker(profile, password)
    return locker.get_account(url)


def get_accounts(profile: str, password: str) -> list[Account]:
    locker = _get_locker(profile, password)
    return locker.get_accounts()
