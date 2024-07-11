import os
from aiogram import types
from sqlalchemy import select
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from DB.Database import User
from aiogram.fsm.context import FSMContext
from ConnectDB.DBconnect import Zaglushka

# Функция для расшифровки пароля
# Измененная функция для расшифровки пароля и возвращения логина и пароля
async def Set_language(callback: types.CallbackQuery, state: FSMContext):
    user_id = callback.from_user.id
    async with Zaglushka.async_session() as session:
        telega_user = select(User).where(User.telegram_id == user_id)
        existing_user = await session.execute(telega_user)
        user_object = existing_user.scalar()

        if user_object:
            lang = user_object.language
            return lang
        else:
            return False