import asyncio
import os
import signal
from datetime import datetime, timezone

from aiokafka import AIOKafkaConsumer, AIOKafkaProducer
from config.settings import settings
from db.engine import async_session_factory
from db.models import Url
from sqlalchemy import select

from common_schemas import kafka_models

ADD_BATCH = 500
MAX_LAG = 10000
SLEEP = 5


async def get_lag(consumer: AIOKafkaConsumer) -> int:
    partitions = consumer.assignment()
    if partitions:
        end_offsets = await consumer.end_offsets(partitions)
        total_lag = 0
        for tp in partitions:
            pos = await consumer.position(tp)
            total_lag += end_offsets[tp] - pos
        return total_lag
    return 0


def compile_domain(obj: Url) -> str:
    url = f"{obj.scheme}://{obj.domain}"
    url += f":{obj.port}" if obj.port else ""
    url += obj.path if obj.path else ""
    url += f"?{obj.param}" if obj.param else ""
    url += f"#{obj.anchor}" if obj.anchor else ""
    return url


async def pipe_push(producer: AIOKafkaProducer):
    async with async_session_factory() as session:
        tasks: list[asyncio.Future] = []
        # сейчас простой запрос на "хотя бы один парсинг"
        # TODO потом переписать на сложный "хотя бы один парсинг за последние Х дней"
        # но с сохранением идемпотентности
        # TODO еще тут нужна проверка на то, сколько сейчас в очереди висит урлов
        stmt = select(Url).where(Url.last_pars.is_(None)).limit(ADD_BATCH)
        result = await session.execute(stmt)
        for item in result.scalars():
            kafka_item = kafka_models.Url(
                url_hash=item.url_hash, url=compile_domain(item)
            )
            message = kafka_item.model_dump_json().encode("utf-8")
            task = await producer.send("topic_url", message)
            tasks.append(task)
            item.last_pars = datetime.now(timezone.utc).replace(tzinfo=None)
        if tasks:
            await asyncio.gather(*tasks)
        await session.commit()


async def pipe_push_while():
    try:
        consumer = AIOKafkaConsumer(
            "topic_res",
            bootstrap_servers=settings.KAFKA_URL,
            group_id="topic_res__group_003",
            auto_offset_reset="earliest",
        )
        producer = AIOKafkaProducer(bootstrap_servers=settings.KAFKA_URL)
        await consumer.start()
        await producer.start()
        try:
            while True:
                lag: int = await get_lag(consumer)
                print(
                    datetime.now(), lag, f"+{ADD_BATCH}" if lag < MAX_LAG else "пропуск"
                )
                if lag < MAX_LAG:
                    await pipe_push(producer)
                await asyncio.sleep(SLEEP)
        finally:
            await consumer.stop()
            await producer.stop()
    except Exception as e:
        print(f"CRITICAL ERROR in background push task: {e}")
        os.kill(os.getpid(), signal.SIGINT)
