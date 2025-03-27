import os
from loguru import logger

from aiogram import Bot, Dispatcher

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    BOT_TOKEN: str

    FORMAT_LOG: str = (
        "{time:YYYY-MM-DD at HH:mm:ss} | {level} | {name}:{function}:{line} - {message}"
    )
    LOG_ROTATION: str = "10 MB"

    REDIS_HOST: str
    REDIS_PORT: int
    REDIS_DB: int


    model_config = SettingsConfigDict(
        env_file=os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".env")
    )

    def get_redis_url(self):
        return (
            f"redis://{self.REDIS_HOST}:{self.REDIS_PORT}/{self.REDIS_DB}"
        )

# Получаем параметры для загрузки переменных среды
settings = Settings()
dp = Dispatcher()
bot = Bot(token=settings.BOT_TOKEN)

log_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "log.log")
logger.add(
    log_file_path,
    format=settings.FORMAT_LOG,
    level="INFO",
    rotation=settings.LOG_ROTATION,
)

REDIS_URL = settings.get_redis_url()
