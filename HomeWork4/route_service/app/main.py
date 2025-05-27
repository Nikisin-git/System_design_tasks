from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI

from app.db import ensure_indexes
from app.routers import route_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    await ensure_indexes()
    yield

app = FastAPI(
    title="Route Service",
    lifespan=lifespan,
)
app.include_router(route_router.router)


if __name__ == "__main__":
    uvicorn.run("main:main_app", host="0.0.0.0", port=8000, reload=True)