from aiogram import types, Router
from aiogram.filters.command import Command
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from workers import locales, config
from workers.utils import is_admin, bot_is_admin

rt = Router()

@rt.message(Command("start"))
async def start(message: types.Message):
    if message.chat.type == 'private':
        lang = message.from_user.language_code
    else:
        lang = config.get_setting(message.chat.id, "Locale")
        if config.get_setting(message.chat.id, "ReturnNotAdminMessage") == True:
            member = await message.bot.get_chat_member(message.chat.id, message.from_user.id)
            if is_admin(member) == False:
                return

    buttontext = locales.string(lang, "ghbutton")
    button = [[InlineKeyboardButton(url = locales.ghlink, text = buttontext)]]
    keyboard = InlineKeyboardMarkup(inline_keyboard = button)
    await message.reply(locales.string(lang, "hi"), reply_markup = keyboard)

@rt.message(Command("settings"))
async def settings(message: types.Message):
    if message.chat.type == 'private':
        await message.reply(locales.string(lang, "settingspm"))
        return

    lang = config.get_setting(message.chat.id, "Locale")

    gotme = await message.bot.get_me()
    me = await message.bot.get_chat_member(message.chat.id, gotme.id)
    if bot_is_admin(me) == False:
        await message.reply(locales.string(lang, "NoRights"))
        return

    member = await message.bot.get_chat_member(message.chat.id, message.from_user.id)
    if is_admin(member) == False:
        if config.get_setting(message.chat.id, 'ReturnNotAdminMessage'):
            await message.reply(locales.string(lang, "NotAdmin"))
        return
    buttons = [
        [InlineKeyboardButton(callback_data = f"ban{message.chat.id}", text = locales.string(lang, "BanMembers")+" "+config.checkmark(message.chat.id, "BanMembers"))],
        [InlineKeyboardButton(callback_data = f"ser{message.chat.id}", text = locales.string(lang, "DeleteServiceMessages")+" "+config.checkmark(message.chat.id, "DeleteServiceMessages"))],
        [InlineKeyboardButton(callback_data = f"nad{message.chat.id}", text = locales.string(lang, "ReturnNotAdminMessage")+" "+config.checkmark(message.chat.id, "ReturnNotAdminMessage"))],
    ]
    keyboard = InlineKeyboardMarkup(inline_keyboard = buttons)
    await message.reply(locales.string(lang, "settings"), reply_markup = keyboard)

@rt.message(Command("toggle"))
async def toggle(message: types.Message):
    if message.chat.type == 'private':
        lang = message.from_user.language_code
        await message.reply(locales.string(lang, "settingspm"))
        return
    else:
        lang = config.get_setting(message.chat.id, "Locale")
        gotme = await message.bot.get_me()
        me = await message.bot.get_chat_member(message.chat.id, gotme.id)
        if bot_is_admin(me) == False:
            return
        
        member = await message.bot.get_chat_member(message.chat.id, message.from_user.id)
        if is_admin(member) == False:
            if config.get_setting(message.chat.id, 'ReturnNotAdminMessage'):
                await message.reply(locales.string(lang, "NotAdmin"))
            return
        
        newvalue = not config.get_setting(message.chat.id, 'Enabled')
        config.save_setting(message.chat.id, 'Enabled', newvalue)
        answer = locales.string(lang, f"bot{newvalue}")
        await message.reply(answer)

@rt.message(Command("language"))
async def lang(message: types.Message):
    if message.chat.type == 'private':
        await message.reply(locales.string(message.from_user.language_code, "settingspm"))
        return
    
    lang = config.get_setting(message.chat.id, "Locale")
    member = await message.bot.get_chat_member(message.chat.id, message.from_user.id)

    if is_admin(member) == False:
        if config.get_setting(message.chat.id, 'ReturnNotAdminMessage'):
            await message.reply(locales.string(lang, "NotAdmin"))
        return
    
    gotme = await message.bot.get_me()
    me = await message.bot.get_chat_member(message.chat.id, gotme.id)

    if bot_is_admin(me) == False:
        await message.reply(locales.string(lang, "NoRights"))
        return

    buttons = []
    for i in locales.existingTranslations.keys():
        if i == lang:
            name = locales.existingTranslations[i] + " ✅"
        else:
            name = locales.existingTranslations[i]
        buttons.append([InlineKeyboardButton(callback_data = f"{i}{message.chat.id}", text = name)])
    keyboard = InlineKeyboardMarkup(inline_keyboard = buttons)
    await message.reply(locales.string(lang, "ChooseLang"), reply_markup = keyboard)