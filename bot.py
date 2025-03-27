import asyncio

from loguru import logger

from aiogram import Bot, types
from aiogram.filters import Command

from app.tkq import broker, schedule_messages
from app.config import dp, bot


# Taskiq calls this function when starting the worker.
@dp.startup()
async def setup_taskiq(bot: Bot, *_args, **_kwargs):
    # Here we check if it's a client-side,
    # Because otherwise you're going to
    # create infinite loop of startup events.
    if not broker.is_worker_process:
        logger.info("Setting up taskiq")
        await broker.startup()


# Taskiq calls this function when shutting down the worker.
@dp.shutdown()
async def shutdown_taskiq(bot: Bot, *_args, **_kwargs):
    if not broker.is_worker_process:
        logger.info("Shutting down taskiq")
        await broker.shutdown()


# # Simple command to handle
@dp.message(Command("task"))
async def message(message: types.Message):
    user_id = message.from_user.id
    counter_mess = 2
    timeout = 2

    try:
        data = {
            "user_id": user_id,
            "counter_mess": counter_mess,
            "timeout": timeout,
        }

        # Вызов задачи с передачей данных
        await schedule_messages.kiq(**data)
        logger.info("taskq work schedule")

    except Exception as e:
        logger.error(e)



## Main function that starts the bot.
async def main():
    try:
        await bot.delete_webhook(drop_pending_updates=True)
        await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())
    except Exception as e:
        logger.error(e)


if __name__ == "__main__":
    asyncio.run(main())
