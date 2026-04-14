# Telegram User Management Service

Асинхронный Telegram-бот для управления списком пользователей в базе данных PostgreSQL.

## Стек
* **Язык:** Python 3.11
* **Библиотека бота:** aiogram 3.4.1 (Asyncio)
* **База данных:** PostgreSQL 15
* **ORM:** SQLAlchemy 2.0.48 (asyncpg)
* **Контейнеризация:** Docker, Docker Compose
* **Дополнительно:** Pandas & Openpyxl (парсинг документов), Faker (сидирование бд)

## Функциональные возможности
- **Автоматическая инициализация:** При первом запуске бот самостоятельно создает таблицы и заполняет их 15 тестовыми записями через библиотеку Faker.
- **Просмотр данных:** Команда `/list` выводит всех пользователей из БД.
- **Точечное удаление:** Команда `/del <email>` для удаления конкретной записи.
- **Массовое удаление через файлы:** Бот принимает файлы `.csv` и `.xlsx`.
- **Надежность:** Асинхронная архитектура позволяет обрабатывать файлы в памяти (io.BytesIO) без создания временных файлов на диске.

## Инструкция по запуску

Для запуска проекта необходимо наличие установленного Docker.

1. **Клонируйте репозиторий:**
   ```bash
   git clone [https://github.com/Acetylsalicylate/Practice-tg-bot.git](https://github.com/Acetylsalicylate/Practice-tg-bot.git)
   cd Practice-tg-bot

2. **Настройте переменные окружения:**
    Создайте файл .env в корневой папке и добавьте туда ваш токен

   ```bash
    bot_token=vash_token
    db_url=postgresql+asyncpg://user:password@db:5432/botdb
    postageres_user=user
    postageres_password=password
    postageres_db=botdb

4. **Запуск:**
   Бот станет доступен сразу после того, как база данных пройдет проверку healthcheck
   ```bash
    docker-compose up --build
