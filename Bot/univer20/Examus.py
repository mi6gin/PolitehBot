import aiohttp
from aiogram import types
from bs4 import BeautifulSoup
from univer20.Language.Set_language import set_lang
from univer20.Language.LangChange import HTTPHeaders
from univer20 import AuthVer2, AuthVer1

async def get_examus(cookies, message: types.Message, user_id):
    headers = HTTPHeaders(user_id, user_id, user_id, user_id, user_id)
    async with aiohttp.ClientSession(cookies=cookies) as session:
        language = await set_lang(user_id)
        async with session.get("https://univer.kstu.kz/student/myexam/schedule/", headers=headers.Language(language)) as response:
            if response.status == 200:
                soup = BeautifulSoup(await response.text(), "html.parser")

                # Найдем все строки таблицы с данными об экзаменах
                exam_rows = soup.find_all("tr", class_="link")

                exam_info_list = []

                for row in exam_rows:
                    # Извлечение данных из каждой строки
                    subject = row.find("td").text.strip()
                    teacher = row.find_all("td")[1].text.strip()
                    date_and_time = row["id"]  # Получаем дату и время из атрибута id
                    date, time = date_and_time.split(" ")

                    date = date.replace(".", "-")  # Преобразуем формат даты
                    time = time.split(":")[0]  # Берем только часы

                    date_time = f"{date} {time}:00"  # Создаем строку с полным временем

                    location = row.find_all("td")[3].text.strip().split("|")[1].strip()

                    # Добавляем извлеченные данные в список
                    exam_info_list.append({
                        "subject": subject,
                        "teacher": teacher,
                        "date_time": date_time,
                        "location": location
                    })

                print(exam_info_list)
                return exam_info_list
            else:
                print("Ошибка получения информации об экзаменах")
                cookies = await AuthVer2.Authorization(user_id)
                if cookies is not False:
                    examus = await get_examus(cookies, message, user_id)
                    return examus

async def Examus(message: types.Message, user_id):
    cookies = await AuthVer1.Authorization(user_id)
    if cookies is not False:
        examus = await get_examus(cookies, message, user_id)
        return examus
    else:
        cookies = await AuthVer2.Authorization(user_id)
        if cookies is not False:
            examus = await get_examus(cookies, message, user_id)
            return examus
        else:
            return False
