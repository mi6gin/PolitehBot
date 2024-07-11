from aiogram import types
from aiogram.fsm.context import FSMContext
from univer20 import Examus


async def examus(callback: types.CallbackQuery, state: FSMContext):
    user_id = callback.from_user.id
    data = await state.get_data()
    message_to_delete = data.get('message_to_delete')
    await message_to_delete.delete()
    exam_info = await Examus.Examus(callback.message, user_id)
    if exam_info:
        # Формируем текст сообщения
        message_text = ""
        for exam in exam_info:
            message_text += f"Экзамен по дисциплине: {exam['subject']}\n"
            message_text += f"Преподаватель: {exam['teacher']}\n"
            message_text += f"Время проведения: {exam['date_time']}\n"
            message_text += f"{exam['location']}\n\n"

        # Отправляем сообщение
        await callback.message.answer(message_text)
    else:
        await callback.message.answer("Ошибка получения информации об экзаменах")
