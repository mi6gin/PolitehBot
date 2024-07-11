from aiogram import types
import aiohttp
from sqlalchemy import select
from DB.Database import UniverAPI
from handlers.user.UserData import UserData
from ConnectDB.DBconnect import Zaglushka

async def Authorization(user_id):
    result = await UserData(user_id)
    if result is not None:  # Проверяем, что результат не пустой и содержит два значения
        login = result[0]
        password = result[1]
        print(login, password)
    async with Zaglushka.async_session() as session:
        print(10909091)
        user = select(UniverAPI).where(UniverAPI.telegram_id == user_id)
        existing_user = await session.execute(user)
        user_object = existing_user.scalar()

        async with aiohttp.ClientSession() as http_session:
            async with http_session.get(f'https://univerapi.kstu.kz/?login={login}&password={password}') as response:
                cookies = response.cookies
                aspxauth_cookie = cookies.get('.ASPXAUTH')
                sessionid_cookie = cookies.get('ASP.NET_SessionId')
                if aspxauth_cookie and sessionid_cookie:
                    cookie_values = {
                        '.ASPXAUTH': aspxauth_cookie.value,
                        'ASP.NET_SessionId': sessionid_cookie.value
                    }

                    if user_object:  # Если пользователь существует, обновляем его данные
                        user_object.ASPXAUTH = cookie_values['.ASPXAUTH']
                        user_object.ASPNET_SessionId = cookie_values['ASP.NET_SessionId']
                    else:  # Если пользователь не существует, добавляем нового пользователя
                        new_user = UniverAPI(
                            telegram_id=user_id,
                            ASPXAUTH=cookie_values['.ASPXAUTH'],
                            ASPNET_SessionId=cookie_values['ASP.NET_SessionId'],
                        )
                        session.add(new_user)
                    session.add(user_object)
                    await session.commit()  # Сохраняем изменения в базе данных
                    if aspxauth_cookie and sessionid_cookie:
                        return {
                            '.ASPXAUTH': aspxauth_cookie.value,
                            'ASP.NET_SessionId': sessionid_cookie.value
                        }
                else:
                    return False
