import os
import signal

from aiokafka import AIOKafkaConsumer
from config.settings import settings

#  from db.engine import session_factory  # TODO работа с базой должна быть асинхронной
#  from common_schemas import kafka_models
#  from db.models import Link, Response, Url


#  async def pipe_pull():


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
            #  async for msg in consumer:
            #  kafka_res: kafka_models.Res = kafka_models.Res.model_validate_json(
            #  msg.value
            #  )
            #  with session_factory() as session:
            #  pass
            pass
        finally:
            await consumer.stop()
    except Exception as e:
        print(f"CRITICAL ERROR in background task: {e}")
        os.kill(os.getpid(), signal.SIGINT)
