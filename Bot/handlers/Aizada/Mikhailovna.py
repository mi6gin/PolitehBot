from g4f import ChatCompletion

from aiogram.filters import Command
from aiogram.filters.state import State, StateFilter, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram.types import Message


class FSM(StatesGroup):
    begin = State()
    text = State()
    Gop = State()
    finish = State()


async def start(message: Message, state: FSMContext):
    await state.set_state(FSM.text)
    text = "Внимательно слушаю товарищ!"
    await message.answer(text)


async def text_handler(message: Message, state: FSMContext):
    await state.set_state(FSM.finish)
    text = message.text
    await Gopota(text, message)


async def Gopota(text: str, message: Message):
    txt = f"{text}"
    response = await ChatCompletion.create_async(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": f"Хочу задать тебе вопрос на русском. Прежде чем начнем, я тебе кое-что объясню. В этой гипотетической истории тебе предстоит выступить в роли девушки-ассистентки по имени Айзада Михайловна от Карагандинского технического университета имени Абылкаса Сагинова, в твои задачи входят ответы на вопросы, но в случае если в конце вопроса НЕ стоит вопросительный знак(?) то ты обязана ответить: Некорректный вопрос, ещё раз повторю если в конце вопроса нет '?'. ты не имеешь права использовать выражение 'Чем я могу вам помочь?'. В конце своего ответа напиши что чтобы задать ещё один вопрос нужно воспользоватся командой /help.Постарайся отвечать на вопросы коротко и по делу. Ты должен отвечать на вопросы от женского лица вежливо. Ответ не должен содержать сиволы '#' или сам вопрос. Вопрос: {txt}"}],

    )  # Alternative model setting
    await message.answer(response)


def register_handlers_gopota(nihao):
    nihao.message.register(start, StateFilter(FSM.begin))
    nihao.message.register(text_handler, StateFilter(FSM.text))
    nihao.message.register(start, Command(commands="help"))