from fastapi import FastAPI
from .exception_handlers import register_exception_handlers
from .routers.tasks import router as tasks_router
from .routers.users import router as users_router
from tasket.backend.db.setup import init_models
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s"
)

app = FastAPI()

@app.on_event("startup")
async def on_startup():
    await init_models()

register_exception_handlers(app)
app.include_router(tasks_router)
app.include_router(users_router)
