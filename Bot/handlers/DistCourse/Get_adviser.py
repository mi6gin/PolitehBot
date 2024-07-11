from aiogram import types
from aiogram.fsm.context import FSMContext
from univer20 import My_adviser, Name_Buttons


async def Adviser(callback: types.CallbackQuery, state: FSMContext):
    user_id = callback.from_user.id
    data = await state.get_data()
    message_to_delete = data.get('message_to_delete')
    await message_to_delete.delete()
    adv = await My_adviser.Adviser(user_id)
    btn = await Name_Buttons.Btn(user_id)
    if adv:
        # Формируем текст сообщения
        message_text = f"{btn['adviser']}\n{adv['name']}: {adv['FIO']}"
        await callback.message.answer(message_text)
    else:
        await callback.message.answer("Ошибка получения информации о кураторах")
