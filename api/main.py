from fastapi import FastAPI
from .routers.tasks import router as tasks_router
from .routers.users import router as users_router
from tasket.db.setup import init_models

app = FastAPI()

@app.on_event("startup")
async def on_startup():
    await init_models()

app.include_router(tasks_router)
app.include_router(users_router)
