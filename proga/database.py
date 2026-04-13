from sqlalchemy import Column, Integer, String, select, delete
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import declarative_base
from faker import Faker
from .config import db_url

engine = create_async_engine(db_url, echo=False)
async_session = async_sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)
Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    user_id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String, nullable=False)
    user_email = Column(String, unique=True, nullable=False)

async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    # Сидирование
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

#Вывод всех
async def get_all_users():
    async with async_session() as session:
        result = await session.execute(select(User))
        return result.scalars().all()

#Удаляет по email. Возвращает True, если удален, иначе False
async def delete_user_by_email(email: str) -> bool:
    async with async_session() as session:
        result = await session.execute(
            delete(User).where(User.user_email == email).returning(User.user_id)
        )
        await session.commit()
        return bool(result.fetchone())

#Удаляет список. Возвращает количество удаленных записей
async def delete_users_by_emails(emails: set) -> int:
    async with async_session() as session:
        result = await session.execute(
            delete(User).where(User.user_email.in_(emails)).returning(User.user_id)
        )
        await session.commit()
        return len(result.fetchall())