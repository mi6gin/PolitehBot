import aiohttp
import requests
from aiogram import types
from bs4 import BeautifulSoup

from univer20 import AuthVer2, AuthVer1


async def get_umkd_id(cookies, message: types.Message, user_id, discipline_name):
    session = requests.session()
    session.cookies.update(cookies)
    async with aiohttp.ClientSession(cookies=cookies) as session:
        async with session.get("https://univer.kstu.kz/student/umkd/") as response:
            if response.status == 200:
                soup = BeautifulSoup(await response.text(), "html.parser")
                discipline_rows = soup.find_all('tr', class_='link', id=lambda value: value and value.isdigit())
                for discipline_row in discipline_rows:
                    discipline_name_element = discipline_row.find('td', text=discipline_name)
                    if discipline_name_element:
                        discipline_id = discipline_row.get('id')
                        return discipline_id
                else:
                    print("Дисциплина не найдена")
                    return None
            else:
                print("Ошибка получения информации о пользователе")
                cookies = await AuthVer2.Authorization(user_id)
                if cookies is not False:
                    discipline_id = await get_umkd_id(cookies, message, user_id, discipline_name)
                    return discipline_id
                else:
                    return False


async def Umkd_id(message: types.Message, user_id, discipline_name):
    cookies = await AuthVer1.Authorization(user_id)
    if cookies is not False:
        umkd = await get_umkd_id(cookies, message, user_id, discipline_name)
        return umkd
    else:
        cookies = await AuthVer2.Authorization(user_id)
        if cookies is not False:
            umkd = await get_umkd_id(cookies, message, user_id, discipline_name)
            return umkd
        else:
            return False
