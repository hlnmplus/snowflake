from aiogram import types, Router
from aiogram.filters import ChatMemberUpdatedFilter
from aiogram.filters.chat_member_updated import IS_NOT_MEMBER, IS_MEMBER
from aiogram.filters.command import Command
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, ContentType
from workers import locales, config

rt = Router()

@rt.message(Command("start"))
async def start(message: types.Message):
    if message.chat.type == 'private':
        lang = message.from_user.language_code
    else:
        lang = config.get_setting(message.chat.id, "Locale")
        if config.get_setting(message.chat.id, "ReturnNotAdminMessage") == True:
            member = await message.bot.get_chat_member(message.chat.id, message.from_user.id)
            if (type(member) == types.chat_member_owner.ChatMemberOwner) or (type(member) == types.chat_member_administrator.ChatMemberAdministrator and member.can_restrict_members == True):
                pass
            else:
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
    if (type(me) == types.chat_member_member.ChatMemberMember) or (types.chat_member_administrator.ChatMemberAdministrator and (me.can_restrict_members == False or me.can_delete_messages == False)):
        await message.reply(locales.string(lang, "NoRights"))
        return

    member = await message.bot.get_chat_member(message.chat.id, message.from_user.id)
    if (type(member) == types.chat_member_owner.ChatMemberOwner) or (type(member) == types.chat_member_administrator.ChatMemberAdministrator and member.can_restrict_members == True):
        pass
    else:
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
        if (type(me) == types.chat_member_member.ChatMemberMember) or (types.chat_member_administrator.ChatMemberAdministrator and (me.can_restrict_members == False or me.can_delete_messages == False)):
            await message.reply(locales.string(lang, "NoRights"))
            return
        
        member = await message.bot.get_chat_member(message.chat.id, message.from_user.id)
        if type(member) == types.chat_member_owner.ChatMemberOwner:
            pass
        elif type(member) == types.chat_member_administrator.ChatMemberAdministrator and member.can_restrict_members == True:
            pass
        else:
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
    if type(member) == types.chat_member_owner.ChatMemberOwner:
        pass
    elif type(member) == types.chat_member_administrator.ChatMemberAdministrator and member.can_restrict_members == True:
        pass
    else:
        if config.get_setting(message.chat.id, 'ReturnNotAdminMessage'):
            await message.reply(locales.string(lang, "NotAdmin"))
        return
    

    gotme = await message.bot.get_me()
    me = await message.bot.get_chat_member(message.chat.id, gotme.id)
    if (type(me) == types.chat_member_member.ChatMemberMember) or (types.chat_member_administrator.ChatMemberAdministrator and (me.can_restrict_members == False or me.can_delete_messages == False)):
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

@rt.chat_member(ChatMemberUpdatedFilter(IS_NOT_MEMBER >> IS_MEMBER))
async def joined(event: types.ChatMemberUpdated):
    gotme = await event.bot.get_me()
    me = await event.bot.get_chat_member(event.chat.id, gotme.id)

    if (type(me) == types.chat_member_member.ChatMemberMember) or (types.chat_member_administrator.ChatMemberAdministrator and (me.can_restrict_members == False or me.can_delete_messages == False)):
        return
    if config.get_setting(event.chat.id, 'Enabled') == False:
        return
    await event.chat.ban(event.new_chat_member.user.id)
    if config.get_setting(event.chat.id, "BanMembers") == False:
        await event.chat.unban(event.new_chat_member.user.id)

@rt.message()
async def anything(message: types.Message):
    lang = config.get_setting(message.chat.id, "Locale")
    if message.content_type in [ContentType.NEW_CHAT_MEMBERS, ContentType.LEFT_CHAT_MEMBER]:
        if config.get_setting(message.chat.id, "DeleteServiceMessages") == True:
            gotme = await message.bot.get_me()
            me = await message.bot.get_chat_member(message.chat.id, gotme.id)
            if (type(me) == types.chat_member_member.ChatMemberMember) or (types.chat_member_administrator.ChatMemberAdministrator and (me.can_restrict_members == False or me.can_delete_messages == False)):
                await message.reply(locales.string(lang, "NoRights"))
                return

            await message.delete()

@rt.callback_query()
async def callback(event: types.CallbackQuery):
    cfg = {
        'ban': 'BanMembers',
        'ser': 'DeleteServiceMessages',
        'nad': 'ReturnNotAdminMessage'
    }
    
    member = await event.message.bot.get_chat_member(event.message.chat.id, event.from_user.id)
    if type(member) == types.chat_member_owner.ChatMemberOwner:
        pass
    elif type(member) == types.chat_member_administrator.ChatMemberAdministrator and member.can_restrict_members == True:
        pass
    else:
        await event.answer(locales.string(event.from_user.language_code, "NoformatNoadmin"))
        return
    lang = config.get_setting(event.message.chat.id, "Locale")

    gotme = await event.bot.get_me()
    me = await event.bot.get_chat_member(event.message.chat.id, gotme.id)

    if (type(me) == types.chat_member_member.ChatMemberMember) or (types.chat_member_administrator.ChatMemberAdministrator and (me.can_restrict_members == False or me.can_delete_messages == False)):
        await event.message.edit_text(locales.string(lang, "NoRights"))
        return
    
    if event.data[:3] in cfg:
        chatid = int(event.data[3:])
        config.save_setting(chatid, cfg[event.data[:3]], not config.get_setting(chatid, cfg[event.data[:3]]))
        buttons = [
            [InlineKeyboardButton(callback_data = f"ban{event.message.chat.id}", text = locales.string(lang, "BanMembers")+" "+config.checkmark(event.message.chat.id, "BanMembers"))],
            [InlineKeyboardButton(callback_data = f"ser{event.message.chat.id}", text = locales.string(lang, "DeleteServiceMessages")+" "+config.checkmark(event.message.chat.id, "DeleteServiceMessages"))],
            [InlineKeyboardButton(callback_data = f"nad{event.message.chat.id}", text = locales.string(lang, "ReturnNotAdminMessage")+" "+config.checkmark(event.message.chat.id, "ReturnNotAdminMessage"))],
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
        
