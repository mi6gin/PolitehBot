from handlers.user.UserData import UserData

async def check(user_id):
    result = await UserData(user_id)
    if result is not False:  # Проверяем, что результат не пустой и содержит два значения
        return True
    else:
        return False








