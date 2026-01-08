from fastapi import FastAPI
from .exception_handlers import register_exception_handlers
from .routers.tasks import router as tasks_router
from .routers.users import router as users_router
from db.setup import init_models
import logging

from contextlib import asynccontextmanager


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_models()
    yield

def create_app() -> FastAPI:
    app = FastAPI(lifespan=lifespan)

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s | %(levelname)s | %(name)s | %(message)s"
    )

    register_exception_handlers(app)
    app.include_router(tasks_router)
    app.include_router(users_router)
    
    return app
