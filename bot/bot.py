import asyncio
import logging
import sys
from loguru import logger

from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command

from tkq import broker, my_task
from config import dp, bot


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


## Simple command to handle
@dp.message(Command("task"))
async def message(message: types.Message):
    logger.info("Sending task")
    await my_task.kiq(message.chat.id)


## Main function that starts the bot.
async def main():
    await dp.start_polling(bot)
    try:
        await bot.delete_webhook(drop_pending_updates=True)
        await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())
    finally:
        await bot.session.close()



if __name__ == "__main__":
    asyncio.run(main())
