from aiogram import types
from sqlalchemy import select
from univer20 import AuthVer2
from DB.Database import User, UniverAPI
from aiogram.fsm.context import FSMContext
from ConnectDB.DBconnect import Zaglushka

async def Set_language(callback: types.CallbackQuery, state: FSMContext):
    user_id = callback.from_user.id
    async with Zaglushka.async_session() as session:
        telega_user = select(User).where(User.telegram_id == user_id)
        existing_user = await session.execute(telega_user)
        user_object = existing_user.scalar()

        univer_users = select(UniverAPI).where(UniverAPI.telegram_id == user_id)
        existing_univer_user = await session.execute(univer_users)
        univer_object = existing_univer_user.scalar()

        if univer_object:
            await AuthVer2.Authorization(user_id)

        if user_object:
            lang = str(callback.data.split(':')[1])
            user_object.language = lang
            session.add(user_object)
            await session.commit()

            data = await state.get_data()
            message_to_delete = data.get('message_to_delete')
            await message_to_delete.delete()
            if lang == 'ru':
                language = 'Язык - 🇷🇺\nПожалуйста нажмите /start'
            elif lang == 'kz':
                language = 'Тiлi - 🇰🇿\nБасыңыз /start'
            elif lang == 'en':
                language = 'Language - 🇬🇧\nPlease click /start'
            message_to_delete = await callback.message.answer(
                text=f'{language}'
            )
            await state.update_data(message_to_delete=message_to_delete)

        else:
            return False
