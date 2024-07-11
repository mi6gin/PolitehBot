import aiohttp
import requests
from aiogram import types
from aiogram.fsm.context import FSMContext
from aiogram.types import BufferedInputFile
from bs4 import BeautifulSoup

from settings import bot
from univer20 import AuthVer2, AuthVer1


async def get_umkd_download_file(cookies, message: types.Message, user_id, file_id):
    session = requests.session()
    session.cookies.update(cookies)
    async with aiohttp.ClientSession(cookies=cookies) as session:
        async with session.get(f'https://univer.kstu.kz/teacher{file_id}') as response:
            if response.status == 200:
                content = await response.read()
                file = BufferedInputFile(content, filename='Unknow.pdf')
                from settings import bot
                await bot.send_document(user_id, file)

async def Umkd_download(message: types.Message, user_id, file_id):
    cookies = await AuthVer1.Authorization(user_id)
    if cookies is not False:
        umkd = await get_umkd_download_file(cookies, message, user_id, file_id)
        return umkd
    else:
        cookies = await AuthVer2.Authorization(user_id)
        if cookies is not False:
            umkd = await get_umkd_download_file(cookies, message, user_id, file_id)
            return umkd
        else:
            return None  # Возвращаем None в случае неудачной авторизации
