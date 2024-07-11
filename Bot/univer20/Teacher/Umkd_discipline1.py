import aiohttp
from aiogram import types
from bs4 import BeautifulSoup
from univer20.Language.LangChange import HTTPHeaders
from univer20.Language.Set_language import set_lang
from univer20 import AuthVer2, AuthVer1


async def get_umkd(cookies, message: types.Message, user_id):
    headers = HTTPHeaders(user_id, user_id, user_id, user_id, user_id)
    async with aiohttp.ClientSession(cookies=cookies) as session:
        language = await set_lang(user_id)
        async with session.get("https://univer.kstu.kz/teacher/umkdpack/index/", headers=headers.Language(language)) as response:
            if response.status == 200:
                disciplines = []
                soup = BeautifulSoup(await response.text(), "html.parser")
                discipline_rows = soup.find_all('tr', class_='link')
                for row in discipline_rows:
                    discipline_name = row.find_all('td')[1].get_text(strip=True)
                    disciplines.append((discipline_name))
                return disciplines
            else:
                print("Ошибка получения информации о пользователе")
                cookies = await AuthVer2.Authorization(user_id)
                if cookies is not False:
                    umkd = await get_umkd(cookies, message, user_id)
                    return umkd

async def Umkd(message: types.Message, user_id):
    cookies = await AuthVer1.Authorization(user_id)
    if cookies is not False:
        umkd = await get_umkd(cookies, message, user_id)
        return umkd
    else:
        cookies = await AuthVer2.Authorization(user_id)
        if cookies is not False:
            umkd = await get_umkd(cookies, message, user_id)
            return umkd
        else:
            return None  # Возвращаем None в случае неудачной авторизации
