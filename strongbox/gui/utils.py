import os
from typing import Optional
from dataclasses import dataclass
from strongbox.locker.io import IO
from strongbox.app.utils import STRONGBOX_PATH

CACHE_FILENAME = ".profile"
CACHE_FILEPATH = os.path.join(STRONGBOX_PATH, CACHE_FILENAME)


@dataclass
class UserCache(IO):
    profile: str


def cache_user(user_cache: UserCache):
    user_cache.to_file(CACHE_FILEPATH)


def get_user_cache() -> Optional[UserCache]:
    if os.path.exists(CACHE_FILEPATH):
        return UserCache.from_file(CACHE_FILEPATH)
    return None
