import asyncio
import logging
from os import getenv
from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties
from dotenv import load_dotenv
load_dotenv()

logging.basicConfig(level = logging.INFO)

token = getenv('API-KEY')
dp = Dispatcher()

from workers import settings, snowflake, inline

dp.include_routers(settings.rt, snowflake.rt, inline.rt)

bot = Bot(token=token, default=DefaultBotProperties(parse_mode = ParseMode.HTML, link_preview_is_disabled = True))

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())