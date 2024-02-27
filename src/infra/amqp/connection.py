from typing import Self
import aio_pika
from decouple import config


class SingletonAMQPConnection:
    _instance = None

    def __init__(self, connection):
        self.connection = connection

    @classmethod
    async def get_instance(cls) -> Self:
        if cls._instance is None:
            connection = await aio_pika.connect_robust(
                f"amqp://{config('BROKER_USER')}:{config('BROKER_PASSWORD')}@{config('BROKER_URL')}/"
            )
            cls._instance = cls(connection)

        return cls._instance
