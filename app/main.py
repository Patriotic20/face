from fastapi import FastAPI
from sqladmin import Admin
from config.db_helper import db_helper
from config.config import settings
import uvicorn

from app.models.admin import register_models
from app.modules.router import router as module_router
from fastapi.staticfiles import StaticFiles
import os

app = FastAPI()


if not os.path.exists("static/uploads"):
    os.makedirs("static/uploads", exist_ok=True)


app.include_router(module_router)

admin = Admin(app, db_helper.engine)
register_models(admin)


app.mount("/static", StaticFiles(directory="static"), name="static")

if __name__ == "__main__":
    uvicorn.run(
        settings.app.app_path,
        host=settings.app.host,
        port=settings.app.port,
        reload=True
    )