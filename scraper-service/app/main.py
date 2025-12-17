import asyncio

#  import requests
from aiokafka import AIOKafkaConsumer, AIOKafkaProducer

#  from config.settings import settings

#  from common_schemas import kafka_models


async def main():
    producer = AIOKafkaProducer(bootstrap_servers="localhost:9092")
    consumer = AIOKafkaConsumer(
        "topic_url",
        bootstrap_servers="localhost:9092",
        group_id="topic_url__group",
        auto_offset_reset="earliest",
    )
    await producer.start()
    await consumer.start()
    try:
        async for msg in consumer:

            print(
                "{}:{:d}:{:d}: key={} value={} timestamp_ms={}".format(
                    msg.topic,
                    msg.partition,
                    msg.offset,
                    msg.key,
                    msg.value,
                    msg.timestamp,
                )
            )

            pass
    finally:
        await producer.stop()
        await consumer.stop()


if __name__ == "__main__":
    asyncio.run(main())
