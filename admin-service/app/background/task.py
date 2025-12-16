from datetime import datetime, timezone

from config.settings import settings
from confluent_kafka import Producer
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
    with session_factory() as session:
        conf = {
            "bootstrap.servers": settings.kafka_url,
            "client.id": "admin-service",
        }
        producer = Producer(conf)
        # сейчас простой запрос на "хотя бы один парсинг"
        # TODO потом переписать на сложный "хотя бы один парсинг за последние Х дней"
        # но с сохранением идемпотентности
        for item in session.query(Url).filter(Url.last_pars.is_(None)).all():
            kafka_item = kafka_models.Url(url_id=item.url_id, url=compile_domain(item))
            message = kafka_item.model_dump_json()
            producer.produce(topic="topic_url", value=message.encode("utf-8"))
            item.last_pars = datetime.now(timezone.utc)
            producer.poll(0)
            session.flush()
        producer.flush()
        session.commit()
