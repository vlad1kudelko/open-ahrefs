import datetime
import os
import signal

from aiokafka import AIOKafkaConsumer
from config.settings import settings, topicbalance
from db.engine import async_session_factory
from db.models import Link, Response, Url
from sqlalchemy.dialects.postgresql import insert
from tools.url_to_obj import obj_to_list_dict, url_to_obj

from common_schemas import kafka_models


async def pipe_pull(consumer: AIOKafkaConsumer):
    async for msg in consumer:
        # BEGIN - topicbalance
        partitions = consumer.assignment()
        if partitions:
            end_offsets = await consumer.end_offsets(partitions)
            total_lag = 0
            for tp in partitions:
                pos = await consumer.position(tp)
                total_lag += end_offsets[tp] - pos
            topicbalance.set(total_lag)
        # END
        kafka_res: kafka_models.Res = kafka_models.Res.model_validate_json(msg.value)
        async with async_session_factory() as session:
            print(datetime.datetime.now())
            db_res = Response(
                url_hash=kafka_res.url_hash,
                status_code=kafka_res.status_code,
                content_type=kafka_res.content_type,
                h1=kafka_res.h1,
                title=kafka_res.title,
                description=kafka_res.description,
                canonical=kafka_res.canonical,
                redirect=kafka_res.redirect,
            )
            list_urls: list[Url] = []
            list_links: list[Link] = []
            if kafka_res.links:
                for item_link in kafka_res.links:
                    db_url = url_to_obj(item_link.full_url)
                    if db_url is None:
                        continue
                    if db_url.url_hash not in [url.url_hash for url in list_urls]:
                        list_urls.append(db_url)
                    list_links.append(
                        Link(
                            source_url_hash=kafka_res.url_hash,
                            target_url_hash=db_url.url_hash,
                            tag=item_link.tag,
                            attr=item_link.attr,
                            field=item_link.field,
                            follow=item_link.follow,
                        )
                    )
            list_urls_dict = obj_to_list_dict(list_urls)
            if list_urls_dict:
                insert_stmt = insert(Url).values(list_urls_dict)
                upsert_stmt = insert_stmt.on_conflict_do_nothing(
                    index_elements=["url_hash"]
                )
                await session.execute(upsert_stmt)
                await session.flush()
            session.add(db_res)
            session.add_all(list_links)
            await session.commit()


async def pipe_pull_while():
    try:
        consumer = AIOKafkaConsumer(
            "topic_res",
            bootstrap_servers=settings.KAFKA_URL,
            group_id="topic_res__group_003",
            auto_offset_reset="earliest",
        )
        await consumer.start()
        try:
            await pipe_pull(consumer)
        finally:
            await consumer.stop()
    except Exception as e:
        print(f"CRITICAL ERROR in background pull task: {e}")
        os.kill(os.getpid(), signal.SIGINT)
