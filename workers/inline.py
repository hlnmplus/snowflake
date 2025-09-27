from aiogram import types, Router
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from workers import locales, config
from workers.utils import is_admin

rt = Router()

@rt.callback_query()
async def callback(event: types.CallbackQuery):
    cfg = {
        'ban': 'BanMembers',
        'ser': 'DeleteServiceMessages',
        'nad': 'ReturnNotAdminMessage'
    }
    
    member = await event.message.bot.get_chat_member(event.message.chat.id, event.from_user.id)
    
    if is_admin(member) == False:
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
            if i == lang: name = locales.existingTranslations[i] + " ✅"
            else: name = locales.existingTranslations[i]
            buttons.append([InlineKeyboardButton(callback_data = f"{i}{event.message.chat.id}", text = name)])
        keyboard = InlineKeyboardMarkup(inline_keyboard = buttons)
        await event.message.edit_text(locales.string(lang, "ChooseLang"), reply_markup = keyboard)
