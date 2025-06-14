import re
import asyncio
import logging
from logging.handlers import RotatingFileHandler

from aiogram import Bot, Dispatcher
from aiogram.enums.parse_mode import ParseMode
from aiogram.client.default import DefaultBotProperties

from config import BOT_TOKEN, FILMS_CHAT
from handlers.groups import register_group_handlers
from handlers.private import register_private_handlers
from services.db import init_db

LOG_FILE = "data/bot.log"
handler = RotatingFileHandler(LOG_FILE, maxBytes=5_000_000, backupCount=2)
logging.basicConfig(level=logging.INFO, handlers=[handler])
logger = logging.getLogger(__name__)

async def main():
    await init_db()

    bot = Bot(token=BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    dp = Dispatcher()

    register_group_handlers(dp, bot)
    register_private_handlers(dp, bot)

    await asyncio.gather(
        dp.start_polling(bot),
    )

if __name__ == "__main__":
    asyncio.run(main())
