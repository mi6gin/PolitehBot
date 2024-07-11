import json
from aiogram.enums import ParseMode
from aiogram.fsm.context import FSMContext
from univer20 import Jornal
from aiogram import types
from univer20 import Name_Buttons

async def jornal(callback: types.CallbackQuery, state: FSMContext):
    user_id = callback.from_user.id
    data = await state.get_data()
    message_to_delete = data.get('message_to_delete')
    await message_to_delete.delete()
    jornal_data = await Jornal.Jornal(callback.message, user_id)
    if jornal_data is not False:
        # Распарсим JSON-строку в словарь
        jornal_dict = json.loads(jornal_data)
        btn = await Name_Buttons.Btn(user_id)
        formatted_text = f'<b>{btn["jornal"]}:</b>'

        # Перебираем данные журнала и форматируем их для вывода
        for subject, subject_data in jornal_dict.items():
            formatted_text += f"\n\n<b>{subject}:</b>\n"
            for lesson, lesson_data in subject_data.items():
                formatted_text += f"  <b>{lesson}:</b>\n"
                for rk, rk_data in lesson_data.items():
                    formatted_text += f"    <b>{rk}:</b>\n"
                    for date, note in rk_data.items():
                        formatted_text += f"      {date}: {note}\n"

        await callback.message.answer(text=formatted_text, parse_mode=ParseMode.HTML)








