import asyncio
from typing import List

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.domain.use_cases.product_inventory_processor import (
    InputInventoryProcessorDTO,
    InventoryProcessorUseCase,
)
from src.infra.amqp.connection import SingletonAMQPConnection
from src.infra.amqp.consumer import AmqpConsumer

from src.infra.http.routers.health_check_router import router as health_check_router
from src.infra.http.routers.product_router import router as product_routers
from src.infra.sqlalchemy import models
from src.infra.sqlalchemy.connection import SingletonSqlAlchemyConnection
from src.infra.sqlalchemy.repositories.product_repository import (
    SQLAlchemyProductRepository,
)

ALLOWED_HOSTS = [
    "http://localhost",
    "http://localhost:8080",
    "http://example.com",
    "https://example.com"
]


def setup_and_get_app():
    app = FastAPI()

    app.include_router(health_check_router)
    app.include_router(product_routers)

    app.add_middleware(
        CORSMiddleware,
        allow_origins=ALLOWED_HOSTS,
        allow_credentials=True,
        allow_methods=["GET", "POST", "PUT", "DELETE"],
        allow_headers=["Authorization", "Content-Type"],
    )

    features_to_stop_in_graceful_shutdown: List[asyncio.Future] = []

    @app.on_event("startup")
    async def setup_models():
        instance = SingletonSqlAlchemyConnection.get_instance()
        async with instance.engine.begin() as conn:
            await conn.run_sync(models.Base.metadata.create_all)

        connection_instance = SingletonSqlAlchemyConnection.get_instance()
        product_repository = SQLAlchemyProductRepository(connection_instance)
        broker_connection = await SingletonAMQPConnection.get_instance()
        consumer = AmqpConsumer(broker_connection)
        consumer.subscribe_from_topic(
            "inventory",
            InventoryProcessorUseCase(product_repository),
            InputInventoryProcessorDTO,
        )
        consumer = asyncio.ensure_future(consumer.run())
        features_to_stop_in_graceful_shutdown.append(consumer)

        @app.on_event("shutdown")
        async def graceful_shutdown():
            broker_connection = await SingletonAMQPConnection.get_instance()
            await broker_connection.close()
            map(lambda feature: feature.cancel(), features_to_stop_in_graceful_shutdown, )

    return app
