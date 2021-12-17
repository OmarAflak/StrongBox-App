from fastapi import FastAPI, Body
from fastapi.middleware.cors import CORSMiddleware
from cryptography.fernet import InvalidToken
from strongbox.locker.locker import Account
from strongbox.app.response import APIResponse, APIError
import strongbox.app.utils as utils

_ERROR_WRONG_PASSWORD = APIError(1, "Wrong password")
_ERROR_URL_NOT_FOUND = APIError(2, "URL not in strongbox")

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


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
