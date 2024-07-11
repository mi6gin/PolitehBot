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
        async with session.get("https://univer.kstu.kz/teacher/practik/index/", headers=headers.Language(language)) as response:
            if response.status == 200:
                soup = BeautifulSoup(await response.text(), 'html.parser')

                mt_tables = soup.find_all('table', class_='mt')

                # Проверяем, что найдено хотя бы две таблицы с классом 'mt'
                if len(mt_tables) >= 2:
                    # Выбираем вторую таблицу (индекс 1, так как индексация начинается с 0)
                    second_mt_table = mt_tables[1]

                    # Находим все теги <td> с классом 'brk' во второй таблице 'mt'
                    brk_td_tags = second_mt_table.find_all('tr', class_='top')[1]

                    # Создаем список для хранения результатов
                    files = []

                    # Перебираем найденные теги
                    for index, brk_td in enumerate(brk_td_tags):
                        # Извлекаем текст из тега
                        brk_text = brk_td.get_text(strip=True)
                        # Проверяем, что текст не пустой
                        if brk_text:
                            # Добавляем текст и его положение в список результатов
                            files.append({'name': brk_text, 'id': index})

                    # Выводим результаты
                    for result in files:
                        print("Текст: ", result['name'])
                        print("Положение: ", result['id'])

                    return files
                else:
                    print("Найдено меньше двух таблиц с классом 'mt'.")


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
