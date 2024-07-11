import json
from bs4 import Tag

from io import BytesIO, StringIO

import aiohttp
from aiogram.types import BufferedInputFile
from bs4 import BeautifulSoup

from settings import bot
from univer20 import AuthVer2, AuthVer1
from univer20.Language.LangChange import HTTPHeaders
from univer20.Language.Set_language import set_lang
from weasyprint import HTML, CSS

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
        async with session.get(f"https://univer.kstu.kz/advicer/students/", headers=headers.Language(language)) as response:
            if response.status == 200:
                soup = BeautifulSoup(await response.text(), 'html.parser')
                # Находим все теги <a> внутри таблицы

                table_elements = soup.find_all("table", class_="mt")

                # Создаем список для хранения найденных элементов <a>
                a_elements = []

                # Проходимся по каждой найденной таблице
                for table in table_elements:
                    # Находим все элементы <td> с классом "ts" внутри текущей таблицы
                    td_elements = table.find_all("tr", class_="top")

                    # Проходимся по каждому найденному элементу <td>
                    for td in td_elements:
                        # Находим все теги <a> внутри текущего элемента <td>
                        a_elements.extend(td.find_all("a", target="_blank"))

                num_buttons = len(a_elements)

                # Если есть кнопки, берем ссылку с последней кнопки
                if num_buttons > 0:
                    last_button_index = num_buttons - 1
                    std_data = {
                        "name": a_elements[last_button_index]['href']
                    }
                    await get_print_info(cookies, user_id, std_data["name"])
                else:
                    # В случае отсутствия кнопок, возвращаем None или другое значение по умолчанию
                    return None


async def get_print_info(cookies, user_id, id):
    headers = HTTPHeaders(user_id, user_id, user_id, user_id, user_id)
    async with aiohttp.ClientSession(cookies=cookies) as session:
        language = await set_lang(user_id)
        async with session.get(f"https://univer.kstu.kz{id}", headers=headers.Language(language)) as response:
            if response.status == 200:
                soup = BeautifulSoup(await response.text(), "html.parser")
                # Получаем HTML-контент из запроса
                html_content = str(soup)

                # Добавляем стили для контроля размера шрифта


                # Используем StringIO для создания временного объекта для записи данных в строку
                string_io = StringIO()
                # Записываем HTML-контент в StringIO объект с добавленными стилями
                string_io.write(html_content)
                # Получаем байтовое представление строки
                bytes_io = BytesIO(string_io.getvalue().encode())

                # Создаем PDF из байтового представления
                pdf_document = HTML(bytes_io).write_pdf(
                    stylesheets=[CSS(string='@page { size: A3; margin: 2cm; }')],
                    presentational_hints=True
                )
                file = BufferedInputFile(pdf_document, filename='Students.pdf')
                await bot.send_document(user_id, file)


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
