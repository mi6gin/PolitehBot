
from sqlalchemy import select
from DB.Database import UniverAPI
from ConnectDB.DBconnect import Zaglushka

async def Authorization(user_id):
    async with Zaglushka.async_session() as session:
        user = select(UniverAPI).where(UniverAPI.telegram_id == user_id)
        existing_user = await session.execute(user)
        user_object = existing_user.scalar()

        if user_object:  # Если пользователь существует
            # Пытаемся взять данные из таблицы
            aspxauth_cookie = user_object.ASPXAUTH
            sessionid_cookie = user_object.ASPNET_SessionId
            return{
                '.ASPXAUTH': aspxauth_cookie,
                'ASP.NET_SessionId': sessionid_cookie
            }
        else:
            return False