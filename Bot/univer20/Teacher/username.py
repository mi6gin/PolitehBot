import aiohttp
from bs4 import BeautifulSoup
from aiogram import types
from univer20 import AuthVer2, AuthVer1
from univer20.Language.LangChange import HTTPHeaders
from univer20.Language.Set_language import set_lang


async def get_user_info(cookies, message: types.Message, user_id):
    headers = HTTPHeaders(user_id, user_id, user_id, user_id, user_id)
    async with aiohttp.ClientSession(cookies=cookies) as session:
        language = await set_lang(user_id)
        async with session.get("https://univer.kstu.kz/teacher/", headers=headers.Language(language)) as response:
            if response.status == 200:
                soup = BeautifulSoup(await response.text(), "html.parser")
                table = soup.find("table", class_="mt")
                ul_tags = table.find_all("td", class_="ct")
                text = "\n".join([ul.get_text(strip=True) for ul in ul_tags])

                phrases_to_remove = [
                    "Если эти данные ошибочны, обратитесь в отдел сопровождения.",
                    "Вы находитесь", "на главной", "странице", "вкладки", "\"Преподаватель\"",
                    "Егер бұл мәлiметтер қате болса, бағдарламаларды қолдау бөлiмiне хабарласыңыз.",
                    "Сіз қойындының негізгі бетіндесіз.", "Сіздің рөліңіз: \"Оқытушы\"",
                    "If this data is invalid, speak to support department",
                    "You are on the main", "page of the", "tab", "\"Teacher\"",
                    "Преподаватель",
                    "Оқытушы",
                    "Faculty member",
                    "\"\""
                ]

                for phrase in phrases_to_remove:
                    text = text.replace(phrase, "")

                formatted_text = text.strip()

                # Удаляем все пробелы перед каждым символом новой строки
                text = "\n".join(line.strip() for line in formatted_text.split("\n"))

                std_data = {
                    "spc": text,
                }
                return std_data

            else:
                print("Ошибка получения информации о пользователе")
                cookies = await AuthVer2.Authorization(user_id)
                if cookies is not False:
                    user = await get_user_info(cookies, message, user_id)
                    return user

async def Username(message: types.Message, user_id):
    cookies = await AuthVer1.Authorization(user_id)
    if cookies is not False:
        std_data = await get_user_info(cookies, message, user_id)
        return std_data
    else:
        cookies = await AuthVer2.Authorization(user_id)
        if cookies is not False:
            std_data = await get_user_info(cookies, message, user_id)
            return std_data
        else:
            return None