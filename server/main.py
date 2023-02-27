from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from server.config import settings
from server.db.init_db import init_db

from .api import api_router

app = FastAPI(
    title="FastAPI Boilerplate",
    description="Boilerplate to build FastAPI applications with SQLAlchemy, Pydantic, JWT, and User Auth Operations",
    version="1.0.0",
    debug=settings.debug,
)

app.include_router(api_router, prefix="/v1")

app.add_middleware(
    CORSMiddleware,
    allow_origins="*",
    allow_headers=["*"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
)


@app.on_event("startup")
def app_startup():
    try:
        init_db()
    except Exception as e:
        # TODO: log error
        print(e)


@app.get("/")
async def welcome():
    return {"status": 200, "message": "Server running"}
