import asyncio
from datetime import datetime, timezone

from aiokafka import AIOKafkaProducer
from config.settings import settings
from db.engine import session_factory
from db.models import Url

from common_schemas import kafka_models


def compile_domain(obj: Url) -> str:
    url = f"{obj.scheme}://{obj.domain}"
    url += f":{obj.port}" if obj.port else ""
    url += obj.path if obj.path else ""
    url += f"?{obj.param}" if obj.param else ""
    url += f"#{obj.anchor}" if obj.anchor else ""
    return url


async def pipe_push():
    producer = AIOKafkaProducer(bootstrap_servers=settings.kafka_url)
    await producer.start()
    try:
        with session_factory() as session:
            tasks: list[asyncio.Future] = []
            # сейчас простой запрос на "хотя бы один парсинг"
            # TODO потом переписать на сложный "хотя бы один парсинг за последние Х дней"
            # но с сохранением идемпотентности
            for item in session.query(Url).filter(Url.last_pars.is_(None)).limit(100):
                kafka_item = kafka_models.Url(
                    url_id=item.url_id, url=compile_domain(item)
                )
                message = kafka_item.model_dump_json().encode("utf-8")
                task = await producer.send("topic_url", message)
                tasks.append(task)
                item.last_pars = datetime.now(timezone.utc)
            if tasks:
                await asyncio.gather(*tasks)
            session.commit()
    finally:
        await producer.stop()
