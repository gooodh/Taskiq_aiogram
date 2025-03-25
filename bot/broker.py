# broker.py
import asyncio
from loguru import logger

from config import bot, REDIS_URL
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


@broker.task(task_name="my_task.add_one", label1=1)
async def best_task_ever() -> None:
    """Solve all problems in the world."""
    await asyncio.sleep(5.5)
    logger.info("All problems are solved!")




@broker.task(task_name="my_task")
async def my_task(chat_id: int) -> None:
    logger.info("Hello from my task!")
    await asyncio.sleep(4)
    await bot.send_message(chat_id, "task completed")


async def main():
    task = await best_task_ever.kiq()
    task_info = await task.wait_result()
    logger.info(f"Task is done! {task_info}")


if __name__ == "__main__":
    asyncio.run(main())
