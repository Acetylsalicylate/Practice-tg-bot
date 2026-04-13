import os

bot_token = os.getenv("bot_token")
db_url = os.getenv("db_url")

if not bot_token or not db_url:
    raise ValueError("Отсутствуют необходимые переменные окружения bot_token или db_url")