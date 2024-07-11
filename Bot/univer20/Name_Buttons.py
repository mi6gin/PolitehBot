import aiohttp
from bs4 import BeautifulSoup
from aiogram import types
from univer20 import AuthVer2, AuthVer1
from univer20.Language.LangChange import HTTPHeaders
from univer20.Language.Set_language import set_lang


async def get_btn_info(cookies, user_id):
    headers = HTTPHeaders(user_id, user_id, user_id, user_id, user_id)
    async with aiohttp.ClientSession(cookies=cookies) as session:
        language = await set_lang(user_id)
        async with session.get("https://univer.kstu.kz/student/advicer/", headers=headers.Language(language)) as response:
            if response.status == 200:
                soup = BeautifulSoup(await response.text(), "html.parser")
                table_elements = soup.find_all("table", class_="tool")  # заменяем find() на find_all()
                td_elements = []

                table_elements1 = soup.find_all("table", class_="tool")  # заменяем find() на find_all()
                td_elements1 = []

                # Проходимся по всем найденным таблицам и добавляем ссылки из них в список td_elements
                for table in table_elements:
                    td_elements.extend(table.find_all("a"))

                for table in table_elements1:
                    td_elements1.extend(table.find_all("td", class_="bottom-center"))

                btn_1 = td_elements[5].text.strip()
                btn_2 = td_elements[6].text.strip()
                btn_3 = td_elements[10].text.strip()
                btn_4 = td_elements[16].text.strip()
                btn_5 = td_elements1[1].text.strip()
                btn_6 = td_elements[2].text.strip()
                btn7 = td_elements[3].text.strip()
                btn8 = td_elements[8].text.strip()
                btn9 = td_elements[13].text.strip()
                btn10 = td_elements[4].text.strip()
                btn11 = td_elements[12].text.strip()
                std_data = {
                    "dst": btn_5,
                    "shl": btn_1,
                    "shlex": btn_2,
                    "jornal": btn_3,
                    "umkd": btn_4,
                    "pract": btn_6,
                    "adviser": btn7,
                    "plan": btn8,
                    "trans": btn9,
                    "calendar": btn10,
                    "userplan": btn11
                }
                print(std_data)
                return std_data


            else:
                print("Ошибка получения информации о пользователе")
                cookies = await AuthVer2.Authorization(user_id)
                if cookies is not False:
                    user = await get_btn_info(cookies, user_id)
                    return user

async def Btn(user_id):
    cookies = await AuthVer1.Authorization(user_id)
    if cookies is not False:
        std_data = await get_btn_info(cookies, user_id)
        return std_data
    else:
        cookies = await AuthVer2.Authorization(user_id)
        if cookies is not False:
            std_data = await get_btn_info(cookies, user_id)
            return std_data
        else:
            return None