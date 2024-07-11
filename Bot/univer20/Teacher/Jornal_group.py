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
        async with session.get("https://univer.kstu.kz/teacher/attendance/index/", headers=headers.Language(language)) as response:
            if response.status == 200:
                soup = BeautifulSoup(await response.text(), 'html.parser')
                target_element = soup.find('a', {'id': f'{id}'})
                files = []

                # Если элемент найден
                if target_element:
                    # Находим таблицу, содержащую нужные данные
                    table = target_element.find_next('table', class_='inner')

                    # Если таблица найдена
                    if table:
                        # Находим все строки таблицы, кроме заголовка
                        rows = table.find_all('tr')[1:]

                        # Проходимся по каждой строке
                        for row in rows:

                            third_td = row.find_all('td')[2]
                            # Находим ссылку внутри ячейки
                            link = row.find('a')
                            # Если ссылка найдена
                            if link:
                                # Получаем текст ссылки и значение атрибута href
                                text = link.get_text(strip=True)
                                third_td = third_td.get_text(strip=True)
                                href = link['href']
                                print("Текст:", text)
                                print("Ссылка:", href)
                                files.append({"name": text[7:]+" "+third_td, "url": href})
                                print(files)

                # Перемещаем эту строку внутрь условия, чтобы она выполнялась только после прохода по всем строкам
                return files

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
