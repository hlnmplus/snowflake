import json

db = {}

initdb = {
    "DeleteServiceMessages": True,
    "BanMembers": False,
    "Enabled": True,
    "Locale": "en",
    "ReturnNotAdminMessage": False
}

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
    db[chat] = initdb
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
        if chat in db.keys() and setting not in db[chat].keys() and setting in initdb.keys():
            db[chat][setting] = initdb[setting]
        return db[chat][setting]
    except KeyError:
        init_chat(chat)
        return db[chat][setting]

def save_setting(chatid, setting, value):
    global db
    chat = str(chatid)
    try:
        if chat in db.keys() and setting not in db[chat].keys() and setting in initdb.keys():
            db[chat][setting] = initdb[setting]
        db[chat][setting] = value
    except KeyError:
        init_chat(chat)
        db[chat][setting] = value
    save_db()
    return

def checkmark(chatid, setting):
    chat = str(chatid)
    try:
        if db[chat][setting] == True: return "✅"
        elif db[chat][setting] == False: return "❌"
        else: return
    except KeyError:
        init_chat(chat)
        if db[chat][setting] == True: return "✅"
        elif db[chat][setting] == False: return "❌"
        else: return

parse_json()