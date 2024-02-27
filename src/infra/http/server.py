import asyncio
from fastapi import FastAPI
from src.domain.use_cases.product_inventory_processor import (
    InputInventoryProcessorDTO,
    InventoryProcessorUseCase,
)
from src.infra.amqp.connection import SingletonAMQPConnection
from src.infra.amqp.consumer import AmqpConsumer

from src.infra.http.routers.health_check_router import router as health_check_router
from src.infra.http.routers.product_router import router as product_routers
from src.infra.sqlalchemy import models
from src.infra.sqlalchemy.instance import SingletonSqlAlchemyConnection
from src.infra.sqlalchemy.product_repository import SQLAlchemyProductRepository


def setup_and_get_app():
    app = FastAPI()

    app.include_router(health_check_router)
    app.include_router(product_routers)

    @app.on_event("startup")
    async def setup_models():
        instance = SingletonSqlAlchemyConnection.get_instance()
        async with instance.engine.begin() as conn:
            await conn.run_sync(models.Base.metadata.create_all)

        connection_instance = SingletonSqlAlchemyConnection.get_instance()
        product_repository = SQLAlchemyProductRepository(connection_instance)
        consumer = AmqpConsumer((await SingletonAMQPConnection.get_instance()).connection)
        consumer.subscribe_from_topic(
            "inventory", InventoryProcessorUseCase(product_repository), InputInventoryProcessorDTO
        )
        asyncio.ensure_future(consumer.run())

    return app
