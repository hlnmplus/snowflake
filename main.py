#evryz4's fork of holinim's project https://github.com/hlnmplus/snowflake

import asyncio
import logging
from os import getenv

from dotenv import load_dotenv

from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties

from workers import snowflake

load_dotenv()

token = getenv('API-KEY')

if token == '123456789:PASTE-YOUR-BOTAPI-TOKEN-HERE':
    print('Please paste botapi token into .env')
    exit(0)

async def main():
    logging.basicConfig(level = logging.INFO)

    dp = Dispatcher()
    dp.include_routers(snowflake.rt)

    bot = Bot(token=token, default=DefaultBotProperties(parse_mode = ParseMode.HTML, link_preview_is_disabled = True))

    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())