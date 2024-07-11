import io
import os

import aiofiles
from aiogram import types
from aiogram.fsm.context import FSMContext
from aiogram.types import BufferedInputFile

from univer20.Teacher import SchldEX
from settings import bot

async def schld(callback: types.CallbackQuery, state: FSMContext):
    user_id = callback.from_user.id
    data = await state.get_data()
    message_to_delete = data.get('message_to_delete')
    await message_to_delete.delete()
    await SchldEX.Plan(user_id)