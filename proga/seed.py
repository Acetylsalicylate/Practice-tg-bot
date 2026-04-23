from sqlalchemy import select
from faker import Faker
from .database import async_session, User

async def seed_db():
    async with async_session() as session:
        result = await session.execute(select(User).limit(1))
        if result.scalar_one_or_none() is None:
            fake = Faker()
            users = [
                User(username=fake.user_name(), user_email=fake.unique.email())
                for _ in range(15)
            ]
            session.add_all(users)
            await session.commit()
            print("БД наполнена тестовыми данными (15 записей).")