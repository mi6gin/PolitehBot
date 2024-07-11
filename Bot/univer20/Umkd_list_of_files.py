import aiohttp
import requests
from aiogram import types
from bs4 import BeautifulSoup

from univer20 import AuthVer2, AuthVer1


async def get_umkd_list_of_files(cookies, message: types.Message, user_id, teacher_number, id):
    session = requests.session()
    session.cookies.update(cookies)
    async with aiohttp.ClientSession(cookies=cookies) as session:
        async with session.get(f'https://univer.kstu.kz/student/umkd/{id}') as response:
            if response.status == 200:
                files = []
                soup = BeautifulSoup(await response.text(), "html.parser")
                professor_rows = soup.find_all('tr', class_='brk')
                if teacher_number == "1" and professor_rows:
                    professor_row = professor_rows[0]
                elif teacher_number == "2" and len(professor_rows) > 1:
                    professor_row = professor_rows[1]
                else:
                    print("Некорректное значение id для преподавателя")
                    return []

                professor_name = professor_row.find('td', class_='ct').get_text(strip=True)
                mt_table = soup.find_all('table', class_='mt')
                if mt_table:
                    brk_row = mt_table[1].find('tr', class_='brk') if mt_table else None
                    if brk_row:
                        mid_rows = mt_table[1].find_all('tr', class_='mid')
                        # Остальной код остается неизменным

                        # Ищем нужные "mid" в зависимости от значения teacher_number
                        if teacher_number == "1" and len(mid_rows) >= 2:
                            relevant_mid = mid_rows[1]  # Второй по порядку "mid"
                        elif teacher_number == "2" and len(mid_rows) >= 4:
                            relevant_mid = mid_rows[3]  # Четвертый по порядку "mid"
                        else:
                            print("Некорректное значение teacher_number")
                            return []

                        file_rows = relevant_mid.find_all('tr', class_='file')

                        for row in file_rows:
                            file_id = row.get('id')  # Получаем значение атрибута id
                            file_name = row.find('td', style='overflow: hidden').find('a').get_text(strip=True)
                            files.append({"id": file_id, "name": file_name})  # Добавляем id и имя файла в виде словаря
                        return files

            else:
                print("Ошибка при получении списка файлов")
                cookies = await AuthVer2.Authorization(user_id)
                if cookies is not False:
                    umkd = await get_umkd_list_of_files(cookies, message, user_id, teacher_number, id)
                    return umkd

async def Umkd_list_of_files(message: types.Message, user_id, teacher_number, id):
    cookies = await AuthVer1.Authorization(user_id)
    if cookies is not False:
        umkd = await get_umkd_list_of_files(cookies, message, user_id, teacher_number, id)
        return umkd
    else:
        cookies = await AuthVer2.Authorization(user_id)
        if cookies is not False:
            umkd = await get_umkd_list_of_files(cookies, message, user_id, teacher_number, id)
            return umkd
        else:
            return None  # Возвращаем None в случае неудачной авторизации
