import asyncio
import os
import signal
from datetime import datetime, timezone

from aiokafka import AIOKafkaProducer
from config.settings import settings
from db.engine import async_session_factory
from db.models import Url
from sqlalchemy import select

from common_schemas import kafka_models


async def pipe_push(producer: AIOKafkaProducer):
    async with async_session_factory() as session:
        tasks: list[asyncio.Future] = []
        # сейчас простой запрос на "хотя бы один парсинг"
        # TODO потом переписать на сложный "хотя бы один парсинг за последние Х дней"
        # но с сохранением идемпотентности
        # TODO еще тут нужна проверка на то, сколько сейчас в очереди висит урлов
        stmt = select(Url).where(Url.last_pars.is_(None)).limit(100)
        result = await session.execute(stmt)
        for item in result.scalars():
            kafka_item = kafka_models.Url(url_hash=item.url_hash, url=item.full_url)
            message = kafka_item.model_dump_json().encode("utf-8")
            task = await producer.send("topic_url", message)
            tasks.append(task)
            item.last_pars = datetime.now(timezone.utc).replace(tzinfo=None)
        if tasks:
            await asyncio.gather(*tasks)
        await session.commit()


async def pipe_push_while():
    try:
        producer = AIOKafkaProducer(bootstrap_servers=settings.KAFKA_URL)
        await producer.start()
        try:
            while True:
                print(datetime.now(), "pipe_push")
                await pipe_push(producer)
                await asyncio.sleep(5)
        finally:
            await producer.stop()
    except Exception as e:
        print(f"CRITICAL ERROR in background push task: {e}")
        os.kill(os.getpid(), signal.SIGINT)
