import datetime
from datetime import timedelta
import random

from loguru import logger

import taskiq_aiogram
from taskiq import Context, TaskiqDepends
from taskiq_redis import RedisAsyncResultBackend, RedisStreamBroker
from taskiq_redis import RedisScheduleSource
from taskiq import TaskiqScheduler
from aiogram import Bot

from app.config import REDIS_URL

result_backend = RedisAsyncResultBackend(
    redis_url=REDIS_URL,
    result_ex_time=1000,
)
redis_source = RedisScheduleSource(REDIS_URL)

broker = RedisStreamBroker(
    url=REDIS_URL,
).with_result_backend(result_backend)

scheduler = TaskiqScheduler(broker, sources=[redis_source])

# This line is going to initialize everything.
taskiq_aiogram.init(
    broker,
    # This is path to the dispatcher.
    "app.config:dp",
    # This is path to the bot instance.
    "app.config:bot",
    # You can specify more bots here.
)


@broker.task
async def send_mail_client(
    user_id: int, bot: Bot = TaskiqDepends(), context: Context = TaskiqDepends()
):
    await bot.send_message(user_id, "task completed")
    schedule_id = context.message.labels.get("schedule_id")

    logger.info(
        f"Сообщение отправлено пользователю {user_id}, schedule_id: {schedule_id}"
    )


@broker.task
async def schedule_messages(user_id, counter_mess, timeout):
    for i in range(counter_mess):
        total_users = 2
        for index in range(total_users):
            wait_time = random.uniform(18, 30) if index < total_users - 1 else 0
            try:
                timeout_duration = timedelta(seconds=timeout * 60)
                wait_time_duration = timedelta(seconds=wait_time)
                timeout_total = (
                    datetime.datetime.now(datetime.timezone.utc)
                    + (timeout_duration * i)
                    + (wait_time_duration * index)
                )
                # Планирование задачи с использованием taskiq
                await send_mail_client.schedule_by_time(
                    redis_source, timeout_total, user_id
                )

                logger.info(
                    f"Запланирована отправка для пользователя {user_id} на {timeout_total}"
                )
            except Exception as e:
                logger.error(f"Ошибка при отправке сообщения {e}")
                return
