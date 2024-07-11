from aiogram import types
from univer20 import Umkd_review, Umkd_list, Umkd_list_of_files, UserPlan_elements
from univer20 import Username, Deauth_name, Name_Buttons
from univer20.Teacher import BTN, Jornal_discipline, Jornal_group
from univer20.Teacher import Attendance_discipline, Attendance_group, Umkd_list1, Umkd_list_of_files1, Umkd_discipline1, stdBTN,Practika_discipline,Practika_group


def get_keyboard_language():
    buttons = [
        [
            types.InlineKeyboardButton(text="🇷🇺", callback_data="lang:ru"),
        ],
        [
            types.InlineKeyboardButton(text="🇰🇿", callback_data="lang:kz"),
        ],
        [
            types.InlineKeyboardButton(text="🇬🇧", callback_data="lang:en"),
        ],
    ]
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard
def get_keyboard_auth():
    buttons = [
        [
            types.InlineKeyboardButton(text="🆕", callback_data="sing in"),
        ],
        [
            types.InlineKeyboardButton(text="🇷🇺/🇰🇿/🇬🇧", callback_data="language"),
        ],
    ]
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard
async def get_keyboard_deauth(message: types.Message, user_id):
    btn = await Name_Buttons.Btn(user_id)
    deauth = await Deauth_name.Deauth(message, user_id)
    buttons = [
        [
            types.InlineKeyboardButton(text=f'{btn["dst"]}', callback_data="dscourse"),
        ],
        [
            types.InlineKeyboardButton(text="🇷🇺/🇰🇿/🇬🇧", callback_data="language"),
        ],
        [
            types.InlineKeyboardButton(text=f'{deauth["name"]}', callback_data="sing out"),
        ],
    ]
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard


async def get_keyboard_teacher(message: types.Message, user_id):
    btn = await BTN.Btn(user_id)
    deauth = await Deauth_name.Deauth(message, user_id)
    buttons = [
        [
            types.InlineKeyboardButton(text=f'{btn["dst"]}', callback_data="dscourse_tch"),
        ],
        [
            types.InlineKeyboardButton(text="🇷🇺/🇰🇿/🇬🇧", callback_data="language"),
        ],
        [
            types.InlineKeyboardButton(text=f'{deauth["name"]}', callback_data="sing out"),
        ],
    ]
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard


async def get_keyboard_distant(message: types.Message, user_id):
    btn = await Name_Buttons.Btn(user_id)
    buttons = [
        [
            types.InlineKeyboardButton(text=f'{btn["shl"]}', callback_data="grafics"),
        ],
        [
            types.InlineKeyboardButton(text=f'{btn["jornal"]}', callback_data="jornal"),
        ],
        [
            types.InlineKeyboardButton(text=f'{btn["umkd"]}', callback_data="umkd"),
        ],
        [
            types.InlineKeyboardButton(text=f'{btn["shlex"]}', callback_data="examus"),
        ],
        [
        types.InlineKeyboardButton(text=f'{btn["pract"]}', callback_data="pract"),
        ],
        [
            types.InlineKeyboardButton(text=f'{btn["adviser"]}', callback_data="adviser"),
        ],
        [
            types.InlineKeyboardButton(text=f'{btn["trans"]}', callback_data="trans"),
        ],
        [
            types.InlineKeyboardButton(text=f'{btn["plan"]}', callback_data="plan"),
        ],
        [
            types.InlineKeyboardButton(text=f'{btn["calendar"]}', callback_data="calendar"),
        ],
        [
            types.InlineKeyboardButton(text=f'{btn["userplan"]}', callback_data="userplan"),
        ],
    ]
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard


async def get_keyboard_distant_thcr(message: types.Message, user_id):
    btn = await BTN.Btn(user_id)
    btn1 = await stdBTN.Btn(user_id)
    buttons = [
        [
            types.InlineKeyboardButton(text=f'{btn["umkd"]}', callback_data="umkd_tch"),
        ],
        [
            types.InlineKeyboardButton(text=f'{btn["jornal"]}', callback_data="jornal_tch"),
        ],
        [
            types.InlineKeyboardButton(text=f'{btn["attest"]}', callback_data="attest"),
        ],
        [
            types.InlineKeyboardButton(text=f'{btn["shld"]}', callback_data="shld"),
        ],
        [
        types.InlineKeyboardButton(text=f'{btn["shldex"]}', callback_data="shldex"),
        ],
        [
            types.InlineKeyboardButton(text=f'{btn["practika"]}', callback_data="practika"),
        ],
        [
            types.InlineKeyboardButton(text=f'{btn1["std"]}', callback_data="spisok"),
        ],
    ]
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard

async def get_keyboard_jornal_dcp_thcr(callback: types.CallbackQuery, user_id):
    dcp = await Jornal_discipline.Jornal(user_id)
    buttons = []
    for item in dcp:
        button = types.InlineKeyboardButton(text=f"{item['name']}",
                                            callback_data=f"jornalTch:{str(item['id'])}")
        buttons.append([button])
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard

async def get_keyboard_jornal_dcp_thck(callback: types.CallbackQuery, user_id, id):
    dcp = await Jornal_group.Jornal(user_id, id)
    buttons = []
    for item in dcp:
        button = types.InlineKeyboardButton(text=f"{str(item['name'])}",
                                            callback_data=f"jornalTchk:{str(item['url'])}")
        buttons.append([button])
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard

async def get_keyboard_attendance_dcp_thcr(callback: types.CallbackQuery, user_id):
    dcp = await Attendance_discipline.Jornal(user_id)
    buttons = []
    for item in dcp:
        button = types.InlineKeyboardButton(text=f"{item['name']}",
                                            callback_data=f"attendanceTch:{str(item['id'])}")
        buttons.append([button])
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard

async def get_keyboard_attendance_dcp_thck(callback: types.CallbackQuery, user_id, id):
    dcp = await Attendance_group.Jornal(user_id, id)
    buttons = []
    for item in dcp:
        button = types.InlineKeyboardButton(text=f"{str(item['name'])}",
                                            callback_data=f"attendanceTchk:{str(item['id'])}")
        buttons.append([button])
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard


async def get_keyboard_attendance_dcp_thcr1(callback: types.CallbackQuery, user_id):
    dcp = await Practika_discipline.Jornal(user_id)
    buttons = []
    for item in dcp:
        button = types.InlineKeyboardButton(text=f"{item['name']}",
                                            callback_data=f"attendanceTch1:{str(item['id'])}")
        buttons.append([button])
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard

async def get_keyboard_attendance_dcp_thck1(callback: types.CallbackQuery, user_id, id):
    dcp = await Practika_group.Jornal(user_id, id)
    buttons = []
    for item in dcp:
        button = types.InlineKeyboardButton(text=f"{str(item['name'])}",
                                            callback_data=f"attendanceTchk1:{str(item['id'])}")
        buttons.append([button])
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard

def get_keyboard_grafics():
    buttons = [
        [
            types.InlineKeyboardButton(text="Знаменатель", callback_data="znml"),
            types.InlineKeyboardButton(text="Числитель", callback_data="chsl"),
        ],
    ]
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard


async def get_keyboard_umkd(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    umkd = await Umkd_review.Umkd(callback.message, user_id)
    buttons = []
    for item in umkd:
        button = types.InlineKeyboardButton(text=f'{item}', callback_data=f'umkd:{str(umkd.index(item) + 1)}')
        buttons.append([button])  # Обратите внимание на двойные скобки здесь
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard

async def get_keyboard_umkd_teacher(callback: types.CallbackQuery, id, user_id):
    umkd = await Umkd_list.Umkd_download(callback.message, id, user_id)
    print(id)
    buttons = []
    for item in umkd:
        button = types.InlineKeyboardButton(text=f'{item}', callback_data=f'umkdp:{str(umkd.index(item) + 1) + str(id)}')

        buttons.append([button])  # Обратите внимание на двойные скобки здесь
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard

async def get_keyboard_umkd_review_file(callback: types.CallbackQuery, teacher_number, id):
    user_id = callback.from_user.id
    umkd = await Umkd_list_of_files.Umkd_list_of_files(callback.message, user_id, teacher_number, id)
    buttons = []
    for item in umkd:
        button = types.InlineKeyboardButton(text=f"{item['name']}", callback_data=f"umkds:{str(item['id'])}z{str(id)}v{str(umkd.index(item) + 1)}")
        buttons.append([button])
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard



async def get_keyboard_umkd1(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    umkd = await Umkd_discipline1.Umkd(callback.message, user_id)
    buttons = []
    for item in umkd:
        button = types.InlineKeyboardButton(text=f'{item}', callback_data=f'umkd1:{str(umkd.index(item) + 1)}')
        buttons.append([button])  # Обратите внимание на двойные скобки здесь
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard

async def get_keyboard_umkd_teacher1(callback: types.CallbackQuery, id, user_id):
    umkd = await Umkd_list1.Umkd_download(callback.message, id, user_id)
    print(id)
    buttons = []
    for item in umkd:
        button = types.InlineKeyboardButton(text=f'{item}', callback_data=f'umkdp1:{str(umkd.index(item) + 1) + str(id)}')

        buttons.append([button])  # Обратите внимание на двойные скобки здесь
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard

async def get_keyboard_umkd_review_file1(callback: types.CallbackQuery, teacher_number, id):
    user_id = callback.from_user.id
    umkd = await Umkd_list_of_files1.Umkd_list_of_files(callback.message, user_id, teacher_number, id)
    buttons = []
    for item in umkd:
        button = types.InlineKeyboardButton(text=f"{item['name']}", callback_data=f"umkds1:{str(item['id'])}")
        buttons.append([button])
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard


async def get_keyboard_userplan(user_id):
    userplan = await UserPlan_elements.UserPlan(user_id)
    buttons = []
    for item in userplan:
        button = types.InlineKeyboardButton(text=f'{item}', callback_data=f'userplan:{str(item)}')

        buttons.append([button])  # Обратите внимание на двойные скобки здесь
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard