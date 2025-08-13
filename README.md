# ❄️ Snowflake

Kicks everybody who trying to join your group. 

## Installation

1. Clone repository and go to the bot's folder
   
   `git clone https://github.com/hlnmplus/snowflake`
   
   `cd snowflake`
3. Install dependencies
   
   `python3 -m pip install -r requirements.txt`
5. Obtain a Telegram BotAPI token at [BotFather](https://t.me/botfather)
   
7. Paste your token to the .env file
   
   `API-KEY=123456789:PASTE-YOUR-BOTAPI-TOKEN-HERE`,
   
   where `123456789:PASTE-YOUR-BOTAPI-TOKEN-HERE` — your BotAPI key
   
9. Done! Run command below to start the bot.
   
   `python main.py`

## Official instance

You can use official instance of bot — https://t.me/projectsnowflakebot. If it's down, message me at (@hlnmplus)[https://hlnmplus.t.me]

## Some questions

### Q: How to translate this bot to my language?

A: Edit locales.py file and add your language to existingTranslations var. Create a pull request and just wait.

### Q: Can you track me?

A: This bot doesn't spy on your chats, but it's collects IDs of chats where this bot is added. Check `workers/config.py` for more details. If you want to use this bot without any settings and tracking, you can use [Snowball](https://github.com/hlnmplus/snowball).
