from aiogram import types
from asyncpg import UniqueViolationError
from core import dp, bot, postgres
from handler.utils import is_group

async def check_create_chat(chat_uuid):
    chat = await postgres.get('chat', chat_uuid)
    if not chat:
        data = {'chat_uuid': chat_uuid}
        await postgres.insert('chat', data)
    return

@dp.message_handler(state='*', commands='add_shillbot')
async def create_user_chat(message: types.Message):
    print(message)
    if not is_group(message.chat.type):
        return
    member = await message.chat.get_member(message.from_user.id)
    if not member.is_chat_admin():
        await message.reply('Only admins can add chats to shillbot')
    user_uuid = message.from_user.id
    chat_uuid = message.chat.id
    await check_create_chat(chat_uuid)
    data = {"user_uuid": user_uuid, "chat_uuid": chat_uuid}
    table = 'user_chat'
    try:
        await postgres.insert(table, data)
    except UniqueViolationError:
        err = "group is already added to your shill groups"
        await message.answer(err)
        return
    print("chat is successfully added to chats")
    await message.reply("Chat is successfully added to chats!")

@dp.message_handler(state=[None], commands='test2')
async def test_handler(message: types.Message):
    print(f'hey we have message {message}')
    member = await message.chat.get_member(message.from_user.id)
    print(member)
    if not member.is_chat_admin():
        await message.reply('А ты не админ!) я тёмчика сразу узнаю')
        return
    await message.reply("Тёмчик твой тест2 успешен!)")