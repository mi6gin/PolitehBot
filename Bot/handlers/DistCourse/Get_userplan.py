import io
import os
import re

import aiofiles
from aiogram import types
from aiogram.fsm.context import FSMContext
from aiogram.types import BufferedInputFile

from handlers.AccountManager import Keyboard
from univer20 import UserPlan
from settings import bot

async def Userplan(callback: types.CallbackQuery, state: FSMContext):
    user_id = callback.from_user.id
    data = await state.get_data()
    message_to_delete = data.get('message_to_delete')
    await message_to_delete.delete()
    message_to_delete = await callback.message.answer(
        text=f'👇',
        reply_markup=await Keyboard.get_keyboard_userplan(user_id)
    )
    await state.update_data(message_to_delete=message_to_delete)

async def button_pressed_userplan_num2(callback: types.CallbackQuery, state: FSMContext):
    user_id = callback.from_user.id
    numbers = callback.data.split(':')[1]
    current = numbers[0]
    await UserPlan.Userplan(user_id, current)
    print(current)
