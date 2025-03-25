import asyncio
from loguru import logger

from aiogram import types
from aiogram.filters import Command

# from broker import my_task
from broker import my_task
from config import bot, dp


async def start_bot():
    logger.info("Бот успешно запущен.")


async def stop_bot():
    logger.error("Бот остановлен!")


@dp.message(Command("task"))
async def message(message: types.Message) -> None:
    logger.info("Ok task!")
    await message.answer("Ok task")
    await my_task.kiq(message.chat.id)


async def main():
    dp.startup.register(start_bot)
    dp.shutdown.register(stop_bot)
    try:
        await bot.delete_webhook(drop_pending_updates=True)
        await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())
    finally:
        await bot.session.close()


if __name__ == "__main__":
    asyncio.run(main())
