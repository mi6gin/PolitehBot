import aiohttp
from bs4 import BeautifulSoup
from univer20 import AuthVer2, AuthVer1
from univer20.Language.LangChange import HTTPHeaders
from univer20.Language.Set_language import set_lang
from aiogram import types
from sqlalchemy import select

from DB.Database import User
from ConnectDB.DBconnect import Zaglushka


async def get_check_info(cookies, message: types.Message, user_id):
    headers = HTTPHeaders(user_id, user_id, user_id, user_id, user_id)
    async with aiohttp.ClientSession(cookies=cookies) as session:
        language = await set_lang(user_id)
        async with session.get("https://univer.kstu.kz", headers=headers.Language(language)) as response:
            if response.status == 200:
                soup = BeautifulSoup(await response.text(), "html.parser")
                for row in soup.find_all('tr'):
                    links = row.find_all('a', href=lambda href: href )

                    for link in links:
                        href_value = link.get('href')
                        if "/student/bachelor/" in href_value:

                            async with Zaglushka.async_session() as session:
                                query = select(User).where(User.telegram_id == user_id)
                                existing_user = await session.execute(query)
                                existing_user = existing_user.scalar()

                                if existing_user:  # Если пользователь существует, обновляем его данные
                                    special = "student"
                                    existing_user.role = special
                                    std_data = {
                                        "spc": special,
                                    }
                                    return std_data

                        elif "/teacher/" in href_value:
                            async with Zaglushka.async_session() as session:
                                query = select(User).where(User.telegram_id == user_id)
                                existing_user = await session.execute(query)
                                existing_user = existing_user.scalar()

                                if existing_user:  # Если пользователь существует, обновляем его данные
                                    special = "teacher"
                                    existing_user.role = special
                                    std_data = {
                                        "spc": special,
                                    }
                                    return std_data

            else:
                print("Ошибка получения информации о пользователе")
                cookies = await AuthVer2.Authorization(user_id)
                if cookies is not False:
                    user = await get_check_info(cookies, message, user_id)
                    return user

async def checking(message: types.Message, user_id):
    cookies = await AuthVer1.Authorization(user_id)
    if cookies is not False:
        std_data = await get_check_info(cookies, message, user_id)
        return std_data
    else:
        cookies = await AuthVer2.Authorization(user_id)
        if cookies is not False:
            std_data = await get_check_info(cookies, message, user_id)
            return std_data
        else:
            return None