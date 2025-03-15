ghlink = "https://github.com/hlnmplus/snowflake"

en = {
    "hi": "<b>❄️ Hi!</b>\n\nThis bot does only one thing — kicks everybody, who joins your group.",
    "ghbutton": "Source code",
    "invitedok": "<b>👋 Thank you for adding me to this group!</b>\n\nBot is already working, and if you want to disable it for a while, the admin with the rights to change the group profile should use /toggle@projectsnowflakebot. That's it!",
    "invitedfail": "<b>👋 Thank you for adding me to this group!</b>\n\nUnfortunately, when I was added, admins took away the administrator rights I needed: blocking users and deleting messages. I will not be able to function until I have these rights.",
    "settingspm": "<b>❌ You can't open setting in DM!</b>",
    "settings": "<b>⚙️ Settings</b>\n\nGroup admins can edit bot settings in this group by using buttons below. Use /language to change the language of the bot.",
    "DeleteServiceMessages": "Delete service messages",
    "BanMembers": "Ban (not kick) everybody, who tried join",
    "Locale": "English",
    "ChooseLang": "<b>🌐 Choose language</b>",
    "AlreadyChosen": "Already chosen",
    "NotAdmin": "<b>❌ You are not an admin.</b>",
    "NoformatNoadmin": "You are not an admin or you don't have rights to restrict members.",
}

ru = {
    "hi": "<b>❄️ Привет!</b>\n\nСуть этого бота проста — кикать всех участников, что посмеют зайти в твою группу.",
    "ghbutton": "Исходный код",
    "invitedok": "<b>👋 Спасибо, что добавили меня в эту группу!</b>\n\nБот уже работает, и если вы захотите его на время отключить — админ с правами на изменение группы должен прописать /toggle@projectsnowflakebot. Всё!",
    "invitedfail": "<b>👋 Спасибо, что добавили меня в эту группу!</b>\n\nК сожалению, при добавлении у меня забрали нужные мне права администратора: блокировка пользователей и удаление сообщений. Я не смогу функционировать, пока у меня не будет этих прав.",
    "settingspm": "<b>❌ Настройки нельзя открыть в ЛС!</b>",
    "settings": "<b>⚙️ Настройки</b>\n\nАдминистраторы группы могут изменять настройки бота, используя кнопки ниже. Используйте /language, чтобы изменить язык бота.",
    "DeleteServiceMessages": "Удалять сообщения о входе/выходе",
    "BanMembers": "Банить всех, кто посмеет зайти (не кикать)",
    "Locale": "Russian (Русский)",
    "ChooseLang": "<b>🌐 Выберите язык</b>",
    "AlreadyChosen": "Уже выбрано",
    "NotAdmin": "<b>❌ Вы не администратор группы.</b>",
    "NoformatNoadmin": "Вы не администратор группы или у Вас нет прав на ограничение участников.",
}

existingTranslations = {
    "en": en['Locale'],
    "ru": ru['Locale']
}

def string(code, name):
    if code not in existingTranslations:
        code = "en"
    return globals()[code][name]