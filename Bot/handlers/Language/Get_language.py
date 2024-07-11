from aiogram import types
from aiogram.fsm.context import FSMContext
from handlers.AccountManager import Keyboard
from FSM.FSMclass import FSM


async def Set_lang(callback: types.CallbackQuery, state: FSMContext):
    await state.set_state(FSM.Start)
    data = await state.get_data()
    message_to_delete = data.get('message_to_delete')
    await message_to_delete.delete()
    message_to_delete = await callback.message.answer(
        text=f'🇷🇺/🇰🇿/🇬🇧',
        reply_markup=Keyboard.get_keyboard_language())
    await state.update_data(message_to_delete=message_to_delete)