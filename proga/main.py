import asyncio
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from proga.config import bot_token
from proga.database import init_db
from proga.seed import seed_db
from proga.handlers import router

async def main():
    bot = Bot(token=bot_token, default=DefaultBotProperties(parse_mode='HTML'))
    dp = Dispatcher()
    dp.include_router(router)

    print("Инициализация БД...")
    await init_db()
    await seed_db()
    
    print("Запуск бота...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())