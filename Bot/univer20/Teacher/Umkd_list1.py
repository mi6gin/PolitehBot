import aiohttp
import requests
from aiogram import types
from bs4 import BeautifulSoup

from univer20 import AuthVer2, AuthVer1


async def get_umkd_download(cookies, message: types.Message, user_id, id):
    session = requests.session()
    session.cookies.update(cookies)
    async with aiohttp.ClientSession(cookies=cookies) as session:
        async with session.get(f'https://univer.kstu.kz/teacher/umkdpack/edit/{user_id}/2023/2') as response:
            if response.status == 200:
                soup = BeautifulSoup(await response.text(), "html.parser")
                teacher_rows = soup.find_all('tr', class_='brk')
                if teacher_rows:
                    teachers = []  # Список для хранения преподавателей
                    for teacher_row in teacher_rows:
                        teacher_name_element = teacher_row.find('b', style="float:left; text-align:right;")
                        if teacher_name_element:
                            teacher_name = teacher_name_element.get_text(strip=True).replace('Преподаватель:', '')
                            teachers.append(teacher_name)
                        else:
                            print("Преподаватель не найден")
                    if len(teachers) > 0:
                        return teachers  # Возвращаем список преподавателей
                    else:
                        return ['нет данных']  # Возвращаем массив с одним элементом 'нет данных'
                else:
                    return ['нет данных']
            else:
                print("Ошибка получения информации о пользователе")
                cookies = await AuthVer2.Authorization(id)
                if cookies is not False:
                    discipline_id = await get_umkd_download(cookies, message, user_id, id)
                    return discipline_id
                else:
                    return None


async def Umkd_download(message: types.Message, user_id, id):
    cookies = await AuthVer1.Authorization(id)
    if cookies is not False:
        umkd = await get_umkd_download(cookies, message, user_id, id)
        return umkd
    else:
        cookies = await AuthVer2.Authorization(user_id)
        if cookies is not False:
            umkd = await get_umkd_download(cookies, message, user_id, id)
            return umkd
        else:
            return None  # Возвращаем None в случае неудачной авторизации
