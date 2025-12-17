import asyncio

#  import requests
from aiokafka import AIOKafkaConsumer, AIOKafkaProducer
from config.settings import settings

from common_schemas import kafka_models


async def main():
    producer = AIOKafkaProducer(bootstrap_servers=settings.KAFKA_URL)
    consumer = AIOKafkaConsumer(
        "topic_url",
        bootstrap_servers=settings.KAFKA_URL,
        group_id="topic_url__group_001",
        auto_offset_reset="earliest",
    )
    await producer.start()
    await consumer.start()
    try:
        async for msg in consumer:
            data = kafka_models.Url.model_validate_json(msg.value)
            print(data)
    finally:
        await producer.stop()
        await consumer.stop()


if __name__ == "__main__":
    asyncio.run(main())
