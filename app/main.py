from contextlib import asynccontextmanager
from fastapi import FastAPI

from .api.students import router as students_router
from .api.fees import router as fees_router
from .core.db import init_db


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    yield


app = FastAPI(title="Smart School Fees Management", lifespan=lifespan)

app.include_router(students_router)
app.include_router(fees_router)


@app.get("/")
async def root() -> dict:
    return {"status": "ok"}