from typing import Generator

from fastapi import Header, HTTPException
from fastapi.security import HTTPBasic

from server.config import settings
from server.db.session import SessionLocal

security = HTTPBasic()


def get_db() -> Generator:
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


async def get_token_header(x_token: str = Header(...)):
    if x_token != settings.AUTH_TOKEN:
        raise HTTPException(status_code=400, detail="X-Token header invalid")


# def get_current_username(credentials: HTTPBasicCredentials = Depends(security)):
#     # this function handles basic auth that checks username and password
#     if (
#         credentials.username != settings.CHARGEBEE_HOOK_USERNAME
#         or credentials.password != settings.CHARGEBEE_HOOK_PASSWORD
#     ):
#         raise HTTPException(
#             status_code=401,
#             detail="Incorrect username or password",
#             headers={"WWW-Authenticate": "Basic"},
#         )
#     return credentials.username
