from aiogram import types
from core import dp, bot, postgres
from states import BotStates
from handler.utils import is_private
from messages import MESSAGES
from logg import log
from exceptions import UserError, to_custom_exc
from postgres.handlers import user_handler, chat_handler


@dp.message_handler(state='*', commands=['start'])
async def create_user_on_start(message:types.Message):
    user_uuid = message.from_user.id
    try:
        await user_handler.get(user_uuid)
    except UserError as exc:
        data = {'user_uuid': user_uuid}
        await user_handler.post(data)
        log.info(f'Create new user in database. UserId: {user_uuid}')
    except Exception as exc:
        exc = to_custom_exc(exc, user_uuid)
        log.error(exc.dev_message)
        await message.answer(exc.user_message)
        return
    await message.answer(MESSAGES['success_start'])