import re
from io import BytesIO, StringIO

import aiohttp
from aiogram.types import BufferedInputFile
from bs4 import BeautifulSoup

from settings import bot
from univer20 import AuthVer2, AuthVer1
from univer20.Language.LangChange import HTTPHeaders
from univer20.Language.Set_language import set_lang
from weasyprint import HTML, CSS


async def get_calendar_info(cookies, user_id):
    headers = HTTPHeaders(user_id, user_id, user_id, user_id, user_id)
    async with aiohttp.ClientSession(cookies=cookies) as session:
        language = await set_lang(user_id)
        async with session.get("https://univer.kstu.kz/student/academcalendar/",
                               headers=headers.Language(language)) as response:
            if response.status == 200:
                soup = BeautifulSoup(await response.text(), "html.parser")

                # Исключаем таблицы с классом "tools"
                tables_to_exclude = soup.find_all('table', class_='tool')
                for table in tables_to_exclude:
                    table.extract()
                divs_to_exclude = soup.find_all('div', class_='links')
                for div in divs_to_exclude:
                    div.extract()

                td_elements_to_exclude = soup.find_all('td', class_='ct message')
                for td_element in td_elements_to_exclude:
                    td_element.extract()

                elements_to_exclude = soup.find_all(text=re.compile(r'[П]'))
                for element in elements_to_exclude:
                    element.extract()

                for row in soup.find_all('tr'):
                    links = row.find_all('a', href=lambda href: href and (
                                "/" in href or "/student/bachelor/" in href or "/ssc/" in href))
                    if links:
                        row.extract()
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
                file = BufferedInputFile(pdf_document, filename='academcalendar.pdf')
                await bot.send_document(user_id, file)
            else:
                print("Ошибка получения информации о пользователе")
                cookies = await AuthVer2.Authorization(user_id)
                if cookies is not False:
                    user = await get_calendar_info(cookies, user_id)
                    return user


async def Calendar(user_id):
    cookies = await AuthVer1.Authorization(user_id)
    if cookies is not False:
        std_data = await get_calendar_info(cookies, user_id)
        return std_data
    else:
        cookies = await AuthVer2.Authorization(user_id)
        if cookies is not False:
            std_data = await get_calendar_info(cookies, user_id)
            return std_data
        else:
            return None
