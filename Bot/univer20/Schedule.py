import aiohttp
from aiogram import types
from bs4 import BeautifulSoup
from univer20.Language.LangChange import HTTPHeaders
from univer20.Language.Set_language import set_lang
from univer20 import AuthVer2, AuthVer1


async def get_schedule(cookies, message: types.Message, user_id):
    headers = HTTPHeaders(user_id, user_id, user_id, user_id, user_id)
    async with aiohttp.ClientSession(cookies=cookies) as session:
        language = await set_lang(user_id)
        async with session.get("https://univer.kstu.kz/student/myschedule/2023/2/22.01.2024/28.01.2024/", headers=headers.Language(language)) as response:
            if response.status == 200:
                schedule_data = {}
                soup = BeautifulSoup(await response.text(), "html.parser")
                table_elements = soup.find_all("table", class_="schedule")  # Находим все таблицы расписания

                for table in table_elements:
                    rows = table.find_all("tr")  # Находим все строки таблицы
                    header_row = rows[0]  # Получаем строку с заголовками дней недели
                    days = [cell.text.strip() for cell in header_row.find_all("th")[1:]]  # Получаем список дней недели, пропуская первую ячейку
                    cells_by_day = list(zip(*[row.find_all("td")[1:] for row in rows[1:]]))  # Группируем ячейки по дням недели, пропуская первую ячейку каждой строки

                    for day, cells in zip(days, cells_by_day):
                        schedule_data[day] = {}

                        for cell in cells:
                            groups = cell.find_all("div", class_="groups")
                            for group in groups:
                                time = group.find_previous("td", class_="time").text.strip()
                                # Найдем все div внутри блока groups
                                lessons = group.find_all("div")
                                for lesson in lessons:
                                    # Извлечем необходимую информацию из каждого занятия
                                    course = lesson.find("p", class_="teacher").text.strip()
                                    instructor = lesson.select_one("p.teacher ~ p.teacher").text.strip()
                                    location = lesson.select_one("span.aud_faculty + span").text.strip()
                                    denominator_tag = lesson.find("span", class_="denominator")
                                    denominator = denominator_tag.text.strip() if denominator_tag else "Каждая неделя"
                                    # Добавляем данные в расписание
                                    schedule_data[day][course] = {
                                        "time": time,
                                        "type": course.split("(")[1][:-1],
                                        "instructor": instructor,
                                        "location": location,
                                        "denominator": denominator,
                                    }

                return schedule_data
            else:
                print("Ошибка получения информации о пользователе")
                cookies = await AuthVer2.Authorization(user_id)
                if cookies is not False:
                    schedule = await get_schedule(cookies, message, user_id)
                    return schedule

async def Schedule(message: types.Message, user_id):
    cookies = await AuthVer1.Authorization(user_id)
    if cookies is not False:
        schedule = await get_schedule(cookies, message, user_id)
        return schedule
    else:
        cookies = await AuthVer2.Authorization(user_id)
        if cookies is not False:
            schedule = await get_schedule(cookies, message, user_id)
            return schedule
        else:
            return None  # Возвращаем None в случае неудачной авторизации
