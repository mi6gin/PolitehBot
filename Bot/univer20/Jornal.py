import json
from bs4 import Tag


import aiohttp
from aiogram import types
from bs4 import BeautifulSoup
from univer20.Language.LangChange import HTTPHeaders
from univer20.Language.Set_language import set_lang
from univer20 import AuthVer2, AuthVer1


async def get_jornal(cookies, message: types.Message, user_id):
    headers = HTTPHeaders(user_id, user_id, user_id, user_id, user_id)
    async with aiohttp.ClientSession(cookies=cookies) as session:
        language = await set_lang(user_id)
        async with session.get("http://univer.kstu.kz/student/attendance/full/", headers=headers.Language(language)) as response:
            if response.status == 200:

                serialized_journal = {}
                soup = BeautifulSoup(await response.text(), "html.parser")
                links = soup.find_all("a")
                # print(links)

                table_with_notes = None
                for l in links:
                    if l["href"].startswith("/student/attendance/show/"):
                        table_with_notes = l.parent.parent.parent
                        break

                if not table_with_notes:
                    raise ValueError("couldnt found table with notes")

                subjects = {}
                current_subject_name = ""
                current_subject_type = ""
                current_rk = ""
                for row in list(table_with_notes.children):
                    if type(row) is Tag and row.has_attr("class") and "top" in row["class"]:
                        current_subject_name = row.find_all(class_="ct")[0].text.strip()
                        subjects[current_subject_name] = {}
                        continue

                    if type(row) is Tag and len(links := row.find_all("a")) > 0:
                        current_subject_type = links[0].text.strip()
                        subjects[current_subject_name][current_subject_type] = {}
                        continue

                    if not row.text.strip():
                        continue

                    if len(trs := row.find_all("tr")) > 0:
                        current_rk = trs[0].find_all("th")[0].text
                        subjects[current_subject_name][current_subject_type][
                            current_rk
                        ] = {}

                        dates = list(
                            map(lambda x: x.text, list(trs[0].find_all("th"))[1:-2])
                        )
                        for i, note_tag in enumerate(list(trs[1].find_all("td")[:-2])):
                            note = note_tag.text
                            if not note_tag.text == "н":
                                note = int(note_tag.text)

                            subjects[current_subject_name][current_subject_type][
                                current_rk
                            ][dates[i]] = note
                first_key = next(iter(subjects))
                subjects.pop(first_key)
                # Сериализация в JSON и вывод
                serialized_journal = json.dumps(subjects, ensure_ascii=False, indent=2)
                print(serialized_journal)
                return serialized_journal



async def Jornal(message: types.Message, user_id):
    cookies = await AuthVer1.Authorization(user_id)
    if cookies is not False:
        jornal = await get_jornal(cookies, message, user_id)
        return jornal
    else:
        cookies = await AuthVer2.Authorization(user_id)
        if cookies is not False:
            jornal = await get_jornal(cookies, message, user_id)
            return jornal
        else:
            return False
