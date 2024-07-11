from aiogram.types import BotCommand, BotCommandScopeDefault

async def set_commands(bot):
    commands = [
        BotCommand(
            command='start',
            description='Информация о пользователе'
        ),
        BotCommand(
            command='help',
            description='Позвать Нихао'
        )
    ]
    await bot.set_my_commands(commands, BotCommandScopeDefault())