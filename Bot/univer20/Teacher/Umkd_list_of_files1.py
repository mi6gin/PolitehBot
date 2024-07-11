import aiohttp
import requests
from aiogram import types
from aiogram.types import BufferedInputFile
from bs4 import BeautifulSoup

from univer20 import AuthVer2, AuthVer1


async def get_umkd_list_of_files(cookies, message: types.Message, user_id, teacher_number, id):
    session = requests.session()
    session.cookies.update(cookies)
    async with aiohttp.ClientSession(cookies=cookies) as session:
        async with session.get(f'https://univer.kstu.kz/teacher/umkdpack/edit/{id}/2023/2') as response:
            if response.status == 200:
                files = []
                soup = BeautifulSoup(await response.text(), "html.parser")

                # Определяем индекс тега <tr class="mid"> в зависимости от teacher_number
                index = (int(teacher_number) - 1) * 2

                # Находим все теги <tr class="mid">
                mid_rows = soup.find_all('tr', class_='mid')

                # Выбираем только те теги <tr class="mid">, которые не находятся внутри тегов <td class="tt">
                relevant_mid = [row for row in mid_rows if not row.find_parents('td', class_='tt')]

                # Извлекаем информацию о файле из нужного тега <tr class="mid">
                if index < len(relevant_mid):
                    relevant_row = relevant_mid[index]
                    # Находим ссылку на скачивание внутри выбранного тега <tr class="mid">
                    download_link = relevant_row.find('a', class_='downLoad')
                    if download_link:
                        file_id = download_link['href']  # id файла
                        # Находим тег <i> с названием файла
                        file_name_tag = relevant_row.find('i')
                        if file_name_tag:
                            file_name = file_name_tag.get_text(strip=True)  # Название файла
                            # Добавляем информацию о файле в список
                            files.append({"id": file_id, "name": file_name})
                            print(files)
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
