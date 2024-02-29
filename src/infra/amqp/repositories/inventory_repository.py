import aio_pika
from src.domain.contracts.repositories.inventory_repository import IInventoryRepository
from src.domain.use_cases.product_inventory_processor import InputInventoryProcessorDTO


class AmqpInventoryRepository(IInventoryRepository):
    def __init__(self, connection, topic):
        self.connection = connection
        self.topic = topic

    async def send(self, dto: InputInventoryProcessorDTO):
        async with self.connection:
            channel = await self.connection.channel()
            await channel.default_exchange.publish(
                aio_pika.Message(body=dto.model_dump_json().encode()),
                routing_key=self.topic,
            )
