import os
from abc import ABC
from dotenv import load_dotenv

load_dotenv()


class Constants(ABC):
    APP_TITLE: str = os.environ.get("APP_TITLE", "StrongBox")
    SERVER_HOST: str = os.environ.get("SERVER_HOST", "127.0.0.1")
    SERVER_PORT: int = int(os.environ.get("SERVER_PORT", 8000))
