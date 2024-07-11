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
        async with session.get("https://univer.kstu.kz/teacher/sheet/list/", headers=headers.Language(language)) as response:
            if response.status == 200:
                soup = BeautifulSoup(await response.text(), 'html.parser')
                files = []
                outer_table = soup.find('table', class_='mt')

                # Если внешняя таблица найдена, ищем в ней внутреннюю таблицу с классом "inner"
                if outer_table:
                    inner_table = outer_table.find('table', class_='inner')

                    # Если внутренняя таблица найдена, ищем все элементы tr внутри нее
                    if inner_table:
                        tr_elements = inner_table.find_all('tr')

                        # Проходимся по каждому элементу tr
                        for tr in tr_elements:
                            # Найдем все ячейки <td> в текущем элементе tr
                            td_elements = tr.find_all('td')

                            # Проверяем, что есть хотя бы две ячейки
                            if len(td_elements) >= 2:
                                # Получаем текст из второй ячейки <td> (индекс 1) внутри <b></b>
                                td_text = td_elements[2].find('b').get_text(strip=True)+"-"+td_elements[3].get_text(strip=True)

                                # Получаем id элемента
                                tr_id = tr.get('id')

                                # Проверяем, что id не равен None, и только тогда выводим информацию
                                if tr_id is not None:
                                    files.append({'name': td_text[8:], 'id': tr_id})

                        return files
                    else:
                        print("Внутренняя таблица не найдена.")
                else:
                    print("Внешняя таблица не найдена.")

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
