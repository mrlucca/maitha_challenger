import asyncio
import aio_pika
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
        def wrapper_message_processor(processor, parser):
            async def process(message: aio_pika.IncomingMessage):
                async with message.process():
                    decoded_message = message.body.decode()
                    await processor(parser(orjson.loads(decoded_message)))

            return process

        if not self.subscribers:
            return

        async with self.connection:
            channel = await self.connection.channel()
            for topic, data in self.subscribers.items():
                queue = await channel.declare_queue(topic)
                parser = data["parser"]
                for subscriber in data["subscribers"]:
                    asyncio.ensure_future(
                        queue.consume(wrapper_message_processor(subscriber, parser))
                    )
