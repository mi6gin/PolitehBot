import aiohttp
import requests
from aiogram import types
from aiogram.fsm.context import FSMContext
from aiogram.types import BufferedInputFile
from bs4 import BeautifulSoup

from settings import bot
from univer20 import AuthVer2, AuthVer1


async def get_umkd_get_name(cookies, message: types.Message, user_id, id, num, state: FSMContext):
    session = requests.session()
    session.cookies.update(cookies)
    async with aiohttp.ClientSession(cookies=cookies) as session:
        async with session.get(f'https://univer.kstu.kz/student/umkd/{num}') as response:
            if response.status == 200:

                soup = BeautifulSoup(await response.text(), "html.parser")
                files = []
                file_rows = soup.find_all('tr', class_='file')
                desired_id = id
                for row in file_rows:
                    file_id = int(row.get('id'))
                    if file_id == desired_id:
                        file_name = row.find('td', style='overflow: hidden').find('a').get_text(strip=True)
                        files.append({"name": file_name})  # Добавляем id и имя файла в виде словаря
                        for file in files:
                            name = file['name']
                            await get_umkd_download_file(cookies, message, user_id, id, num, name, state)
            else:
                print("Ошибка при получении списка файлов")
                cookies = await AuthVer2.Authorization(user_id)
                if cookies is not False:
                    umkd = await get_umkd_get_name(cookies, message, user_id, id, num, state)
                    return umkd

async def get_umkd_download_file(cookies, message: types.Message, user_id, id, num, name, state: FSMContext):
    session = requests.session()
    session.cookies.update(cookies)
    async with aiohttp.ClientSession(cookies=cookies) as session:
        async with session.get(f'https://univer.kstu.kz/student/umkd/get/{id}/{num}') as response:
            if response.status == 200:
                data = await state.get_data()
                message_to_delete = data.get('message_to_delete')
                await message_to_delete.delete()
                content = await response.read()
                file = BufferedInputFile(content, filename=name)
                await bot.send_document(user_id, file)
            else:
                print("Ошибка при получении списка файлов")
                cookies = await AuthVer2.Authorization(user_id)
                if cookies is not False:
                    umkd = await get_umkd_get_name(cookies, message, user_id, id, num, state)
                    return umkd

async def Umkd_download(message: types.Message, user_id, id, num, state: FSMContext):
    cookies = await AuthVer1.Authorization(user_id)
    if cookies is not False:
        umkd = await get_umkd_get_name(cookies, message, user_id, id, num, state)
        return umkd
    else:
        cookies = await AuthVer2.Authorization(user_id)
        if cookies is not False:
            umkd = await get_umkd_get_name(cookies, message, user_id, id, num, state)
            return umkd
        else:
            return None  # Возвращаем None в случае неудачной авторизации
