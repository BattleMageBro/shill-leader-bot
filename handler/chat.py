from aiogram import types
from asyncpg import UniqueViolationError
from core import dp, bot, postgres
from handler import utils
from states import TestStates
from handler.utils import is_group

@dp.message_handler(state='*', commands='add_shillbot')
async def add_new_chat(message: types.Message):
    print(message)
    if not is_group(message.chat.type):
        return
    user_uuid = message.from_user.id
    chat_uuid = message.chat.id
    data = {"user_uuid": user_uuid, "chat_uuid": chat_uuid}
    try:
        res = await postgres.insert(data)
    except UniqueViolationError:
        err = "group is already added to your shill groups"
        await message.answer(err)
        return
    print("chat is successfully added to chats")
    await message.reply("Тёмчик твой тест с добавлением бота успешен!)")

@dp.message_handler(state=[None], commands='test2')
async def test_handler(message: types.Message):
    print(f'hey we have message {message}')
    await message.reply("Тёмчик твой тест2 успешен!)")