from aiogram import types
from core import dp
from messages import MESSAGES
from logg import log
from exceptions import UserError
from postgres.handlers import user_handler


@dp.message_handler(state='*', commands=['start'], chat_type=types.ChatType.PRIVATE)
async def create_user_on_start(message:types.Message):
    user_uuid = message.from_user.id
    try:
        await user_handler.get(user_uuid)
    except UserError:
        data = {'id': user_uuid}
        await user_handler.post(data)
        log.info(f'Create new user in database. UserId: {user_uuid}')
    await message.answer(MESSAGES['success_start'])