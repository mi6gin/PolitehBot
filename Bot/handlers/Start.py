from aiogram import Dispatcher, types
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from handlers.Language import Get_language
from handlers.user import Check
from univer20 import Username, FIO, Operation
from univer20.Teacher import username
from handlers.user.Language import Set_language
from handlers.AccountManager import Keyboard
from FSM.FSMclass import FSM


async def start(message: types.Message, state: FSMContext):
    await state.set_state(FSM.Start)
    user_id = message.from_user.id
    first = await Check.check(user_id)
    if first is not False:
        check = await Operation.checking(message, user_id)
        if check["spc"]=="student":
            result = await Username.Username(message, user_id)
            fio = await FIO.FIO(message, user_id)
            if "name" in result:
                message_to_delete = await message.reply(
                    text=f'Telegram bot "Бала үйрен!"\n👋 {result["name"]}\n\n{fio["name"]}: {result["name"]}\n{result["course"]}\n{result["special"]}',
                    reply_markup=await Keyboard.get_keyboard_deauth(message, user_id))
                await state.update_data(message_to_delete=message_to_delete)
            else:
                print("Неизвестный тип данных")
        if check["spc"]=="teacher":
            result = await username.Username(message, user_id)
            if "spc" in result:
                message_to_delete = await message.reply(
                    text=f'Telegram bot "Бала үйрен!"\n👋 {result["spc"]}',
                    reply_markup=await Keyboard.get_keyboard_teacher(message, user_id))
                await state.update_data(message_to_delete=message_to_delete)
            else:
                print("Неизвестный тип данных")

    else:
        await state.set_state(FSM.Start)
        message_to_delete = await message.answer(
            text="Telegram bot 'Бала үйрен!'🎓\n👉 🆕 👈"
            , reply_markup=Keyboard.get_keyboard_auth()
        )
        await state.update_data(message_to_delete=message_to_delete)

def register_handlers_start(nihao: Dispatcher):
    nihao.message.register(start, Command('start'))
    nihao.message.register(start, StateFilter(FSM.Start))
    nihao.callback_query.register(Get_language.Set_lang, lambda c: c.data == 'language')
    nihao.callback_query.register(Set_language, lambda c: c.data.startswith('lang:'))