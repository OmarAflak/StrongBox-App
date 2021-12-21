import os
from abc import ABC
from dotenv import load_dotenv

load_dotenv()


def _get_int(key: str, default: int) -> int:
    return int(os.environ.get(key, default))


def _get_string(key: str, default: str) -> str:
    return os.environ.get(key, default)


class Constants(ABC):
    APP_TITLE: str = _get_string("APP_TITLE", "StrongBox")
    SERVER_HOST: str = _get_string("SERVER_HOST", "127.0.0.1")
    SERVER_PORT: int = _get_int("SERVER_PORT", 8000)
