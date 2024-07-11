import aiohttp
from bs4 import BeautifulSoup
from aiogram import types
from univer20 import AuthVer2, AuthVer1
from univer20.Language.LangChange import HTTPHeaders
from univer20.Language.Set_language import set_lang


async def get_adviser_info(cookies, user_id):
    headers = HTTPHeaders(user_id, user_id, user_id, user_id, user_id)
    async with aiohttp.ClientSession(cookies=cookies) as session:
        language = await set_lang(user_id)
        async with session.get("https://univer.kstu.kz/student/advicer/", headers=headers.Language(language)) as response:
            if response.status == 200:
                soup = BeautifulSoup(await response.text(), "html.parser")
                name_element = soup.find("div", class_="links")
                inner_div = soup.find("div", class_="inner")

                # Находим все теги <td> внутри этого <div>
                td_elements = inner_div.find_all("td")

                FIO = td_elements[0].text.strip()
                Name = td_elements[1].text.strip()
                adviser_data = {
                    "name": FIO,
                    "FIO": Name
                }
                print(adviser_data)
                return adviser_data
            else:
                print("Ошибка получения информации о пользователе")
                cookies = await AuthVer2.Authorization(user_id)
                if cookies is not False:
                    user = await get_adviser_info(cookies, user_id)
                    return user

async def Adviser(user_id):
    cookies = await AuthVer1.Authorization(user_id)
    if cookies is not False:
        std_data = await get_adviser_info(cookies, user_id)
        return std_data
    else:
        cookies = await AuthVer2.Authorization(user_id)
        if cookies is not False:
            std_data = await get_adviser_info(cookies, user_id)
            return std_data
        else:
            return None