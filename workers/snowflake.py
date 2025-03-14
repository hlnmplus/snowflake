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
    await message.reply(locales.string(lang, "hi"), reply_markup = keyboard)

@rt.message(Command("settings"))
async def settings(message: types.Message):
    if message.chat.type == 'private':
        lang = message.from_user.language_code
        await message.reply(locales.string(lang, "settingspm"))
    else:
        lang = config.get_setting(message.chat.id, "Locale")
        buttons = [
            [InlineKeyboardButton(callback_data = f"ban{message.chat.id}", text = locales.string(lang, "BanMembers")+" "+config.checkmark(message.chat.id, "BanMembers"))],
            [InlineKeyboardButton(callback_data = f"ser{message.chat.id}", text = locales.string(lang, "DeleteServiceMessages")+" "+config.checkmark(message.chat.id, "DeleteServiceMessages"))],
        ]
        keyboard = InlineKeyboardMarkup(inline_keyboard = buttons)
        await message.reply(locales.string(lang, "settings"), reply_markup = keyboard)

@rt.message(Command("language"))
async def lang(message: types.Message):
    if message.chat.type == 'private':
        lang = message.from_user.language_code
        await message.reply(locales.string(lang, "settingspm"))
    else:
        lang = config.get_setting(message.chat.id, "Locale")
        buttons = []
        for i in locales.existingTranslations.keys():
            if i == lang:
                name = locales.existingTranslations[i] + " ✅"
            else:
                name = locales.existingTranslations[i]
            buttons.append([InlineKeyboardButton(callback_data = f"{i}{message.chat.id}", text = name)])
        keyboard = InlineKeyboardMarkup(inline_keyboard = buttons)
        await message.reply(locales.string(lang, "ChooseLang"), reply_markup = keyboard)

@rt.chat_member(ChatMemberUpdatedFilter(IS_NOT_MEMBER >> IS_MEMBER))
async def joined(event: types.ChatMemberUpdated):
    await event.chat.ban(event.new_chat_member.user.id)
    if config.get_setting(event.chat.id, "BanMembers") == True:
        await event.chat.unban(event.new_chat_member.user.id)

@rt.message()
async def anything(message: types.Message):
    if message.content_type in [ContentType.NEW_CHAT_MEMBERS, ContentType.LEFT_CHAT_MEMBER]:
        if config.get_setting(message.chat.id, "DeleteServiceMessages") == True:
            await message.delete()

@rt.callback_query()
async def callback(event: types.CallbackQuery):
    cfg = {
        'ban': 'BanMembers',
        'ser': 'DeleteServiceMessages'
    }
    if event.data[:3] in cfg:
        chatid = int(event.data[3:])
        config.save_setting(chatid, cfg[event.data[:3]], not config.get_setting(chatid, cfg[event.data[:3]]))
        lang = config.get_setting(event.message.chat.id, "Locale")
        buttons = [
            [InlineKeyboardButton(callback_data = f"ban{event.message.chat.id}", text = locales.string(lang, "BanMembers")+" "+config.checkmark(event.message.chat.id, "BanMembers"))],
            [InlineKeyboardButton(callback_data = f"ser{event.message.chat.id}", text = locales.string(lang, "DeleteServiceMessages")+" "+config.checkmark(event.message.chat.id, "DeleteServiceMessages"))],
        ]
        keyboard = InlineKeyboardMarkup(inline_keyboard = buttons)
        await event.message.edit_text(locales.string(lang, "settings"), reply_markup = keyboard)
    if event.data[:2] in locales.existingTranslations:
        if event.data[:2] == config.get_setting(event.message.chat.id, "Locale"):
            await event.answer(locales.string(config.get_setting(event.message.chat.id, "Locale"), "AlreadyChosen"))
            return

        config.save_setting(event.message.chat.id, "Locale", event.data[:2])
        lang = config.get_setting(event.message.chat.id, "Locale")
        buttons = []
        for i in locales.existingTranslations.keys():
            if i == lang:
                name = locales.existingTranslations[i] + " ✅"
            else:
                name = locales.existingTranslations[i]
            buttons.append([InlineKeyboardButton(callback_data = f"{i}{event.message.chat.id}", text = name)])
        keyboard = InlineKeyboardMarkup(inline_keyboard = buttons)
        await event.message.edit_text(locales.string(lang, "ChooseLang"), reply_markup = keyboard)
        
