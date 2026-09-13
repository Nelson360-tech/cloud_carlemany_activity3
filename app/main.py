from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.authentication.api.authentication_router import router as authentication_router
from app.database import TORTOISE_ORM
from app.files.api.files_router import router as files_router
from tortoise.contrib.fastapi import RegisterTortoise


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with RegisterTortoise(
        app,
        config=TORTOISE_ORM,
        generate_schemas=False,
    ):
        yield


app = FastAPI(lifespan=lifespan)


@app.get("/healthcheck")
async def healthcheck() -> dict[str, str]:
    return {"status": "ok"}


app.include_router(authentication_router)
app.include_router(files_router, prefix="/files")