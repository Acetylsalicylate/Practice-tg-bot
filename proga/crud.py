from sqlalchemy import select, delete
from .database import async_session, User

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