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
    if message.chat.type == 'private':
        lang = message.from_user.language_code
    else:
        lang = config.get_setting(message.chat.id, "Locale")
    buttontext = locales.string(lang, "ghbutton")
    button = [[InlineKeyboardButton(url = locales.ghlink, text = buttontext)]]
    keyboard = InlineKeyboardMarkup(inline_keyboard = button)
    await message.reply(locales.string(lang, "hi"), disable_web_page_preview = True, reply_markup = keyboard)

@rt.chat_member(ChatMemberUpdatedFilter(IS_NOT_MEMBER >> IS_MEMBER))
async def joined(event: types.ChatMemberUpdated):
    await event.chat.ban(event.new_chat_member.user.id)
    if config.get_setting(message.chat.id, "BanMembers") == True:
        await event.chat.unban(event.new_chat_member.user.id)

@rt.message()
async def anything(message: types.Message):
    if message.content_type in [ContentType.NEW_CHAT_MEMBERS, ContentType.LEFT_CHAT_MEMBER]:
        if config.get_setting(message.chat.id, "DeleteServiceMessages") == True:
            await message.delete()