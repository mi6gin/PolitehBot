import aiohttp
from bs4 import BeautifulSoup
from aiogram import types
from univer20 import AuthVer2, AuthVer1
from univer20.Language.LangChange import HTTPHeaders
from univer20.Language.Set_language import set_lang


async def get_userplan_info(cookies, user_id):
    headers = HTTPHeaders(user_id, user_id, user_id, user_id, user_id)
    async with aiohttp.ClientSession(cookies=cookies) as session:
        language = await set_lang(user_id)
        async with session.get("https://univer.kstu.kz/student/iup/0", headers=headers.Language(language)) as response:
            if response.status == 200:
                soup = BeautifulSoup(await response.text(), "html.parser")
                br_tags = soup.find_all('br')  # Найти все теги <br>
                if len(br_tags) >= 2:  # Проверить, что есть хотя бы два <br>
                    second_br = br_tags[1]  # Второй тег <br>
                    # Ищем все <a> после второго <br>
                    a_tags = second_br.find_all_next('a')
                    tag_data = []  # Создаем список для хранения данных тегов <a>
                    for a_tag in a_tags:
                        tag_data.append(a_tag.text)  # Добавляем текст тега <a> в список tag_data
                    print(tag_data)
                    return tag_data
            else:
                print("Ошибка получения информации о пользователе")
                cookies = await AuthVer2.Authorization(user_id)
                if cookies is not False:
                    user = await get_userplan_info(cookies, user_id)
                    return user

async def UserPlan(user_id):
    cookies = await AuthVer1.Authorization(user_id)
    if cookies is not False:
        std_data = await get_userplan_info(cookies, user_id)
        return std_data
    else:
        cookies = await AuthVer2.Authorization(user_id)
        if cookies is not False:
            std_data = await get_userplan_info(cookies, user_id)
            return std_data
        else:
            return None