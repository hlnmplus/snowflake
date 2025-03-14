from aiogram import types, Router
from aiogram.filters import ChatMemberUpdatedFilter
from aiogram.filters.chat_member_updated import IS_NOT_MEMBER, IS_MEMBER, KICKED
from aiogram.filters.command import Command
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, ContentType
from aiogram.utils.keyboard import InlineKeyboardBuilder
from workers import locales, config
from dotenv import load_dotenv
from os import getenv

load_dotenv()

rt = Router()

@rt.message(Command("start"))
async def start(message: types.Message):
    buttontext = locales.string(message.from_user.language_code, "ghbutton")
    button = [[InlineKeyboardButton(url = locales.ghlink, text = buttontext)]]
    keyboard = InlineKeyboardMarkup(inline_keyboard = button)
    await message.reply(locales.string(message.from_user.language_code, "hi"), disable_web_page_preview = True, reply_markup = keyboard)

@rt.message(Command("f"))
async def f(message: types.Message):
    await message.answer(str(await message.bot.get_me()))

@rt.chat_member(ChatMemberUpdatedFilter(IS_NOT_MEMBER >> IS_MEMBER))
async def joined(event: types.ChatMemberUpdated):
    await event.chat.ban(event.new_chat_member.user.id)
    await event.chat.unban(event.new_chat_member.user.id)

@rt.message()
async def anything(message: types.Message):
    if message.content_type in [ContentType.NEW_CHAT_MEMBERS, ContentType.LEFT_CHAT_MEMBER]:
        await message.delete()