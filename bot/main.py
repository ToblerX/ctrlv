import asyncio
import logging
import os
import sys

from aiogram import Bot, Dispatcher

from bot.api_client import ApiClient
from bot.handlers.commands import router

logging.basicConfig(level=logging.INFO, stream=sys.stdout)
logger = logging.getLogger(__name__)


async def main():
    bot_token = os.environ.get("BOT_TOKEN")
    if not bot_token:
        logger.error("BOT_TOKEN environment variable is not set")
        sys.exit(1)

    api_url = os.environ.get("API_URL", "http://api:8000")

    bot = Bot(token=bot_token)
    dp = Dispatcher()
    dp.include_router(router)

    api_client = ApiClient(api_url)
    dp["api_client"] = api_client

    logger.info("Bot starting (API: %s)", api_url)

    try:
        await dp.start_polling(bot)
    finally:
        await api_client.close()
        await bot.session.close()


if __name__ == "__main__":
    asyncio.run(main())
