import aiohttp
from bs4 import BeautifulSoup
from aiogram import types
from univer20 import AuthVer2, AuthVer1
from univer20.Language.LangChange import HTTPHeaders
from univer20.Language.Set_language import set_lang


async def get_practics_info(cookies, user_id):
    headers = HTTPHeaders(user_id, user_id, user_id, user_id, user_id)
    async with aiohttp.ClientSession(cookies=cookies) as session:
        language = await set_lang(user_id)
        async with session.get("https://univer.kstu.kz/student/practik/indexlist/", headers=headers.Language(language)) as response:
            if response.status == 200:
                soup = BeautifulSoup(await response.text(), "html.parser")
                table_elements = soup.find_all("table", class_="inner")
                th_elements = []
                td_elements = []
                for table in table_elements:
                    th_elements.extend(table.find_all("th"))
                for table in table_elements:
                    wewe = table.find_all("tr", class_="link")
                    for row in wewe:
                        td_elements = row.find_all("td")

                nmb_gr = th_elements[0].text.strip()
                periud = th_elements[2].text.strip()
                maneger = th_elements[3].text.strip()
                organ = th_elements[4].text.strip()

                nmb_gr1 = td_elements[0].text.strip()
                periud1 = td_elements[2].text.strip()
                maneger1 = td_elements[3].text.strip()
                organ1 = td_elements[4].text.strip()
                prct_data = {
                    "nmb_gr": nmb_gr,
                    "periud": periud,
                    "maneger": maneger,
                    "organ": organ,

                    "nmb_gr1": nmb_gr1,
                    "periud1": periud1,
                    "maneger1": maneger1,
                    "organ1": organ1,
                }
                print(prct_data)
                return prct_data




async def Practics(user_id):
    cookies = await AuthVer1.Authorization(user_id)
    if cookies is not False:
        std_data = await get_practics_info(cookies, user_id)
        return std_data
    else:
        cookies = await AuthVer2.Authorization(user_id)
        if cookies is not False:
            std_data = await get_practics_info(cookies, user_id)
            return std_data
        else:
            return None