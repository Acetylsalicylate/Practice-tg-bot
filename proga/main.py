import io
import re
import asyncio
import pandas as pd
from aiogram import Bot, Dispatcher, F, types
from aiogram.filters import CommandStart, Command
from aiogram.types import Message
from aiogram.client.default import DefaultBotProperties
from .config import bot_token
from .database import init_db, get_all_users, delete_user_by_email, delete_users_by_emails

bot = Bot(token=bot_token, default=DefaultBotProperties(parse_mode='HTML'))
dp = Dispatcher()

email_regex = re.compile(r'[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+')

@dp.message(CommandStart())
async def cmd_start(message: Message):
    help_text = (
        "<b>Добро пожаловать в систему управления пользователями!</b>\n\n"
        "Доступные команды:\n"
        "/list — Вывод списка пользователей\n"
        "/del <i>email</i> — Точечное удаление пользователя\n\n"
        "<b>Массовое удаление:</b>\n"
        "Просто отправьте мне файл .csv или .xlsx. Я найду в нем все email-адреса и удалю их из базы."
    )
    await message.answer(help_text)

@dp.message(Command("list"))
async def cmd_list(message: Message):
    users = await get_all_users()
    if not users:
        await message.answer("База данных пользователей пуста.")
        return

    response = "<b>Список пользователей:</b>\n\n"
    for u in users:
        response += f"{u.user_id} | {u.username} | {u.user_email}\n"

    if len(response) > 4000:
        response = response[:4000] + "\n... [Превышен лимит символов]"
        
    await message.answer(response)

@dp.message(Command("del"))
async def cmd_delete_single(message: Message):
    args = message.text.split(maxsplit=1)
    if len(args) < 2:
        await message.answer("Использование: /del <code>user@example.com</code>")
        return
    
    email = args[1].strip()
    if not email_regex.match(email):
        await message.answer("Некорректный формат email.")
        return

    deleted = await delete_user_by_email(email)
    if deleted:
        await message.answer(f"Пользователь с email <b>{email}</b> успешно удален.")
    else:
        await message.answer(f"Пользователь с email <b>{email}</b> не найден в базе.")

@dp.message(F.document)
async def process_document(message: Message):
    doc = message.document
    if not doc.file_name.endswith(('.csv', '.xlsx')):
        await message.answer("Поддерживаются только форматы <b>.csv</b> и <b>.xlsx</b>")
        return

    file_in_memory = io.BytesIO()
    try:
        await bot.download(doc, destination=file_in_memory)
        file_in_memory.seek(0)
        
        if doc.file_name.endswith('.csv'):
            df = pd.read_csv(file_in_memory, dtype=str, header=None)
        else:
            df = pd.read_excel(file_in_memory, dtype=str, header=None)

        content_stack = df.stack().astype(str).tolist()
        full_text = " ".join(content_stack)

        found_emails = set(email_regex.findall(full_text))
        
        if not found_emails:
            await message.answer("В файле не найдено ни одного корректного email-адреса.")
            return
            
        deleted_count = await delete_users_by_emails(found_emails)
        
        await message.answer(
            f"<b>Результат обработки:</b>\n"
            f"Найдено уникальных адресов: <b>{len(found_emails)}</b>\n"
            f"Удалено из базы данных: <b>{deleted_count}</b>\n\n"
            f"<i>Примечание: Цвет текста или наличие ссылок в Excel не влияет на поиск.</i>"
        )
        
    except Exception as e:
        print(f"Error: {e}")
        await message.answer("Произошла ошибка при разборе файла. Убедитесь, что это корректная таблица.")

async def main():
    print("Инициализация БД...")
    await init_db()
    print("Запуск бота...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())