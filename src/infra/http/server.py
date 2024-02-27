from fastapi import FastAPI

from src.infra.http.routers.health_check_router import router as health_check_router


def setup_and_get_app():
    app = FastAPI()

    app.include_router(health_check_router)

    return app
