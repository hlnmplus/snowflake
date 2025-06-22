#evryz4's fork of holinim's project https://github.com/hlnmplus/snowflake

import json
import os

db = {}

sample = {
    "DeleteServiceMessages": True,
    "BanMembers": False,
    "Enabled": True,
    "Locale": "en",
    "ReturnNotAdminMessage": False
}

def parse_json():
    global db

    try:
        with open('db.json') as file:
            db = json.load(file)

    except FileNotFoundError:
        with open('db.json', 'w') as file:
            file.truncate(0)
            file.write(json.dumps(db))

def init_chat(chatid: int | str):
    global db

    chat = str(chatid)
    db[chat] = sample

    save_db()

def save_db():
    with open('db.json', 'w') as file:
        file.truncate(0)
        file.write(json.dumps(db))

def get_setting(chatid: int | str, setting: str) -> str | bool:
    chatid = str(chatid)

    if chatid not in db.keys():
        init_chat(chatid)

    return db[chatid][setting]

def save_setting(chatid: int | str, setting: str, value: bool | str):
    global db

    chatid = str(chatid)

    if chatid not in db.keys():
        init_chat(chatid)

    db[chatid][setting] = value
    save_db()

def checkmark(chatid: int | str, setting: str) -> str | None:
    chatid = str(chatid)

    try: db[chatid][setting]
    except: init_chat(chatid)

    return '✅' if db[chatid][setting] else '❌'

parse_json()