from fastapi import FastAPI

from src.infra.http.routers.health_check_router import router as health_check_router
from src.infra.http.routers.product_router import router as product_routers
from src.infra.sqlalchemy import models
from src.infra.sqlalchemy.instance import SingletonSqlAlchemyConnection


def setup_and_get_app():
    app = FastAPI()

    app.include_router(health_check_router)
    app.include_router(product_routers)

    @app.on_event("startup")
    async def setup_models():
        instance = SingletonSqlAlchemyConnection.get_instance()
        async with instance.engine.begin() as conn:
            await conn.run_sync(models.Base.metadata.create_all)

    return app
