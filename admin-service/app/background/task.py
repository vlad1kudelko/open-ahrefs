import asyncio
import os
import signal
from datetime import datetime, timezone

from aiokafka import AIOKafkaProducer
from config.settings import settings
from db.engine import session_factory  # TODO работа с базой должна быть асинхронной
from db.models import Url

from common_schemas import kafka_models


def compile_domain(obj: Url) -> str:
    url = f"{obj.scheme}://{obj.domain}"
    url += f":{obj.port}" if obj.port else ""
    url += obj.path if obj.path else ""
    url += f"?{obj.param}" if obj.param else ""
    url += f"#{obj.anchor}" if obj.anchor else ""
    return url


async def pipe_push(producer: AIOKafkaProducer):
    with session_factory() as session:
        tasks: list[asyncio.Future] = []
        # сейчас простой запрос на "хотя бы один парсинг"
        # TODO потом переписать на сложный "хотя бы один парсинг за последние Х дней"
        # но с сохранением идемпотентности
        # TODO еще тут нужна проверка на то, сколько сейчас в очереди висит урлов
        for item in session.query(Url).filter(Url.last_pars.is_(None)).limit(100):
            kafka_item = kafka_models.Url(url_id=item.url_id, url=compile_domain(item))
            message = kafka_item.model_dump_json().encode("utf-8")
            task = await producer.send("topic_url", message)
            tasks.append(task)
            item.last_pars = datetime.now(timezone.utc)
        if tasks:
            await asyncio.gather(*tasks)
        session.commit()


async def pipe_push_while():
    try:
        producer = AIOKafkaProducer(bootstrap_servers=settings.kafka_url)
        await producer.start()
        try:
            while True:
                await pipe_push(producer)
                await asyncio.sleep(10)
        finally:
            await producer.stop()
    except Exception as e:
        print(f"CRITICAL ERROR in background task: {e}")
        os.kill(os.getpid(), signal.SIGINT)
