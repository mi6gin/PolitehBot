import json
from bs4 import Tag


import aiohttp
from aiogram import types
from bs4 import BeautifulSoup
from univer20.Language.LangChange import HTTPHeaders
from univer20.Language.Set_language import set_lang
from univer20 import AuthVer2, AuthVer1


async def get_jornal(cookies, user_id):
    headers = HTTPHeaders(user_id, user_id, user_id, user_id, user_id)
    async with aiohttp.ClientSession(cookies=cookies) as session:
        language = await set_lang(user_id)
        async with session.get("https://univer.kstu.kz/teacher/attendance/index/", headers=headers.Language(language)) as response:
            if response.status == 200:
                soup = BeautifulSoup(await response.text(), 'html.parser')
                files = []  # Создаем список для хранения словарей с данными

                # Находим все элементы <tr> с классом "brk"
                brk_rows = soup.find_all('tr', class_='brk')

                # Проходим по каждому элементу и извлекаем id и текст ссылки
                for row in brk_rows:
                    a_tag = row.find('a', class_='hider')
                    if a_tag:
                        tag_id = a_tag.get('id')
                        tag_text = a_tag.get_text().strip()
                        # Проверяем, что в названии отсутствуют слова "практика" или "practice"
                        if 'практика' not in tag_text.lower() and 'practice' not in tag_text.lower():
                            files.append(
                                {"id": tag_id, "name": tag_text[3:]})  # Добавляем id и название в список в виде словаря

                return files

async def Jornal(user_id):
    cookies = await AuthVer1.Authorization(user_id)
    if cookies is not False:
        jornal = await get_jornal(cookies, user_id)
        return jornal
    else:
        cookies = await AuthVer2.Authorization(user_id)
        if cookies is not False:
            jornal = await get_jornal(cookies, user_id)
            return jornal
        else:
            return False
