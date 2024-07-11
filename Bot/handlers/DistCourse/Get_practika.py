import io
import os

import aiofiles
from aiogram import types
from aiogram.fsm.context import FSMContext
from aiogram.types import BufferedInputFile

from handlers.AccountManager import Keyboard
from univer20.Teacher import Attendance_list, Attendance_pdf, Practika_group, Practika_list
from settings import bot

async def jornal(callback: types.CallbackQuery, state: FSMContext):
    user_id = callback.from_user.id
    data = await state.get_data()
    message_to_delete = data.get('message_to_delete')
    await message_to_delete.delete()
    message_to_delete = await callback.message.answer(
        text=f'Дистанционные курсы',
        reply_markup=await Keyboard.get_keyboard_attendance_dcp_thcr1(callback, user_id)
    )
    await state.update_data(message_to_delete=message_to_delete)

async def jornal_1(callback: types.CallbackQuery, state: FSMContext):
    user_id = callback.from_user.id
    data = await state.get_data()
    message_to_delete = data.get('message_to_delete')
    await message_to_delete.delete()
    teacher_id = callback.data.split(':')[1]
    id = teacher_id
    print(id)
    message_to_delete = await callback.message.answer(
        text=f'Дистанционные курсы',
        reply_markup=await Keyboard.get_keyboard_attendance_dcp_thck1(callback, user_id, id)
    )
    await state.update_data(message_to_delete=message_to_delete)

async def jornal_2(callback: types.CallbackQuery, state: FSMContext):
    user_id = callback.from_user.id
    data = await state.get_data()
    message_to_delete = data.get('message_to_delete')
    await message_to_delete.delete()
    teacher_id = callback.data.split(':')[1]
    id = teacher_id
    print(id)
    g = await Practika_list.Jornal(user_id, id)
