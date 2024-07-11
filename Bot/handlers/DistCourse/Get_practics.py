from aiogram import types
from aiogram.fsm.context import FSMContext
from univer20 import Practics


async def practics(callback: types.CallbackQuery, state: FSMContext):
    user_id = callback.from_user.id
    data = await state.get_data()
    message_to_delete = data.get('message_to_delete')
    await message_to_delete.delete()
    pract = await Practics.Practics(user_id)
    if pract:
        message_text = ""
        message_text += f"{pract['nmb_gr']}: {pract['nmb_gr1']}\n"
        message_text += f"{pract['maneger']}: {pract['maneger1']}\n"
        message_text += f"{pract['periud']}: {pract['periud1']}\n"
        message_text += f"{pract['organ']}: {pract['organ1']}\n"
        await callback.message.answer(message_text)
    else:
        await callback.message.answer("Ошибка получения информации о практике")
