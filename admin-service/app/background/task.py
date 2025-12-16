#  import asyncio

#  from config.settings import settings

#  from common_schemas.user_models import Link, Res, Url

#  from confluent_kafka.aio import AIOProducer


#  async def main():
#  p = AIOProducer({"bootstrap.servers": settings.kafka_url})
#  try:
#  # produce() returns a Future; first await the coroutine to get the Future,
#  # then await the Future to get the delivered Message.

#  #  delivery_future = await p.produce("mytopic", value=b"hello")
#  #  delivered_msg = await delivery_future

#  # Optionally flush any remaining buffered messages before shutdown
#  await p.flush()
#  finally:
#  await p.close()


#  asyncio.run(main())


def pipe_push():
    #  p = AIOProducer({"bootstrap.servers": settings.kafka_url})
    pass
