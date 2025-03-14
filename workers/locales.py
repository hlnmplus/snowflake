ghlink = "https://github.com/hlnmplus/snowflake"

existingTranslations = ["en", "ru"]

en = {
    "hi": "<b>❄️ Hi!</b>\n\nThis bot does only one thing — kicks everybody, who joins your group.",
    "ghbutton": "Source code",
    "invitedok": "<b>👋 Thank you for adding me to this group!</b>\n\nBot is already working, and if you want to disable it for a while, the admin with the rights to change the group profile should use /toggle@projectsnowflakebot. That's it!",
    "invitedfail": "<b>👋 Thank you for adding me to this group!</b>\n\nUnfortunately, when I was added, admins took away the administrator rights I needed: blocking users and deleting messages. I will not be able to function until I have these rights."
}

ru = {
    "hi": "<b>❄️ Привет!</b>\n\nСуть этого бота проста — кикать всех участников, что посмеют зайти в твою группу.",
    "ghbutton": "Исходный код",
    "invitedok": "<b>👋 Спасибо, что добавили меня в эту группу!</b>\n\nБот уже работает, и если вы захотите его на время отключить — админ с правами на изменение группы должен прописать /toggle@projectsnowflakebot. Всё!",
    "invitedfail": "<b>👋 Спасибо, что добавили меня в эту группу!</b>\n\nК сожалению, при добавлении у меня забрали нужные мне права администратора: блокировка пользователей и удаление сообщений. Я не смогу функционировать, пока у меня не будет этих прав."
}

def string(code, name):
    if code not in existingTranslations:
        code = "en"
    return globals()[code][name]