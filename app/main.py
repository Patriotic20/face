from fastapi import FastAPI
from sqladmin import Admin
from config.db_helper import db_helper
from config.config import settings
import uvicorn

from app.models.admin import register_models
from app.modules.router import router as module_router

app = FastAPI()
app.include_router(module_router)

admin = Admin(app, db_helper.engine)
register_models(admin)


if __name__ == "__main__":
    uvicorn.run(
        settings.app.app_path,
        host=settings.app.host,
        port=settings.app.port,
        reload=True
    )