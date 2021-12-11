from typing import Generic, Optional, TypeVar
from fastapi import FastAPI, Body
from dataclasses import dataclass
from fastapi.middleware.cors import CORSMiddleware
from cryptography.fernet import InvalidToken
from strongbox.locker.io import IO
from strongbox.locker.locker import Account
import strongbox.server.utils as utils

_ERROR_WRONG_PASSWORD = "Wrong password"
_ERROR_URL_NOT_FOUND = "URL not in strongbox"

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


T = TypeVar("T", bound=IO)


@dataclass
class APIResponse(Generic[T]):
    success: bool
    message: Optional[str] = None
    data: Optional[T] = None

    @classmethod
    def on_success(cls, data: T) -> 'APIResponse[T]':
        return cls(success=True, message=None, data=data)

    @classmethod
    def on_fail(cls, message: Optional[str] = None) -> 'APIResponse[T]':
        return cls(success=False, message=message, data=None)


@app.post("/account")
def get_account(
    profile: str = Body(None),
    password: str = Body(None),
    url: str = Body(None)
) -> APIResponse[Account]:
    try:
        account = utils.get_account(profile, password, url)
        if account:
            return APIResponse[Account].on_success(account)
        else:
            return APIResponse[Account].on_fail(_ERROR_URL_NOT_FOUND)
    except InvalidToken:
        return APIResponse[Account].on_fail(_ERROR_WRONG_PASSWORD)


@app.post("/account/new")
def add_account(
    profile: str = Body(None),
    password: str = Body(None),
    account: Account = Body(None)
) -> APIResponse[bool]:
    try:
        utils.add_account(profile, password, account)
        return APIResponse[bool].on_success(True)
    except InvalidToken:
        return APIResponse[bool].on_fail(_ERROR_WRONG_PASSWORD)
