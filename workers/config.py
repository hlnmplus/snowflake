import json

db = {}

def parse_json():
    global db
    try:
        file = open('db.json', 'r')
        db = json.load(file)
        file.close()
    except FileNotFoundError:
        db = {}
        file = open('db.json', 'w')
        file.truncate(0)
        file.write(json.dumps(db))
        file.close()        
    return

def init_chat(chatid):
    global db
    chat = str(chatid)
    db[chat] = {
        "DeleteServiceMessages": True,
        "BanMembers": False,
        "Enable": True,
        "Locale": "en"
    }
    save_db()
    return

def save_db():
    file = open('db.json', 'w')
    file.truncate(0)
    file.write(json.dumps(db))
    file.close()
    return

def get_setting(chatid, setting):
    chat = str(chatid)
    try:
        return db[chat][setting]
    except KeyError:
        init_chat(chat)
        return db[chat][setting]

def save_setting(chatid, setting, value):
    global db
    chat = str(chatid)
    try:
        db[chat][setting] = value
    except KeyError:
        init_chat(chat)
        db[chat][setting] = value
    save_db()
    return

parse_json()