import asyncio
import aio_pika
import aiormq
import orjson


class AmqpConsumer:
    def __init__(self, connection):
        self.connection = connection
        self.subscribers = {}

    def subscribe_from_topic(self, topic, subscriber, parser):
        if self.subscribers.get(topic) is None:
            self.subscribers[topic] = {}
            self.subscribers[topic]["subscribers"] = []

        self.subscribers[topic]["parser"] = parser
        self.subscribers[topic]["subscribers"].append(subscriber)

    async def run(self):
        def wrapper_consumer(processor, parser):

            async def consumer(message: aio_pika.IncomingMessage):
                async with message.process():
                    decoded_message = message.body.decode()
                    await processor.execute(parser(**orjson.loads(decoded_message)))

            return consumer

        if not self.subscribers:
            return

        for topic, data in self.subscribers.items():
            channel = await self.connection.channel()
            queue = await channel.declare_queue(topic)
            parser = data["parser"]

            for subscriber in data["subscribers"]:
                asyncio.ensure_future(
                    queue.consume(
                        wrapper_consumer(subscriber, parser)
                    )
                )

