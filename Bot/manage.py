import logging
from settings import nihao, bot
from handlers import Start
from handlers.AccountManager import Auth
from handlers.DistCourse import DsCourse
from handlers.Aizada import Mikhailovna
from UserInterface import BotCommands
from DB import Database
logging.basicConfig(level=logging.INFO)

Start.register_handlers_start(nihao)
Auth.register_handlers_sComm(nihao)
DsCourse.register_handlers_cComm(nihao)
Mikhailovna.register_handlers_gopota(nihao)

async def main():
    await BotCommands.set_commands(bot)
    await Database.create_database()
    await nihao.start_polling(bot)
