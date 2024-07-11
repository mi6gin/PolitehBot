from aiogram import types
from aiogram.fsm.context import FSMContext
from sqlalchemy import select

from DB.Database import User, UniverAPI
from handlers.Start import FSM
from ConnectDB.DBconnect import Zaglushka

async def process_callback_deautorisation(callback: types.CallbackQuery, state: FSMContext):
    await state.set_state(FSM.Deauth)
    data = await state.get_data()
    message_to_delete = data.get('message_to_delete')
    await message_to_delete.delete()
    message_to_delete = await callback.message.answer(
        "Вы действительно хотите выйти из аккаунта?\nда/нет")
    await state.update_data(message_to_delete=message_to_delete)
    await state.set_state(FSM.End)

async def Deauth(message: types.Message, state: FSMContext):
    telegram_user_id = message.from_user.id
    text = message.text
    async with Zaglushka.async_session() as session:
        query = select(User).where(User.telegram_id == telegram_user_id)
        existing_user = await session.execute(query)
        existing_user = existing_user.scalar()

        query_alt = select(UniverAPI).where(UniverAPI.telegram_id == telegram_user_id)
        existing_api = await session.execute(query_alt)
        existing_api = existing_api.scalar()

        if existing_user:
            if text == 'да' or text == 'Да':
                data = await state.get_data()
                message_to_delete = data.get('message_to_delete')
                await message_to_delete.delete()
                await message.answer(
                    "Вы вышли из аккаунта")
                await session.delete(existing_user)  # Удаляем строку из базы данных
                await session.commit()

                await session.delete(existing_api)  # Удаляем строку из базы данных
                await session.commit()
            else:
                data = await state.get_data()
                message_to_delete = data.get('message_to_delete')
                await message_to_delete.delete()
                await message.answer(
                    "Действие отменено")
        else:
            await message.answer(
                "Ок")
