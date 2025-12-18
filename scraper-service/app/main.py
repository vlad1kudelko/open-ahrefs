import asyncio
import datetime

import aiohttp
from aiokafka import AIOKafkaConsumer, AIOKafkaProducer
from config.settings import settings
from tools.scraper import scraper_200

from common_schemas import kafka_models


async def main():
    producer = AIOKafkaProducer(bootstrap_servers=settings.KAFKA_URL)
    consumer = AIOKafkaConsumer(
        "topic_url",
        bootstrap_servers=settings.KAFKA_URL,
        group_id="topic_url__group_012",
        auto_offset_reset="earliest",
    )
    await producer.start()
    await consumer.start()
    timeout = aiohttp.ClientTimeout(total=30, connect=10, sock_read=10)
    async with aiohttp.ClientSession(timeout=timeout) as session:
        try:
            async for msg in consumer:
                print(datetime.datetime.now())
                kafka_url: kafka_models.Url = kafka_models.Url.model_validate_json(
                    msg.value
                )
                my_headers: dict = {
                    "User-Agent": "Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)"
                }
                kafka_res: kafka_models.Res | None = None
                try:
                    async with session.get(
                        kafka_url.url,
                        cookies={},
                        headers=my_headers,
                        allow_redirects=False,
                    ) as resp:
                        if 200 <= resp.status < 300:
                            kafka_res = await scraper_200(kafka_url.url_hash, resp)
                        if 300 <= resp.status < 400:
                            kafka_res = kafka_models.Res(
                                url_hash=kafka_url.url_hash,
                                status_code=resp.status,
                                content_type=resp.headers.get("content-type", ""),
                                redirect=resp.headers["Location"],
                            )
                        if kafka_res is None:
                            kafka_res = kafka_models.Res(
                                url_hash=kafka_url.url_hash,
                                status_code=resp.status,
                                content_type=resp.headers.get("content-type", ""),
                            )
                        message = kafka_res.model_dump_json().encode("utf-8")
                        await producer.send_and_wait("topic_res", message)
                except Exception:
                    kafka_res = kafka_models.Res(
                        url_hash=kafka_url.url_hash, status_code=999, content_type=""
                    )
                    message = kafka_res.model_dump_json().encode("utf-8")
                    await producer.send_and_wait("topic_res", message)
        finally:
            await producer.stop()
            await consumer.stop()


if __name__ == "__main__":
    asyncio.run(main())
