import asyncio

from loguru import logger
import taskiq_aiogram
from aiogram import Bot
from taskiq import TaskiqDepends
from config import REDIS_URL

from taskiq_redis import RedisAsyncResultBackend, RedisStreamBroker

result_backend = RedisAsyncResultBackend(
    redis_url=REDIS_URL,
    result_ex_time=1000,
)

# Or you can use PubSubBroker if you need broadcasting
# Or ListQueueBroker if you don't want acknowledges
broker = RedisStreamBroker(
    url=REDIS_URL,
).with_result_backend(result_backend)

# This line is going to initialize everything.
taskiq_aiogram.init(
    broker,
    # This is path to the dispatcher.
    "config:dp",
    # This is path to the bot instance.
    "config:bot",
    # You can specify more bots here.
)


@broker.task(task_name="my_task")
async def my_task(chat_id: int, bot: Bot = TaskiqDepends()) -> None:
    logger.info("Hello from my task!")
    await asyncio.sleep(4)
    await bot.send_message(chat_id, "task completed")
