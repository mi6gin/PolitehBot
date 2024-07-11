import re
import aiohttp
from aiogram import Dispatcher, types
from aiogram.client.session import aiohttp
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from sqlalchemy import select

from DB.Database import User, encrypt_password, UniverAPI
from handlers.Start import FSM, start
from ConnectDB.DBconnect import Zaglushka
from handlers.AccountManager import Deauth

async def process_callback_autorisation(callback: types.CallbackQuery, state: FSMContext):
    await state.set_state(FSM.Auth)
    data = await state.get_data()
    message_to_delete = data.get('message_to_delete')
    await message_to_delete.delete()
    message_to_delete = await callback.message.answer(
        "Прошу следовать инструкциям!\nВведите свое ФИО и индивидуальный код абитуриента\nОтправьте по примеру:\n\nВладимир Ильич Ленин\n1917rev01uti0nye@R")
    await state.update_data(message_to_delete=message_to_delete)
    await state.set_state(FSM.Finish)

async def Auth(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    async with Zaglushka.async_session() as session:
        telega_user = select(User).where(User.telegram_id == user_id)
        existing_user = await session.execute(telega_user)
        user_object = existing_user.scalar()

    text = message.text
    match = re.match(r'^(.+)\n(.+)$', text, re.DOTALL)
    if match:
        full_name = match.group(1).strip()
        password = match.group(2).strip()
        encrypted_password = encrypt_password(password)  # Шифруем пароль
        async with Zaglushka.async_session() as session:
            async with aiohttp.ClientSession() as http_session:
                async with http_session.get(
                        f'https://univerapi.kstu.kz/?login={full_name}&password={password}') as response:
                    cookies = response.cookies
                    aspxauth_cookie = cookies.get('.ASPXAUTH')
                    sessionid_cookie = cookies.get('ASP.NET_SessionId')
                    if aspxauth_cookie is not None and sessionid_cookie is not None:
                        cookie_values = {
                            '.ASPXAUTH': aspxauth_cookie.value,
                            'ASP.NET_SessionId': sessionid_cookie.value
                        }

                        new_user1 = UniverAPI(
                            telegram_id=user_id,
                            ASPXAUTH=cookie_values['.ASPXAUTH'],
                            ASPNET_SessionId=cookie_values['ASP.NET_SessionId']
                        )

                        if user_object:  # Если пользователь существует, обновляем его данные
                            user_object.login = full_name
                            user_object.password_hash = encrypted_password
                        session.add(user_object)
                        session.add(new_user1)
                        await session.commit()
                        await start(message, state)
                    else:
                        return False
def register_handlers_sComm(nihao: Dispatcher):
    nihao.message.register(Auth, StateFilter(FSM.Finish))
    nihao.message.register(Deauth.Deauth, StateFilter(FSM.End))
    nihao.callback_query.register(process_callback_autorisation, lambda c: c.data == 'sing in')
    nihao.callback_query.register(Deauth.process_callback_deautorisation, lambda c: c.data == 'sing out')