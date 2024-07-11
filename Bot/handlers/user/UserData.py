from sqlalchemy import select
from DB.Database import User
from ConnectDB.DBconnect import Zaglushka
def decrypt_password(encrypted_password):
    # Простой XOR шифр с тем же ключом
    key = 0b10101010
    decrypted_password = "".join(chr(ord(char) ^ key) for char in encrypted_password)
    return decrypted_password

# Измененная функция для расшифровки пароля и возвращения логина и пароля
async def UserData(user_id):
    async with Zaglushka.async_session() as session:
        telega_user = select(User).where(User.telegram_id == user_id)
        existing_user = await session.execute(telega_user)
        user_object = existing_user.scalar()

        if user_object is not None and user_object.login != "none":
            print(12345)
            encrypted_password = user_object.password_hash
            decrypted_password = decrypt_password(encrypted_password)
            login = user_object.login
            password = decrypted_password
            print( login, password, user_id)
            return login, password, user_id

        else:
            if user_object is not None and user_object.login == "none":
                return False
            new_user2 = User(login="none",
                             password_hash="none",
                             telegram_id=user_id,
                             language="ru",
                             role = "none")
            session.add(new_user2)
            await session.commit()
            return False