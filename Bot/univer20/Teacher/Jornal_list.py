import json
from bs4 import Tag


import aiohttp
from aiogram import types
from bs4 import BeautifulSoup
from univer20.Language.LangChange import HTTPHeaders
from univer20.Language.Set_language import set_lang
from univer20 import AuthVer2, AuthVer1


async def get_jornal(cookies, user_id, id):
    headers = HTTPHeaders(user_id, user_id, user_id, user_id, user_id)
    async with aiohttp.ClientSession(cookies=cookies) as session:
        language = await set_lang(user_id)
        async with session.get(f"https://univer.kstu.kz/{id}", headers=headers.Language(language)) as response:
            if response.status == 200:
                soup = BeautifulSoup(await response.text(), 'html.parser')
                # Находим все теги <a> внутри таблицы

                table_elements = soup.find_all("table", class_="mt")

                # Создаем список для хранения найденных элементов <a>
                a_elements = []

                # Проходимся по каждой найденной таблице
                for table in table_elements:
                    # Находим все элементы <td> с классом "ts" внутри текущей таблицы
                    td_elements = table.find_all("td", class_="ts")

                    # Проходимся по каждому найденному элементу <td>
                    for td in td_elements:
                        # Находим все теги <a> внутри текущего элемента <td>
                        a_elements.extend(td.find_all("a"))

                num_buttons = len(a_elements)

                # Если есть кнопки, берем ссылку с последней кнопки
                if num_buttons > 0:
                    last_button_index = num_buttons - 1
                    std_data = {
                        "name": a_elements[last_button_index]['href']
                    }
                    return std_data
                else:
                    # В случае отсутствия кнопок, возвращаем None или другое значение по умолчанию
                    return None


async def Jornal(user_id, id):
    cookies = await AuthVer1.Authorization(user_id)
    if cookies is not False:
        jornal = await get_jornal(cookies, user_id, id)
        return jornal
    else:
        cookies = await AuthVer2.Authorization(user_id)
        if cookies is not False:
            jornal = await get_jornal(cookies, user_id, id)
            return jornal
        else:
            return False
