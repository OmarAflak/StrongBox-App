from typing import Optional
from fastapi import FastAPI, Body
from fastapi.middleware.cors import CORSMiddleware
from strongbox.locker.locker import Account
import strongbox.server.utils as utils


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
) -> Optional[Account]:
    return utils.get_account(profile, password, url)


@app.post("/account/new")
def add_account(
    profile: str = Body(None),
    password: str = Body(None),
    account: Account = Body(None)
):
    utils.add_account(profile, password, account)
