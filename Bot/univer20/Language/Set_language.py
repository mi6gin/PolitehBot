from ConnectDB.DBconnect import Zaglushka
from DB.Database import User
from sqlalchemy import select

async def set_lang(user_id):
    async with Zaglushka.async_session() as session:
        telega_user = select(User).where(User.telegram_id == user_id)
        existing_user = await session.execute(telega_user)
        user_object = existing_user.scalar()
        if user_object:
            language = user_object.language
            return language