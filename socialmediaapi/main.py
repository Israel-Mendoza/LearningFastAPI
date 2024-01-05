from fastapi import FastAPI
from socialmediaapi.routers.post import router as post_router
from contextlib import asynccontextmanager
from socialmediaapi.database import database


@asynccontextmanager
async def lifespan(app: FastAPI) -> None:
    await database.connect()
    yield
    await database.disconnect()

app = FastAPI(lifespan=lifespan)

app.include_router(post_router)
