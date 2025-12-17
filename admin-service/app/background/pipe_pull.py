import datetime
import os
import signal
from urllib.parse import ParseResult, urlparse

from aiokafka import AIOKafkaConsumer
from config.settings import settings
from db.engine import async_session_factory
from db.models import Link, Response
from tools.find_add_url import find_add_url

from common_schemas import kafka_models


async def pipe_pull_while():
    try:
        consumer = AIOKafkaConsumer(
            "topic_res",
            bootstrap_servers=settings.KAFKA_URL,
            group_id="topic_res__group_001",
            auto_offset_reset="earliest",
        )
        await consumer.start()
        try:
            async for msg in consumer:
                kafka_res: kafka_models.Res = kafka_models.Res.model_validate_json(
                    msg.value
                )
                async with async_session_factory() as session:
                    print(datetime.datetime.now())
                    db_res = Response(
                        url_id=kafka_res.url_id,
                        status_code=kafka_res.status_code,
                        content_type=kafka_res.content_type,
                        h1=kafka_res.h1,
                        title=kafka_res.title,
                        description=kafka_res.description,
                        canonical=kafka_res.canonical,
                        redirect=kafka_res.redirect,
                    )
                    session.add(db_res)
                    if kafka_res.links:
                        for item_link in kafka_res.links:
                            parse_url: ParseResult = urlparse(item_link.full_url)
                            if parse_url.scheme not in ["http", "https"]:
                                continue
                            if not parse_url.hostname:
                                continue
                            db_url, _ = await find_add_url(session, parse_url)
                            db_link = Link(
                                source_url_id=kafka_res.url_id,
                                target_url_id=db_url.url_id,
                                tag=item_link.tag,
                                attr=item_link.attr,
                                field=item_link.field,
                                follow=item_link.follow,
                            )
                            session.add(db_link)
                    await session.commit()
        finally:
            await consumer.stop()
    except Exception as e:
        print(f"CRITICAL ERROR in background pull task: {e}")
        os.kill(os.getpid(), signal.SIGINT)
