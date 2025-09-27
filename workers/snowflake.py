from aiogram import types, Router
from aiogram.filters import ChatMemberUpdatedFilter
from aiogram.filters.chat_member_updated import IS_NOT_MEMBER, IS_MEMBER
from aiogram.types import ContentType
from workers import locales, config
from workers.utils import bot_is_admin

rt = Router()

@rt.chat_member(ChatMemberUpdatedFilter(IS_NOT_MEMBER >> IS_MEMBER))
async def joined(event: types.ChatMemberUpdated):
    gotme = await event.bot.get_me()
    me = await event.bot.get_chat_member(event.chat.id, gotme.id)

    if bot_is_admin(me) == False:
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
            if bot_is_admin(me) == False:
                if config.get_setting(message.chat.id, 'ReturnNotAdminMessage'):
                    await message.reply(locales.string(lang, "NoRights"))
                return

            await message.delete()