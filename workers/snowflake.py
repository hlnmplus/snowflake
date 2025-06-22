#evryz4's fork of holinim's project https://github.com/hlnmplus/snowflake

from aiogram import types, Router
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, ContentType
from aiogram.filters import ChatMemberUpdatedFilter
from aiogram.filters.chat_member_updated import IS_NOT_MEMBER, IS_MEMBER
from aiogram.filters.command import Command

from workers import locales, config

rt = Router()

cfg = {
    'ban': 'BanMembers',
    'ser': 'DeleteServiceMessages',
    'nad': 'ReturnNotAdminMessage'
}

def check(member: types.chat_member.ChatMember, message_delete: bool = False) -> bool:
    if type(member) not in [types.chat_member_owner.ChatMemberOwner,
                            types.chat_member_administrator.ChatMemberAdministrator]:
        return False
    
    try:
        if not member.can_restrict_members:
            return False

        if message_delete and not member.can_delete_messages:
            return False
    except:
        pass

    return True

async def private_check(message: types.Message) -> bool:
    if message.chat.type == 'private':
        lang = message.from_user.language_code

        settingspm_text = locales.string(lang, "settingspm")
        await message.reply(text=settingspm_text)

        return True
    return False

@rt.message(Command("start"))
async def startcmd(message: types.Message):
    if message.chat.type == 'private':
        lang = message.from_user.language_code

    else:
        lang = config.get_setting(message.chat.id, "Locale")
        
        member = await message.bot.get_chat_member(message.chat.id, message.from_user.id)
        if config.get_setting(message.chat.id, "ReturnNotAdminMessage") and not check(member):
            return

    button_text = locales.string(lang, "ghbutton")
    button = [
        [InlineKeyboardButton(url = locales.ghlink,
                              text = button_text)]
    ]
    reply_markup = InlineKeyboardMarkup(inline_keyboard=button)

    hi_text = locales.string(lang, "hi")
    await message.reply(text=hi_text,
                        reply_markup=reply_markup)

@rt.message(Command("settings"))
async def settingscmd(message: types.Message):
    if await private_check(message): return

    lang = config.get_setting(message.chat.id, "Locale")

    bot = await message.bot.get_me()
    me = await message.bot.get_chat_member(message.chat.id, bot.id)

    if not check(me):
        norights_text = locales.string(lang, "NoRights")
        await message.reply(norights_text)

        return

    member = await message.bot.get_chat_member(message.chat.id, message.from_user.id)
    if not check(member):
        if config.get_setting(message.chat.id, 'ReturnNotAdminMessage'):
            notadmin_text = locales.string(lang, "NotAdmin")
            await message.reply(notadmin_text)

        return

    buttons = [
        [InlineKeyboardButton(callback_data = f"ban{message.chat.id}",
                              text = locales.string(lang, "BanMembers")+" "+config.checkmark(message.chat.id, "BanMembers"))],
        
        [InlineKeyboardButton(callback_data = f"ser{message.chat.id}",
                              text = locales.string(lang, "DeleteServiceMessages")+" "+config.checkmark(message.chat.id, "DeleteServiceMessages"))],
        
        [InlineKeyboardButton(callback_data = f"nad{message.chat.id}",
                              text = locales.string(lang, "ReturnNotAdminMessage")+" "+config.checkmark(message.chat.id, "ReturnNotAdminMessage"))],
    ]

    reply_markup = InlineKeyboardMarkup(inline_keyboard=buttons)

    settings_text = locales.string(lang, "settings")
    await message.reply(text=settings_text,
                        reply_markup=reply_markup)

@rt.message(Command("toggle"))
async def togglecmd(message: types.Message):
    if await private_check(message): return

    lang = config.get_setting(message.chat.id, "Locale")

    bot = await message.bot.get_me()
    me = await message.bot.get_chat_member(message.chat.id, bot.id)

    if not check(me):
        norights_text = locales.string(lang, "NoRights")
        await message.reply(norights_text)

        return
        
    member = await message.bot.get_chat_member(message.chat.id, message.from_user.id)
    if not check(member):
        if config.get_setting(message.chat.id, 'ReturnNotAdminMessage'):
            notadmin_text = locales.string(lang, "NotAdmin")
            await message.reply(notadmin_text)

        return

    newvalue = not config.get_setting(message.chat.id, 'Enabled')
    config.save_setting(message.chat.id, 'Enabled', newvalue)

    answer = locales.string(lang, f"bot{newvalue}")
    await message.reply(text=answer)

@rt.message(Command("language"))
async def languagecmd(message: types.Message):
    if await private_check(message): return
    
    lang = config.get_setting(message.chat.id, "Locale")

    member = await message.bot.get_chat_member(message.chat.id, message.from_user.id)
    if not check(member):
        if config.get_setting(message.chat.id, 'ReturnNotAdminMessage'):
            notadmin_text = locales.string(lang, "NotAdmin")
            await message.reply(notadmin_text)
        
        return

    bot = await message.bot.get_me()
    me = await message.bot.get_chat_member(message.chat.id, bot.id)

    if not check(me):
        norights_text = locales.string(lang, "NoRights")
        await message.reply(norights_text)

        return

    buttons = []
    for translation in locales.translations.keys():
        name = locales.translations[translation]
        name +=  "✅" if translation == lang else ''

        buttons.append([InlineKeyboardButton(callback_data = f"{translation}{message.chat.id}",
                                             text = name)])

    reply_markup = InlineKeyboardMarkup(inline_keyboard=buttons)

    chooselang_text = locales.string(lang, "ChooseLang")
    await message.reply(text=chooselang_text,
                        reply_markup=reply_markup)

@rt.chat_member(ChatMemberUpdatedFilter(IS_NOT_MEMBER >> IS_MEMBER))
async def joinedupd(event: types.ChatMemberUpdated):
    bot = await event.bot.get_me()
    me = await event.bot.get_chat_member(event.chat.id, bot.id)

    if not check(me, True): return
    if not config.get_setting(event.chat.id, 'Enabled'): return

    user_id = event.new_chat_member.user.id
    await event.chat.ban(user_id=user_id)

    banmembers = config.get_setting(event.chat.id, "BanMembers")
    if not banmembers:
        await event.chat.unban(user_id=user_id)

@rt.message()
async def msg(message: types.Message):
    lang = config.get_setting(message.chat.id, "Locale")

    if message.content_type not in [ContentType.NEW_CHAT_MEMBERS, ContentType.LEFT_CHAT_MEMBER]: return
    if not config.get_setting(message.chat.id, "DeleteServiceMessages"): return

    bot = await message.bot.get_me()
    me = await message.bot.get_chat_member(message.chat.id, bot.id)

    if not check(me, True):
        norights_text = locales.string(lang, "NoRights")
        await message.reply(norights_text)

        return

    await message.delete()

@rt.callback_query()
async def callback_query(event: types.CallbackQuery):
    member = await event.message.bot.get_chat_member(event.message.chat.id, event.from_user.id)
    if not check(member):
        noformatnoadmin_text = locales.string(event.from_user.language_code, "NoformatNoadmin")
        await event.answer(noformatnoadmin_text)

        return

    lang = config.get_setting(event.message.chat.id, "Locale")

    bot = await event.bot.get_me()
    me = await event.bot.get_chat_member(event.message.chat.id, bot.id)

    if not check(me, True):
        norights_text = locales.string(lang, "NoRights")
        await event.message.edit_text(norights_text)

        return
    
    if event.data[:3] in cfg:
        chatid = int(event.data[3:])
        config.save_setting(chatid, cfg[event.data[:3]],
                            not config.get_setting(chatid, cfg[event.data[:3]]))
        
        buttons = [
            [InlineKeyboardButton(callback_data = f"ban{event.message.chat.id}",
                                  text = locales.string(lang, "BanMembers")+" "+config.checkmark(event.message.chat.id, "BanMembers"))],
            
            [InlineKeyboardButton(callback_data = f"ser{event.message.chat.id}",
                                  text = locales.string(lang, "DeleteServiceMessages")+" "+config.checkmark(event.message.chat.id, "DeleteServiceMessages"))],
            
            [InlineKeyboardButton(callback_data = f"nad{event.message.chat.id}",
                                  text = locales.string(lang, "ReturnNotAdminMessage")+" "+config.checkmark(event.message.chat.id, "ReturnNotAdminMessage"))],
        ]
        reply_markup = InlineKeyboardMarkup(inline_keyboard=buttons)

        settings_text = locales.string(lang, "settings")
        await event.message.edit_text(text=settings_text,
                                      reply_markup=reply_markup)

    if event.data[:2] in locales.translations:
        chatid = event.message.chat.id

        locale = config.get_setting(chatid, "Locale")
        if event.data[:2] == locale:
            alreadychosen_text = locales.string(locale, "AlreadyChosen")
            await event.answer(alreadychosen_text)

            return

        config.save_setting(chatid, "Locale", event.data[:2])
        lang = config.get_setting(chatid, "Locale")

        buttons = []
        for translation in locales.translations.keys():
            name = locales.translations[translation]
            name +=  "✅" if translation == lang else ''

            buttons.append([InlineKeyboardButton(callback_data = f"{translation}{chatid}",
                                                 text = name)])

        reply_markup = InlineKeyboardMarkup(inline_keyboard=buttons)
        
        chooselang_text = locales.string(lang, "ChooseLang")
        await event.message.edit_text(text=chooselang_text,
                                      reply_markup=reply_markup)
